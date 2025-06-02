export interface RationInput {
  id?: number
  ration_stock_id: number
  amount: number
  date: string
  description: string
  ration_stock?: {
    id: number
    name: string
    unit: string
  }
}