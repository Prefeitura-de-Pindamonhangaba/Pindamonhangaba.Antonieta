export default defineNuxtRouteMiddleware((to, from) => {
  const { checkAuth, currentUser } = useAuth()
  
  // Verificar se está autenticado
  if (!checkAuth()) {
    return navigateTo('/login')
  }
  
  // Forçar recarregar o usuário do localStorage
  checkAuth()
  
  console.log('Admin middleware - Current user:', currentUser.value)
  
  // Verificar se é administrador usando o estado reativo
  if (currentUser.value?.role !== 'administrador') {
    console.warn('Access denied - User is not admin')
    // Redirecionar para dashboard se não for admin
    return navigateTo('/dashboard')
  }
})
