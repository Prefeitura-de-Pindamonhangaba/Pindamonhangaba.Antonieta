<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <n-space vertical size="small">
        <n-h1 style="color: #f77800; margin: 0">Entradas de Ração</n-h1>
        <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
      </n-space>

      <!-- Search and Action Buttons -->
      <n-space justify="space-between" align="center">
        <n-input
          v-model:value="searchQuery"
          placeholder="Buscar por tipo de ração..."
          clearable
          style="width: 300px"
          @update:value="handleSearch"
        >
          <template #prefix>
            <n-icon><IconSearch /></n-icon>
          </template>
        </n-input>

        <n-button 
          type="primary" 
          style="background-color: #f77800; font-size: 14px; padding: 12px 24px"
          @click="showInputModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Registrar Nova Entrada
        </n-button>
      </n-space>

      <!-- Table -->
      <n-card>
        <n-data-table
          :columns="columns"
          :data="tableData"
          :pagination="pagination"
          :loading="loading"
          @update:sorter="handleSort"
        />
      </n-card>

      <InputModal 
        v-model="showInputModal" 
        @submit="handleInputSubmit" 
      />
  
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { NCard, NDataTable, NButton, NIcon, NLayout, NLayoutContent, NSpace, NH1, NDivider, NInput, useMessage } from 'naive-ui'
import { IconPlus, IconSettings, IconSearch } from '@tabler/icons-vue'
import InputModal from '../components/modals/InputModal.vue'
import { rationInputService } from '~/services/rationInputService'
import { rationStockService } from '~/services/rationStockService'
import type { RationInput } from '~/models/rationInputModel'
import type { RationStock } from '~/models/rationStockModel'

const message = useMessage()
const loading = ref(false)
const showInputModal = ref(false)
const showrationStockModal = ref(false)
const tableData = ref<RationInput[]>([])
const allInputs = ref<RationInput[]>([])
const rationStocksMap = ref<Map<number, string>>(new Map())
const selectedrationStock = ref<RationStock | null>(null)
const pageLoading = ref(true)
const searchQuery = ref('')

// Adicione a função de busca
const handleSearch = (query: string) => {
  if (!query) {
    // Se a busca for limpa, mostre todas as entradas
    tableData.value = [...allInputs.value]
    return
  }
  
  // Filtra entradas por tipo de ração
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allInputs.value.filter(input => 
    input.rationStockName?.toLowerCase().includes(normalizedQuery)
  )
}

const fetchInputs = async () => {
  try {
    loading.value = true
    
    // Adiciona um pequeno atraso para mostrar o loading (apenas se estiver recarregando)
    if (!pageLoading.value) {
      const loadingMsg = message.loading('Atualizando lista de entradas...', {
        duration: 0
      })
      
      await loadRationStocks()
      
      const [inputs, total] = await rationInputService.getAll()
      
      loadingMsg.destroy()
      message.success(`${inputs.length} entradas carregadas com sucesso!`)
      
      const processedInputs = inputs.map(input => ({
        ...input,
        rationStockName: rationStocksMap.value.get(input.ration_stock_id) || 'N/A'
      }))
      
      allInputs.value = processedInputs
      tableData.value = processedInputs
      pagination.value.itemCount = total || inputs.length
    } else {
      // Carregamento inicial, sem mensagem
      await loadRationStocks()
      
      const [inputs, total] = await rationInputService.getAll()
      
      const processedInputs = inputs.map(input => ({
        ...input,
        rationStockName: rationStocksMap.value.get(input.ration_stock_id) || 'N/A'
      }))
      
      allInputs.value = processedInputs
      tableData.value = processedInputs
      pagination.value.itemCount = total || inputs.length
    }
  } catch (error) {
    console.error('Error fetching inputs:', error)
    message.error({
      content: 'Erro ao carregar entradas. Tente novamente.',
      duration: 5000,
      closable: true
    })
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

const loadRationStocks = async () => {
  try {
    const rationStocks = await rationStockService.getAll()
    rationStocksMap.value = new Map(
      rationStocks.map(rs => [rs.id, rs.name])
    )
  } catch (error) {
    console.error('Error loading ration types:', error)
    message.error('Erro ao carregar tipos de ração')
  }
}

// Ordenação
const handleSort = (sorter: { columnKey: keyof RationInput, order: 'ascend' | 'descend' | false }) => {
  const { columnKey, order } = sorter
  
  if (!order || !columnKey) {
    fetchInputs()
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
    
    // Para rationStockName
    const aValue = String(a[columnKey as keyof RationInput] || '')
    const bValue = String(b[columnKey as keyof RationInput] || '')
    return aValue.localeCompare(bValue) * multiplier
  })

  tableData.value = sortedData
}

const handleInputSubmit = async (formData: Omit<RationInput, 'id'>) => {
  try {
    const loadingMsg = message.loading('Registrando entrada...', {
      duration: 0
    })
    
    await rationInputService.create(formData)
    
    loadingMsg.destroy()
    message.success('Entrada registrada com sucesso')
    
    await fetchInputs()
  } catch (error) {
    message.error({
      content: 'Erro ao registrar entrada. Tente novamente.',
      duration: 5000,
      closable: true
    })
    console.error(error)
  }
}

const columns: DataTableColumns<RationInput> = [
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
    title: 'Tipo de Ração',
    key: 'rationStockName',
    sorter: 'default',
    render(row) {
      return row.rationStockName || 'N/A'
    }
  },
  {
    title: 'Quantidade',
    key: 'amount',
    sorter: (row1: RationInput, row2: RationInput) => 
      (row1.amount || 0) - (row2.amount || 0),
    render(row) {
      return `${row.amount} kg`
    }
  },
  {
    title: 'Descrição',
    key: 'description',
    sorter: 'default'
  }
]

const pagination = ref({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  onUpdatePage: (page: number) => {
    pagination.value.page = page
    fetchInputs()
  }
})

onMounted(() => {
  pageLoading.value = true
  fetchInputs()
})

// Reset search when data is refreshed
watch(() => allInputs.value, () => {
  if (!searchQuery.value) {
    tableData.value = [...allInputs.value]
  } else {
    handleSearch(searchQuery.value)
  }
})
</script>

<style scoped>
</style>