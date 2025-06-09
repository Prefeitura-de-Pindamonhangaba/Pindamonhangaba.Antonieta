<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <n-space vertical size="small">
        <n-h1 style="color: #f77800; margin: 0">Distribuições</n-h1>
        <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
      </n-space>

      <!-- Action Buttons -->
      <n-space>
        <n-button 
          type="primary" 
          style="background-color: #f77800; font-size: 14px; padding: 12px 24px"
          @click="showDistributionModal = true"
        >
          <template #icon>
            <n-icon><IconPlus /></n-icon>
          </template>
          Registrar Nova Distribuição
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

      <DistributionModal 
        v-model="showDistributionModal" 
        @submit="handleDistributionSubmit" 
      />
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { NCard, NDataTable, NButton, NIcon, NLayout, NLayoutContent, NSpace, NH1, NDivider, useMessage } from 'naive-ui'
import { IconPlus } from '@tabler/icons-vue'
import DistributionModal from '../components/modals/DistributionModal.vue'
import { distributionService } from '~/services/distributionService'
import { beneficiaryService } from '~/services/beneficiaryService'
import { rationTypeService } from '~/services/rationTypeService'
import type { Distribution } from '~/models/distributionModel'
import { rationStockService } from '~/services/rationStockService'

const message = useMessage()
const loading = ref(false)
const showDistributionModal = ref(false)
const tableData = ref<Distribution[]>([])
const beneficiariesMap = ref<Map<number, string>>(new Map())
const rationTypesMap = ref<Map<number, string>>(new Map())
const pageLoading = ref(true)

// Função para buscar distribuições
const fetchDistributions = async () => {
  try {
    pageLoading.value = true
    loading.value = true
    await Promise.all([loadBeneficiaries(), loadRationStocks()])
    
    const [distributions] = await distributionService.getAll()
    tableData.value = distributions.map(dist => ({
      ...dist,
      beneficiaryName: dist.beneficiary_id ? beneficiariesMap.value.get(dist.beneficiary_id) : 'N/A',
      rationTypeName: rationTypesMap.value.get(dist.ration_id) || 'N/A'
    }))
  } catch (error) {
    console.error('Error fetching distributions:', error)
    message.error('Erro ao carregar distribuições')
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

// Função para carregar beneficiários
const loadBeneficiaries = async () => {
  try {
    const [beneficiaries] = await beneficiaryService.getAll()
    beneficiariesMap.value = new Map(
      beneficiaries.map(b => [b.id, b.name])
    )
  } catch (error) {
    console.error('Error loading beneficiaries:', error)
  }
}

const loadRationStocks = async () => {
  try {
    const rationStocks = await rationStockService.getAll()
    rationTypesMap.value = new Map(
      rationStocks.map(rs => [rs.id, rs.name])
    )
  } catch (error) {
    console.error('Error loading ration types:', error)
    message.error('Erro ao carregar tipos de ração')
  }
}

// Atualiza o manipulador de envio para usar o serviço
const handleDistributionSubmit = async (formData: Omit<Distribution, 'id'>) => {
  try {
    await distributionService.create(formData)
    message.success('Distribuição registrada com sucesso')
    await fetchDistributions()
  } catch (error) {
    message.error('Erro ao registrar distribuição')
    console.error(error)
  }
}

// Atualiza as colunas para corresponder ao modelo de Distribuição
const columns: DataTableColumns<Distribution> = [
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
    title: 'Beneficiário',
    key: 'beneficiaryName',
    render(row) {
      return row.beneficiaryName || 'N/A'
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

// Carrega os dados quando o componente é montado
onMounted(() => {
  fetchDistributions()
})
</script>

<style scoped>
</style>