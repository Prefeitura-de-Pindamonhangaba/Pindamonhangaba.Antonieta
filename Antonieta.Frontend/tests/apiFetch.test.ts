import { beforeEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from '../utils/apiFetch'
import { useAuth } from '../composables/useAuth'

const token = `a.${Buffer.from(JSON.stringify({ exp: Date.now() / 1000 + 300 })).toString('base64url')}.c`

describe('shared API client', () => {
  beforeEach(() => { useAuth().clearToken(); useAuth().setToken(token) })

  it('attaches the bearer token and preserves request options', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response('{}'))
    await apiFetch('http://api.test/beneficiary/', { method: 'POST', body: '{}' })
    const [, options] = vi.mocked(fetch).mock.calls[0]
    expect(new Headers(options?.headers).get('Authorization')).toBe(`Bearer ${token}`)
    expect(options?.method).toBe('POST')
    expect(options?.body).toBe('{}')
  })

  it('clears the session and redirects on 401', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response('{}', { status: 401 }))
    await apiFetch('http://api.test/beneficiary/')
    expect(useAuth().isAuthenticated.value).toBe(false)
    expect(navigateTo).toHaveBeenCalledWith('/login')
  })

  it('preserves the session on forbidden access and server errors', async () => {
    for (const status of [403, 500]) {
      vi.mocked(fetch).mockResolvedValue(new Response('{}', { status }))
      await apiFetch('http://api.test/users/')
      expect(localStorage.getItem('access_token')).toBe(token)
      expect(navigateTo).not.toHaveBeenCalled()
    }
  })

  it('does not attach credentials or clear the session for failed login', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response('{}', { status: 401 }))
    await apiFetch('http://api.test/auth/token', {}, false)
    expect(new Headers(vi.mocked(fetch).mock.calls[0][1]?.headers).has('Authorization')).toBe(false)
    expect(localStorage.getItem('access_token')).toBe(token)
  })

  it('does not clear a new session when an older request returns 401', async () => {
    let finish!: (response: Response) => void
    vi.mocked(fetch).mockReturnValue(new Promise(resolve => { finish = resolve }))
    const pending = apiFetch('http://api.test/beneficiary/')
    const newToken = `a.${Buffer.from(JSON.stringify({ exp: Date.now() / 1000 + 600 })).toString('base64url')}.c`
    useAuth().setToken(newToken)
    finish(new Response('{}', { status: 401 }))
    await pending
    expect(localStorage.getItem('access_token')).toBe(newToken)
    expect(navigateTo).not.toHaveBeenCalled()
  })

  it('redirects if the token expires while a request is pending', async () => {
    const future = Date.now() + 600_000
    vi.mocked(fetch).mockImplementation(async () => {
      vi.spyOn(Date, 'now').mockReturnValue(future)
      return new Response('{}', { status: 401 })
    })
    try {
      await apiFetch('http://api.test/beneficiary/')
      expect(navigateTo).toHaveBeenCalledWith('/login')
      expect(localStorage.getItem('access_token')).toBeNull()
    } finally {
      vi.restoreAllMocks()
    }
  })
})
