<template>
  <n-layout style="min-height: 100vh">
    <n-spin :show="pageLoading" description="Carregando dashboard...">
      <n-layout-content style="padding: 24px">
        <n-space vertical size="large">
          <!-- Header -->
          <n-space vertical size="small">
            <n-h1 style="color: #f77800; margin: 0">Dashboard</n-h1>
            <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
          </n-space>

          <!-- Action Buttons -->
          <n-space>
            <n-button 
              type="primary" 
              style="font-size: 14px; padding: 12px 24px"
              @click="showDonationModal = true"
            >
              <template #icon>
                <n-icon><IconPlus /></n-icon>
              </template>
              Registrar Nova Saída
            </n-button>
            <n-button 
              type="primary"
              style="font-size: 14px; padding: 12px 24px"
              @click="showInputModal = true"
            >
              <template #icon>
                <n-icon><IconPlus /></n-icon>
              </template>
              Registrar Nova Entrada
            </n-button>
            <n-button 
              style="color: #f77800; border-color: #f77800; font-size: 14px; padding: 12px 24px"
              @click="showBeneficiaryModal = true"
            >
              <template #icon>
                <n-icon><IconUserPlus /></n-icon>
              </template>
              Adicionar Novo Beneficiário
            </n-button>
          </n-space>

          <DonationModal v-model="showDonationModal" @submit="handleDonationSubmit" />
          <InputModal v-model="showInputModal" @submit="handleInputSubmit" />
          <BeneficiaryModal v-model="showBeneficiaryModal" @submit="handleBeneficiarySubmit" />

          <!-- Summary Cards -->
          <n-grid x-gap="12" y-gap="12" cols="3" responsive="self">
            <n-gi>
              <n-card>
                <n-space vertical align="center">
                  <n-text depth="3">Entrada Total (Mês)</n-text>
                  <n-statistic :value="`${total_inputs} kg`" />
                </n-space>
              </n-card>
            </n-gi>
            <n-gi>
              <n-card>
                <n-space vertical align="center">
                  <n-text depth="3">Saída Total (Mês)</n-text>
                  <n-statistic :value="`${total_distributions} kg`" />
                </n-space>
              </n-card>
            </n-gi>
            <n-gi>
              <n-card>
                <n-space vertical align="center">
                  <n-text depth="3">Estoque Atual</n-text>
                  <n-statistic :value="`${current_stock} kg`" />
                </n-space>
              </n-card>
            </n-gi>
          </n-grid>

          <!-- Beneficiaries Table -->
          <n-card title="Beneficiários e Controle Mensal">
            <n-data-table
              :loading="loading"
              :columns="columns"
              :data="tableData"
              :pagination="pagination"
              remote
            />
          </n-card>
        </n-space>
      </n-layout-content>
    </n-spin>
  </n-layout>
</template>

<script setup lang="ts">
import { h, ref, onMounted, onUnmounted, reactive } from 'vue'
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
  NSpin
} from 'naive-ui'
import { IconPlus, IconUserPlus, IconCheck, IconAlertTriangle, IconX } from '@tabler/icons-vue'
import DonationModal from '../components/modals/DonationModal.vue'
import BeneficiaryModal from '../components/modals/BeneficiaryModal.vue'
import InputModal from '../components/modals/InputModal.vue'
import type { Beneficiary } from '../models/beneficiary'
import { beneficiaryService } from '../services/beneficiaryService'
import { rationStockService } from '../services/rationStockService'
import { distributionService } from '~/services/distributionService'
import { rationInputService } from '~/services/rationInputService'
import { dashboardService } from '~/services/dashboardService'
import { useRoute } from 'vue-router'

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
const current_stock = ref(0)
const total_inputs = ref(0)
const total_distributions = ref(0)

const showDonationModal = ref(false)
const showBeneficiaryModal = ref(false)
const showInputModal = ref(false)
const pageLoading = ref(true)

const handleDonationSubmit = (formData: any) => {
  console.log('Doação registrada:', formData)
  // Aqui você pode implementar a lógica para salvar a doação
}

const handleBeneficiarySubmit = (formData: Beneficiary) => {
  console.log('Beneficiary submitted:', formData)
}

// Add handler function
const handleInputSubmit = async (formData: any) => {
  try {
    await rationInputService.create(formData)
    message.success('Entrada registrada com sucesso')
    await fetchDashboardData()
  } catch (error) {
    message.error('Erro ao registrar entrada')
    console.error(error)
  }
}

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

const columns: DataTableColumns<BeneficiaryData> = [
  {
    title: 'Nome',
    key: 'nome'
  },
  {
    title: 'Limite Mensal',
    key: 'limite_mensal',  // Changed from limiteMensal
    render(row) {
      return `${row.limite_mensal} kg`
    }
  },
  {
    title: 'Recebido Este Mês',
    key: 'recebido_mes',   // Changed from recebido
    render(row) {
      return `${row.recebido_mes} kg`
    }
  },
  {
    title: 'Progresso',
    key: 'progresso',
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

// Add onMounted hook to fetch initial data
onMounted(async () => {
  if (route.query.loading === 'true') {
    pageLoading.value = true
    await new Promise(resolve => setTimeout(resolve, 1000)) // Add minimal delay for better UX
  }
  await fetchDashboardData()
  startPolling()
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
</style>