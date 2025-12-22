import { ref } from 'vue'
import type User from '~/models/userModel'

export const useAuth = () => {
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const currentUser = ref<User | null>(null)

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

  const setUser = (user: User) => {
    currentUser.value = user
    localStorage.setItem('current_user', JSON.stringify(user))
  }

  const getUser = (): User | null => {
    if (!currentUser.value) {
      const storedUser = localStorage.getItem('current_user')
      if (storedUser) {
        currentUser.value = JSON.parse(storedUser)
      }
    }
    return currentUser.value
  }

  const isAdmin = (): boolean => {
    const user = getUser()
    return user?.role === 'administrador'
  }

  const clearToken = () => {
    token.value = null
    currentUser.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('current_user')
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
    setUser,
    getUser,
    isAdmin,
    clearToken,
    checkAuth,
    isAuthenticated,
    currentUser
  }
}