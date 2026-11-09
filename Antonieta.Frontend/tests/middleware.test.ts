import { beforeEach, expect, it, vi } from 'vitest'
import authGuard from '../middleware/auth'
import adminGuard from '../middleware/admin'
import { useAuth } from '../composables/useAuth'

const token = `a.${Buffer.from(JSON.stringify({ exp: Date.now() / 1000 + 300 })).toString('base64url')}.c`
beforeEach(() => useAuth().clearToken())

it('redirects an unauthenticated visitor to login', async () => {
  await authGuard({ path: '/beneficiary' })
  expect(navigateTo).toHaveBeenCalledWith('/login')
})

it('keeps unauthenticated visitors on login', async () => {
  await authGuard({ path: '/login' })
  expect(navigateTo).not.toHaveBeenCalled()
})

it('uses the server role even if local storage claims administrator access', async () => {
  useAuth().setToken(token)
  localStorage.setItem('current_user', JSON.stringify({ role: 'administrador' }))
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ id: 1, role: 'comum' })))
  await adminGuard()
  expect(navigateTo).toHaveBeenCalledWith('/dashboard')
  expect(useAuth().isAdmin()).toBe(false)
})

it('allows an administrator confirmed by the server', async () => {
  useAuth().setToken(token)
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ id: 1, role: 'administrador' })))
  await adminGuard()
  expect(navigateTo).not.toHaveBeenCalled()
})

it('preserves credentials on temporary server errors', async () => {
  useAuth().setToken(token)
  vi.mocked(fetch).mockResolvedValue(new Response('{}', { status: 503 }))
  await expect(authGuard({ path: '/dashboard' })).rejects.toThrow('Unable to validate session')
  expect(localStorage.getItem('access_token')).toBe(token)
  expect(navigateTo).not.toHaveBeenCalled()
})
