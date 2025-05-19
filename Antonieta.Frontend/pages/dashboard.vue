<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <div class="title-underline"></div>
    </div>

    <div class="action-buttons">
      <n-button type="primary" class="action-button" style="background-color: #f77800" @click="showDonationModal = true">
        <template #icon>
          <n-icon><IconPlus /></n-icon>
        </template>
        Registrar Nova Doação
      </n-button>
      <n-button class="action-button" type="default" style="color: #f77800; border-color: #f77800" @click="showBeneficiaryModal = true">
        <template #icon>
          <n-icon><IconUserPlus /></n-icon>
        </template>
        Adicionar Novo Beneficiário
      </n-button>
    </div>

    <DonationModal v-model="showDonationModal" @submit="handleDonationSubmit" />
    <BeneficiaryModal v-model="showBeneficiaryModal" @submit="handleBeneficiarySubmit" />

    <div class="summary-cards">
      <n-card class="summary-card">
        <div class="card-content">
          <div class="card-title">Entrada Total (Mês)</div>
          <div class="card-value">550 kg</div>
        </div>
      </n-card>
      <n-card class="summary-card">
        <div class="card-content">
          <div class="card-title">Saída Total (Mês)</div>
          <div class="card-value">320 kg</div>
        </div>
      </n-card>
      <n-card class="summary-card">
        <div class="card-content">
          <div class="card-title">Estoque Atual</div>
          <div class="card-value">230 kg</div>
        </div>
      </n-card>
    </div>

    <n-card class="beneficiaries-card" title="Beneficiários e Controle Mensal">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :pagination="pagination"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { NCard, NDataTable, NPageHeader, NTag, NButton, NIcon, NProgress } from 'naive-ui'
import { IconPlus, IconUserPlus, IconCheck, IconAlertTriangle, IconX } from '@tabler/icons-vue'
import DonationModal from '../components/modals/DonationModal.vue'
import BeneficiaryModal from '../components/modals/BeneficiaryModal.vue'
import type { Beneficiary } from '../models/beneficiary'

interface BeneficiaryData {
  nome: string
  limiteMensal: number
  recebido: number
  status: string
  progresso: number
}

const showDonationModal = ref(false)
const showBeneficiaryModal = ref(false)

const handleDonationSubmit = (formData: any) => {
  console.log('Doação registrada:', formData)
  // Aqui você pode implementar a lógica para salvar a doação
}

const handleBeneficiarySubmit = (formData: Beneficiary) => {
  console.log('Beneficiary submitted:', formData)
}

const columns: DataTableColumns<BeneficiaryData> = [
  {
    title: 'Nome',
    key: 'nome'
  },
  {
    title: 'Limite Mensal',
    key: 'limiteMensal',
    render(row) {
      return `${row.limiteMensal} kg`
    }
  },
  {
    title: 'Recebido Este Mês',
    key: 'recebido',
    render(row) {
      return `${row.recebido} kg`
    }
  },
  {
    title: 'Progresso',
    key: 'progresso',
    render(row) {
      return h(NProgress, {
        type: 'line',
        percentage: row.progresso,
        indicatorPlacement: 'inside',
        processing: row.progresso < 100,
        status: row.progresso >= 80 ? 'error' : row.progresso >= 50 ? 'warning' : 'success',
        style: { width: '120px' }
      })
    }
  },
  {
    title: 'Status',
    key: 'status',
    render(row) {
      const statusConfig = {
        'Pode Receber': {
          icon: IconCheck,
          type: 'success',
          style: { backgroundColor: '#18a058', color: 'white' }
        },
        'Próx. Limite': {
          icon: IconAlertTriangle,
          type: 'warning',
          style: { backgroundColor: '#f0a020', color: 'white' }
        },
        'Limite Atingido': {
          icon: IconX,
          type: 'error',
          style: { backgroundColor: '#d03050', color: 'white' }
        }
      }

      const config = statusConfig[row.status as keyof typeof statusConfig]
      
      return h(
        NTag,
        {
          type: config.type,
          style: {
            ...config.style,
            padding: '4px 12px',
            fontSize: '14px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '4px'
          }
        },
        {
          default: () => [
            h(config.icon, { size: 16 }),
            row.status
          ]
        }
      )
    }
  }
]

const tableData: BeneficiaryData[] = [
  {
    nome: 'Ana Silva',
    limiteMensal: 15,
    recebido: 5,
    status: 'Pode Receber',
    progresso: 33
  },
  {
    nome: 'João Santos',
    limiteMensal: 20,
    recebido: 18,
    status: 'Próx. Limite',
    progresso: 90
  },
  {
    nome: 'Maria Oliveira',
    limiteMensal: 10,
    recebido: 10,
    status: 'Limite Atingido',
    progresso: 100
  },
  {
    nome: 'Pedro Souza',
    limiteMensal: 25,
    recebido: 0,
    status: 'Pode Receber',
    progresso: 0
  }
]

const pagination = {
  pageSize: 10
}
</script>

<style scoped>
.dashboard-container {
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

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background-color: #ffffff;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-content {
  text-align: center;
  padding: 1rem;
}

.card-title {
  color: #263238;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.card-value {
  color: #f77800;
  font-size: 2rem;
  font-weight: 600;
}

.beneficiaries-card {
  background-color: #ffffff;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

:deep(.n-card-header__title) {
  color: #263238;
  font-size: 1.25rem;
  font-weight: 600;
}
</style>