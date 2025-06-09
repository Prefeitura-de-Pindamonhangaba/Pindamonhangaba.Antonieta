<template>
  <n-modal v-model:show="show" preset="dialog" title="Nova Distribuição de Ração">
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
      <n-form-item label="Beneficiário" path="beneficiary_id">
        <n-select
          v-model:value="formData.beneficiary_id"
          :options="beneficiaryOptions"
          placeholder="Selecione o beneficiário"
          :loading="!beneficiaryOptions.length"
          clearable
        />
      </n-form-item>

      <n-form-item label="Tipo de Ração" path="ration_id">
        <n-select
          v-model:value="formData.ration_id"
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
          :precision="0"
          placeholder="Informe a quantidade em kg"
        />
      </n-form-item>
    </n-form>

    <template #action>
      <n-space justify="end">
        <n-button @click="handleCancel" :disabled="loading">Cancelar</n-button>
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
import { ref, onMounted } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { NModal, NForm, NFormItem, NInput, NInputNumber, NButton, NSelect, useMessage } from 'naive-ui'
import { beneficiaryService } from '~/services/beneficiaryService'
import type { Distribution } from '~/models/distributionModel'
import { rationStockService } from '~/services/rationStockService'
import { distributionService } from '~/services/distributionService'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', formData: Distribution): void
}>()

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const beneficiaryOptions = ref<Array<{ label: string; value: number }>>([])
const rationOptions = ref<Array<{ label: string; value: number }>>([])

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const formData = ref({
  beneficiary_id: null as number | null,
  ration_id: null as number | null,
  amount: null as number | null,
  date: new Date().toISOString()
})

const rules: FormRules = {
  beneficiary_id: {
    required: true,
    type: 'number',
    message: 'Por favor, selecione o beneficiário',
    trigger: 'change'
  },
  ration_id: {
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
  }
}

const loadBeneficiaries = async () => {
  try {
    const [beneficiaries] = await beneficiaryService.getAll()
    beneficiaryOptions.value = beneficiaries.map(b => ({
      label: b.name,
      value: b.id
    }))
  } catch (error) {
    console.error('Error loading beneficiaries:', error)
    message.error('Erro ao carregar beneficiários')
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

const submitDistribution = async (data: Distribution) => {
  try {
    await distributionService.create(data)
    message.success('Distribuição registrada com sucesso!')
  } catch (error) {
    console.error('Error submitting distribution:', error)
    message.error('Erro ao registrar distribuição')
  }
}

onMounted(() => {
  Promise.all([loadBeneficiaries(), loadRationStocks()])
})

const handleSubmit = () => {
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      try {
        loading.value = true
        await submitDistribution(formData.value)
        show.value = false
        resetForm()
      } catch (error) {
        console.error('Error submitting distribution:', error)
        message.error('Erro ao registrar distribuição')
      } finally {
        loading.value = false
      }
    }
  })
}

const resetForm = () => {
  formData.value = {
    beneficiary_id: null,
    ration_id: null,
    amount: null,
    date: new Date().toISOString()
  }
  formRef.value?.restoreValidation()
}

const handleCancel = () => {
  show.value = false
  resetForm()
}
</script>