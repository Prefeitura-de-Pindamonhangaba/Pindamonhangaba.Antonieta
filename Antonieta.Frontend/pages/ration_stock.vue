<template>
  <page-wrapper :loading="pageLoading">
    <div class="ration-stock-container">
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
              :options="feedTypes"
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
              :data="feedTypes"
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
  </page-wrapper>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NCard, NButton, NDataTable, NModal, NForm, NFormItem, NInput, NInputNumber, NDatePicker, NSelect, NIcon, useMessage } from 'naive-ui'
import { IconPlus, IconSettings } from '@tabler/icons-vue'
import type { DataTableColumns } from 'naive-ui'
import { useAuth } from '~/composables/useAuth'

const { getAuthHeaders } = useAuth()
const loading = ref(false)
const showAddModal = ref(false)
const showManageTypesModal = ref(false)
const formRef = ref()
const typeFormRef = ref()
const message = useMessage()

const pageLoading = ref(true)

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

const feedTypes = ref([])

const fetchRationTypes = async () => {
  try {
    pageLoading.value = true
    loading.value = true
    const response = await fetch('http://localhost:5000/api/ration_type', {
      method: 'GET',
      headers: {
        ...getAuthHeaders(),
        'Accept': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Falha ao carregar tipos de ração')
    }

    const data = await response.json()
    console.log('API Response:', data)

    feedTypes.value = data.map(item => ({
      id: item.id,
      name: item.name,
      description: item.description,
      value: item.id,
      label: item.name
    })).filter(Boolean)

    console.log('Processed Data:', feedTypes.value)
  } catch (error) {
    message.error(error.message || 'Erro ao carregar tipos de ração')
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

const handleAddType = async () => {
  typeFormRef.value?.validate(async (errors: any) => {
    if (!errors) {
      try {
        loading.value = true
        const response = await fetch('http://localhost:5000/api/ration_type', {
          method: 'POST',
          headers: {
            ...getAuthHeaders(),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: typeFormData.value.name,
            description: typeFormData.value.description
          })
        })

        if (!response.ok) {
          throw new Error('Falha ao adicionar tipo de ração')
        }

        await fetchRationTypes()
        message.success('Tipo de ração adicionado com sucesso!')
        typeFormData.value = { name: '', description: '' }
        typeFormRef.value?.restoreValidation()
      } catch (error) {
        message.error(error.message || 'Erro ao adicionar tipo de ração')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleDeleteType = async (type: any) => {
  try {
    loading.value = true
    const response = await fetch(`http://localhost:5000/api/ration_type/${type.id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })

    if (!response.ok) {
      throw new Error('Falha ao remover tipo de ração')
    }

    await fetchRationTypes()
    message.success('Tipo de ração removido com sucesso!')
  } catch (error) {
    message.error(error.message || 'Erro ao remover tipo de ração')
  } finally {
    loading.value = false
  }
}

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

const handleSubmit = async () => {
  formRef.value?.validate(async (errors: any) => {
    if (!errors) {
      try {
        loading.value = true
        const response = await fetch('http://localhost:5000/api/ration-stock', {
          method: 'POST',
          headers: {
            ...getAuthHeaders(),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: formData.value.observations,
            ration_type_id: parseInt(formData.value.type),
            unit: 'kg',
            stock: formData.value.quantity,
            description: formData.value.observations
          })
        })

        if (!response.ok) {
          throw new Error('Falha ao adicionar entrada de ração')
        }

        message.success('Entrada de ração adicionada com sucesso!')
        showAddModal.value = false
        resetForm()
      } catch (error) {
        message.error(error.message || 'Erro ao adicionar entrada de ração')
      } finally {
        loading.value = false
      }
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

onMounted(() => {
  fetchRationTypes()
})
</script>

<style scoped>
.ration-stock-container {
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