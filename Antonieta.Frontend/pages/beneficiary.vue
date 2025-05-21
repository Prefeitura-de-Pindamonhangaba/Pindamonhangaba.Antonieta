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
import { h, ref, onMounted } from 'vue'

onMounted(() => {
  fetchBeneficiaries()
})
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

let tableData = ref<Beneficiary[]>([])

async function fetchBeneficiaries() {
  try {
    loading.value = true
    const { getAuthHeaders } = useAuth()
    const response = await fetch('http://localhost:8000/beneficiary', {
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        message.error('Sessão expirada. Por favor, faça login novamente.')
        return
      }
      throw new Error('Erro ao carregar beneficiários')
    }

    const data: any = await response.json()
    console.log('Dados recebidos da API:', data)

    // Garante que data seja sempre um array
    const beneficiariesArray: Beneficiary[] = data[0] || []

    // Mapeia os dados e atualiza a tableData
    tableData.value = beneficiariesArray.map(item => ({
      id: Number(item.id) || 0,
      name: String(item.name || ''),
      document: String(item.document || ''),
      address: String(item.address || ''),
      contact: String(item.contact || ''),
      limit: Number(item.limit) || 0
    }))

    console.log('Dados da tabela atualizados:', tableData.value)
  } catch (error) {
    console.error('Erro ao carregar beneficiários:', error)
    message.error('Erro ao carregar beneficiários: ' + error.message)
  } finally {
    loading.value = false
  }
}

const columns: DataTableColumns<Beneficiary> = [
  { title: 'Nome', key: 'name', render: (row: Beneficiary) => row.name },
  { title: 'Documento', key: 'document', render: (row: Beneficiary) => row.document },
  { title: 'Endereço', key: 'address', render: (row: Beneficiary) => row.address },
  { title: 'Contato', key: 'contact', render: (row: Beneficiary) => row.contact },
  {
    title: 'Limite Mensal',
    key: 'limit',
    render: (row: Beneficiary) => `${row.limit} kg`
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

async function confirmDelete() {
  if (selectedBeneficiaryId.value !== null) {
    try {
      loading.value = true
      const { getAuthHeaders } = useAuth()
      const response = await fetch(`http://localhost:8000/beneficiary/${selectedBeneficiaryId.value}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      })
      if (!response.ok) throw new Error('Erro ao excluir beneficiário')
      message.success('Beneficiário excluído com sucesso')
      await fetchBeneficiaries()
      showDeleteModal.value = false
    } catch (error) {
      message.error('Erro ao excluir beneficiário: ' + error.message)
    } finally {
      loading.value = false
    }
  }
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    loading.value = true

    if (editingBeneficiary.value) {
      // Atualizar beneficiário existente
      const { getAuthHeaders } = useAuth()
      const response = await fetch('http://localhost:8000/beneficiary', {
        method: 'PUT',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData.value)
      })
      if (!response.ok) throw new Error('Erro ao atualizar beneficiário')
      message.success('Beneficiário atualizado com sucesso')
    } else {
      // Adicionar novo beneficiário
      const { getAuthHeaders } = useAuth()
      const response = await fetch('http://localhost:8000/beneficiary', {
        method: 'POST',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData.value)
      })
      if (!response.ok) throw new Error('Erro ao criar beneficiário')
      message.success('Beneficiário adicionado com sucesso')
    }

    await fetchBeneficiaries()
    showAddModal.value = false
    resetForm()
  } catch (error) {
    message.error('Erro: ' + error.message)
  } finally {
    loading.value = false
  }
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