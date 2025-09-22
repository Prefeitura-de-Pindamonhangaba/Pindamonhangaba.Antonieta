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

      <!-- ✅ ATUALIZADO: Summary Cards com formatação correta -->
      <n-grid x-gap="12" y-gap="12" cols="3" responsive="self">
        <n-grid-item>
          <n-card class="page-card">
            <n-space vertical align="center">
              <n-text depth="3">Entrada Total (Mês)</n-text>
              <n-statistic :value="formatWeight(total_inputs)" />
            </n-space>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card class="page-card">
            <n-space vertical align="center">
              <n-text depth="3">Saída Total (Mês)</n-text>
              <!-- ✅ CORRIGIDO: Formatação com 2 casas decimais -->
              <n-statistic :value="formatWeight(total_distributions)" />
            </n-space>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card class="page-card">
            <n-space vertical align="center">
              <n-text depth="3">Estoque Atual</n-text>
              <n-statistic :value="formatWeight(current_stock)" />
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
  NCard,
  NDataTable,
  NProgress,
  NTag,
  NGrid,
  NDivider,
  NText,
  NStatistic
} from 'naive-ui'
import { IconPlus, IconUserPlus } from '@tabler/icons-vue'
import DistributionModal from '../components/modals/DistributionModal.vue'
import BeneficiaryModal from '../components/modals/BeneficiaryModal.vue'
import InputModal from '../components/modals/InputModal.vue'
import { beneficiaryService } from '../services/beneficiaryService'
import { rationStockService } from '../services/rationStockService'
import { distributionService } from '~/services/distributionService'
import { rationInputService } from '~/services/rationInputService'
import { dashboardService } from '~/services/dashboardService'
import { useRoute } from 'vue-router'
import { useMessage } from 'naive-ui'

// Update BeneficiaryData interface to only include received-this-month
interface BeneficiaryData {
  id: number
  nome: string
  recebido_mes: number
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

// Keep format helper
const formatWeight = (value: number): string => {
  if (value === 0) return '0,00 kg'
  return `${Number(value || 0).toFixed(2).replace('.', ',')} kg`
}

// Handle search function
const handleSearch = (query: string) => {
  if (!query) {
    tableData.value = [...allBeneficiariesData.value]
    return
  }
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allBeneficiariesData.value.filter(beneficiary => 
    beneficiary.nome.toLowerCase().includes(normalizedQuery)
  )
}

// Handle sorting (only by nome or recebido_mes)
const handleSort = (sorter: { columnKey: keyof BeneficiaryData, order: 'ascend' | 'descend' | false }) => {
  const { columnKey, order } = sorter
  if (!order || !columnKey) {
    tableData.value = [...allBeneficiariesData.value]
    return
  }
  const sortedData = [...tableData.value]
  const multiplier = order === 'ascend' ? 1 : -1
  sortedData.sort((a, b) => {
    const aVal = a[columnKey] ?? ''
    const bVal = b[columnKey] ?? ''
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return (aVal - bVal) * multiplier
    }
    return String(aVal).localeCompare(String(bVal)) * multiplier
  })
  tableData.value = sortedData
}

// Columns: only Nome e Recebido Este Mês
const columns: DataTableColumns<BeneficiaryData> = [
  {
    title: 'Nome',
    key: 'nome',
    sorter: 'default'
  },
  {
    title: 'Recebido Este Mês',
    key: 'recebido_mes',
    sorter: 'default',
    render(row) {
      return formatWeight(row.recebido_mes)
    }
  }
]

// Fetch beneficiaries and normalize shape to incluir somente recebido_mes
const fetchBeneficiariesData = async (page: number = 1) => {
  try {
    loading.value = true
    const skip = (page - 1) * pagination.pageSize
    const resp = await dashboardService.getBeneficiariesDashboard(skip, pagination.pageSize)
    // normalizar campos: backend pode retornar "recebido" ou "recebido_mes"
    const normalized = resp.data.map((item: any) => ({
      id: item.id,
      nome: item.nome ?? item.name ?? '',
      recebido_mes: Number(item.recebido ?? item.recebido_mes ?? item.recebidoMes ?? 0)
    }))
    allBeneficiariesData.value = normalized
    tableData.value = normalized
    pagination.itemCount = resp.total
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

/* ✅ NOVO: Estilo para estatísticas */
:deep(.n-statistic .n-statistic-value) {
  font-size: 2rem;
  font-weight: 600;
  color: #f77800;
}
</style>