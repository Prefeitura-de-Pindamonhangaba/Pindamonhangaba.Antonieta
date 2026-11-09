import { navigateTo } from '#app'
import { useAuth } from '~/composables/useAuth'

export async function apiFetch(url: string, options: RequestInit = {}, authenticated = true): Promise<Response> {
  const auth = useAuth()
  const activeToken = authenticated ? auth.getToken() : null
  const headers = new Headers(options.headers)
  if (authenticated) {
    headers.delete('Authorization')
    if (activeToken) headers.set('Authorization', `Bearer ${activeToken}`)
  }
  const response = await fetch(url, { ...options, headers })
  const currentToken = process.client ? localStorage.getItem('access_token') : auth.getToken()
  if (authenticated && response.status === 401 && currentToken === activeToken) {
    auth.clearToken()
    await navigateTo('/login')
  }
  return response
}
