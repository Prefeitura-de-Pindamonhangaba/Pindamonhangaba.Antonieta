import type { Distribution } from '../models/distributionModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/distribution`

export const distributionService = {
  async getAll(includeOld: boolean = false): Promise<[Distribution[], number]> {
    try {
      const url = includeOld 
        ? `${BASE_URL}/?include_old=true`
        : `${BASE_URL}/`
        
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch distributions')
      }
      
      const [distributions, count] = await response.json()
      return [distributions, count]
    } catch (error) {
      console.error('Error fetching distributions:', error)
      throw error
    }
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

  async getByBeneficiaryId(beneficiaryId: number): Promise<[Distribution[], number]> {
    try {
      const response = await fetch(`${BASE_URL}/beneficiary/${beneficiaryId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch beneficiary distributions')
      }
      
      const [distributions, count] = await response.json()
      return [distributions, count]
    } catch (error) {
      console.error('Error fetching beneficiary distributions:', error)
      throw error
    }
  },

  async create(distribution: Omit<Distribution, 'id'>): Promise<Distribution> {
    const response = await fetch(`${BASE_URL}/`, {
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
      method: 'PUT',  // Changed from PATCH to PUT
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        id,
        ...distribution
      })
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