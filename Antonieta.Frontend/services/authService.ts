import { useAuth } from '~/composables/useAuth'
import { userService } from './userService'
import { apiFetch } from '~/utils/apiFetch'
import type User from '../models/userModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/auth`

export const authService = {
  async register(user: { email: string; password: string; full_name: string }): Promise<User> {
    return userService.create(user)
  },

  async login(email: string, password: string): Promise<{ access_token: string; token_type: string; user: User }> {
    try {
      const response = await apiFetch(`${BASE_URL}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
          username: email,
          password: password,
          grant_type: 'password'
        })
      }, false)
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }
      
      return response.json()
    } catch (error) {
      console.error('Error during login:', error)
      throw error
    }
  },

  async getCurrentUser(): Promise<User> {
    const token = localStorage.getItem('access_token')
    if (!token) {
      throw new Error('No authentication token found')
    }

    const response = await apiFetch(`${BASE_URL}/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch user data')
    }

    return response.json()
  },

  setToken(token: string) {
    useAuth().setToken(token)
  },

  getToken(): string | null {
    return useAuth().getToken()
  },

  removeToken() {
    useAuth().clearToken()
  },

  isAuthenticated(): boolean {
    return useAuth().checkAuth()
  }
}
