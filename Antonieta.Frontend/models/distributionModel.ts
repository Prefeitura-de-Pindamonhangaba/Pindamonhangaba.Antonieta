export interface Distribution {
  id?: number
  beneficiary_id: number
  ration_stock_id: number
  amount: number
  date: string
  description?: string
  beneficiary?: {
    id: number
    name: string
  }
  ration_stock?: {
    id: number
    name: string
    unit: string
  }
}