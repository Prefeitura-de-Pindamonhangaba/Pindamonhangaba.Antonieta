import { ref } from 'vue'

export const useAuth = () => {
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)

  const getToken = () => {
    if (!token.value) {
      token.value = localStorage.getItem('access_token')
    }
    return token.value
  }

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
    isAuthenticated.value = true
  }

  const clearToken = () => {
    token.value = null
    localStorage.removeItem('access_token')
    isAuthenticated.value = false
  }

  const checkAuth = () => {
    const storedToken = getToken()
    isAuthenticated.value = !!storedToken
    return isAuthenticated.value
  }

  return {
    getToken,
    setToken,
    clearToken,
    checkAuth,
    isAuthenticated
  }
}