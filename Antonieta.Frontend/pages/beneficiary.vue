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
const tableData = ref<Beneficiary[]>([])
const loading = ref(false)
const showBeneficiaryModal = ref(false)
const showDeleteModal = ref(false)
const selectedBeneficiaryId = ref<number | null>(null)

async function fetchBeneficiaries() {
  try {
    loading.value = true
    const [beneficiaries] = await beneficiaryService.getAll()
    tableData.value = beneficiaries
  } catch (error) {
    console.error('Erro ao carregar beneficiários:', error)
    message.error('Erro ao carregar beneficiários')
  } finally {
    loading.value = false
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

const pagination = {
  pageSize: 10
}

function handleEdit(beneficiary: Beneficiary) {
  // Will be implemented with edit modal
  console.log('Edit beneficiary:', beneficiary)
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

// Load data when component mounts
onMounted(() => {
  fetchBeneficiaries()
})
</script>

<style scoped>

</style>