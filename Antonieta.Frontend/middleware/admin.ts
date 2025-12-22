export default defineNuxtRouteMiddleware((to, from) => {
  const { isAdmin, checkAuth } = useAuth()
  
  // Verificar se está autenticado
  if (!checkAuth()) {
    return navigateTo('/login')
  }
  
  // Verificar se é administrador
  if (!isAdmin()) {
    // Redirecionar para dashboard se não for admin
    return navigateTo('/dashboard')
  }
})
