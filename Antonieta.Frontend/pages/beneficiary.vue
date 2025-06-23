<template>
  <page-wrapper :loading="pageLoading">
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
import { h, ref, onMounted, watch } from 'vue'
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

async function fetchBeneficiaries() {
  try {
    loading.value = true
    const [beneficiaries, total] = await beneficiaryService.getAll()
    tableData.value = beneficiaries
    pagination.value.itemCount = total
  } catch (error) {
    console.error('Erro ao carregar beneficiários:', error)
    message.error('Erro ao carregar beneficiários')
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

const columns: DataTableColumns<Beneficiary> = [
  { title: 'Nome', key: 'name' },
  { title: 'Documento', key: 'document' },
  { title: 'Endereço', key: 'address' },
  { title: 'Contato', key: 'contact' },
  {
    title: 'Limite Mensal',
    key: 'monthly_limit',
    render: (row: Beneficiary) => `${row.monthly_limit} kg`
  },
  {
    title: 'Ações',
    key: 'actions',
    render(row) {
      return h(NSpace, { justify: 'center', align: 'center' }, {
        default: () => [
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
        ]
      })
    }
  }
]

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
      await beneficiaryService.delete(selectedBeneficiaryId.value)
      message.success('Beneficiário excluído com sucesso')
      await fetchBeneficiaries()
      showDeleteModal.value = false
    } catch (error) {
      message.error('Erro ao excluir beneficiário')
    } finally {
      loading.value = false
    }
  }
}

// Add these functions after handleEdit
const handleBeneficiarySubmit = async (beneficiary: Beneficiary) => {
  try {
    await beneficiaryService.create(beneficiary)
    message.success('Beneficiário cadastrado com sucesso')
    await fetchBeneficiaries()
  } catch (error) {
    message.error('Erro ao cadastrar beneficiário')
    console.error(error)
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

// Update onMounted to set initial loading state
onMounted(async () => {
  pageLoading.value = true
  await fetchBeneficiaries()
})

watch(showBeneficiaryModal, (newValue) => {
  if (!newValue) {
    selectedBeneficiary.value = null
  }
})
</script>

<style scoped>

</style>