import type { RationType } from '../models/rationTypeModel'
import { rationStockService } from './rationStockService'
import { apiFetch } from '~/utils/apiFetch'
import { useRuntimeConfig } from '#app'

export const rationTypeService = {
  async getAll(): Promise<RationType[]> {
    return rationStockService.getAll()
  },
  async getById(id: number): Promise<RationType> {
    return rationStockService.getById(id)
  },
  async create(rationType: Omit<RationType, 'id'>): Promise<RationType> {
    return rationStockService.create({ ...rationType, unit: 'kg', stock: 0 })
  },
  async update(id: number, rationType: Partial<RationType>): Promise<RationType> {
    // Metadata updates never send a stale stock balance from a prior read.
    const response = await apiFetch(`${useRuntimeConfig().public.backendUrl}/ration-stock/${id}`, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...rationType, id }),
    })
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to update ration type')
    return response.json()
  },
  async delete(id: number): Promise<void> {
    return rationStockService.delete(id)
  },
}
