import type { RationType } from '../models/rationTypeModel'

const BASE_URL = useRuntimeConfig().public.backendUrl + '/ration_type'

export const rationTypeService = {
  async getAll(): Promise<RationType[]> {
    const response = await fetch(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch ration types')
    }
    
    return response.json()
  },

  async getById(id: number): Promise<RationType> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch ration type')
    }
    
    return response.json()
  },

  async create(rationType: Omit<RationType, 'id'>): Promise<RationType> {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(rationType)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create ration type')
    }
    
    return response.json()
  },

  async update(id: number, rationType: Partial<RationType>): Promise<RationType> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(rationType)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update ration type')
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
      throw new Error(error.detail || 'Failed to delete ration type')
    }
  }
}