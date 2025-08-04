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
          placeholder="Buscar por beneficiário ou tipo de ração..."
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
        />
      </n-card>

      <DistributionModal 
        v-model="showDistributionModal" 
        @submit="handleDistributionSubmit" 
      />
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { NCard, NDataTable, NButton, NIcon, NLayout, NLayoutContent, NSpace, NH1, NDivider, NInput, useMessage } from 'naive-ui'
import { IconPlus, IconSearch } from '@tabler/icons-vue'
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

// Adiciona a função de busca
const handleSearch = (query: string) => {
  if (!query) {
    // Se a busca for limpa, mostre todas as distribuições
    tableData.value = [...allDistributions.value]
    return
  }
  
  // Filtra distribuições por beneficiário ou tipo de ração
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allDistributions.value.filter(distribution => 
    (distribution.beneficiaryName?.toLowerCase().includes(normalizedQuery) || 
     distribution.rationTypeName?.toLowerCase().includes(normalizedQuery))
  )
}

// Função para buscar distribuições
const fetchDistributions = async () => {
  try {
    loading.value = true
    
    // Adiciona um pequeno atraso para mostrar o loading (apenas se estiver recarregando)
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
      // Carregamento inicial, sem mensagem
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

// // Atualiza o manipulador de envio para usar o serviço
// const handleDistributionSubmit = async (formData: Omit<Distribution, 'id'>) => {
//   try {
//     const loadingMsg = message.loading('Registrando distribuição...', {
//       duration: 0
//     })
    
//     await distributionService.create(formData)
    
//     loadingMsg.destroy()
//     message.success('Distribuição registrada com sucesso')
    
//     await fetchDistributions()
//   } catch (error) {
//     message.error({
//       content: 'Erro ao registrar distribuição. Tente novamente.',
//       duration: 5000,
//       closable: true
//     })
//     console.error(error)
//   }
// }

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
    
    // Para beneficiaryName e rationTypeName
    const aValue = String(a[columnKey as keyof Distribution] || '')
    const bValue = String(b[columnKey as keyof Distribution] || '')
    return aValue.localeCompare(bValue) * multiplier
  })

  tableData.value = sortedData
}

// Atualiza as colunas para corresponder ao modelo de Distribuição
const columns: DataTableColumns<Distribution> = [
  {
    title: 'Data',
    key: 'date',
    sorter: 'default',
    render(row) {
      return new Date(row.date).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
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
    render: (row: Distribution) => `${row.amount.toFixed(2)} kg` // Mostrar com 2 casas decimais
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
</style>