import { useAuth } from '~/composables/useAuth'

export default defineNuxtRouteMiddleware(async (to) => {
  const { validateSession } = useAuth()
  const authenticated = await validateSession()
  if (to.path === '/login') {
    if (authenticated) return navigateTo('/dashboard')
    return
  }
  if (!authenticated) return navigateTo('/login')
})
