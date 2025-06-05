<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 600px">
    <template #header>
      <div class="modal-header">
        <h3>Cadastrar Novo Beneficiário</h3>
      </div>
    </template>
    <div class="modal-content">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-form-item label="Nome" path="name">
          <n-input 
            v-model:value="formData.name" 
            clearable 
            style="width: 100%" 
            placeholder="Nome do beneficiário"/>
        </n-form-item>
        <n-form-item label="Documento" path="document">
          <n-input 
            v-model:value="formData.document" 
            clearable 
            style="width: 100%" 
            placeholder="CPF ou RG"/>
        </n-form-item>
        <n-form-item label="Endereço" path="address">
          <n-input 
            v-model:value="formData.address" 
            clearable 
            style="width: 100%" 
            placeholder="Endereço completo"/>
        </n-form-item>
        <n-form-item label="Contato" path="contact">
          <n-input 
            v-model:value="formData.contact" 
            clearable 
            style="width: 100%" 
            placeholder="Telefone ou e-mail"/>
        </n-form-item>
        <n-form-item label="Limite Mensal (kg)" path="monthly_limit">
          <n-input-number 
            v-model:value="formData.monthly_limit" 
            clearable 
            style="width: 100%" 
            placeholder="Limite mensal em kg"
          />
        </n-form-item>
      </n-form>
    </div>
    <template #action>
      <div class="modal-actions">
        <n-button @click="handleCancel" :disabled="submitting">
          Cancelar
        </n-button>
        <n-button 
          type="primary" 
          style="background-color: #f77800" 
          @click="handleSubmit"
          :loading="submitting"
          :disabled="submitting"
        >
          {{ submitting ? 'Salvando...' : 'Salvar' }}
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { NModal, NForm, NFormItem, NInput, NInputNumber, NButton } from 'naive-ui'
import { beneficiaryService } from '~/services/beneficiaryService'
import type { Beneficiary } from '~/models/beneficiary'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [formData: Beneficiary]
}>()

const formRef = ref()
const submitting = ref(false)
const formData = ref({
  name: '',
  document: '',
  address: '',
  contact: '',
  monthly_limit: null as number | null // Changed from limit to monthly_limit to match backend
})

const rules = {
  name: {
    required: true,
    message: 'Por favor, informe o nome do beneficiário'
  },
  document: {
    required: true,
    message: 'Por favor, informe o documento'
  },
  address: {
    required: true,
    message: 'Por favor, informe o endereço'
  },
  contact: {
    required: true,
    message: 'Por favor, informe o contato'
  },
  limit: {
    required: true,
    message: 'Por favor, informe o limite mensal'
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true

    const newBeneficiary = await beneficiaryService.create({
      name: formData.value.name,
      document: formData.value.document,
      address: formData.value.address,
      contact: formData.value.contact,
      monthly_limit: formData.value.monthly_limit || 0
    })

    window.$message?.success('Beneficiário cadastrado com sucesso!')
    emit('submit', newBeneficiary)
    emit('update:modelValue', false)
    resetForm()
  } catch (error) {
    if (error instanceof Error) {
      window.$message?.error(error.message)
    } else {
      window.$message?.error('Erro ao cadastrar beneficiário')
    }
    console.error('Error creating beneficiary:', error)
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  formData.value = {
    name: '',
    document: '',
    address: '',
    contact: '',
    monthly_limit: null
  }
}

const handleCancel = () => {
  emit('update:modelValue', false)
  resetForm()
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