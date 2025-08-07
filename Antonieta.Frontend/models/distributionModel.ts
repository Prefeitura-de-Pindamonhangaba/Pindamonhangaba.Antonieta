export interface Distribution {
  id?: number
  beneficiary_id: number
  ration_id: number
  amount: number 
  date: string
  observations?: string | null
  beneficiary?: {
    id: number
    name: string
    document: string
  }
  ration?: {
    id: number
    name: string
    description?: string
  }
}

export interface DistributionCreate {
  beneficiary_id: number
  ration_id: number
  amount: number 
  date: string
  observations?: string | null
}

export interface DistributionUpdate {
  beneficiary_id?: number
  ration_id?: number
  amount?: number
  date?: string
  observations?: string | null
}