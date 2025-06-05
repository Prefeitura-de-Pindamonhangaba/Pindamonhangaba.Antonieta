<template>
  <n-layout style="min-height: 100vh">
    <n-layout-content style="padding: 24px">
      <n-space vertical size="large">
        <!-- Header -->
        <n-space vertical size="small">
          <n-h1 style="color: #f77800; margin: 0">Beneficiários</n-h1>
          <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
        </n-space>

        <!-- Action Buttons -->
        <n-space>
          <n-button
            type="primary"
            style="background-color: #f77800; font-size: 14px; padding: 12px 24px"
            @click="showBeneficiaryModal = true"
          >
            <template #icon>
              <n-icon><IconUserPlus /></n-icon>
            </template>
            Adicionar Novo Beneficiário
          </n-button>
        </n-space>

        <!-- Table -->
        <n-card>
          <n-data-table
            :columns="columns"
            :data="tableData"
            :pagination="pagination"
            :loading="loading"
          />
        </n-card>

        <!-- Use BeneficiaryModal component -->
        <BeneficiaryModal
          v-model="showBeneficiaryModal"
          @submit="handleBeneficiarySubmit"
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
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import { h, ref, onMounted } from 'vue'
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
  useMessage
} from 'naive-ui'
import { IconUserPlus, IconEdit, IconTrash } from '@tabler/icons-vue'
import BeneficiaryModal from '../components/modals/BeneficiaryModal.vue'
import type { DataTableColumns } from 'naive-ui'
import type { Beneficiary } from '../models/beneficiary'
import { beneficiaryService } from '~/services/beneficiaryService'

const message = useMessage()
const loading = ref(false)
const showBeneficiaryModal = ref(false) // Changed from showAddModal
const showDeleteModal = ref(false)
const selectedBeneficiaryId = ref<number | null>(null)

// Remove formRef and formData since they're now in BeneficiaryModal

const handleBeneficiarySubmit = async (beneficiary: Beneficiary) => {
  try {
    await beneficiaryService.create(beneficiary)
    message.success('Beneficiário adicionado com sucesso')
    await fetchBeneficiaries()
  } catch (error) {
    message.error('Erro ao adicionar beneficiário')
    console.error(error)
  }
}

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