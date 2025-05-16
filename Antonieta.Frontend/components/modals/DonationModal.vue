<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 600px">
    <template #header>
      <div class="modal-header">
        <h3>Registrar Nova Doação</h3>
      </div>
    </template>
    <div class="modal-content">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-form-item label="Data da Saída" path="date">
          <n-date-picker 
            v-model:value="formData.date" 
            type="date" 
            clearable 
            style="width: 100%" 
            placeholder="Data de saída"/>
        </n-form-item>
        <n-form-item label="Quantidade (kg)" path="amount">
          <n-input-number 
            v-model:value="formData.amount" 
            clearable 
            style="width: 100%" 
            placeholder="Quantidade"/>
        </n-form-item>
        <n-form-item label="Beneficiário" path="beneficiary">
          <n-select
            v-model:value="formData.beneficiary.name"
            clearable
            style="width: 100%"
            filterable
            placeholder="Please select a song"
            :options="beneficiaryOptions"
          />
        </n-form-item>
        <n-form-item label="Observações" path="observacoes">
          <n-input 
            v-model:value="formData.observacoes" 
            type="textarea" 
            clearable 
            placeholder="Observações"/>
        </n-form-item>
      </n-form>
    </div>
    <template #action>
      <div class="modal-actions">
        <n-button @click="handleCancel">Cancelar</n-button>
        <n-button type="primary" style="background-color: #f77800" @click="handleSubmit">Salvar</n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { NModal, NForm, NFormItem, NInput, NInputNumber, NDatePicker, NButton } from 'naive-ui'
import Beneficiary  from '~/models/beneficiary';
import type { DonationType } from '~/types/donation_type';

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [formData: any]
}>()

const formRef = ref()
const formData = ref({
  date: null,
  amount: null,
  type: null as DonationType | null, 
  beneficiary: new Beneficiary(),
  observacoes: ''
})

const beneficiaryOptions = [
  { label: 'Entrada', value: 'entrada' },
  { label: 'Saída', value: 'saida' }
]

const beneficiaryList: Beneficiary[] = [
  {
    id: 0, 
    name: 'Maria',
    document: '12345678901',
    address: 'Rua das Flores, 123',
    contact: '987654321',
    limit: 100,
  },
  {
    id: 0, 
    name: 'João',
    document: '12345678901',
    address: 'Rua das Flores, 123',
    contact: '987654321',
    limit: 100,
  },
]

const rules = {
  data: {
    required: true,
    message: 'Por favor, selecione a data da doação'
  },
  amount: {
    required: true,
    message: 'Por favor, informe a quantidade'
  },
  beneficiary: {
    required: true,
    message: 'Por favor, informe o doador'
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    emit('submit', formData.value)
    emit('update:modelValue', false)
    formData.value = {
      data: null,
      quantidade: null,
      doador: '',
      observacoes: ''
    }
  } catch (e) {
    // Erros de validação são tratados automaticamente pelo naive-ui
  }
}

const handleCancel = () => {
  emit('update:modelValue', false)
  formData.value = {
    data: null,
    quantidade: null,
    doador: '',
    observacoes: ''
  }
}


</script>

<style scoped>
.modal-header h3 {
  margin: 0;
  color: #263238;
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-content {
  padding: 1rem 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>