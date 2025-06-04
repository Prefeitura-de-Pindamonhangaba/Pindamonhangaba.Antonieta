<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 600px">
    <template #header>
      <div class="modal-header">
        <h3>Registrar Nova Doação</h3>
      </div>
    </template>
    <div class="modal-content">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-form-item label="Data" path="date">
          <n-date-picker 
            v-model:value="formData.date" 
            type="date" 
            clearable 
            style="width: 100%" 
          />
        </n-form-item>
        <n-form-item label="Tipo de Ração" path="ration_id">
          <n-select
            v-model:value="formData.ration_id"
            :options="rationOptions"
            clearable
            filterable
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="Beneficiário" path="beneficiary_id">
          <n-select
            v-model:value="formData.beneficiary_id"
            :options="beneficiaryOptions"
            :loading="loading"
            clearable
            filterable
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="Quantidade (kg)" path="amount">
          <n-input-number 
            v-model:value="formData.amount" 
            clearable 
            style="width: 100%" 
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
import { ref, watch } from 'vue'
import { NModal, NForm, NFormItem, NInput, NInputNumber, NDatePicker, NButton, NSelect } from 'naive-ui'
import { beneficiaryService } from '~/services/beneficiaryService'
import { rationTypeService } from '~/services/rationTypeService'
import { distributionService } from '~/services/distributionService'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [formData: any]
}>()

const formRef = ref()
const loading = ref(false)
const submitting = ref(false)
const beneficiaryOptions = ref<Array<{ label: string; value: number }>>([])
const rationOptions = ref<Array<{ label: string; value: number }>>([])

const formData = ref({
  date: null as Date | null,
  amount: null as number | null,
  beneficiary_id: null as number | null,
  ration_id: null as number | null
})

const rules = {
  date: {
    required: true,
    message: 'Por favor, selecione a data'
  },
  amount: {
    required: true,
    message: 'Por favor, informe a quantidade'
  },
  beneficiary_id: {
    required: true,
    message: 'Por favor, selecione um beneficiário'
  },
  ration_id: {
    required: true,
    message: 'Por favor, selecione o tipo de ração'
  }
}

// Load data when modal opens
watch(() => props.modelValue, async (newValue) => {
  if (newValue) {
    await Promise.all([
      loadBeneficiaries(),
      loadRations()
    ])
  }
})

const loadBeneficiaries = async () => {
  try {
    loading.value = true
    const [beneficiariesData] = await beneficiaryService.getAll()
    beneficiaryOptions.value = beneficiariesData.map(beneficiary => ({
      label: beneficiary.name,
      value: beneficiary.id
    }))
  } catch (error) {
    console.error('Error loading beneficiaries:', error)
  } finally {
    loading.value = false
  }
}

const loadRations = async () => {
  try {
    const rationTypes = await rationTypeService.getAll()
    rationOptions.value = rationTypes.map(type => ({
      label: type.name, // Adjust this to match your RationType model property
      value: type.id
    }))
  } catch (error) {
    console.error('Error loading ration types:', error)
    window.$message?.error('Erro ao carregar tipos de ração')
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true
    
    const distribution = {
      date: formData.value.date,
      amount: formData.value.amount!,
      beneficiary_id: formData.value.beneficiary_id!,
      ration_id: formData.value.ration_id!
    }

    await distributionService.create(distribution)
    window.$message?.success('Doação registrada com sucesso!')
    emit('submit', distribution)
    emit('update:modelValue', false)
    resetForm()
  } catch (error) {
    console.error('Error submitting distribution:', error)
    window.$message?.error('Erro ao registrar doação')
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  emit('update:modelValue', false)
  resetForm()
}

const resetForm = () => {
  formData.value = {
    date: null,
    amount: null,
    beneficiary_id: null,
    ration_id: null
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