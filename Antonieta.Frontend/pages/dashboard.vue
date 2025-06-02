<template>
  <n-layout style="min-height: 100vh">
    <n-layout-content style="padding: 24px">
      <n-space vertical size="large">
        <!-- Header -->
        <n-space vertical size="small">
          <n-h1 style="color: #f77800; margin: 0">Dashboard</n-h1>
          <n-divider style="width: 100px; margin: 0; background-color: #f77800" />
        </n-space>

        <!-- Action Buttons -->
        <n-space>
          <n-button 
            type="primary" 
            style="background-color: #f77800; font-size: 14px; padding: 12px 24px"
            @click="showDonationModal = true"
          >
            <template #icon>
              <n-icon><IconPlus /></n-icon>
            </template>
            Registrar Nova Doação
          </n-button>
          <n-button 
            style="color: #f77800; border-color: #f77800; font-size: 14px; padding: 12px 24px"
            @click="showBeneficiaryModal = true"
          >
            <template #icon>
              <n-icon><IconUserPlus /></n-icon>
            </template>
            Adicionar Novo Beneficiário
          </n-button>
        </n-space>

        <DonationModal v-model="showDonationModal" @submit="handleDonationSubmit" />
        <BeneficiaryModal v-model="showBeneficiaryModal" @submit="handleBeneficiarySubmit" />

        <!-- Summary Cards -->
        <n-grid x-gap="12" y-gap="12" cols="3" responsive="self">
          <n-gi>
            <n-card>
              <n-space vertical align="center">
                <n-text depth="3">Entrada Total (Mês)</n-text>
                <n-statistic value="550 kg" />
              </n-space>
            </n-card>
          </n-gi>
          <n-gi>
            <n-card>
              <n-space vertical align="center">
                <n-text depth="3">Saída Total (Mês)</n-text>
                <n-statistic value="320 kg" />
              </n-space>
            </n-card>
          </n-gi>
          <n-gi>
            <n-card>
              <n-space vertical align="center">
                <n-text depth="3">Estoque Atual</n-text>
                <n-statistic value="230 kg" />
              </n-space>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- Beneficiaries Table -->
        <n-card title="Beneficiários e Controle Mensal">
          <n-data-table
            :columns="columns"
            :data="tableData"
            :pagination="pagination"
          />
        </n-card>
      </n-space>
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import type { DataTableColumns } from 'naive-ui'
import { 
  NLayout,
  NLayoutContent,
  NSpace,
  NButton,
  NCard,
  NDataTable,
  NIcon,
  NProgress,
  NTag,
  NGrid,
  NGi,
  NH1,
  NDivider,
  NText,
  NStatistic
} from 'naive-ui'
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

</style>