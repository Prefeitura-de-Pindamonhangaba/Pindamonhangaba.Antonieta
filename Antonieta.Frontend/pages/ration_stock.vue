<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <n-space vertical size="small">
        <n-h1 style="color: #f77800; margin: 0">Estoque de Rações</n-h1>
        <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
      </n-space>

      <!-- Action Buttons -->
      <n-space>
        <n-button
          type="primary"
          style="background-color: #f77800; font-size: 14px; padding: 12px 24px"
          @click="showRationStockModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Adicionar Nova Ração
        </n-button>
      </n-space>

      <!-- Table -->
      <n-card>
        <n-data-table
          :columns="columns"
          :data="tableData"
          :pagination="pagination"
          :loading="loading"
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
        <n-form
          ref="formRef"
          :model="formValue"
          :rules="rules"
          label-placement="left"
          label-width="auto"
          require-mark-placement="right-hanging"
          size="medium"
        >
          <n-form-item label="Nome" path="name">
            <n-input v-model:value="formValue.name" placeholder="Nome da ração" />
          </n-form-item>

          <n-form-item label="Descrição" path="description">
            <n-input
              v-model:value="formValue.description"
              type="textarea"
              placeholder="Descrição da ração"
            />
          </n-form-item>

          <n-form-item label="Unidade" path="unit">
            <n-input v-model:value="formValue.unit" placeholder="Unidade (ex: kg)" />
          </n-form-item>

          <n-form-item label="Estoque Inicial" path="stock">
            <n-input-number v-model:value="formValue.stock" placeholder="Quantidade inicial" />
          </n-form-item>
        </n-form>

        <template #footer>
          <n-space justify="end">
            <n-button @click="closeModal">Cancelar</n-button>
            <n-button
              type="primary"
              :loading="submitLoading"
              @click="handleSubmit"
              style="background-color: #f77800"
            >
              {{ editMode ? 'Atualizar' : 'Adicionar' }}
            </n-button>
          </n-space>
        </template>
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
import { h, ref, onMounted } from 'vue'
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
import { IconPlus, IconEdit, IconTrash } from '@tabler/icons-vue'
import type { RationStock } from '~/models/rationStockModel'
import { rationStockService } from '~/services/rationStockService'

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

const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0,
  onChange: (page: number) => {
    pagination.value.page = page
    fetchRationStocks()
  }
})

const columns: DataTableColumns<RationStock> = [
  {
    title: 'Nome',
    key: 'name'
  },
  {
    title: 'Descrição',
    key: 'description'
  },
  {
    title: 'Unidade',
    key: 'unit'
  },
  {
    title: 'Estoque',
    key: 'stock'
  },
  {
    title: 'Ações',
    key: 'actions',
    render(row) {
      return h(NSpace, { justify: 'end' }, {
        default: () => [
          h(
            NButton,
            {
              quaternary: true,
              type: 'info',
              onClick: () => handleEdit(row)
            },
            { icon: () => h(IconEdit) }
          ),
          h(
            NButton,
            {
              quaternary: true,
              type: 'error',
              onClick: () => handleDelete(row.id)
            },
            { icon: () => h(IconTrash) }
          )
        ]
      })
    }
  }
]

async function fetchRationStocks() {
  try {
    loading.value = true
    const stocks = await rationStockService.getAll()
    tableData.value = stocks
    pagination.value.total = stocks.length
  } catch (error) {
    console.error('Error fetching ration stocks:', error)
    message.error('Erro ao carregar estoque de rações')
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
    await rationStockService.delete(selectedId.value)
    message.success('Ração excluída com sucesso')
    await fetchRationStocks()
  } catch (error) {
    console.error('Error deleting ration stock:', error)
    message.error('Erro ao excluir ração')
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
  await formRef.value?.validate()

  try {
    submitLoading.value = true
    if (editMode.value && selectedId.value) {
      await rationStockService.update(selectedId.value, formValue.value)
      message.success('Ração atualizada com sucesso')
    } else {
      await rationStockService.create(formValue.value)
      message.success('Ração adicionada com sucesso')
    }
    closeModal()
    await fetchRationStocks()
  } catch (error) {
    console.error('Error submitting ration stock:', error)
    message.error('Erro ao salvar ração')
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  fetchRationStocks()
})
</script>