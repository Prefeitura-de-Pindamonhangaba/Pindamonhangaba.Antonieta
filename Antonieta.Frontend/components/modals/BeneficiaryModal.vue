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

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Contato" path="contact">
              <n-input 
                v-model:value="formData.contact" 
                clearable 
                style="width: 100%" 
                placeholder="Telefone ou e-mail"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Limite Mensal (kg)" path="monthly_limit">
              <n-input-number 
                v-model:value="formData.monthly_limit" 
                clearable 
                style="width: 100%" 
                placeholder="Limite mensal em kg"
                :precision="2"
                :step="0.1"
                :min="0"
              />
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
                style="width: 100%"/>
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

        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <n-form-item label="Recebe Benefício do Governo" path="government_benefit">
              <n-switch v-model:value="formData.government_benefit"/>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="Recebe Cesta Básica" path="receives_basic_basket">
              <n-switch v-model:value="formData.receives_basic_basket"/>
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

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [formData: Beneficiary]
  'update': [id: number, formData: Partial<Beneficiary>]
}>()

const formRef = ref()
const submitting = ref(false)

// ✅ NOVO: FormData com campos de endereço estruturados
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
  monthly_limit: 4.5,
  mother_name: '',
  birth_date: '2025-01-01',
  qtd_dogs: 0,
  qtd_castred_dogs: 0,
  qtd_cats: 0,
  qtd_castred_cats: 0,
  government_benefit: false,
  receives_basic_basket: false,
  how_did_you_hear: '',
  observations: ''
})

// ✅ NOVO: Opções de estados
const stateOptions = [
  { label: 'São Paulo', value: 'SP' },
  { label: 'Rio de Janeiro', value: 'RJ' },
  { label: 'Minas Gerais', value: 'MG' },
  { label: 'Espírito Santo', value: 'ES' },
  // Adicione outros estados conforme necessário
]

function timestamp_to_date(timestamp: number): string {
  const data = new Date(timestamp);
  data.setUTCDate(data.getUTCDate() + 1);
  const ano = data.getUTCFullYear();
  const mes = (data.getUTCMonth() + 1).toString().padStart(2, '0');
  const dia = data.getUTCDate().toString().padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

const message = useMessage()

// ✅ ATUALIZADO: Rules para nova estrutura
const rules = {
  name: {
    required: true,
    message: 'Por favor, informe o nome do beneficiário'
  },
  document: {
    required: true,
    message: 'Por favor, informe o documento'
  },
  street: {
    required: true,
    message: 'Por favor, informe a rua/avenida'
  },
  neighborhood: {
    required: true,
    message: 'Por favor, informe o bairro'
  },
  contact: {
    required: true,
    message: 'Por favor, informe o contato'
  },
  monthly_limit: {
    required: true,
    message: 'Por favor, informe o limite mensal'
  }
}

// ✅ ATUALIZADO: Watch para nova estrutura
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
      monthly_limit: newValue.monthly_limit,
      mother_name: newValue.mother_name,
      birth_date: timestamp_to_date(newValue.birth_date),
      qtd_dogs: newValue.qtd_dogs,
      qtd_castred_dogs: newValue.qtd_castred_dogs,
      qtd_cats: newValue.qtd_cats,
      qtd_castred_cats: newValue.qtd_castred_cats,
      government_benefit: newValue.government_benefit,
      receives_basic_basket: newValue.receives_basic_basket,
      how_did_you_hear: newValue.how_did_you_hear,
      observations: newValue.observations
    }
  }
}, { immediate: true })

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true

    // ✅ REMOVIDO: address (agora usa campos estruturados)
    const beneficiaryData = {
      ...formData.value,
      monthly_limit: formData.value.monthly_limit || 0,
      qtd_dogs: formData.value.qtd_dogs || 0,
      qtd_castred_dogs: formData.value.qtd_castred_dogs || 0,
      qtd_cats: formData.value.qtd_cats || 0,
      qtd_castred_cats: formData.value.qtd_castred_cats || 0,
      government_benefit: formData.value.government_benefit || false,
      receives_basic_basket: formData.value.receives_basic_basket || false
    }

    if (props.editMode && props.beneficiaryData) {
      const loadingMsg = message.loading('Atualizando beneficiário...', {
        duration: 0
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
        duration: 0
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

// ✅ ATUALIZADO: Reset form para nova estrutura
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
    monthly_limit: null,
    mother_name: null,
    birth_date: null,
    qtd_dogs: 0,
    qtd_castred_dogs: 0,
    qtd_cats: 0,
    qtd_castred_cats: 0,
    government_benefit: false,
    receives_basic_basket: false,
    how_did_you_hear: null,
    observations: null
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