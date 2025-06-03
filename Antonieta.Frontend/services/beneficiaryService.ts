import type { Beneficiary } from '../models/beneficiary'

const BASE_URL = useRuntimeConfig().public.backendUrl + '/beneficiary'

export const beneficiaryService = {
  async getAll(): Promise<Beneficiary[]> {
    const response = await fetch(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch beneficiaries')
    }
    
    return response.json()
  },

  async getById(id: number): Promise<Beneficiary> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch beneficiary')
    }
    
    return response.json()
  },

  async create(beneficiary: Omit<Beneficiary, 'id'>): Promise<Beneficiary> {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(beneficiary)
    })
    
    if (!response.ok) {
      throw new Error('Failed to create beneficiary')
    }
    
    return response.json()
  },

  async update(id: number, beneficiary: Partial<Beneficiary>): Promise<Beneficiary> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(beneficiary)
    })
    
    if (!response.ok) {
      throw new Error('Failed to update beneficiary')
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
      throw new Error('Failed to delete beneficiary')
    }
  }
}