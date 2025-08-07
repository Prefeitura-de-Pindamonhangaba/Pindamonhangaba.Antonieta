import Beneficiary from '../models/beneficiaryModel'
import { useRuntimeConfig } from '#app'

const BASE_URL = `${useRuntimeConfig().public.backendUrl}/beneficiary`

function timestamp_to_date(timestamp: number): string {
  const data = new Date(timestamp)
  data.setUTCDate(data.getUTCDate())
  const ano = data.getUTCFullYear()
  const mes = (data.getUTCMonth() + 1).toString().padStart(2, '0')
  const dia = data.getUTCDate().toString().padStart(2, '0')
  return `${ano}-${mes}-${dia}`
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
      
      const [beneficiariesData, count] = await response.json()
      
      // ✅ NOVO: Converter dados do backend para instâncias do model
      const beneficiaries = beneficiariesData.map((data: any) => Beneficiary.fromBackend(data))
      
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
      
      const data = await response.json()
      
      // ✅ NOVO: Converter dados do backend para instância do model
      return Beneficiary.fromBackend(data)
    } catch (error) {
      console.error('Error fetching beneficiary:', error)
      throw error
    }
  },

  // ✅ ATUALIZADO: Usar novo model com endereço estruturado
  async create(beneficiaryData: Omit<Beneficiary, 'id'>): Promise<Beneficiary> {
    console.log('🔄 beneficiaryService.create chamado', { beneficiaryData })
    
    try {
      // ✅ NOVO: Validar endereço antes de enviar
      if (!beneficiaryData.street || !beneficiaryData.neighborhood) {
        throw new Error('Rua e bairro são obrigatórios')
      }

      // ✅ NOVO: Tratar data de nascimento se necessário
      let processedData = { ...beneficiaryData }
      if (processedData.birth_date && processedData.birth_date.toString().length > 10) {
        processedData.birth_date = timestamp_to_date(processedData.birth_date as unknown as number)
      }

      // ✅ NOVO: Preparar dados para envio (estrutura granularizada)
      const dataToSend = {
        name: processedData.name,
        document: processedData.document,
        
        // ✅ Endereço estruturado
        street: processedData.street,
        number: processedData.number || null,
        neighborhood: processedData.neighborhood,
        city: processedData.city || 'Pindamonhangaba',
        state: processedData.state || 'SP',
        zip_code: processedData.zip_code || null,
        complement: processedData.complement || null,
        
        contact: processedData.contact,
        monthly_limit: processedData.monthly_limit || 0.0,
        mother_name: processedData.mother_name || null,
        birth_date: processedData.birth_date || null,
        qtd_dogs: processedData.qtd_dogs || 0,
        qtd_castred_dogs: processedData.qtd_castred_dogs || 0,
        qtd_cats: processedData.qtd_cats || 0,
        qtd_castred_cats: processedData.qtd_castred_cats || 0,
        government_benefit: processedData.government_benefit || false,
        receives_basic_basket: processedData.receives_basic_basket || false,
        how_did_you_hear: processedData.how_did_you_hear || null,
        observations: processedData.observations || null
      }

      console.log('📤 Dados enviados para o backend:', dataToSend)

      const response = await fetch(`${BASE_URL}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(dataToSend)
      })
      
      if (!response.ok) {
        const error = await response.json()
        console.error('❌ Erro do backend:', error)
        throw new Error(error.detail || 'Failed to create beneficiary')
      }
      
      const responseData = await response.json()
      console.log('✅ Resposta do backend:', responseData)
      
      // ✅ NOVO: Converter resposta para instância do model
      return Beneficiary.fromBackend(responseData)
    } catch (error) {
      console.error('Error creating beneficiary:', error)
      throw error
    }
  },

  // ✅ ATUALIZADO: Usar novo model com endereço estruturado
  async update(id: number, beneficiaryData: Partial<Beneficiary>): Promise<Beneficiary> {
    console.log('🔄 beneficiaryService.update chamado', { id, beneficiaryData })
    
    try {
      // ✅ NOVO: Tratar data de nascimento se necessário
      let processedData = { ...beneficiaryData }
      if (processedData.birth_date && processedData.birth_date.toString().length > 10) {
        processedData.birth_date = timestamp_to_date(processedData.birth_date as unknown as number)
      }

      // ✅ NOVO: Preparar dados para envio (incluindo id como requerido pelo DTO)
      const dataToSend = {
        id, // ✅ ID obrigatório no update_beneficiary_dto
        name: processedData.name,
        document: processedData.document,
        
        // ✅ Endereço estruturado
        street: processedData.street,
        number: processedData.number,
        neighborhood: processedData.neighborhood,
        city: processedData.city,
        state: processedData.state,
        zip_code: processedData.zip_code,
        complement: processedData.complement,
        
        contact: processedData.contact,
        monthly_limit: processedData.monthly_limit,
        mother_name: processedData.mother_name,
        birth_date: processedData.birth_date,
        qtd_dogs: processedData.qtd_dogs,
        qtd_castred_dogs: processedData.qtd_castred_dogs,
        qtd_cats: processedData.qtd_cats,
        qtd_castred_cats: processedData.qtd_castred_cats,
        government_benefit: processedData.government_benefit,
        receives_basic_basket: processedData.receives_basic_basket,
        how_did_you_hear: processedData.how_did_you_hear,
        observations: processedData.observations
      }

      // ✅ NOVO: Remover campos undefined para envio limpo
      Object.keys(dataToSend).forEach(key => {
        if (dataToSend[key] === undefined) {
          delete dataToSend[key]
        }
      })

      console.log('📤 Dados de update enviados:', dataToSend)

      const response = await fetch(`${BASE_URL}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(dataToSend)
      })
      
      if (!response.ok) {
        const error = await response.json()
        console.error('❌ Erro do backend no update:', error)
        throw new Error(error.detail || 'Failed to update beneficiary')
      }
      
      const responseData = await response.json()
      console.log('✅ Resposta do update:', responseData)
      
      // ✅ NOVO: Converter resposta para instância do model
      return Beneficiary.fromBackend(responseData)
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
  },

  // ✅ NOVO: Métodos para buscar por endereço granularizado
  async searchByNeighborhood(neighborhood: string, skip: number = 0, limit: number = 100): Promise<[Beneficiary[], number]> {
    try {
      const response = await fetch(`${BASE_URL}/search/neighborhood/${encodeURIComponent(neighborhood)}?skip=${skip}&limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to search by neighborhood')
      }
      
      const data = await response.json()
      const beneficiaries = data.beneficiaries.map((item: any) => Beneficiary.fromBackend(item))
      
      return [beneficiaries, data.total]
    } catch (error) {
      console.error('Error searching by neighborhood:', error)
      throw error
    }
  },

  async searchByStreet(street: string, skip: number = 0, limit: number = 100): Promise<[Beneficiary[], number]> {
    try {
      const response = await fetch(`${BASE_URL}/search/street/${encodeURIComponent(street)}?skip=${skip}&limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to search by street')
      }
      
      const data = await response.json()
      const beneficiaries = data.beneficiaries.map((item: any) => Beneficiary.fromBackend(item))
      
      return [beneficiaries, data.total]
    } catch (error) {
      console.error('Error searching by street:', error)
      throw error
    }
  }
}