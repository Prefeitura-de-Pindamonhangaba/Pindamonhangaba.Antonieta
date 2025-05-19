<template>
  <div class="beneficiary-container">
    <div class="page-header">
      <h1 class="page-title">Beneficiários</h1>
      <div class="title-underline"></div>
    </div>

    <div class="action-buttons">
      <n-button type="primary" class="action-button" style="background-color: #f77800" @click="showAddModal = true">
        <template #icon>
          <n-icon><IconUserPlus /></n-icon>
        </template>
        Adicionar Novo Beneficiário
      </n-button>
    </div>

    <n-card class="beneficiaries-table-card">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :pagination="pagination"
        :loading="loading"
      />
    </n-card>

    <!-- Modal de Adição/Edição -->
    <n-modal
      v-model:show="showAddModal"
      preset="dialog"
      style="width: 600px"
      :title="editingBeneficiary ? 'Editar Beneficiário' : 'Adicionar Novo Beneficiário'"
    >
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="auto"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <n-form-item label="Nome" path="name">
          <n-input v-model:value="formData.name" placeholder="Nome completo" />
        </n-form-item>
        <n-form-item label="Documento" path="document">
          <n-input v-model:value="formData.document" placeholder="CPF" />
        </n-form-item>
        <n-form-item label="Endereço" path="address">
          <n-input v-model:value="formData.address" placeholder="Endereço completo" />
        </n-form-item>
        <n-form-item label="Contato" path="contact">
          <n-input v-model:value="formData.contact" placeholder="Telefone" />
        </n-form-item>
        <n-form-item label="Limite Mensal (kg)" path="limit">
          <n-input-number v-model:value="formData.limit" placeholder="Limite em kg" />
        </n-form-item>
      </n-form>
      <template #action>
        <div class="modal-actions">
          <n-button @click="showAddModal = false">Cancelar</n-button>
          <n-button
            type="primary"
            style="background-color: #f77800"
            @click="handleSubmit"
          >
            {{ editingBeneficiary ? 'Salvar Alterações' : 'Adicionar' }}
          </n-button>
        </div>
      </template>
    </n-modal>

    <!-- Modal de Confirmação de Exclusão -->
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
  </div>
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import {
  NButton,
  NCard,
  NDataTable,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NIcon,
  useMessage
} from 'naive-ui'
import { IconUserPlus, IconEdit, IconTrash } from '@tabler/icons-vue'
import type { Beneficiary } from '../models/beneficiary'

const message = useMessage()
const loading = ref(false)
const showAddModal = ref(false)
const showDeleteModal = ref(false)
const editingBeneficiary = ref<Beneficiary | null>(null)
const selectedBeneficiaryId = ref<number | null>(null)

const formRef = ref()
const formData = ref<Beneficiary>({
  id: 0,
  name: '',
  document: '',
  address: '',
  contact: '',
  limit: 0
})

const rules = {
  name: { required: true, message: 'Por favor, insira o nome', trigger: 'blur' },
  document: { required: true, message: 'Por favor, insira o documento', trigger: 'blur' },
  address: { required: true, message: 'Por favor, insira o endereço', trigger: 'blur' },
  contact: { required: true, message: 'Por favor, insira o contato', trigger: 'blur' },
  limit: { required: true, message: 'Por favor, insira o limite mensal', trigger: 'blur', type: 'number' }
}

const tableData = ref<Beneficiary[]>([
  {
    id: 1,
    name: 'Maria Silva',
    document: '123.456.789-00',
    address: 'Rua das Flores, 123',
    contact: '(12) 98765-4321',
    limit: 15
  },
  {
    id: 2,
    name: 'João Santos',
    document: '987.654.321-00',
    address: 'Av. Principal, 456',
    contact: '(12) 91234-5678',
    limit: 20
  }
])

const columns: DataTableColumns<Beneficiary> = [
  { title: 'Nome', key: 'name' },
  { title: 'Documento', key: 'document' },
  { title: 'Endereço', key: 'address' },
  { title: 'Contato', key: 'contact' },
  {
    title: 'Limite Mensal',
    key: 'limit',
    render(row) {
      return `${row.limit} kg`
    }
  },
  {
    title: 'Ações',
    key: 'actions',
    render(row) {
      return h('div', { style: 'display: flex; gap: 8px;' }, [
        h(
          NButton,
          {
            size: 'small',
            quaternary: true,
            style: { color: '#f77800' },
            onClick: () => handleEdit(row)
          },
          { default: () => h(IconEdit) }
        ),
        h(
          NButton,
          {
            size: 'small',
            quaternary: true,
            style: { color: '#d03050' },
            onClick: () => handleDelete(row)
          },
          { default: () => h(IconTrash) }
        )
      ])
    }
  }
]

const pagination = {
  pageSize: 10
}

function handleEdit(beneficiary: Beneficiary) {
  editingBeneficiary.value = beneficiary
  formData.value = { ...beneficiary }
  showAddModal.value = true
}

function handleDelete(beneficiary: Beneficiary) {
  selectedBeneficiaryId.value = beneficiary.id
  showDeleteModal.value = true
}

function confirmDelete() {
  if (selectedBeneficiaryId.value !== null) {
    tableData.value = tableData.value.filter(
      (b) => b.id !== selectedBeneficiaryId.value
    )
    message.success('Beneficiário excluído com sucesso')
    showDeleteModal.value = false
  }
}

async function handleSubmit() {
  await formRef.value?.validate()

  if (editingBeneficiary.value) {
    // Atualizar beneficiário existente
    const index = tableData.value.findIndex((b) => b.id === editingBeneficiary.value?.id)
    if (index !== -1) {
      tableData.value[index] = { ...formData.value }
      message.success('Beneficiário atualizado com sucesso')
    }
  } else {
    // Adicionar novo beneficiário
    const newId = Math.max(...tableData.value.map((b) => b.id)) + 1
    tableData.value.push({ ...formData.value, id: newId })
    message.success('Beneficiário adicionado com sucesso')
  }

  showAddModal.value = false
  resetForm()
}

function resetForm() {
  formData.value = {
    id: 0,
    name: '',
    document: '',
    address: '',
    contact: '',
    limit: 0
  }
  editingBeneficiary.value = null
}
</script>

<style scoped>
.beneficiary-container {
  padding: 2rem;
  background-color: #fff8e1;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: #f77800;
  margin: 0;
}

.title-underline {
  width: 100px;
  height: 4px;
  background-color: #f77800;
  margin-top: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-button {
  font-weight: 500;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
}

.beneficiaries-table-card {
  background-color: #ffffff;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>