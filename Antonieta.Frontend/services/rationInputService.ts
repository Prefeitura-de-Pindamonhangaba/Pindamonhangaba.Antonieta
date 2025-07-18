import type { RationInput } from '../models/rationInputModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/ration-input`

export const rationInputService = {
  async getAll(): Promise<[RationInput[], number]> {
    try {
      const response = await fetch(`${BASE_URL}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch ration inputs')
      }
      
      const [inputs, count] = await response.json()
      return [inputs, count]
    } catch (error) {
      console.error('Error fetching ration inputs:', error)
      throw error
    }
  },

  async getById(id: number): Promise<RationInput> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch ration input')
    }
    
    return response.json()
  },

  async getByRationStockId(stockId: number): Promise<RationInput[]> {
    const response = await fetch(`${BASE_URL}/ration-stock/${stockId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch ration stock inputs')
    }
    
    return response.json()
  },

  async create(rationInput: Omit<RationInput, 'id'>): Promise<RationInput> {
    const response = await fetch(`${BASE_URL}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(rationInput)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create ration input')
    }
    
    return response.json()
  },

  async update(id: number, rationInput: Partial<RationInput>): Promise<RationInput> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',  // Changed from PATCH to PUT
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        id,
        ...rationInput
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update ration input')
    }
    
    return response.json()
  },

  async delete(id: number): Promise<void> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to delete ration input')
    }
  }
}