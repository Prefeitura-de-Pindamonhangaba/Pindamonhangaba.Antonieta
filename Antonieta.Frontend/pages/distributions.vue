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
        <search-field
          v-model:value="searchQuery"
          placeholder="Buscar por beneficiário, ração ou observações..."
          @search="handleSearch"
        />

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

      <DistributionModal 
        v-model="showDistributionModal"
        @submit="handleDistributionSubmit"
      />

      <!-- ✅ NOVO: Modal para visualizar observações completas -->
      <n-modal
        v-model:show="showObservationsModal"
        preset="card"
        title="Observações da Distribuição"
        style="width: 600px"
      >
        <div class="observations-modal">
          <div class="distribution-info">
            <n-text strong>📋 Distribuição</n-text>
            <br>
            <n-text depth="2" style="font-size: 14px">
              👤 {{ selectedDistribution?.beneficiaryName }}
            </n-text>
            <br>
            <n-text depth="2" style="font-size: 14px">
              🥫 {{ selectedDistribution?.rationTypeName }} - {{ selectedDistribution?.amount.toFixed(2) }}kg
            </n-text>
            <br>
            <n-text depth="2" style="font-size: 14px">
              📅 {{ selectedDistribution ? formatDate(selectedDistribution.date) : '' }}
            </n-text>
          </div>
          
          <n-divider />
          
          <div class="observations-content">
            <n-text strong>📝 Observações:</n-text>
            <div class="observations-text">
              {{ selectedDistribution?.observations || 'Nenhuma observação registrada.' }}
            </div>
          </div>
        </div>
        
        <template #action>
          <n-button @click="showObservationsModal = false">
            Fechar
          </n-button>
        </template>
      </n-modal>
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { 
  NCard, NDataTable, NButton, NIcon, NLayout, NLayoutContent, 
  NSpace, NH1, NDivider, NInput, NModal, NText, NTooltip, useMessage 
} from 'naive-ui'
import { IconPlus, IconSearch, IconEye, IconFileText } from '@tabler/icons-vue'
import DistributionModal from '../components/modals/DistributionModal.vue'
import { distributionService } from '~/services/distributionService'
import { beneficiaryService } from '~/services/beneficiaryService'
import { rationTypeService } from '~/services/rationTypeService'
import type { Distribution } from '~/models/distributionModel'
import { rationStockService } from '~/services/rationStockService'

const message = useMessage()
const loading = ref(false)
const showDistributionModal = ref(false)
const tableData = ref<Distribution[]>([])
const allDistributions = ref<Distribution[]>([])
const beneficiariesMap = ref<Map<number, string>>(new Map())
const rationTypesMap = ref<Map<number, string>>(new Map())
const pageLoading = ref(true)
const searchQuery = ref('')

// ✅ NOVO: Estado para modal de observações
const showObservationsModal = ref(false)
const selectedDistribution = ref<Distribution | null>(null)

// ✅ NOVO: Função para mostrar observações
const showObservations = (distribution: Distribution) => {
  selectedDistribution.value = distribution
  showObservationsModal.value = true
}

// ✅ NOVO: Função para formatar data
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// ✅ ATUALIZADO: Busca incluindo observações
const handleSearch = (query: string) => {
  if (!query) {
    tableData.value = [...allDistributions.value]
    return
  }
  
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allDistributions.value.filter(distribution => 
    (distribution.beneficiaryName?.toLowerCase().includes(normalizedQuery) || 
     distribution.rationTypeName?.toLowerCase().includes(normalizedQuery) ||
     distribution.observations?.toLowerCase().includes(normalizedQuery)) // ✅ NOVO: Buscar nas observações
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
      
      const [distributions, total] = await distributionService.getAll()
      
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
      
      const [distributions, total] = await distributionService.getAll()
      
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

// ✅ NOVO: Manipulador de envio de distribuição
const handleDistributionSubmit = async (newDistribution: Distribution) => {
  try {
    // Recarregar lista após nova distribuição
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
    width: 150,
    render(row) {
      return formatDate(row.date)
    }
  },
  {
    title: 'Beneficiário',
    key: 'beneficiaryName',
    sorter: 'default',
    render(row) {
      return row.beneficiaryName || 'N/A'
    }
  },
  {
    title: 'Tipo de Ração',
    key: 'rationTypeName',
    sorter: 'default',
    render(row) {
      return row.rationTypeName || 'N/A'
    }
  },
  {
    title: 'Quantidade',
    key: 'amount',
    sorter: (row1: Distribution, row2: Distribution) => 
      row1.amount - row2.amount,
    width: 120,
    render: (row: Distribution) => `${row.amount.toFixed(2)} kg`
  },
  // ✅ NOVO: Coluna de observações
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

      // Se a observação é muito longa, truncar e mostrar botão para ver completa
      const maxLength = 50
      const truncated = row.observations.length > maxLength
      const displayText = truncated 
        ? row.observations.substring(0, maxLength) + '...'
        : row.observations

      return h('div', { style: { display: 'flex', alignItems: 'center', gap: '8px' } }, [
        // Texto das observações (truncado se necessário)
        h('span', { 
          title: row.observations,
          style: { 
            flex: 1,
            fontSize: '13px',
            lineHeight: '1.4'
          } 
        }, displayText),
        
        // Botão para ver observações completas (se truncado)
        truncated && h(NButton, {
          size: 'tiny',
          text: true,
          type: 'primary',
          onClick: () => showObservations(row),
          style: { fontSize: '12px' }
        }, {
          default: () => 'Ver mais',
          icon: () => h(NIcon, { size: 14 }, { default: () => h(IconEye) })
        })
      ])
    }
  },
  // ✅ NOVO: Coluna de ações (se precisar de mais ações no futuro)
  {
    title: 'Ações',
    key: 'actions',
    width: 80,
    render(row) {
      return h('div', { style: { display: 'flex', gap: '4px' } }, [
        // Botão para ver observações (sempre visível se há observações)
        row.observations && h(NTooltip, { trigger: 'hover' }, {
          default: () => 'Ver observações completas',
          trigger: () => h(NButton, {
            size: 'small',
            text: true,
            type: 'info',
            onClick: () => showObservations(row)
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

/* ✅ NOVO: Estilos para modal de observações */
.observations-modal {
  padding: 8px 0;
}

.distribution-info {
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #f77800;
}

.observations-content {
  margin-top: 16px;
}

.observations-text {
  margin-top: 8px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #52c41a;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap; /* Preserva quebras de linha */
  word-break: break-word;
}

/* ✅ NOVO: Estilo para linha da tabela com observações */
:deep(.n-data-table-td) {
  vertical-align: top;
}

/* ✅ NOVO: Estilo para texto truncado */
.observation-truncated {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>