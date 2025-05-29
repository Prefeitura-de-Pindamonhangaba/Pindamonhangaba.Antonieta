export interface RationStock {
  id: number
  name: string
  ration_type_id: number
  unit: string
  stock: number
  description: string
  distributions_id?: number[]
}
export interface Ration {
  id: number
  name: string
  ration_type_id: number
  unit: string
  stock: number
  description: string
  distributions_id?: number[]
}