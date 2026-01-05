<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 900px">
    <template #header>
      <div class="modal-header">
        <h3>{{ props.editMode ? 'Editar Beneficiário' : 'Cadastrar Novo Beneficiário' }}</h3>
      </div>
    </template>
    <div class="modal-content">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <!-- Dados Pessoais -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">Dados Pessoais</span>
        </n-divider>

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Nome" path="name">
              <n-input 
                v-model:value="formData.name" 
                clearable 
                style="width: 100%" 
                placeholder="Nome completo do beneficiário"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Documento" path="document">
              <n-input 
                v-model:value="formData.document" 
                clearable 
                style="width: 100%" 
                placeholder="CPF ou RG"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- REMOVIDO: Limite Mensal -->
        <n-grid :cols="1" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Contato" path="contact">
              <n-input 
                v-model:value="formData.contact" 
                clearable 
                style="width: 100%" 
                placeholder="Telefone ou e-mail"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- ✅ NOVO: Endereço Estruturado -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">Endereço</span>
        </n-divider>

        <n-form-item label="Rua/Avenida" path="street">
          <n-input 
            v-model:value="formData.street" 
            clearable 
            style="width: 100%" 
            placeholder="Rua, Avenida, Travessa, etc."/>
        </n-form-item>

        <n-grid :cols="4" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Número" path="number">
              <n-input 
                v-model:value="formData.number" 
                clearable 
                style="width: 100%" 
                placeholder="123"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Complemento" path="complement">
              <n-input 
                v-model:value="formData.complement" 
                clearable 
                style="width: 100%" 
                placeholder="Apt, Casa, etc."/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="CEP" path="zip_code">
              <n-input 
                v-model:value="formData.zip_code" 
                clearable 
                style="width: 100%" 
                placeholder="12345-678"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Bairro" path="neighborhood">
              <n-input 
                v-model:value="formData.neighborhood" 
                clearable 
                style="width: 100%" 
                placeholder="Centro, Vila, etc."/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Cidade" path="city">
              <n-input 
                v-model:value="formData.city" 
                clearable 
                style="width: 100%" 
                placeholder="Pindamonhangaba"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Estado" path="state">
              <n-select
                v-model:value="formData.state"
                :options="stateOptions"
                placeholder="SP"
                style="width: 100%"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- Dados Pessoais Adicionais -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">Dados Adicionais</span>
        </n-divider>

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Nome da Mãe" path="mother_name">
              <n-input 
                v-model:value="formData.mother_name" 
                clearable 
                style="width: 100%" 
                placeholder="Nome da mãe do beneficiário"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Data de Nascimento" path="birth_date">
              <n-date-picker 
                v-model:value="formData.birth_date"
                type="date"
                clearable
                style="width: 100%"
                placeholder="DD/MM/AAAA"
                :format="dateFormat"
                :value-format="dateValueFormat"
                :actions="datePickerActions"
                @update:value="onDateChange"
              />
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- Dados dos Animais -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">Dados dos Animais</span>
        </n-divider>

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Quantidade de Cães" path="qtd_dogs">
              <n-input-number 
                v-model:value="formData.qtd_dogs"
                clearable
                :min="0"
                style="width: 100%"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Cães Castrados" path="qtd_castred_dogs">
              <n-input-number 
                v-model:value="formData.qtd_castred_dogs"
                clearable
                :min="0"
                style="width: 100%"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Quantidade de Gatos" path="qtd_cats">
              <n-input-number 
                v-model:value="formData.qtd_cats"
                clearable
                :min="0"
                style="width: 100%"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Gatos Castrados" path="qtd_castred_cats">
              <n-input-number 
                v-model:value="formData.qtd_castred_cats"
                clearable
                :min="0"
                style="width: 100%"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- Benefícios Sociais -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">Benefícios Sociais</span>
        </n-divider>

        <n-grid :cols="3" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Recebe BPC/LOAS" path="receives_bpc_loas">
              <n-switch v-model:value="formData.receives_bpc_loas"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- CadÚnico (Cadastro Único) -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">CadÚnico (Cadastro Único)</span>
        </n-divider>

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Código Familiar" path="cadunico_code">
              <n-input 
                v-model:value="formData.cadunico_code" 
                clearable 
                style="width: 100%" 
                placeholder="Ex: 123456789"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Faixa de Renda" path="income_range">
              <n-select
                v-model:value="formData.income_range"
                :options="incomeRangeOptions"
                clearable
                placeholder="Selecione a faixa de renda"
                style="width: 100%"/>
            </n-form-item>
          </n-grid-item>
        </n-grid>

        <!-- Informações Adicionais -->
        <n-divider title-placement="left">
          <span style="font-weight: 600; color: #f77800;">Informações Adicionais</span>
        </n-divider>

        <n-form-item label="Como Soube do Projeto" path="how_did_you_hear">
          <n-input 
            v-model:value="formData.how_did_you_hear"
            type="textarea"
            clearable
            :rows="2"
            placeholder="Ex: Redes Sociais, Amigos, etc."
            style="width: 100%"/>
        </n-form-item>

        <n-form-item label="Observações" path="observations">
          <n-input 
            v-model:value="formData.observations"
            type="textarea"
            clearable
            :rows="3"
            placeholder="Observações adicionais sobre o beneficiário"
            style="width: 100%"/>
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
import { ref, defineProps, defineEmits, watch } from 'vue'
import { 
  NModal, NForm, NFormItem, NInput, NInputNumber, 
  NButton, NGrid, NGridItem, NSwitch, NDatePicker, NDivider, NSelect, useMessage 
} from 'naive-ui'
import { beneficiaryService } from '~/services/beneficiaryService'
import type { Beneficiary } from '~/models/beneficiaryModel'

const props = defineProps<{
  modelValue: boolean
  editMode?: boolean
  beneficiaryData?: Beneficiary
}>()

console.log('🚀 BeneficiaryModal props:', props)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [formData: Beneficiary]
  'update': [id: number, formData: Partial<Beneficiary>]
}>()

const formRef = ref()
const submitting = ref(false)

// ✅ NOVO: Formatação de data
const dateFormat = 'dd/MM/yyyy'
const dateValueFormat = 'yyyy-MM-dd'

// ✅ NOVO: Configuração para fechar automaticamente após seleção
const datePickerActions = null // Remove os botões de ação padrão

// ✅ NOVO: Função para lidar com mudança de data
const onDateChange = (value: number | null) => {
  // A data já foi atualizada pelo v-model, não precisa fazer nada especial
  // O picker fechará automaticamente quando actions é null
  console.log('📅 Data selecionada:', value)
}

// ✅ NOVO: Função para converter string YYYY-MM-DD para timestamp
function dateStringToTimestamp(dateString: string): number | null {
  if (!dateString) return null
  const date = new Date(dateString + 'T00:00:00.000Z')
  return date.getTime()
}

// ✅ NOVO: Função para converter timestamp para string YYYY-MM-DD
function timestampToDateString(timestamp: number | string): string | null {
  if (!timestamp) return null
  
  let date: Date
  if (typeof timestamp === 'string') {
    // Se já é string, assumir formato YYYY-MM-DD
    return timestamp
  } else {
    // Se é timestamp, converter
    date = new Date(timestamp)
  }
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
}

const message = useMessage()

const rules = {
  name: [
    { required: true, message: 'Por favor, informe o nome do beneficiário' },
    {
      validator: (_rule, value) => {
        if (!value) return Promise.reject(new Error('Por favor, informe o nome do beneficiário'))
        return value.trim().length >= 3
          ? Promise.resolve()
          : Promise.reject(new Error('Nome deve ter ao menos 3 caracteres'))
      }
    }
  ],
  document: [
    { required: true, message: 'Por favor, informe o documento' },
    {
      validator: (_rule, value) => {
        if (!value) return Promise.reject(new Error('Por favor, informe o documento'))
        const digits = String(value).replace(/\D/g, '')
        return digits.length >= 8
          ? Promise.resolve()
          : Promise.reject(new Error('Documento inválido, informe ao menos 8 dígitos'))
      }
    }
  ],
  street: [
    { required: true, message: 'Por favor, informe a rua/avenida' },
    {
      validator: (_rule, value) => {
        if (!value) return Promise.reject(new Error('Por favor, informe a rua/avenida'))
        return value.trim().length >= 5
          ? Promise.resolve()
          : Promise.reject(new Error('Rua/Avenida deve ter ao menos 5 caracteres'))
      }
    }
  ],
  neighborhood: [
    { required: true, message: 'Por favor, informe o bairro' },
    {
      validator: (_rule, value) => {
        if (!value) return Promise.reject(new Error('Por favor, informe o bairro'))
        return value.trim().length >= 3
          ? Promise.resolve()
          : Promise.reject(new Error('Bairro deve ter ao menos 3 caracteres'))
      }
    }
  ],
  contact: [
    { required: true, message: 'Por favor, informe o contato' },
    {
      validator: (_rule, value) => {
        if (!value) return Promise.reject(new Error('Por favor, informe o contato'))
        return String(value).trim().length >= 8
          ? Promise.resolve()
          : Promise.reject(new Error('Contato deve ter ao menos 8 caracteres'))
      }
    }
  ],
  // opcional: número do endereço deve ser apenas dígitos quando preenchido
  number: [
    {
      validator: (_rule, value) => {
        if (!value) return Promise.resolve()
        return /^\d+$/.test(String(value))
          ? Promise.resolve()
          : Promise.reject(new Error('Número inválido (somente dígitos)'))
      }
    }
  ],
  // CEP opcional com formato 12345-678
  zip_code: [
    {
      validator: (_rule, value) => {
        if (!value) return Promise.resolve()
        return /^\d{5}-\d{3}$/.test(String(value))
          ? Promise.resolve()
          : Promise.reject(new Error('CEP inválido (ex: 12345-678)'))
      }
    }
  ],
  // data de nascimento opcional, valida formato/timestamp
  birth_date: [
    {
      validator: (_rule, value) => {
        if (!value) return Promise.resolve()
        const date = typeof value === 'number' ? new Date(value) : new Date(String(value))
        return isNaN(date.getTime())
          ? Promise.reject(new Error('Data de nascimento inválida'))
          : Promise.resolve()
      }
    }
  ],
  // quantidades de animais: inteiros >= 0
  qtd_dogs: [
    {
      validator: (_rule, value) => {
        if (value === null || value === undefined || value === '') return Promise.resolve()
        const n = Number(value)
        return Number.isInteger(n) && n >= 0
          ? Promise.resolve()
          : Promise.reject(new Error('Informe um número inteiro >= 0'))
      }
    }
  ],
  qtd_castred_dogs: [
    {
      validator: (_rule, value) => {
        if (value === null || value === undefined || value === '') return Promise.resolve()
        const n = Number(value)
        return Number.isInteger(n) && n >= 0
          ? Promise.resolve()
          : Promise.reject(new Error('Informe um número inteiro >= 0'))
      }
    }
  ],
  qtd_cats: [
    {
      validator: (_rule, value) => {
        if (value === null || value === undefined || value === '') return Promise.resolve()
        const n = Number(value)
        return Number.isInteger(n) && n >= 0
          ? Promise.resolve()
          : Promise.reject(new Error('Informe um número inteiro >= 0'))
      }
    }
  ],
  qtd_castred_cats: [
    {
      validator: (_rule, value) => {
        if (value === null || value === undefined || value === '') return Promise.resolve()
        const n = Number(value)
        return Number.isInteger(n) && n >= 0
          ? Promise.resolve()
          : Promise.reject(new Error('Informe um número inteiro >= 0'))
      }
    }
  ]
}

// ✅ ATUALIZADO: FormData com data como timestamp para o date-picker
const formData = ref({
  name: '',
  document: '',
  
  // ✅ ENDEREÇO ESTRUTURADO
  street: '',
  number: '',
  neighborhood: '',
  city: 'Pindamonhangaba',
  state: 'SP',
  zip_code: '',
  complement: '',
  
  contact: '',
  mother_name: '',
  birth_date: null as number | null, // ✅ timestamp para o date-picker
  qtd_dogs: 0,
  qtd_castred_dogs: 0,
  qtd_cats: 0,
  qtd_castred_cats: 0,
  government_benefit: false,
  receives_basic_basket: false,
  receives_bpc_loas: false,
  cadunico_code: '',
  income_range: '',
  how_did_you_hear: '',
  observations: ''
})

const stateOptions = [
  { label: 'São Paulo', value: 'SP' },
  { label: 'Rio de Janeiro', value: 'RJ' },
  { label: 'Minas Gerais', value: 'MG' },
  { label: 'Espírito Santo', value: 'ES' },
]

const incomeRangeOptions = [
  { label: 'Até meio salário mínimo', value: 'Até meio salário mínimo' },
  { label: 'Entre meio e um salário mínimo', value: 'Entre meio e um salário mínimo' },
  { label: 'Acima de meio salário mínimo', value: 'Acima de meio salário mínimo' },
  { label: 'Acima de um salário mínimo', value: 'Acima de um salário mínimo' },
]

// ✅ ATUALIZADO: Watch para nova estrutura de data
watch(() => props.beneficiaryData, (newValue) => {
  if (newValue && props.editMode) {
    formData.value = {
      name: newValue.name,
      document: newValue.document,
      
      // ✅ ENDEREÇO ESTRUTURADO
      street: newValue.street || '',
      number: newValue.number || '',
      neighborhood: newValue.neighborhood || '',
      city: newValue.city || 'Pindamonhangaba',
      state: newValue.state || 'SP',
      zip_code: newValue.zip_code || '',
      complement: newValue.complement || '',
      
      contact: newValue.contact,
      mother_name: newValue.mother_name || '',
      // ✅ NOVO: Converter data para timestamp se necessário
      birth_date: newValue.birth_date ? (
        typeof newValue.birth_date === 'number' 
          ? newValue.birth_date 
          : dateStringToTimestamp(newValue.birth_date)
      ) : null,
      qtd_dogs: newValue.qtd_dogs || 0,
      qtd_castred_dogs: newValue.qtd_castred_dogs || 0,
      qtd_cats: newValue.qtd_cats || 0,
      qtd_castred_cats: newValue.qtd_castred_cats || 0,
      government_benefit: newValue.government_benefit || false,
      receives_basic_basket: newValue.receives_basic_basket || false,
      receives_bpc_loas: newValue.receives_bpc_loas || false,
      cadunico_code: newValue.cadunico_code || '',
      income_range: newValue.income_range || '',
      how_did_you_hear: newValue.how_did_you_hear || '',
      observations: newValue.observations || ''
    }
  }
}, { immediate: true })

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true

    // ✅ NOVO: Preparar dados com data formatada
    const beneficiaryData = {
      ...formData.value,
      // ✅ NOVO: Converter timestamp para string YYYY-MM-DD para o backend
      birth_date: formData.value.birth_date ? timestampToDateString(formData.value.birth_date) : null,
      qtd_dogs: formData.value.qtd_dogs || 0,
      qtd_castred_dogs: formData.value.qtd_castred_dogs || 0,
      qtd_cats: formData.value.qtd_cats || 0,
      qtd_castred_cats: formData.value.qtd_castred_cats || 0,
      government_benefit: formData.value.government_benefit || false,
      receives_basic_basket: formData.value.receives_basic_basket || false,
      receives_bpc_loas: formData.value.receives_bpc_loas || false
    }

    console.log('📅 Data formatada para envio:', beneficiaryData.birth_date)

    if (props.editMode && props.beneficiaryData) {
      const loadingMsg = message.loading({
        content: 'Atualizando beneficiário...',
        duration: 5000,
        closable: true
      })
      
      const updatedBeneficiary = await beneficiaryService.update(
        props.beneficiaryData.id,
        beneficiaryData
      )
      
      loadingMsg.destroy()
      message.success(`Beneficiário ${updatedBeneficiary.name} atualizado com sucesso!`)
      emit('update', props.beneficiaryData.id, updatedBeneficiary)
    } else {
      const loadingMsg = message.loading('Cadastrando novo beneficiário...', {
        duration: 5000
      })
      
      const newBeneficiary = await beneficiaryService.create(beneficiaryData)
      
      loadingMsg.destroy()
      message.success(`Beneficiário ${newBeneficiary.name} cadastrado com sucesso!`)
      emit('submit', newBeneficiary)
    }

    setTimeout(() => {
      emit('update:modelValue', false)
      resetForm()
    }, 500)
    
  } catch (error) {
    console.error('Erro detalhado:', error)
    
    if (error instanceof Error) {
      message.error({
        content: error.message,
        duration: 5000,
        closable: true
      })
    } else {
      const actionType = props.editMode ? 'atualizar' : 'cadastrar'
      message.error({
        content: `Erro ao ${actionType} beneficiário. Tente novamente.`,
        duration: 5000,
        closable: true
      })
    }
  } finally {
    submitting.value = false
  }
}

// ✅ ATUALIZADO: Reset form
const resetForm = () => {
  formData.value = {
    name: '',
    document: '',
    
    // ✅ ENDEREÇO ESTRUTURADO
    street: '',
    number: '',
    neighborhood: '',
    city: 'Pindamonhangaba',
    state: 'SP',
    zip_code: '',
    complement: '',
    
    contact: '',
    mother_name: '',
    birth_date: null, // ✅ NOVO: null para timestamp
    qtd_dogs: 0,
    qtd_castred_dogs: 0,
    qtd_cats: 0,
    qtd_castred_cats: 0,
    government_benefit: false,
    receives_basic_basket: false,
    receives_bpc_loas: false,
    cadunico_code: '',
    income_range: '',
    how_did_you_hear: '',
    observations: ''
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
  max-height: 70vh;
  overflow-y: auto;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* ✅ NOVO: Estilo para os divisores */
:deep(.n-divider .n-divider__title) {
  font-size: 0.95rem;
}
</style>