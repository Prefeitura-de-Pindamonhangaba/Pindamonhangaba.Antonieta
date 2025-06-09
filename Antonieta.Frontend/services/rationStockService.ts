import type { RationStock } from '../models/rationStockModel'

const BASE_URL = useRuntimeConfig().public.backendUrl + '/ration-stock'

export const rationStockService = {
  async getAll(): Promise<RationStock[]> {
    const response = await fetch(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch ration stocks')
    }
    let listOfStocks = await response.json()
    return listOfStocks[0] ?? []
  },

  async getById(id: number): Promise<RationStock> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch ration stock')
    }
    
    return response.json()
  },

  async create(rationStock: Omit<RationStock, 'id'>): Promise<RationStock> {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(rationStock)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create ration stock')
    }
    
    return response.json()
  },

  async update(id: number, rationStock: Partial<RationStock>): Promise<RationStock> {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',  // Changed from PATCH to PUT
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        id,
        ...rationStock
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update ration stock')
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
      throw new Error(error.detail || 'Failed to delete ration stock')
    }
  }
}