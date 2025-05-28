<template>
  <div class="ration-container">
    <div class="page-header">
      <h1 class="page-title">Entradas de Ração</h1>
      <div class="title-underline"></div>
    </div>

    <!-- Resumo do Estoque -->
    <n-card class="stock-summary">
      <div class="stock-grid">
        <div class="stock-item" v-for="stock in stockSummary" :key="stock.type">
          <h3>{{ stock.type }}</h3>
          <p class="stock-quantity">{{ stock.quantity }}kg</p>
        </div>
      </div>
    </n-card>

    <div class="action-buttons">
      <n-button type="primary" class="action-button" style="background-color: #f77800; margin-right: 12px" @click="showAddModal = true">
        <template #icon>
          <n-icon><IconPlus /></n-icon>
        </template>
        Nova Entrada
      </n-button>
      <n-button type="default" class="action-button" @click="showManageTypesModal = true">
        <template #icon>
          <n-icon><IconSettings /></n-icon>
        </template>
        Gerenciar Tipos de Ração
      </n-button>
    </div>

    <n-card class="entries-table-card">
      <n-data-table
        :columns="columns"
        :data="tableData"
        :pagination="pagination"
        :loading="loading"
      />
    </n-card>

    <!-- Modal de Nova Entrada -->
    <n-modal
      v-model:show="showAddModal"
      preset="dialog"
      style="width: 600px"
      title="Nova Entrada de Ração"
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
        <n-form-item label="Data" path="date">
          <n-date-picker
            v-model:value="formData.date"
            type="date"
            clearable
            style="width: 100%"
          />
        </n-form-item>

        <n-form-item label="Tipo de Ração" path="type">
          <n-select
            v-model:value="formData.type"
            :options="rationTypes"
            placeholder="Selecione o tipo de ração"
            clearable
          />
        </n-form-item>

        <n-form-item label="Quantidade (kg)" path="quantity">
          <n-input-number
            v-model:value="formData.quantity"
            :min="1"
            :precision="0"
            placeholder="Informe a quantidade em kg"
            style="width: 100%"
          />
        </n-form-item>

        <n-form-item label="Observações" path="observations">
          <n-input
            v-model:value="formData.observations"
            type="textarea"
            placeholder="Observações adicionais"
          />
        </n-form-item>
      </n-form>

      <template #action>
        <div class="modal-actions">
          <n-button @click="handleCancel">Cancelar</n-button>
          <n-button type="primary" style="background-color: #f77800" :loading="loading" @click="handleSubmit">Salvar</n-button>
        </div>
      </template>
    </n-modal>

    <!-- Modal de Gerenciamento de Tipos de Ração -->
    <n-modal
      v-model:show="showManageTypesModal"
      preset="dialog"
      style="width: 800px"
      title="Gerenciar Tipos de Ração"
    >
      <div class="types-management-container">
        <n-form
          ref="typeFormRef"
          :model="typeFormData"
          :rules="typeRules"
          label-placement="left"
          label-width="auto"
          require-mark-placement="right-hanging"
          size="medium"
        >
          <n-form-item label="Nome" path="name">
            <n-input
              v-model:value="typeFormData.name"
              placeholder="Nome do tipo de ração"
            />
          </n-form-item>

          <n-form-item label="Descrição" path="description">
            <n-input
              v-model:value="typeFormData.description"
              type="textarea"
              placeholder="Descrição do tipo de ração"
            />
          </n-form-item>

          <div class="form-actions">
            <n-button type="primary" style="background-color: #f77800" @click="handleAddType">
              Adicionar Tipo
            </n-button>
          </div>
        </n-form>

        <div class="types-table">
          <n-data-table
            :columns="typeColumns"
            :data="rationTypes"
            :pagination="{ pageSize: 5 }"
          />
        </div>
      </div>

      <template #action>
        <div class="modal-actions">
          <n-button @click="showManageTypesModal = false">Fechar</n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NCard, NButton, NDataTable, NModal, NForm, NFormItem, NInput, NInputNumber, NDatePicker, NSelect, NIcon, useMessage } from 'naive-ui'
import { IconPlus, IconSettings } from '@tabler/icons-vue'
import type { DataTableColumns } from 'naive-ui'
import type { RationType } from '~/models/rationTypeModel'

const loading = ref(false)
const showAddModal = ref(false)
const showManageTypesModal = ref(false)
const formRef = ref()
const typeFormRef = ref()
const message = useMessage()

const typeFormData = ref({
  name: '',
  description: ''
})

const typeRules = {
  name: {
    required: true,
    message: 'Por favor, informe o nome do tipo de ração'
  },
  description: {
    required: true,
    message: 'Por favor, informe a descrição do tipo de ração'
  }
}

const formData = ref({
  date: null,
  type: null,
  quantity: null as number | null,
  observations: ''
})

const rationTypes = ref<RationType[]>([
  { id: 1, name: 'Ração Gato', description: 'Ração para gatos adultos' },
  { id: 2, name: 'Ração Filhote', description: 'Ração para filhotes'},
  { id: 3, name: 'Ração Premium', description: 'Ração premium para gatos'}
])

const typeColumns = [
  {
    title: 'Nome',
    key: 'name'
  },
  {
    title: 'Descrição',
    key: 'description'
  },
  {
    title: 'Ações',
    key: 'actions',
    render: (row: any) => {
      return h(
        NButton,
        {
          size: 'small',
          type: 'error',
          onClick: () => handleDeleteType(row)
        },
        { default: () => 'Excluir' }
      )
    }
  }
]

const handleAddType = () => {
  typeFormRef.value?.validate((errors: any) => {
    if (!errors) {
      const newType = {
        id: rationTypes.value.length + 1,
        name: typeFormData.value.name,
        description: typeFormData.value.description,
        value: typeFormData.value.name.toLowerCase().replace(/\s+/g, '_'),
        label: typeFormData.value.name
      }
      rationTypes.value.push(newType)
      message.success('Tipo de ração adicionado com sucesso!')
      typeFormData.value = { name: '', description: '' }
      typeFormRef.value?.restoreValidation()
    }
  })
}

const handleDeleteType = (type: any) => {
  const index = rationTypes.value.findIndex(t => t.id === type.id)
  if (index > -1) {
    rationTypes.value.splice(index, 1)
    message.success('Tipo de ração removido com sucesso!')
  }
}

const rules = {
  date: {
    required: true,
    message: 'Por favor, selecione a data'
  },
  type: {
    required: true,
    message: 'Por favor, selecione o tipo de ração'
  },
  quantity: {
    required: true,
    type: 'number',
    message: 'Por favor, informe a quantidade'
  }
}

// Exemplo de dados para a tabela
const tableData = ref([
  {
    id: 1,
    date: '2024-01-15',
    type: 'Ração Adulto',
    quantity: 100,
    observations: 'Doação mensal'
  },
  {
    id: 2,
    date: '2024-01-16',
    type: 'Ração Filhote',
    quantity: 50,
    observations: 'Compra emergencial'
  }
])

// Exemplo de resumo do estoque
const stockSummary = ref([
  { type: 'Ração Adulto', quantity: 250 },
  { type: 'Ração Filhote', quantity: 150 },
  { type: 'Ração Premium', quantity: 100 }
])

const columns: DataTableColumns = [
  {
    title: 'Data',
    key: 'date',
    sorter: true
  },
  {
    title: 'Tipo',
    key: 'type',
    sorter: true
  },
  {
    title: 'Quantidade (kg)',
    key: 'quantity',
    sorter: true
  },
  {
    title: 'Observações',
    key: 'observations'
  }
]

const pagination = {
  pageSize: 10
}

const handleSubmit = () => {
  formRef.value?.validate((errors: any) => {
    if (!errors) {
      loading.value = true
      // Aqui você implementaria a lógica para salvar os dados
      console.log('Dados do formulário:', formData.value)
      loading.value = false
      showAddModal.value = false
      resetForm()
    }
  })
}

const handleCancel = () => {
  showAddModal.value = false
  resetForm()
}

const resetForm = () => {
  formData.value = {
    date: null,
    type: null,
    quantity: null,
    observations: ''
  }
  formRef.value?.restoreValidation()
}
</script>

<style scoped>
.ration-container {
  padding: 24px;
  background-color: #fff8e1;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 12px;
  color: #f77800;
}

.title-underline {
  width: 100px;
  height: 4px;
  background-color: #f77800;
  border-radius: 2px;
}

.stock-summary {
  margin-bottom: 32px;
  box-shadow: 0 4px 16px rgba(247, 120, 0, 0.1);
  border-radius: 16px;
  background-color: #ffffff;
}

.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  padding: 24px;
}

.stock-item {
  text-align: center;
  padding: 28px;
  border-radius: 16px;
  background-color: #fff;
  border: 2px solid #f8f0d8;
  transition: all 0.3s ease;
}

.stock-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(247, 120, 0, 0.15);
  border-color: #f77800;
}

.stock-item h3 {
  margin: 0;
  color: #4a4a4a;
  font-size: 18px;
  font-weight: 600;
}

.stock-quantity {
  margin: 12px 0 0;
  font-size: 32px;
  font-weight: bold;
  color: #f77800;
}

.action-buttons {
  margin-bottom: 28px;
}

.entries-table-card {
  margin-bottom: 32px;
  box-shadow: 0 4px 16px rgba(247, 120, 0, 0.1);
  border-radius: 16px;
  background-color: #ffffff;
  padding: 8px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.types-management-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.types-table {
  margin-top: 24px;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 16px;
}
</style>