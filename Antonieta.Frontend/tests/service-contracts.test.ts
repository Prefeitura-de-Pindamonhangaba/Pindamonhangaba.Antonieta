import { beforeEach, expect, it, vi } from 'vitest'
import { rationTypeService } from '../services/rationTypeService'
import { dashboardService } from '../services/dashboardService'
import { authService } from '../services/authService'
import { useAuth } from '../composables/useAuth'

beforeEach(() => {
  useAuth().clearToken()
  useAuth().setToken(`a.${Buffer.from(JSON.stringify({ exp: Date.now() / 1000 + 300 })).toString('base64url')}.c`)
})

it('loads ration types from the real stock endpoint and unwraps pagination', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify([[{ id: 1, name: 'Dog food' }], 1])))
  expect(await rationTypeService.getAll()).toEqual([{ id: 1, name: 'Dog food' }])
  expect(fetch).toHaveBeenCalledWith('http://api.test/ration-stock/', expect.anything())
})

it('loads current stock using the documented total endpoint', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ current_stock: 12.5 })))
  expect(await dashboardService.getCurrentStock()).toBe(12.5)
  expect(fetch).toHaveBeenCalledWith('http://api.test/dashboard/current-total-stock', expect.anything())
})

it('registers users through the protected user endpoint', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ id: 3 })))
  await authService.register({ email: 'user@example.com', full_name: 'User', password: 'Password123!' })
  expect(fetch).toHaveBeenCalledWith('http://api.test/users/', expect.objectContaining({ method: 'POST' }))
})

it('does not attach an existing token to the public login', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ access_token: 'new-token' })))
  await authService.login('user@example.com', 'Password123!')
  expect(new Headers(vi.mocked(fetch).mock.calls[0][1]?.headers).has('Authorization')).toBe(false)
  expect(vi.mocked(fetch).mock.calls[0][1]?.body?.toString()).toContain('grant_type=password')
})

it('updates ration metadata without overwriting stock balance', async () => {
  vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ id: 1, name: 'Updated' })))
  await rationTypeService.update(1, { name: 'Updated', description: 'Food' })
  const [url, options] = vi.mocked(fetch).mock.calls[0]
  expect(url).toBe('http://api.test/ration-stock/1')
  expect(options?.method).toBe('PATCH')
  expect(JSON.parse(options?.body as string)).not.toHaveProperty('stock')
})
