<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <div class="page-header">
        <n-h1>Distribuições</n-h1>
        <n-divider class="divider" />
      </div>

      <!-- Search and Action Buttons -->
      <n-space justify="space-between" align="center">
        <n-space align="center">
          <search-field
            v-model:value="searchQuery"
            placeholder="Buscar por beneficiário, ração ou observações..."
            @search="handleSearch"
          />
          
          <!-- Toggle para visualizar dados antigos (apenas para gestores) -->
          <n-space v-if="canViewOldRecords()" align="center">
            <n-switch v-model:value="showOldRecords" @update:value="handleToggleOldRecords">
              <template #checked>
                Mostrando Todos
              </template>
              <template #unchecked>
                Apenas Ativos
              </template>
            </n-switch>
            <n-text depth="3" style="font-size: 12px;">
              {{ showOldRecords ? 'Incluindo registros antigos' : 'Apenas registros ativos' }}
            </n-text>
          </n-space>
        </n-space>

        <app-button 
          type="primary" 
          @click="showDistributionModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Registrar Nova Distribuição
        </app-button>
      </n-space>

      <!-- Table -->
      <n-card class="page-card">
        <n-data-table
          :columns="columns"
          :data="tableData"
          :pagination="pagination"
          :loading="loading"
          @update:sorter="handleSort"
          :row-key="(row: Distribution) => row.id"
        />
      </n-card>

      <!-- ✅ ATUALIZADO: Modal de nova distribuição -->
      <DistributionModal 
        v-model="showDistributionModal"
        @submit="handleDistributionSubmit"
      />

      <!-- ✅ NOVO: Modal de detalhes extraído -->
      <DistributionDetailsModal
        v-model="showDetailsModal"
        :distribution="selectedDistribution"
      />
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { 
  NCard, NDataTable, NButton, NIcon, NSpace, NH1, NDivider, 
  NTooltip, NSwitch, NText, useMessage 
} from 'naive-ui'
import { IconPlus, IconEye, IconFileText } from '@tabler/icons-vue'
import DistributionModal from '../components/modals/DistributionModal.vue'
import DistributionDetailsModal from '../components/modals/DistributionDetailsModal.vue' // ✅ NOVO
import { distributionService } from '~/services/distributionService'
import { beneficiaryService } from '~/services/beneficiaryService'
import { rationStockService } from '~/services/rationStockService'
import { useAuth } from '~/composables/useAuth'
import type { Distribution } from '~/models/distributionModel'

const { canViewOldRecords } = useAuth()
const message = useMessage()
const loading = ref(false)
const showDistributionModal = ref(false)
const tableData = ref<Distribution[]>([])
const allDistributions = ref<Distribution[]>([])
const beneficiariesMap = ref<Map<number, string>>(new Map())
const rationTypesMap = ref<Map<number, string>>(new Map())
const pageLoading = ref(true)
const searchQuery = ref('')
const showOldRecords = ref(false)

// ✅ ATUALIZADO: Estado para modal de detalhes
const showDetailsModal = ref(false)
const selectedDistribution = ref<Distribution | null>(null)

// ✅ ATUALIZADO: Função para mostrar detalhes
const showDistributionDetails = (distribution: Distribution) => {
  selectedDistribution.value = distribution
  showDetailsModal.value = true
}

// Função para formatar data
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Busca incluindo observações
const handleSearch = (query: string) => {
  if (!query) {
    tableData.value = [...allDistributions.value]
    return
  }
  
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allDistributions.value.filter(distribution => 
    (distribution.beneficiaryName?.toLowerCase().includes(normalizedQuery) || 
     distribution.rationTypeName?.toLowerCase().includes(normalizedQuery) ||
     distribution.observations?.toLowerCase().includes(normalizedQuery))
  )
}

// Função para buscar distribuições
const fetchDistributions = async () => {
  try {
    loading.value = true
    
    if (!pageLoading.value) {
      const loadingMsg = message.loading('Atualizando lista de distribuições...', {
        duration: 0
      })
      
      await Promise.all([loadBeneficiaries(), loadRationStocks()])
      
      const [distributions, total] = await distributionService.getAll(showOldRecords.value)
      
      loadingMsg.destroy()
      message.success(`${distributions.length} distribuições carregadas com sucesso!`)
      
      const processedDistributions = distributions.map(dist => ({
        ...dist,
        beneficiaryName: dist.beneficiary_id ? beneficiariesMap.value.get(dist.beneficiary_id) : 'N/A',
        rationTypeName: rationTypesMap.value.get(dist.ration_id) || 'N/A'
      }))
      
      allDistributions.value = processedDistributions
      tableData.value = processedDistributions
      pagination.value.itemCount = total || distributions.length
    } else {
      await Promise.all([loadBeneficiaries(), loadRationStocks()])
      
      const [distributions, total] = await distributionService.getAll(showOldRecords.value)
      
      const processedDistributions = distributions.map(dist => ({
        ...dist,
        beneficiaryName: dist.beneficiary_id ? beneficiariesMap.value.get(dist.beneficiary_id) : 'N/A',
        rationTypeName: rationTypesMap.value.get(dist.ration_id) || 'N/A'
      }))
      
      allDistributions.value = processedDistributions
      tableData.value = processedDistributions
      pagination.value.itemCount = total || distributions.length
    }
  } catch (error) {
    console.error('Error fetching distributions:', error)
    message.error({
      content: 'Erro ao carregar distribuições. Tente novamente.',
      duration: 5000,
      closable: true
    })
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

// Função para carregar beneficiários
const loadBeneficiaries = async () => {
  try {
    const [beneficiaries] = await beneficiaryService.getAll()
    beneficiariesMap.value = new Map(
      beneficiaries.map(b => [b.id, b.name])
    )
  } catch (error) {
    console.error('Error loading beneficiaries:', error)
  }
}

const loadRationStocks = async () => {
  try {
    const rationStocks = await rationStockService.getAll()
    rationTypesMap.value = new Map(
      rationStocks.map(rs => [rs.id, rs.name])
    )
  } catch (error) {
    console.error('Error loading ration types:', error)
    message.error('Erro ao carregar tipos de ração')
  }
}

// Função para lidar com toggle de dados antigos
const handleToggleOldRecords = async () => {
  await fetchDistributions()
}

// Manipulador de envio de distribuição
const handleDistributionSubmit = async (newDistribution: Distribution) => {
  try {
    await fetchDistributions()
    showDistributionModal.value = false
  } catch (error) {
    console.error('Error handling distribution submit:', error)
  }
}

// Ordenação
const handleSort = (sorter: { columnKey: keyof Distribution, order: 'ascend' | 'descend' | false }) => {
  const { columnKey, order } = sorter
  
  if (!order || !columnKey) {
    fetchDistributions()
    return
  }

  const sortedData = [...tableData.value]
  
  sortedData.sort((a, b) => {
    const multiplier = order === 'ascend' ? 1 : -1
    
    if (columnKey === 'date') {
      return (new Date(a.date).getTime() - new Date(b.date).getTime()) * multiplier
    }
    
    if (columnKey === 'amount') {
      return ((a.amount || 0) - (b.amount || 0)) * multiplier
    }
    
    const aValue = String(a[columnKey as keyof Distribution] || '')
    const bValue = String(b[columnKey as keyof Distribution] || '')
    return aValue.localeCompare(bValue) * multiplier
  })

  tableData.value = sortedData
}

// ✅ ATUALIZADO: Colunas com observações
const columns: DataTableColumns<Distribution> = [
  {
    title: 'Data',
    key: 'date',
    sorter: 'default',
    minWidth: 110,
    render(row) {
      return formatDate(row.date)
    }
  },
  {
    title: 'Beneficiário',
    key: 'beneficiaryName',
    sorter: 'default',
    minWidth: 180,
    render(row) {
      return row.beneficiaryName || 'N/A'
    }
  },
  {
    title: 'Tipo de Ração',
    key: 'rationTypeName',
    sorter: 'default',
    minWidth: 160,
    render(row) {
      return row.rationTypeName || 'N/A'
    }
  },
  {
    title: 'Quantidade',
    key: 'amount',
    sorter: (row1: Distribution, row2: Distribution) => 
      row1.amount - row2.amount,
    width: 130,
    render: (row: Distribution) => `${row.amount.toFixed(2)} kg`
  },
  // Coluna de observações
  {
    title: 'Observações',
    key: 'observations',
    width: 200,
    render(row) {
      if (!row.observations || row.observations.trim() === '') {
        return h('span', { 
          style: { color: '#999', fontStyle: 'italic' } 
        }, 'Sem observações')
      }

      const maxLength = 50
      const truncated = row.observations.length > maxLength
      const displayText = truncated 
        ? row.observations.substring(0, maxLength) + '...'
        : row.observations

      return h('div', { style: { display: 'flex', alignItems: 'center', gap: '8px' } }, [
        h('span', { 
          title: row.observations,
          style: { 
            flex: 1,
            fontSize: '13px',
            lineHeight: '1.4'
          } 
        }, displayText),
        
        // ✅ ATUALIZADO: Botão usa função atualizada
        truncated && h(NButton, {
          size: 'tiny',
          text: true,
          type: 'primary',
          onClick: () => showDistributionDetails(row),
          style: { fontSize: '12px' }
        }, {
          default: () => 'Ver mais',
          icon: () => h(NIcon, { size: 14 }, { default: () => h(IconEye) })
        })
      ])
    }
  },
  // Coluna de ações
  {
    title: 'Ações',
    key: 'actions',
    width: 80,
    render(row) {
      return h('div', { style: { display: 'flex', gap: '4px' } }, [
        // ✅ ATUALIZADO: Botão sempre visível para ver detalhes
        h(NTooltip, { trigger: 'hover' }, {
          default: () => 'Ver detalhes da distribuição',
          trigger: () => h(NButton, {
            size: 'small',
            text: true,
            type: 'info',
            onClick: () => showDistributionDetails(row)
          }, {
            icon: () => h(NIcon, { size: 16 }, { default: () => h(IconFileText) })
          })
        })
      ])
    }
  }
]

const pagination = ref({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  onUpdatePage: (page: number) => {
    pagination.value.page = page
    fetchDistributions()
  }
})

// Carrega os dados quando o componente é montado
onMounted(() => {
  pageLoading.value = true
  fetchDistributions()
})

// Reset search when data is refreshed
watch(() => allDistributions.value, () => {
  if (!searchQuery.value) {
    tableData.value = [...allDistributions.value]
  } else {
    handleSearch(searchQuery.value)
  }
})
</script>

<style scoped>
.page-header {
  color: #f77800;
  margin: 0;
}

.divider {
  width: 100px;
  margin: 0;
  background-color: #f77800;
}

.search-field {
  width: 350px;
}

.app-button {
  background-color: #f77800;
  font-size: 14px;
  padding: 12px 24px;
}

.page-card {
  margin-top: 24px;
}

/* Estilo para linha da tabela com observações */
:deep(.n-data-table-td) {
  vertical-align: top;
}
</style>