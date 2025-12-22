import type { User } from '../models/userModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/auth`

export const authService = {
  async register(user: UserCreate): Promise<User> {
    const response = await fetch(`${BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to register user')
    }

    return response.json()
  },

  async login(email: string, password: string): Promise<{ access_token: string; token_type: string; user: User }> {
    try {
      const response = await fetch(`${BASE_URL}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
          username: email,
          password: password,
          grant_type: 'password'
        })
      })
      
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

    const response = await fetch(`${BASE_URL}/me`, {
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
    localStorage.setItem('access_token', token)
  },

  getToken(): string | null {
    return localStorage.getItem('access_token')
  },

  removeToken() {
    localStorage.removeItem('access_token')
  },

  isAuthenticated(): boolean {
    return !!this.getToken()
  }
}