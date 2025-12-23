import { ref } from 'vue'
import type User from '~/models/userModel'

// Estado global compartilhado entre todos os componentes
const token = ref<string | null>(null)
const isAuthenticated = ref(false)
const currentUser = ref<User | null>(null)

// Inicializar estado do localStorage
if (process.client) {
  const storedToken = localStorage.getItem('access_token')
  const storedUser = localStorage.getItem('current_user')
  
  if (storedToken) {
    token.value = storedToken
    isAuthenticated.value = true
  }
  
  if (storedUser) {
    try {
      currentUser.value = JSON.parse(storedUser)
    } catch (e) {
      console.error('Error parsing stored user:', e)
      localStorage.removeItem('current_user')
    }
  }
}

export const useAuth = () => {
  const getToken = () => {
    if (!token.value && process.client) {
      token.value = localStorage.getItem('access_token')
    }
    return token.value
  }

  const setToken = (newToken: string) => {
    token.value = newToken
    if (process.client) {
      localStorage.setItem('access_token', newToken)
    }
    isAuthenticated.value = true
  }

  const setUser = (user: User) => {
    currentUser.value = user
    if (process.client) {
      localStorage.setItem('current_user', JSON.stringify(user))
    }
  }

  const getUser = (): User | null => {
    if (!currentUser.value && process.client) {
      const storedUser = localStorage.getItem('current_user')
      if (storedUser) {
        try {
          currentUser.value = JSON.parse(storedUser)
        } catch (e) {
          console.error('Error parsing stored user:', e)
        }
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
    isAuthenticated.value = false
    
    if (process.client) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('current_user')
    }
  }

  const checkAuth = () => {
    const storedToken = getToken()
    if (storedToken && process.client) {
      const storedUser = localStorage.getItem('current_user')
      if (storedUser) {
        try {
          currentUser.value = JSON.parse(storedUser)
        } catch (e) {
          console.error('Error parsing stored user:', e)
        }
      }
    }
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