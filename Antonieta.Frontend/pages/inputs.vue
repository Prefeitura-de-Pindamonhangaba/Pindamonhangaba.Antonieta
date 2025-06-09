<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <n-space vertical size="small">
        <n-h1 style="color: #f77800; margin: 0">Entradas de Ração</n-h1>
        <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
      </n-space>

      <!-- Action Buttons -->
      <n-space>
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
import { h, ref, onMounted } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { NCard, NDataTable, NButton, NIcon, NLayout, NLayoutContent, NSpace, NH1, NDivider, useMessage } from 'naive-ui'
import { IconPlus } from '@tabler/icons-vue'
import InputModal from '../components/modals/InputModal.vue'
import { rationInputService } from '~/services/rationInputService'
import { rationTypeService } from '~/services/rationTypeService'
import type { RationInput } from '~/models/rationInputModel'

const message = useMessage()
const loading = ref(false)
const showInputModal = ref(false)
const tableData = ref<RationInput[]>([])
const rationTypesMap = ref<Map<number, string>>(new Map())
const pageLoading = ref(true)

const fetchInputs = async () => {
  try {
    loading.value = true
    pageLoading.value = true
    await loadRationTypes()
    
    const [inputs] = await rationInputService.getAll()
    tableData.value = inputs.map(input => ({
      ...input,
      rationTypeName: rationTypesMap.value.get(input.ration_id) || 'N/A'
    }))
  } catch (error) {
    console.error('Error fetching inputs:', error)
    message.error('Erro ao carregar entradas')
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

const loadRationTypes = async () => {
  try {
    const rationTypes = await rationTypeService.getAll()
    rationTypesMap.value = new Map(
      rationTypes.map(rt => [rt.id, rt.name])
    )
  } catch (error) {
    console.error('Error loading ration types:', error)
  }
}

const handleInputSubmit = async (formData: Omit<RationInput, 'id'>) => {
  try {
    await rationInputService.create(formData)
    message.success('Entrada registrada com sucesso')
    await fetchInputs()
  } catch (error) {
    message.error('Erro ao registrar entrada')
    console.error(error)
  }
}

const columns: DataTableColumns<RationInput> = [
  {
    title: 'Data',
    key: 'date',
    sorter: true,
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
    key: 'rationTypeName',
    render(row) {
      return row.rationTypeName || 'N/A'
    }
  },
  {
    title: 'Quantidade',
    key: 'amount',
    render(row) {
      return `${row.amount} kg`
    }
  }
]

const pagination = {
  pageSize: 10
}

onMounted(() => {
  fetchInputs()
})
</script>