import { ref } from 'vue'
import { useRuntimeConfig } from '#app'
import type User from '~/models/userModel'

const token = ref<string | null>(null)
const isAuthenticated = ref(false)
const currentUser = ref<User | null>(null)
let validation: { token: string; promise: Promise<boolean> } | null = null

function validToken(value: string | null): boolean {
  if (!value) return false
  try {
    const parts = value.split('.')
    if (parts.length !== 3) return false
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))
    return typeof payload.exp === 'number' && payload.exp * 1000 > Date.now()
  } catch {
    return false
  }
}

export const useAuth = () => {
  const clearToken = () => {
    token.value = null
    currentUser.value = null
    isAuthenticated.value = false
    validation = null
    if (process.client) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('current_user')
    }
  }

  const getToken = () => {
    const stored = process.client ? localStorage.getItem('access_token') : token.value
    if (!validToken(stored)) {
      clearToken()
      return null
    }
    token.value = stored
    return stored
  }

  const setToken = (value: string) => {
    if (!validToken(value)) {
      clearToken()
      return
    }
    token.value = value
    if (process.client) localStorage.setItem('access_token', value)
    isAuthenticated.value = true
  }

  const setUser = (user: User) => {
    currentUser.value = user
    if (process.client) localStorage.setItem('current_user', JSON.stringify(user))
  }

  const getUser = (): User | null => {
    if (!getToken()) return null
    if (!currentUser.value && process.client) {
      try {
        currentUser.value = JSON.parse(localStorage.getItem('current_user') || 'null')
      } catch {
        localStorage.removeItem('current_user')
      }
    }
    return currentUser.value
  }

  const checkAuth = () => {
    isAuthenticated.value = !!getToken()
    return isAuthenticated.value
  }

  // Local expiry checks improve navigation; only the API validates identity and role.
  const validateSession = async (): Promise<boolean> => {
    const activeToken = getToken()
    if (!activeToken) return false
    if (validation?.token === activeToken) return validation.promise
    const promise = (async () => {
      const response = await fetch(`${useRuntimeConfig().public.backendUrl}/auth/me`, {
        headers: { Authorization: `Bearer ${activeToken}` },
      })
      // A stale request must not overwrite a newly signed-in account.
      if (getToken() !== activeToken) return false
      if (response.status === 401) {
        clearToken()
        return false
      }
      if (!response.ok) throw new Error('Unable to validate session')
      const user = await response.json()
      if (getToken() !== activeToken) return false
      setUser(user)
      isAuthenticated.value = true
      return true
    })()
    validation = { token: activeToken, promise }
    try {
      return await promise
    } finally {
      if (validation?.promise === promise) validation = null
    }
  }

  return {
    getToken, setToken, setUser, getUser,
    isAdmin: () => getUser()?.role === 'administrador',
    clearToken, checkAuth, validateSession, isAuthenticated, currentUser,
  }
}
