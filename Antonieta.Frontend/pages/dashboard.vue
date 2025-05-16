<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <div class="title-underline"></div>
    </div>
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
import { NCard, NDataTable, NPageHeader, NTag } from 'naive-ui'

interface BeneficiaryData {
  nome: string
  limiteMensal: string
  recebido: string
  status: string
}

const columns: DataTableColumns<BeneficiaryData> = [
  {
    title: 'Nome',
    key: 'nome'
  },
  {
    title: 'Limite Mensal',
    key: 'limiteMensal'
  },
  {
    title: 'Recebido Este Mês',
    key: 'recebido'
  },
  {
    title: 'Status',
    key: 'status',
    render(row) {
      const statusMap = {
        'Pode Receber': 'success',
        'Próx. Limite': 'warning',
        'Limite Atingido': 'error'
      }
      return h(
        'n-tag',
        {
          type: statusMap[row.status as keyof typeof statusMap] || 'default',
          style: {
            marginRight: '6px'
          }
        },
        { default: () => row.status }
      )
    }
  }
]

const tableData: BeneficiaryData[] = [
  {
    nome: 'Ana Silva',
    limiteMensal: '15 kg',
    recebido: '5 kg',
    status: 'Pode Receber'
  },
  {
    nome: 'João Santos',
    limiteMensal: '20 kg',
    recebido: '18 kg',
    status: 'Próx. Limite'
  },
  {
    nome: 'Maria Oliveira',
    limiteMensal: '10 kg',
    recebido: '10 kg',
    status: 'Limite Atingido'
  },
  {
    nome: 'Pedro Souza',
    limiteMensal: '25 kg',
    recebido: '0 kg',
    status: 'Pode Receber'
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

:deep(.n-card-header__title) {
  color: #263238;
  font-size: 1.25rem;
  font-weight: 600;
}
</style>