interface DashboardData {
  total_amount: number;
  month: number;
  year: number;
}

interface StockData {
  current_stock: number;
  last_updated: string;
}

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  skip: number;
  limit: number;
}

interface BeneficiaryDashboardData {
  id: number;
  nome: string;
  limiteMensal: number;
  recebido: number;
  progresso: number;
  status: 'Pode Receber' | 'Próx. Limite' | 'Limite Atingido';
}

const BASE_URL = useRuntimeConfig().public.backendUrl + '/dashboard'

export const dashboardService = {
  async getTotalInputsMonth(): Promise<DashboardData> {
    const response = await fetch(`${BASE_URL}/total-inputs-month`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch total inputs for month')
    }
    
    return response.json()
  },

  async getTotalDistributionsMonth(): Promise<DashboardData> {
    const response = await fetch(`${BASE_URL}/total-distributions-month`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch total distributions for month')
    }
    
    return response.json()
  },

  async getCurrentTotalStock(): Promise<StockData> {
    const response = await fetch(`${BASE_URL}/current-total-stock`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch current total stock')
    }
    
    return response.json()
  },

  async getBeneficiariesDashboard(skip: number = 0, limit: number = 10): Promise<PaginatedResponse<BeneficiaryDashboardData>> {
    const response = await fetch(`${BASE_URL}/beneficiaries-dashboard?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch beneficiaries dashboard')
    }
    
    return response.json()
  }
}