import { useAuth } from '~/composables/useAuth'

export default defineNuxtRouteMiddleware(async () => {
  const { validateSession, isAdmin } = useAuth()
  if (!await validateSession()) return navigateTo('/login')
  if (!isAdmin()) return navigateTo('/dashboard')
})
