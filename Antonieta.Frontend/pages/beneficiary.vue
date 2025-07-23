<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <div class="page-header">
        <n-h1>Beneficiários</n-h1>
        <n-divider class="divider" />
      </div>

      <!-- Search and Action Buttons -->
      <n-space justify="space-between" align="center">
        <search-field
          v-model:value="searchQuery"
          placeholder="Buscar por nome ou documento..."
          @search="handleSearch"
        />

        <n-space align="center">
          <app-button 
            type="primary"
            @click="handleExport"
          >
            <template #icon>
              <n-icon><IconDownload /></n-icon>
            </template>
            Exportar Dados
          </app-button>

          <app-button 
            type="primary"
            @click="showBeneficiaryModal = true"
          >
            <template #icon>
              <n-icon><IconUserPlus /></n-icon>
            </template>
            Adicionar Novo Beneficiário
          </app-button>
        </n-space>
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

      <!-- Use BeneficiaryModal component -->
      <BeneficiaryModal
        v-model="showBeneficiaryModal"
        :edit-mode="!!selectedBeneficiary"
        :beneficiary-data="selectedBeneficiary"
        @submit="handleBeneficiarySubmit"
        @update="handleBeneficiaryUpdate"
      />

      <!-- Delete Modal -->
      <n-modal
        v-model:show="showDeleteModal"
        preset="dialog"
        title="Confirmar Exclusão"
        content="Tem certeza que deseja excluir este beneficiário? Esta ação não pode ser desfeita."
        positive-text="Sim, Excluir"
        negative-text="Cancelar"
        @positive-click="confirmDelete"
        @negative-click="showDeleteModal = false"
      />
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch, computed } from 'vue'
import {
  NLayout,
  NLayoutContent,
  NSpace,
  NButton,
  NCard,
  NDataTable,
  NModal,
  NIcon,
  NH1,
  NDivider,
  NInput,
  useMessage
} from 'naive-ui'
import { IconUserPlus, IconEdit, IconTrash, IconSearch, IconDownload } from '@tabler/icons-vue'
import BeneficiaryModal from '../components/modals/BeneficiaryModal.vue'
import ActionButtons from '../components/ActionButtons.vue'
import type { DataTableColumns } from 'naive-ui'
import type { Beneficiary } from '../models/beneficiaryModel'
import { beneficiaryService } from '~/services/beneficiaryService'

const message = useMessage()
const tableData = ref<Beneficiary[]>([])
const loading = ref(false)
const showBeneficiaryModal = ref(false)
const showDeleteModal = ref(false)
const selectedBeneficiaryId = ref<number | null>(null)
const selectedBeneficiary = ref<Beneficiary | null>(null)
const pageLoading = ref(true)
const searchQuery = ref('')
const allBeneficiaries = ref<Beneficiary[]>([])

// Objeto interno para organizar dados de exportação
const exportData = computed(() => {
  return allBeneficiaries.value.map(beneficiary => ({
    telefone: beneficiary.contact || 'Não informado',
    documento: beneficiary.document || 'Não informado',
    adicional1: beneficiary.name || 'Não informado', // Nome como Adicional 1
  }))
})

// Função para exportar dados (agora usando o objeto interno)
const handleExport = () => {
  // Log do objeto organizado para verificação
  console.log('📊 Dados organizados para exportação:', exportData.value)
  
  // Exemplo de como acessar os dados organizados
  const dadosSimplificados = exportData.value.map(item => ({
    Telefone: item.telefone,
    Documento: item.documento,
    'Adicional 1': item.adicional1
  }))
  
  console.log('📋 Dados simplificados (Telefone, Documento, Adicional 1):', dadosSimplificados)
  
  message.info({
    content: `${exportData.value.length} beneficiários organizados para exportação. Verifique o console para ver os dados.`,
    duration: 4000,
    closable: true
  })
}

// Função para obter resumo dos dados organizados
const getExportSummary = computed(() => {
  const total = exportData.value.length
  const comTelefone = exportData.value.filter(item => item.telefone !== 'Não informado').length
  const comDocumento = exportData.value.filter(item => item.documento !== 'Não informado').length
  const comNome = exportData.value.filter(item => item.adicional1 !== 'Não informado').length
  
  return {
    total,
    comTelefone,
    comDocumento,
    comNome,
    porcentagemCompletos: Math.round((Math.min(comTelefone, comDocumento, comNome) / total) * 100)
  }
})

// Função para obter dados formatados para diferentes tipos de exportação
const getFormattedExportData = (formato: 'simples' | 'completo' = 'simples') => {
  if (formato === 'simples') {
    return exportData.value.map(item => ({
      'Telefone': item.telefone,
      'Documento': item.documento,
      'Adicional 1': item.adicional1
    }))
  }
  
  return exportData.value.map(item => ({
    'Telefone': item.telefone,
    'Documento': item.documento,
    'Adicional 1': item.adicional1,
  }))
}

// Watch para atualizar dados quando beneficiários mudarem
watch(allBeneficiaries, () => {
  const summary = getExportSummary.value
  console.log('📈 Resumo dos dados organizados:', summary)
}, { deep: true })

// Resto do código permanece igual...
const handleSearch = (query: string) => {
  if (!query) {
    tableData.value = [...allBeneficiaries.value]
    return
  }
  
  const normalizedQuery = query.toLowerCase().trim()
  tableData.value = allBeneficiaries.value.filter(beneficiary => 
    beneficiary.name.toLowerCase().includes(normalizedQuery) || 
    beneficiary.document.toLowerCase().includes(normalizedQuery)
  )
}

async function fetchBeneficiaries() {
  try {
    loading.value = true
    
    if (!pageLoading.value) {
      const loadingMsg = message.loading('Atualizando lista de beneficiários...', {
        duration: 0
      })
      
      const [beneficiaries, total] = await beneficiaryService.getAll()
      
      loadingMsg.destroy()
      message.success(`${total} beneficiários carregados com sucesso!`)
      
      allBeneficiaries.value = beneficiaries
      tableData.value = beneficiaries
      pagination.value.itemCount = total
    } else {
      const [beneficiaries, total] = await beneficiaryService.getAll()
      allBeneficiaries.value = beneficiaries
      tableData.value = beneficiaries
      pagination.value.itemCount = total
    }
  } catch (error) {
    console.error('Erro ao carregar beneficiários:', error)
    message.error({
      content: 'Erro ao carregar beneficiários. Tente novamente.',
      duration: 5000,
      closable: true
    })
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

const sorter = ref<{ columnKey: keyof Beneficiary | null, order: 'ascend' | 'descend' | false }>({
  columnKey: null,
  order: false
})

const columns: DataTableColumns<Beneficiary> = [
  { 
    title: 'Nome', 
    key: 'name',
    sorter: 'default'
  },
  { 
    title: 'Documento', 
    key: 'document',
    sorter: 'default'
  },
  { 
    title: 'Endereço', 
    key: 'address',
    sorter: 'default'
  },
  { 
    title: 'Contato', 
    key: 'contact',
    sorter: 'default'
  },
  {
    title: 'Limite Mensal',
    key: 'monthly_limit',
    sorter: (row1: Beneficiary, row2: Beneficiary) => 
      (row1.monthly_limit || 0) - (row2.monthly_limit || 0),
    render: (row: Beneficiary) => `${row.monthly_limit || 0} kg`
  },
  {
    title: 'Ações',
    key: 'actions',
    render(row) {
      return h(ActionButtons, {
        onEdit: () => handleEdit(row),
        onDelete: () => handleDelete(row)
      })
    }
  }
]

const handleSort = (sorter: { columnKey: keyof Beneficiary, order: 'ascend' | 'descend' | false }) => {
  const { columnKey, order } = sorter
  
  if (!order || !columnKey) {
    fetchBeneficiaries()
    return
  }

  const sortedData = [...tableData.value]
  
  sortedData.sort((a, b) => {
    const multiplier = order === 'ascend' ? 1 : -1
    
    if (columnKey === 'monthly_limit') {
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
  onUpdatePage: (page: number) => {
    pagination.value.page = page
    fetchBeneficiaries()
  }
})

function handleEdit(beneficiary: Beneficiary) {
  selectedBeneficiary.value = beneficiary
  showBeneficiaryModal.value = true
}

function handleDelete(beneficiary: Beneficiary) {
  selectedBeneficiaryId.value = beneficiary.id
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (selectedBeneficiaryId.value !== null) {
    try {
      loading.value = true
      
      const loadingMsg = message.loading('Excluindo beneficiário...', {
        duration: 0
      })
      
      await beneficiaryService.delete(selectedBeneficiaryId.value)
      
      loadingMsg.destroy()
      message.success('Beneficiário excluído com sucesso!')
      
      await fetchBeneficiaries()
      showDeleteModal.value = false
    } catch (error) {
      message.error({
        content: 'Erro ao excluir beneficiário. Tente novamente.',
        duration: 5000,
        closable: true
      })
    } finally {
      loading.value = false
    }
  }
}

const handleBeneficiaryUpdate = async (id: number, updatedData: Beneficiary) => {
  try {
    await beneficiaryService.update(id, updatedData)
    message.success('Beneficiário atualizado com sucesso')
    await fetchBeneficiaries()
  } catch (error) {
    message.error('Erro ao atualizar beneficiário')
    console.error(error)
  } finally {
    selectedBeneficiary.value = null
  }
}

onMounted(async () => {
  pageLoading.value = true
  await fetchBeneficiaries()
})

watch(showBeneficiaryModal, (newValue) => {
  if (!newValue) {
    selectedBeneficiary.value = null
  }
})

watch(() => allBeneficiaries.value, () => {
  if (!searchQuery.value) {
    tableData.value = [...allBeneficiaries.value]
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
  width: 300px;
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