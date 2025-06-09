<template>
  <n-modal 
    v-model:show="show" 
    style="width: 800px"
    preset="card"
    title="Gerenciar Tipos de Ração"
    :bordered="false"
    size="huge"
    :segmented="{ content: true, footer: 'soft' }"
  >
    <!-- Form Section -->
    <n-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
    >
      <n-space vertical>
        <n-form-item label="Nome" path="name">
          <n-input
            v-model:value="formData.name"
            placeholder="Nome do tipo de ração"
            clearable
          />
        </n-form-item>

        <n-form-item label="Descrição" path="description">
          <n-input
            v-model:value="formData.description"
            type="textarea"
            placeholder="Descrição do tipo de ração"
          />
        </n-form-item>

        <n-space justify="end">
          <n-button @click="handleCancel" :disabled="loading">
            Cancelar
          </n-button>
          <n-button 
            type="primary" 
            :loading="loading" 
            :disabled="loading"
            style="background-color: #f77800"
            @click="handleSubmit"
          >
            {{ loading ? 'Salvando...' : (editMode ? 'Atualizar' : 'Adicionar') }}
          </n-button>
        </n-space>
      </n-space>
    </n-form>

    <n-divider />

    <!-- Table Section -->
    <n-data-table
      :columns="columns"
      :data="rationTypes"
      :loading="tableLoading"
      :pagination="{ pageSize: 5 }"
    />

    <!-- Delete Confirmation Modal -->
    <n-modal
      v-model:show="showDeleteModal"
      preset="dialog"
      title="Confirmar Exclusão"
      content="Tem certeza que deseja excluir este tipo de ração? Esta ação não pode ser desfeita."
      positive-text="Sim, Excluir"
      negative-text="Cancelar"
      @positive-click="confirmDelete"
      @negative-click="showDeleteModal = false"
    />
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, h, onMounted } from 'vue'
import type { FormInst, FormRules, DataTableColumns } from 'naive-ui'
import { NModal, NForm, NFormItem, NInput, NButton, NSpace, NDataTable, NDivider, useMessage } from 'naive-ui'
import { rationTypeService } from '~/services/rationTypeService'
import type { RationType } from '~/models/rationTypeModel'
import { IconEdit, IconTrash } from '@tabler/icons-vue'

const props = defineProps<{
  modelValue: boolean
  editMode?: boolean
  rationTypeData?: RationType
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', data: Omit<RationType, 'id'>): void
  (e: 'update', id: number, data: Partial<RationType>): void
}>()

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const formData = ref({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: {
    required: true,
    message: 'Por favor, informe o nome',
    trigger: ['blur', 'input']
  },
  description: {
    required: true,
    message: 'Por favor, informe uma descrição',
    trigger: ['blur', 'input']
  }
}

const rationTypes = ref<RationType[]>([])
const tableLoading = ref(false)
const showDeleteModal = ref(false)
const selectedId = ref<number | null>(null)
const editMode = ref(false)

// Add columns configuration
const columns: DataTableColumns<RationType> = [
  {
    title: 'Nome',
    key: 'name',
  },
  {
    title: 'Descrição',
    key: 'description',
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

// Add handlers for edit and delete
const handleEdit = (rationType: RationType) => {
  editMode.value = true
  formData.value = {
    name: rationType.name,
    description: rationType.description
  }
  selectedId.value = rationType.id
}

const handleDelete = (id: number) => {
  selectedId.value = id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!selectedId.value) return
  
  try {
    await rationTypeService.delete(selectedId.value)
    message.success('Tipo de ração excluído com sucesso')
    await fetchRationTypes()
  } catch (error) {
    message.error('Erro ao excluir tipo de ração')
    console.error(error)
  } finally {
    showDeleteModal.value = false
    selectedId.value = null
  }
}

// Add method to fetch ration types
const fetchRationTypes = async () => {
  try {
    tableLoading.value = true
    rationTypes.value = await rationTypeService.getAll()
  } catch (error) {
    message.error('Erro ao carregar tipos de ração')
    console.error(error)
  } finally {
    tableLoading.value = false
  }
}

// Modify handleSubmit to handle both create and update
const handleSubmit = () => {
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      try {
        loading.value = true
        if (editMode.value && selectedId.value) {
          await rationTypeService.update(selectedId.value, formData.value)
          message.success('Tipo de ração atualizado com sucesso')
        } else {
          await rationTypeService.create(formData.value)
          message.success('Tipo de ração criado com sucesso')
        }
        resetForm()
        await fetchRationTypes()
      } catch (error) {
        message.error('Erro ao salvar tipo de ração')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

// Modify resetForm to handle editMode
const resetForm = () => {
  formData.value = {
    name: '',
    description: ''
  }
  editMode.value = false
  selectedId.value = null
  formRef.value?.restoreValidation()
}

// Fetch data when modal opens
onMounted(() => {
  fetchRationTypes()
})
</script>