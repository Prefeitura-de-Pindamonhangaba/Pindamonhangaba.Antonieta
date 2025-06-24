<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <div class="page-header">
        <n-h1>Dashboard</n-h1>
        <n-divider class="divider" />
      </div>

      <!-- Action Buttons -->
      <n-space>
        <app-button 
          type="primary" 
          @click="showDistributionModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Registrar Nova Saída
        </app-button>
        
        <app-button 
          type="primary"
          @click="showInputModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Registrar Nova Entrada
        </app-button>
        
        <app-button 
          @click="showBeneficiaryModal = true"
        >
          <template #icon>
            <n-icon><IconUserPlus /></n-icon>
          </template>
          Adicionar Novo Beneficiário
        </app-button>
      </n-space>

      <DistributionModal v-model="showDistributionModal" @submit="handleDistributionSubmit" />
      <InputModal v-model="showInputModal" @submit="handleInputSubmit" />
      <BeneficiaryModal v-model="showBeneficiaryModal" @submit="handleBeneficiarySubmit" />

      <!-- Summary Cards -->
      <n-grid x-gap="12" y-gap="12" cols="3" responsive="self">
        <n-grid-item>
          <n-card class="page-card">
            <n-space vertical align="center">
              <n-text depth="3">Entrada Total (Mês)</n-text>
              <n-statistic :value="`${total_inputs} kg`" />
            </n-space>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card class="page-card">
            <n-space vertical align="center">
              <n-text depth="3">Saída Total (Mês)</n-text>
              <n-statistic :value="`${total_distributions} kg`" />
            </n-space>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card class="page-card">
            <n-space vertical align="center">
              <n-text depth="3">Estoque Atual</n-text>
              <n-statistic :value="`${current_stock} kg`" />
            </n-space>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- Beneficiaries Table with Search -->
      <n-card class="page-card" title="Beneficiários e Controle Mensal">
        <n-space vertical size="small">
          <!-- Search input -->
          <search-field
            v-model:value="searchQuery"
            placeholder="Buscar por nome de beneficiário..."
            @search="handleSearch"
            style="margin-bottom: 12px;"
          />
          
          <!-- Data table -->
          <n-data-table
            :loading="loading"
            :columns="columns"
            :data="tableData"
            :pagination="pagination"
            @update:sorter="handleSort"
            remote
          />
        </n-space>
      </n-card>
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, onUnmounted, reactive, watch } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { 
  NLayout,
  NLayoutContent,
  NSpace,
  NButton,
  NCard,
  NDataTable,
  NIcon,
  NProgress,
  NTag,
  NGrid,
  NGi,
  NH1,
  NDivider,
  NText,
  NStatistic,
  NSpin,
  NInput
} from 'naive-ui'
import { IconPlus, IconUserPlus, IconCheck, IconAlertTriangle, IconX, IconSearch } from '@tabler/icons-vue'
import DistributionModal from '../components/modals/DistributionModal.vue'
import BeneficiaryModal from '../components/modals/BeneficiaryModal.vue'
import InputModal from '../components/modals/InputModal.vue'
import type { Beneficiary } from '../models/beneficiaryModel'
import { beneficiaryService } from '../services/beneficiaryService'
import { rationStockService } from '../services/rationStockService'
import { distributionService } from '~/services/distributionService'
import { rationInputService } from '~/services/rationInputService'
import { dashboardService } from '~/services/dashboardService'
import { useRoute } from 'vue-router'
import { useMessage } from 'naive-ui'

// Update BeneficiaryData interface to match the service response
interface BeneficiaryData {
  id: number
  nome: string
  limite_mensal: number  // Changed from limiteMensal to match backend
  recebido_mes: number   // Changed from recebido to match backend
  progresso: number
  status: 'Pode Receber' | 'Próx. Limite' | 'Limite Atingido'
}

const route = useRoute()
const message = useMessage()
const current_stock = ref(0)
const total_inputs = ref(0)
const total_distributions = ref(0)

const showDistributionModal = ref(false)
const showBeneficiaryModal = ref(false)
const showInputModal = ref(false)
const pageLoading = ref(true)

// Search state
const searchQuery = ref('')
const allBeneficiariesData = ref<BeneficiaryData[]>([])

// Add reactive refs for table data and loading state
const tableData = ref<BeneficiaryData[]>([])
const loading = ref(true)
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  onChange: async (page: number) => {
    await fetchBeneficiariesData(page)
  }
})

// Add sorting state
const sorter = ref<{ columnKey: keyof BeneficiaryData | null, order: 'ascend' | 'descend' | false }>({
  columnKey: null,
  order: false
})

// Handle search function
const handleSearch = (query: string) => {
  if (!query) {
    // If search is cleared, show all beneficiaries
    tableData.value = [...allBeneficiariesData.value]
    return
  }
  
  // Filter beneficiaries by name
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allBeneficiariesData.value.filter(beneficiary => 
    beneficiary.nome.toLowerCase().includes(normalizedQuery)
  )
}

// Handle sorting
const handleSort = (sorter: { columnKey: keyof BeneficiaryData, order: 'ascend' | 'descend' | false }) => {
  const { columnKey, order } = sorter
  
  if (!order || !columnKey) {
    // Reset to original data
    tableData.value = [...allBeneficiariesData.value]
    return
  }

  const sortedData = [...tableData.value]
  
  sortedData.sort((a, b) => {
    const multiplier = order === 'ascend' ? 1 : -1
    
    if (columnKey === 'limite_mensal' || columnKey === 'recebido_mes' || columnKey === 'progresso') {
      return (a[columnKey] - b[columnKey]) * multiplier
    }
    
    // For text columns
    const aValue = String(a[columnKey] || '')
    const bValue = String(b[columnKey] || '')
    return aValue.localeCompare(bValue) * multiplier
  })

  tableData.value = sortedData
}

const columns: DataTableColumns<BeneficiaryData> = [
  {
    title: 'Nome',
    key: 'nome',
    sorter: 'default'
  },
  {
    title: 'Limite Mensal',
    key: 'limite_mensal',
    sorter: 'default',
    render(row) {
      return `${row.limite_mensal} kg`
    }
  },
  {
    title: 'Recebido Este Mês',
    key: 'recebido_mes',
    sorter: 'default',
    render(row) {
      return `${row.recebido_mes} kg`
    }
  },
  {
    title: 'Progresso',
    key: 'progresso',
    sorter: 'default',
    render(row) {
      return h(NProgress, {
        type: 'line',
        percentage: row.progresso,
        indicatorPlacement: 'inside',
        processing: row.progresso < 100,
        status: row.progresso >= 80 ? 'error' : row.progresso >= 50 ? 'warning' : 'success',
        style: { width: '120px' }
      })
    }
  },
  {
    title: 'Status',
    key: 'status',
    sorter: 'default',
    render(row) {
      const statusConfig = {
        'Pode Receber': {
          icon: IconCheck,
          type: 'success',
          style: { backgroundColor: '#18a058', color: 'white' }
        },
        'Próx. Limite': {
          icon: IconAlertTriangle,
          type: 'warning',
          style: { backgroundColor: '#f0a020', color: 'white' }
        },
        'Limite Atingido': {
          icon: IconX,
          type: 'error',
          style: { backgroundColor: '#d03050', color: 'white' }
        }
      }

      const config = statusConfig[row.status as keyof typeof statusConfig]
      
      return h(
        NTag,
        {
          type: config.type,
          style: {
            ...config.style,
            padding: '4px 12px',
            fontSize: '14px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '4px'
          }
        },
        {
          default: () => [
            h(config.icon, { size: 16 }),
            row.status
          ]
        }
      )
    }
  }
]

// Add function to fetch beneficiaries data
const fetchBeneficiariesData = async (page: number = 1) => {
  try {
    loading.value = true
    const skip = (page - 1) * pagination.pageSize
    const beneficiariesData = await dashboardService.getBeneficiariesDashboard(skip, pagination.pageSize)
    
    allBeneficiariesData.value = beneficiariesData.data
    tableData.value = beneficiariesData.data
    pagination.itemCount = beneficiariesData.total
  } catch (error) {
    console.error('Error fetching beneficiaries:', error)
  } finally {
    loading.value = false
  }
}

// Update fetchDashboardData to handle loading state
const fetchDashboardData = async () => {
  try {
    pageLoading.value = true
    const [stockData, inputsData, distributionsData] = await Promise.all([
      dashboardService.getCurrentTotalStock(),
      dashboardService.getTotalInputsMonth(),
      dashboardService.getTotalDistributionsMonth()
    ])

    current_stock.value = stockData.current_stock
    total_inputs.value = inputsData.total_amount
    total_distributions.value = distributionsData.total_amount
    
    await fetchBeneficiariesData(pagination.page)
  } catch (error) {
    console.error('Error loading dashboard data:', error)
    message.error('Erro ao carregar dados do dashboard')
  } finally {
    pageLoading.value = false
  }
}

// Add all the existing handler functions
const handleDistributionSubmit = async (formData: any) => {
  try {
    const loadingMsg = message.loading('Registrando distribuição...', {
      duration: 0
    })
    
    await distributionService.create(formData)
    
    loadingMsg.destroy()
    message.success('Distribuição registrada com sucesso')
    
    await fetchDashboardData()
  } catch (error) {
    message.error('Erro ao registrar distribuição')
    console.error(error)
  }
}

const handleBeneficiarySubmit = async (formData: Beneficiary) => {
  try {
    const loadingMsg = message.loading('Cadastrando beneficiário...', {
      duration: 0
    })
    
    await beneficiaryService.create(formData)
    
    loadingMsg.destroy()
    message.success('Beneficiário cadastrado com sucesso')
    
    await fetchDashboardData()
  } catch (error) {
    message.error('Erro ao cadastrar beneficiário')
    console.error(error)
  }
}

const handleInputSubmit = async (formData: any) => {
  try {
    const loadingMsg = message.loading('Registrando entrada...', {
      duration: 0
    })
    
    await rationInputService.create(formData)
    
    loadingMsg.destroy()
    message.success('Entrada registrada com sucesso')
    
    await fetchDashboardData()
  } catch (error) {
    message.error('Erro ao registrar entrada')
    console.error(error)
  }
}

// Add onMounted hook to fetch initial data
onMounted(async () => {
  if (route.query.loading === 'true') {
    pageLoading.value = true
    await new Promise(resolve => setTimeout(resolve, 1000)) // Add minimal delay for better UX
  }
  await fetchDashboardData()
  startPolling()
})

// Watch for changes in all beneficiaries data
watch(() => allBeneficiariesData.value, () => {
  if (!searchQuery.value) {
    tableData.value = [...allBeneficiariesData.value]
  } else {
    handleSearch(searchQuery.value)
  }
})

// Add a function to update data periodically (optional)
let pollingInterval: NodeJS.Timer | null = null

const startPolling = () => {
  const interval = 30000 // 30 seconds
  pollingInterval = setInterval(() => {
    fetchDashboardData()
  }, interval)
}

// Clean up interval when component is unmounted
onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
})
</script>

<style scoped>
.n-spin {
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
}

.divider {
  width: 100px;
  margin: 0;
  background-color: #f77800;
}

.app-button {
  font-size: 14px;
  padding: 12px 24px;
}

.page-card {
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-field {
  max-width: 300px;
  margin-bottom: 12px;
}
</style>