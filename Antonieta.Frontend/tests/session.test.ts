import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useAuth } from '../composables/useAuth'

export const token = (exp = Date.now() / 1000 + 300) =>
  `header.${Buffer.from(JSON.stringify({ sub: 'user@example.com', exp })).toString('base64url')}.signature`

describe('session validation', () => {
  beforeEach(() => useAuth().clearToken())

  it('rejects expired and malformed stored tokens', () => {
    for (const value of ['invalid', token(1)]) {
      localStorage.setItem('access_token', value)
      expect(useAuth().checkAuth()).toBe(false)
      expect(localStorage.getItem('access_token')).toBeNull()
    }
  })

  it('confirms the session and current role with the backend', async () => {
    const auth = useAuth()
    auth.setToken(token())
    vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ id: 1, role: 'comum' })))
    expect(await auth.validateSession()).toBe(true)
    expect(auth.isAdmin()).toBe(false)
    expect(fetch).toHaveBeenCalledWith('http://api.test/auth/me', expect.anything())
  })

  it('clears an invalid session confirmed by the server', async () => {
    const auth = useAuth()
    auth.setToken(token())
    vi.mocked(fetch).mockResolvedValue(new Response('{}', { status: 401 }))
    expect(await auth.validateSession()).toBe(false)
    expect(auth.isAuthenticated.value).toBe(false)
    expect(localStorage.getItem('current_user')).toBeNull()
  })
})
