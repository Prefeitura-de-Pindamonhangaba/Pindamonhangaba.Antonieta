import User from '../models/userModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/users`

export const userService = {
  /**
   * Obter todos os usuários
   */
  async getAll(): Promise<User[]> {
    try {
      const response = await fetch(`${BASE_URL}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch users')
      }
      
      const usersData = await response.json()
      return usersData.map((data: any) => new User(data))
    } catch (error) {
      console.error('Error fetching users:', error)
      throw error
    }
  },

  /**
   * Obter um usuário por ID
   */
  async getById(id: number): Promise<User> {
    try {
      const response = await fetch(`${BASE_URL}/${id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch user')
      }
      
      const data = await response.json()
      return new User(data)
    } catch (error) {
      console.error('Error fetching user:', error)
      throw error
    }
  },

  /**
   * Criar um novo usuário
   */
  async create(userData: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User> {
    try {
      const response = await fetch(`${BASE_URL}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(userData)
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create user')
      }
      
      const data = await response.json()
      return new User(data)
    } catch (error) {
      console.error('Error creating user:', error)
      throw error
    }
  },

  /**
   * Atualizar um usuário existente
   */
  async update(id: number, userData: Partial<Omit<User, 'id' | 'created_at' | 'updated_at'>>): Promise<User> {
    try {
      const response = await fetch(`${BASE_URL}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(userData)
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to update user')
      }
      
      const data = await response.json()
      return new User(data)
    } catch (error) {
      console.error('Error updating user:', error)
      throw error
    }
  },

  /**
   * Deletar um usuário
   */
  async delete(id: number): Promise<void> {
    try {
      const response = await fetch(`${BASE_URL}/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to delete user')
      }
    } catch (error) {
      console.error('Error deleting user:', error)
      throw error
    }
  }
}
