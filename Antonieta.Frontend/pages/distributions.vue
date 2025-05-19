<template>
  <div class="distributions-container">
    <div class="page-header">
      <h1 class="page-title">Distribuições de Ração</h1>
      <div class="title-underline"></div>
    </div>

    <div class="action-buttons">
      <n-button type="primary" class="action-button" style="background-color: #f77800" @click="showDistributionModal = true">
        <template #icon>
          <n-icon><IconPlus /></n-icon>
        </template>
        Registrar Nova Distribuição
      </n-button>
    </div>

    <DistributionModal v-model="showDistributionModal" @submit="handleDistributionSubmit" />

    <n-card class="distributions-table-card">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :pagination="pagination"
        :loading="loading"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { NCard, NDataTable, NTag, NButton, NIcon } from 'naive-ui'
import { IconPlus } from '@tabler/icons-vue'
import DistributionModal from '../components/modals/DistributionModal.vue'

interface DistributionData {
  id: number
  data: string
  beneficiario: string
  quantidade: number
  observacoes: string
}

const loading = ref(false)
const showDistributionModal = ref(false)

const handleDistributionSubmit = (formData: any) => {
  console.log('Distribuição registrada:', formData)
  // Aqui você pode implementar a lógica para salvar a distribuição
}

const columns: DataTableColumns<DistributionData> = [
  {
    title: 'Data',
    key: 'data',
    sorter: true
  },
  {
    title: 'Beneficiário',
    key: 'beneficiario',
    sorter: true
  },
  {
    title: 'Quantidade',
    key: 'quantidade',
    render(row) {
      return `${row.quantidade} kg`
    }
  },
  {
    title: 'Observações',
    key: 'observacoes'
  }
]

const tableData: DistributionData[] = [
  {
    id: 1,
    data: '2024-01-16',
    beneficiario: 'João Santos',
    quantidade: 10,
    observacoes: 'Retirada regular'
  }
]

const pagination = {
  pageSize: 10
}
</script>

<style scoped>
.distributions-container {
  padding: 2rem;
  background-color: #fff8e1;
  min-height: 100vh;
}

.action-buttons {
  margin-bottom: 2rem;
}

.action-button {
  font-weight: 600;
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

.distributions-table-card {
  background-color: #ffffff;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

:deep(.n-data-table-th) {
  background-color: #fff8e1;
}

:deep(.n-data-table-td) {
  padding: 12px !important;
}
</style>