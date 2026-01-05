<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <div class="page-header">
        <n-h1>Estoque de Rações</n-h1>
        <n-divider class="divider" />
      </div>

      <!-- Search and Action Buttons -->
      <n-space justify="space-between" align="center">
        <search-field
          v-model:value="searchQuery"
          placeholder="Buscar por nome ou descrição..."
          @search="handleSearch"
        />

        <app-button
          type="primary"
          @click="showRationStockModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Adicionar Nova Ração
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
          remote
        />
      </n-card>

      <!-- Modal -->
      <n-modal
        v-model:show="showRationStockModal"
        preset="card"
        style="width: 600px"
        :title="editMode ? 'Editar Ração' : 'Nova Ração'"
      >
        <div class="modal-content">
          <n-form
            ref="formRef"
            :model="formValue"
            :rules="rules"
            label-placement="left"
            label-width="auto"
            require-mark-placement="right-hanging"
            size="medium"
          >
            <n-form-item label="Nome" path="name" class="form-item">
              <n-input v-model:value="formValue.name" placeholder="Nome da ração" />
            </n-form-item>

            <n-form-item label="Descrição" path="description" class="form-item">
              <n-input
                v-model:value="formValue.description"
                type="textarea"
                placeholder="Descrição da ração"
              />
            </n-form-item>

            <n-form-item label="Unidade" path="unit" class="form-item">
              <n-input v-model:value="formValue.unit" placeholder="Unidade (ex: kg)" />
            </n-form-item>

            <n-form-item label="Estoque Inicial" path="stock" class="form-item">
              <n-input-number v-model:value="formValue.stock" placeholder="Quantidade inicial" />
            </n-form-item>
          </n-form>
        </div>

        <div class="modal-footer">
          <n-space justify="end">
            <app-button @click="closeModal">Cancelar</app-button>
            <app-button
              type="primary"
              :loading="submitLoading"
              @click="handleSubmit"
            >
              {{ editMode ? 'Atualizar' : 'Adicionar' }}
            </app-button>
          </n-space>
        </div>
      </n-modal>

      <!-- Delete Modal -->
      <n-modal
        v-model:show="showDeleteModal"
        preset="dialog"
        title="Confirmar Exclusão"
        content="Tem certeza que deseja excluir esta ração? Esta ação não pode ser desfeita."
        positive-text="Sim, Excluir"
        negative-text="Cancelar"
        @positive-click="confirmDelete"
        @negative-click="showDeleteModal = false"
      />
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch } from 'vue'
import type { DataTableColumns, FormInst, FormRules } from 'naive-ui'
import { 
  NCard, 
  NDataTable, 
  NButton, 
  NIcon, 
  NSpace, 
  NH1, 
  NDivider, 
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  useMessage 
} from 'naive-ui'
import { IconPlus, IconEdit, IconTrash, IconSearch } from '@tabler/icons-vue'
import type { RationStock } from '~/models/rationStockModel'
import { rationStockService } from '~/services/rationStockService'
import ActionButtons from '../components/ActionButtons.vue'

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const pageLoading = ref(true)
const loading = ref(false)
const submitLoading = ref(false)
const showRationStockModal = ref(false)
const showDeleteModal = ref(false)
const editMode = ref(false)
const selectedId = ref<number | null>(null)
const tableData = ref<RationStock[]>([])
const allRationStocks = ref<RationStock[]>([])
const searchQuery = ref('')

const formValue = ref({
  name: '',
  description: '',
  unit: '',
  stock: 0
})

const rules: FormRules = {
  name: {
    required: true,
    message: 'Por favor, informe o nome',
    trigger: ['blur', 'input']
  },
  description: {
    required: true,
    message: 'Por favor, informe a descrição',
    trigger: ['blur', 'input']
  },
  unit: {
    required: true,
    message: 'Por favor, informe a unidade',
    trigger: ['blur', 'input']
  },
  stock: {
    required: true,
    type: 'number',
    message: 'Por favor, informe o estoque inicial',
    trigger: ['blur', 'change']
  }
}

// Função de busca
const handleSearch = (query: string) => {
  if (!query) {
    // Se a busca for limpa, mostre todas as rações
    tableData.value = [...allRationStocks.value]
    return
  }
  
  // Filtra rações por nome ou descrição
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allRationStocks.value.filter(stock => 
    stock.name.toLowerCase().includes(normalizedQuery) || 
    stock.description.toLowerCase().includes(normalizedQuery)
  )
}

// Ordenação
const handleSort = (sorter: { columnKey: keyof RationStock, order: 'ascend' | 'descend' | false }) => {
  const { columnKey, order } = sorter
  
  if (!order || !columnKey) {
    tableData.value = [...allRationStocks.value]
    return
  }

  const sortedData = [...tableData.value]
  
  sortedData.sort((a, b) => {
    const multiplier = order === 'ascend' ? 1 : -1
    
    if (columnKey === 'stock') {
      return ((a[columnKey] || 0) - (b[columnKey] || 0)) * multiplier
    }
    
    const aValue = String(a[columnKey] || '')
    const bValue = String(b[columnKey] || '')
    return aValue.localeCompare(bValue) * multiplier
  })

  tableData.value = sortedData
}

const pagination = ref({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  onChange: (page: number) => {
    pagination.value.page = page
    // Não precisamos recarregar os dados do servidor, apenas paginar os dados locais
  }
})

const columns: DataTableColumns<RationStock> = [
  {
    title: 'Nome',
    key: 'name',
    sorter: 'default'
  },
  {
    title: 'Descrição',
    key: 'description',
    sorter: 'default'
  },
  {
    title: 'Unidade',
    key: 'unit',
    sorter: 'default'
  },
  {
    title: 'Estoque',
    key: 'stock',
    sorter: (row1: RationStock, row2: RationStock) => (row1.stock || 0) - (row2.stock || 0),
    render(row) {
      return (row.stock || 0).toFixed(2)
    }
  },
  {
    title: 'Ações',
    key: 'actions',
    render(row) {
      return h(ActionButtons, {
        onEdit: () => handleEdit(row),
        onDelete: () => handleDelete(row.id)
      })
    }
  }
]

async function fetchRationStocks() {
  try {
    loading.value = true
    
    // Adiciona um pequeno atraso para mostrar o loading (apenas se estiver recarregando)
    if (!pageLoading.value) {
      const loadingMsg = message.loading('Atualizando estoque de rações...', {
        duration: 0
      })
      
      const stocks = await rationStockService.getAll()
      
      loadingMsg.destroy()
      message.success(`${stocks.length} tipos de ração carregados com sucesso!`)
      
      allRationStocks.value = stocks
      tableData.value = stocks
      pagination.value.itemCount = stocks.length
    } else {
      // Carregamento inicial, sem mensagem
      const stocks = await rationStockService.getAll()
      allRationStocks.value = stocks
      tableData.value = stocks
      pagination.value.itemCount = stocks.length
    }
  } catch (error) {
    console.error('Error fetching ration stocks:', error)
    message.error({
      content: 'Erro ao carregar estoque de rações. Tente novamente.',
      duration: 5000,
      closable: true
    })
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

function handleEdit(row: RationStock) {
  editMode.value = true
  selectedId.value = row.id
  formValue.value = { ...row }
  showRationStockModal.value = true
}

function handleDelete(id: number) {
  selectedId.value = id
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!selectedId.value) return

  try {
    const loadingMsg = message.loading('Excluindo ração...', {
      duration: 0
    })
    
    await rationStockService.delete(selectedId.value)
    
    loadingMsg.destroy()
    message.success('Ração excluída com sucesso')
    
    await fetchRationStocks()
  } catch (error) {
    console.error('Error deleting ration stock:', error)
    message.error({
      content: 'Erro ao excluir ração. Tente novamente.',
      duration: 5000,
      closable: true
    })
  } finally {
    showDeleteModal.value = false
    selectedId.value = null
  }
}

function closeModal() {
  showRationStockModal.value = false
  editMode.value = false
  selectedId.value = null
  formValue.value = {
    name: '',
    description: '',
    unit: '',
    stock: 0
  }
  formRef.value?.restoreValidation()
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    submitLoading.value = true
    
    const loadingMsg = message.loading(editMode.value ? 'Atualizando ração...' : 'Adicionando ração...', {
      duration: 0
    })
    
    if (editMode.value && selectedId.value) {
      await rationStockService.update(selectedId.value, formValue.value)
      loadingMsg.destroy()
      message.success('Ração atualizada com sucesso')
    } else {
      await rationStockService.create(formValue.value)
      loadingMsg.destroy()
      message.success('Ração adicionada com sucesso')
    }
    
    closeModal()
    await fetchRationStocks()
  } catch (error) {
    console.error('Error submitting ration stock:', error)
    message.error({
      content: 'Erro ao salvar ração. Tente novamente.',
      duration: 5000,
      closable: true
    })
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  pageLoading.value = true
  fetchRationStocks()
})

// Reset search when data is refreshed
watch(() => allRationStocks.value, () => {
  if (!searchQuery.value) {
    tableData.value = [...allRationStocks.value]
  } else {
    handleSearch(searchQuery.value)
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 24px;
}

.divider {
  width: 100px;
  margin: 0;
  background-color: #f77800;
}

.search-field {
  width: 300px;
}

.app-button {
  background-color: #f77800;
  font-size: 14px;
  padding: 12px 24px;
}

.page-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.modal-content {
  padding: 16px;
}

.form-item {
  margin-bottom: 16px;
}

.modal-footer {
  padding: 16px;
  text-align: right;
}
</style>