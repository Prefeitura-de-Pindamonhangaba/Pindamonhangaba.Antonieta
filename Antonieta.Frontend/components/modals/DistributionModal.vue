<template>
  <n-modal v-model:show="show" preset="dialog" title="Nova Distribuição de Ração" style="width: 700px">
    <n-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
    >
      <!-- Select de Beneficiário -->
      <n-form-item label="Beneficiário" path="beneficiary_id">
        <n-select
          v-model:value="formData.beneficiary_id"
          filterable
          placeholder="Selecione um beneficiário"
          :options="beneficiaryOptions"
          :loading="loadingBeneficiaries"
          clearable
        />
      </n-form-item>

      <!-- Select de Ração -->
      <n-form-item label="Tipo de Ração" path="ration_id">
        <n-select
          v-model:value="formData.ration_id"
          filterable
          placeholder="Selecione um tipo de ração"
          :options="rationOptions"
          :loading="loadingRations"
          clearable
        />
      </n-form-item>

      <!-- Input de Quantidade -->
      <n-form-item label="Quantidade (kg)" path="amount">
        <n-input-number
          v-model:value="formData.amount"
          :min="0.1"
          :max="maxAmount"
          :precision="2"
          :step="0.25"
          placeholder="Digite a quantidade (ex: 1.75)"
          style="width: 100%"
        />
      </n-form-item>

      <!-- Campo Observations -->
      <n-form-item label="Observações" path="observations">
        <n-input
          v-model:value="formData.observations"
          type="textarea"
          placeholder="Observações sobre esta distribuição (opcional)"
          :autosize="{
            minRows: 2,
            maxRows: 4
          }"
          maxlength="500"
          show-count
          clearable
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
          style="background-color: #f77800"
          @click="handleSubmit"
        >
          {{ loading ? 'Registrando...' : 'Registrar' }}
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { 
  NModal, NForm, NFormItem, NInputNumber, NInput, NButton, 
  NSelect, NSpace, NText, useMessage 
} from 'naive-ui'
import { beneficiaryService } from '~/services/beneficiaryService'
import { rationStockService } from '~/services/rationStockService'
import { distributionService } from '~/services/distributionService'
import type { Distribution, DistributionCreate } from '~/models/distributionModel'
import type { Beneficiary } from '~/models/beneficiaryModel'
import type { RationStock } from '~/models/rationStockModel'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [formData: Distribution]
}>()

const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const loadingBeneficiaries = ref(false)
const loadingRations = ref(false)
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
  observations: '' as string,
  date: new Date().toISOString()
})

// Opções para os selects
const beneficiaryOptions = computed(() => 
  beneficiaries.value.map(beneficiary => ({
    label: beneficiary.name,
    value: beneficiary.id
  }))
)

const rationOptions = computed(() => 
  rationStocks.value
    .filter(ration => ration.stock > 0)
    .map(ration => ({
      label: `${ration.name} (${ration.stock}kg disponível)`,
      value: ration.id
    }))
)

// Computeds para itens selecionados
const selectedBeneficiary = computed(() => {
  if (!formData.value.beneficiary_id) return null
  return beneficiaries.value.find(b => b.id === formData.value.beneficiary_id) || null
})

const selectedRation = computed(() => {
  if (!formData.value.ration_id) return null
  return rationStocks.value.find(r => r.id === formData.value.ration_id) || null
})

// Quantidade máxima permitida (agora com decimais)
const maxAmount = computed(() => {
  if (!selectedRation.value) return 999.99

  const stockLimit = selectedRation.value.stock ?? 0
  return stockLimit
})

// Regras de validação
const rules: FormRules = {
  beneficiary_id: {
    required: true,
    type: 'number',
    message: 'Selecione um beneficiário',
    trigger: 'change'
  },
  ration_id: {
    required: true,
    type: 'number',
    message: 'Selecione um tipo de ração',
    trigger: 'change'
  },
  amount: {
    required: true,
    type: 'number',
    message: 'Informe a quantidade',
    trigger: ['blur', 'change'],
    validator: (rule, value) => {
      if (!value || value <= 0) {
        return new Error('A quantidade deve ser maior que 0')
      }
      if (value < 0.1) {
        return new Error('A quantidade mínima é 0.1kg')
      }
      if (value > maxAmount.value) {
        return new Error(`Máximo permitido: ${maxAmount.value.toFixed(2)}kg`)
      }
      // Verificar se tem no máximo 2 casas decimais
      if (Number(value.toFixed(2)) !== value) {
        return new Error('Máximo 2 casas decimais permitidas')
      }
      return true
    }
  }
}

// Carregar dados
const loadBeneficiaries = async () => {
  try {
    loadingBeneficiaries.value = true
    const [data] = await beneficiaryService.getAll()
    beneficiaries.value = data
  } catch (error) {
    console.error('Erro ao carregar beneficiários:', error)
    message.error({
        content: 'Erro ao carregar beneficiários',
        duration: 5000,
        closable: true
      })
  } finally {
    loadingBeneficiaries.value = false
  }
}

const loadRationStocks = async () => {
  try {
    loadingRations.value = true
    const data = await rationStockService.getAll()
    rationStocks.value = data
  } catch (error) {
    console.error('Erro ao carregar rações:', error)
    message.error({
        content: 'Erro ao carregar tipos de ração',
        duration: 5000,
        closable: true
      })
  } finally {
    loadingRations.value = false
  }
}

// Submeter distribuição
const handleSubmit = async () => {
  try {
    const isValid = await new Promise((resolve) => {
      formRef.value?.validate((errors) => {
        resolve(!errors)
      })
    })

    if (!isValid) return

    loading.value = true

    const distributionData: DistributionCreate = {
      beneficiary_id: formData.value.beneficiary_id!,
      ration_id: formData.value.ration_id!,
      amount: Number(formData.value.amount!.toFixed(2)),
      observations: formData.value.observations || null,
      date: new Date().toISOString()
    }

    console.log('📦 Enviando distribuição com observações:', distributionData)

    const response = await distributionService.create(distributionData)
    
    message.success('Distribuição registrada com sucesso!')
    emit('submit', response)
    
    // Fechar modal e resetar
    show.value = false
    resetForm()
    
  } catch (error) {
    console.error('Erro ao registrar distribuição:', error)
    message.error({
        content: 'Erro ao registrar distribuição',
        duration: 5000,
        closable: true
      })
  } finally {
    loading.value = false
  }
}

// Reset form com observations
const resetForm = () => {
  formData.value = {
    beneficiary_id: null,
    ration_id: null,
    amount: null,
    observations: '',
    date: new Date().toISOString()
  }
  formRef.value?.restoreValidation()
}

const handleCancel = () => {
  show.value = false
  resetForm()
}

// Carregar dados ao montar
onMounted(() => {
  Promise.all([loadBeneficiaries(), loadRationStocks()])
})
</script>

<style scoped>
.info-box {
  margin-top: 4px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 3px solid #f77800;
}

/* Estilo customizado para os selects */
:deep(.n-base-selection) {
  border-radius: 6px;
  transition: all 0.2s ease;
}

:deep(.n-base-selection:hover) {
  border-color: #f77800;
}

:deep(.n-base-selection.n-base-selection--focus) {
  border-color: #f77800;
  box-shadow: 0 0 0 2px rgba(247, 120, 0, 0.2);
}

:deep(.n-input--textarea .n-input__input-el) {
  resize: vertical;
  min-height: 60px;
}

:deep(.n-input:hover) {
  border-color: #f77800;
}

:deep(.n-input.n-input--focus) {
  border-color: #f77800;
  box-shadow: 0 0 0 2px rgba(247, 120, 0, 0.2);
}

/* Estilo do dropdown */
:deep(.n-base-select-menu) {
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* Estilo das opções */
:deep(.n-base-select-option) {
  padding: 12px 16px;
  border-radius: 6px;
  margin: 2px 4px;
  transition: all 0.2s ease;
}

:deep(.n-base-select-option:hover) {
  background-color: #f8f9fa;
}

:deep(.n-base-select-option.n-base-selection--selected) {
  background-color: #f77800;
  color: white;
}

:deep(.n-base-select-option.n-base-selection--selected:hover) {
  background-color: #e56b00;
}
</style>