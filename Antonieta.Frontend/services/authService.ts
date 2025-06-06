interface User {
  email: string;
  full_name: string;
}

interface UserCreate {
  email: string;
  password: string;
  full_name: string;
}

interface Token {
  access_token: string;
  token_type: string;
}

const BASE_URL = useRuntimeConfig().public.backendUrl + '/auth'

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

  async login(email: string, password: string): Promise<Token> {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    formData.append('grant_type', 'password')

    const response = await fetch(`${BASE_URL}/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to authenticate')
    }

    return response.json()
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