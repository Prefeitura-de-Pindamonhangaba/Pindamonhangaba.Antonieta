import type { Beneficiary } from '../models/beneficiary'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/beneficiary`

export const beneficiaryService = {
  async getAll(): Promise<Beneficiary[]> {
    try {
      const response = await fetch(`${BASE_URL}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch beneficiaries')
      }
      
      const data = await response.json()
      return data[0] ?? []
    } catch (error) {
      console.error('Error fetching beneficiaries:', error)
      throw error
    }
  },

  async getById(id: number): Promise<Beneficiary> {
    try {
      const response = await fetch(`${BASE_URL}/${id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to fetch beneficiary')
      }
      
      return response.json()
    } catch (error) {
      console.error('Error fetching beneficiary:', error)
      throw error
    }
  },

  async create(beneficiary: Omit<Beneficiary, 'id'>): Promise<Beneficiary> {
    try {
      const response = await fetch(`${BASE_URL}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(beneficiary)
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create beneficiary')
      }
      
      return response.json()
    } catch (error) {
      console.error('Error creating beneficiary:', error)
      throw error
    }
  },

  async update(id: number, beneficiary: Partial<Beneficiary>): Promise<Beneficiary> {
    try {
      const response = await fetch(`${BASE_URL}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          id,
          ...beneficiary
        })
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to update beneficiary')
      }
      
      return response.json()
    } catch (error) {
      console.error('Error updating beneficiary:', error)
      throw error
    }
  },

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
        throw new Error(error.detail || 'Failed to delete beneficiary')
      }
    } catch (error) {
      console.error('Error deleting beneficiary:', error)
      throw error
    }
  }
}