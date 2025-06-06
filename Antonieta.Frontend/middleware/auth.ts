export default defineNuxtRouteMiddleware((to) => {
  const { checkAuth } = useAuth()
  
  // Allow access to login page
  if (to.path === '/login') {
    if (checkAuth()) {
      return navigateTo('/dashboard')
    }
    return
  }

  // Check if not authenticated
  if (!checkAuth()) {
    return navigateTo('/login')
  }
})