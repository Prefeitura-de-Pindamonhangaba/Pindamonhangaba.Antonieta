import type { Beneficiary } from '../models/beneficiaryModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/beneficiary`

function timestamp_to_date(timestamp: number): string {
  const data = new Date(timestamp);

  // Adiciona 1 dia ao timestamp
  data.setUTCDate(data.getUTCDate() + 1); // Incrementa o dia UTC

  const ano = data.getUTCFullYear();
  const mes = (data.getUTCMonth() + 1).toString().padStart(2, '0');
  const dia = data.getUTCDate().toString().padStart(2, '0'); // Altere de padStart(1, '0') para padStart(2, '0') para dias como '01'

  return `${ano}-${mes}-${dia}`;
}

export const beneficiaryService = {
  async getAll(): Promise<[Beneficiary[], number]> {
    try {
      const response = await fetch(`${BASE_URL}/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch beneficiaries')
      }
      
      const [beneficiaries, count] = await response.json()
      return [beneficiaries, count]
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
    console.log('🔄 beneficiaryService.create chamado')
    if(beneficiary.birth_date.toString().length > 10) {
      beneficiary.birth_date = timestamp_to_date(beneficiary.birth_date as unknown as number);
    }
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
    console.log('🔄 beneficiaryService.update chamado', { id, beneficiary })
    if(beneficiary.birth_date.toString().length > 10) {
      beneficiary.birth_date = timestamp_to_date(beneficiary.birth_date as unknown as number);
    }
    try {
      const response = await fetch(`${BASE_URL}/`, {
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