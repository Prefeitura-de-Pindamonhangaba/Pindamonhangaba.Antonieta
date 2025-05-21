import { ref } from 'vue'

export const useAuth = () => {
  const token = ref<string | null>(null)

  const getToken = () => {
    if (!token.value) {
      token.value = localStorage.getItem('auth_token')
    }
    return token.value
  }

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('auth_token', newToken)
  }

  const clearToken = () => {
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const getAuthHeaders = () => {
    const token = getToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  return {
    getToken,
    setToken,
    clearToken,
    getAuthHeaders
  }
}