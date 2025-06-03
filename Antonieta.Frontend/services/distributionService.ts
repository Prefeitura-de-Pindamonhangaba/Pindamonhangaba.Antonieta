import type { Distribution } from '../models/distributionModel'

const BASE_URL = useRuntimeConfig().public.backendUrl + '/distribution'

export const distributionService = {
  async getAll(): Promise<Distribution[]> {
    const response = await fetch(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch distributions')
    }
    
    return response.json()
  },

  async getById(id: number): Promise<Distribution> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch distribution')
    }
    
    return response.json()
  },

  async getByBeneficiaryId(beneficiaryId: number): Promise<Distribution[]> {
    const response = await fetch(`${BASE_URL}/beneficiary/${beneficiaryId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch beneficiary distributions')
    }
    
    return response.json()
  },

  async create(distribution: Omit<Distribution, 'id'>): Promise<Distribution> {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(distribution)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create distribution')
    }
    
    return response.json()
  },

  async update(id: number, distribution: Partial<Distribution>): Promise<Distribution> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(distribution)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update distribution')
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
      throw new Error(error.detail || 'Failed to delete distribution')
    }
  }
}