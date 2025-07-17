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
          placeholder="Buscar e selecionar beneficiário..."
          :loading="!beneficiaryOptions.length"
          clearable
          filterable
          :filter="filterBeneficiaries"
          :render-label="renderBeneficiaryLabel"
          :render-option="renderBeneficiaryOption"
        />
      </n-form-item>

      <n-form-item label="Tipo de Ração" path="ration_id">
        <n-select
          v-model:value="formData.ration_id"
          :options="rationOptions"
          placeholder="Buscar e selecionar tipo de ração..."
          :loading="!rationOptions.length"
          clearable
          filterable
          :filter="filterRations"
          :render-label="renderRationLabel"
          :render-option="renderRationOption"
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
import { h, ref, onMounted, computed } from 'vue'
import type { FormInst, FormRules, SelectOption } from 'naive-ui'
import { NModal, NForm, NFormItem, NInput, NInputNumber, NButton, NSelect, NSpace, useMessage } from 'naive-ui'
import { beneficiaryService } from '~/services/beneficiaryService'
import type { Distribution } from '~/models/distributionModel'
import type { Beneficiary } from '~/models/beneficiaryModel'
import type { RationStock } from '~/models/rationStockModel'
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
const beneficiaries = ref<Beneficiary[]>([])
const rationStocks = ref<RationStock[]>([])

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

// Computed para opções com dados completos
const beneficiaryOptions = computed(() => 
  beneficiaries.value.map(beneficiary => ({
    label: `${beneficiary.name} - ${beneficiary.document}`,
    value: beneficiary.id,
    beneficiary: beneficiary
  }))
)

const rationOptions = computed(() => 
  rationStocks.value.map(ration => ({
    label: `${ration.name} (${ration.stock} kg disponível)`,
    value: ration.id,
    ration: ration
  }))
)

// Funções de filtro customizadas para busca
const filterBeneficiaries = (pattern: string, option: SelectOption) => {
  const beneficiary = option.beneficiary as Beneficiary
  const searchPattern = pattern.toLowerCase()
  
  return (
    beneficiary.name.toLowerCase().includes(searchPattern) ||
    beneficiary.document.toLowerCase().includes(searchPattern) ||
    (beneficiary.contact && beneficiary.contact.toLowerCase().includes(searchPattern))
  )
}

const filterRations = (pattern: string, option: SelectOption) => {
  const ration = option.ration as RationStock
  const searchPattern = pattern.toLowerCase()
  
  return (
    ration.name.toLowerCase().includes(searchPattern) ||
    (ration.description && ration.description.toLowerCase().includes(searchPattern))
  )
}

// Funções de renderização customizadas
const renderBeneficiaryLabel = (option: SelectOption) => {
  const beneficiary = option.beneficiary as Beneficiary
  return h('div', { style: { display: 'flex', flexDirection: 'column' } }, [
    h('span', { style: { fontWeight: '500' } }, beneficiary.name),
    h('span', { style: { fontSize: '12px', color: '#999' } }, `Doc: ${beneficiary.document}`)
  ])
}

const renderBeneficiaryOption = ({ node, option }: { node: any, option: SelectOption }) => {
  const beneficiary = option.beneficiary as Beneficiary
  return h('div', { style: { padding: '4px 0' } }, [
    h('div', { style: { fontWeight: '500' } }, beneficiary.name),
    h('div', { style: { fontSize: '12px', color: '#666' } }, `Documento: ${beneficiary.document}`),
    h('div', { style: { fontSize: '12px', color: '#999' } }, `Limite mensal: ${beneficiary.monthly_limit} kg`)
  ])
}

const renderRationLabel = (option: SelectOption) => {
  const ration = option.ration as RationStock
  return h('div', { style: { display: 'flex', justifyContent: 'space-between' } }, [
    h('span', ration.name),
    h('span', { style: { fontSize: '12px', color: '#999' } }, `${ration.stock} kg`)
  ])
}

const renderRationOption = ({ node, option }: { node: any, option: SelectOption }) => {
  const ration = option.ration as RationStock
  return h('div', { style: { padding: '4px 0' } }, [
    h('div', { style: { fontWeight: '500' } }, ration.name),
    h('div', { style: { fontSize: '12px', color: '#666' } }, ration.description),
    h('div', { style: { fontSize: '12px', color: ration.stock > 0 ? '#18a058' : '#d03050' } }, 
      `Estoque: ${ration.stock} kg`)
  ])
}

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
    const [beneficiariesData] = await beneficiaryService.getAll()
    beneficiaries.value = beneficiariesData
  } catch (error) {
    console.error('Error loading beneficiaries:', error)
    message.error('Erro ao carregar beneficiários')
  }
}

const loadRationStocks = async () => {
  try {
    const rationStocksData = await rationStockService.getAll()
    rationStocks.value = rationStocksData
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

<style scoped>
:deep(.n-select) {
  min-height: 34px;
}

:deep(.n-base-selection-label) {
  line-height: 1.4;
}

:deep(.n-base-select-option) {
  min-height: 60px;
  padding: 8px 12px;
}
</style>