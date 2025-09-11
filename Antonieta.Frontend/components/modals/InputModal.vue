<template>
  <n-modal v-model:show="show" preset="dialog" title="Nova Entrada de Ração">
    <n-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
      style="max-width: 640px"
    >
      <n-form-item label="Tipo de Ração" path="ration_stock_id">
        <n-select
          v-model:value="formData.ration_stock_id"
          :options="rationOptions"
          placeholder="Selecione o tipo de ração"
          :loading="!rationOptions.length"
          clearable
        />
      </n-form-item>

      <n-form-item label="Quantidade (kg)" path="amount">
        <n-input-number
          v-model:value="formData.amount"
          :min="1"
          :precision="2"
          placeholder="Informe a quantidade em kg"
        />
      </n-form-item>

      <n-form-item label="Descrição" path="description">
        <n-input
          v-model:value="formData.description"
          type="text"
          placeholder="Informe uma descrição para esta entrada"
        />
      </n-form-item>
    </n-form>

    <template #action>
      <n-space justify="end">
        <n-button @click="handleCancel" :disabled="loading">
          Cancelar
        </n-button>
        <n-button 
          type="primary" 
          :loading="loading" 
          :disabled="loading"
          style="background-color: #f77800"
          @click="handleSubmit"
        >
          {{ loading ? 'Salvando...' : 'Registrar' }}
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { NModal, NForm, NFormItem, NInputNumber, NButton, NSelect, NSpace, NInput, useMessage } from 'naive-ui'
import { rationInputService } from '~/services/rationInputService'
import type { RationInput } from '~/models/rationInputModel'
import { rationStockService } from '~/services/rationStockService'

const props = defineProps<{
  modelValue: boolean
}>()

// Update emit types
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', formData: Omit<RationInput, 'id'>): void
}>()

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const rationOptions = ref<Array<{ label: string; value: number }>>([])

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const formData = ref({
  ration_stock_id: null as number | null,
  amount: null as number | null,
  date: new Date().toISOString(),
  description: '' as string
})

const rules: FormRules = {
  ration_stock_id: {
    required: true,
    type: 'number',
    message: 'Por favor, selecione o tipo de ração',
    trigger: 'change'
  },
  amount: {
    required: true,
    type: 'number',
    message: 'Por favor, informe a quantidade',
    trigger: ['blur', 'change']
  },
  description: {
    required: true,
    message: 'Por favor, informe uma descrição',
    trigger: ['blur', 'input']
  }
}

const loadRationStocks = async () => {
  try {
    const rationStocks = await rationStockService.getAll()
    rationOptions.value = rationStocks.map(rs => ({
      label: rs.name,
      value: rs.id
    }))
  } catch (error) {
    console.error('Error loading ration types:', error)
    message.error('Erro ao carregar tipos de ração')
  }
}

const handleSubmit = () => {
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      try {
        loading.value = true
        const inputData = {
          ration_stock_id: formData.value.ration_stock_id!,
          amount: formData.value.amount!,
          date: formData.value.date,
          description: formData.value.description
        }
        
        // Remove the service call from here
        await rationInputService.create(inputData)
        message.success('Entrada de ração registrada com sucesso!')
        show.value = false
        resetForm()
      } catch (error) {
        console.error('Error submitting input:', error)
        message.error('Erro ao registrar entrada')
      } finally {
        loading.value = false
      }
    }
  })
}

const resetForm = () => {
  formData.value = {
    ration_stock_id: null,
    amount: null,
    date: new Date().toISOString(),
    description: ''
  }
  formRef.value?.restoreValidation()
}

const handleCancel = () => {
  show.value = false
  resetForm()
}

onMounted(() => {
  loadRationStocks()
})
</script>