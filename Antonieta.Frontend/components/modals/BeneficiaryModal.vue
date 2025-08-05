<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 800px">
    <template #header>
      <div class="modal-header">
        <h3>{{ props.editMode ? 'Editar Beneficiário' : 'Cadastrar Novo Beneficiário' }}</h3>
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
            :precision="2"
            :step="0.1"
            :min="0"
          />
        </n-form-item>

        <n-form-item label="Nome da Mãe" path="mother_name">
          <n-input 
            v-model:value="formData.mother_name" 
            clearable 
            style="width: 100%" 
            placeholder="Nome da mãe do beneficiário"/>
        </n-form-item>

        <n-form-item label="Data de Nascimento" path="birth_date">
          <n-date-picker 
            v-model:value="formData.birth_date"
            type="date"
            clearable
            style="width: 100%"/>
        </n-form-item>

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

        <n-form-item label="Como Soube do Projeto" path="how_did_you_hear">
          <n-input 
            v-model:value="formData.how_did_you_hear"
            type="textarea"
            clearable
            style="width: 100%"/>
        </n-form-item>

        <n-form-item label="Observações" path="observations">
          <n-input 
            v-model:value="formData.observations"
            type="textarea"
            clearable
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
  NButton, NGrid, NGridItem, NSwitch, NDatePicker, useMessage 
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
const formData = ref({
  name: '',
  document: '',
  address: '',
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

function timestamp_to_date(timestamp: number): string {
  const data = new Date(timestamp);

  // Adiciona 1 dia ao timestamp
  data.setUTCDate(data.getUTCDate() + 1); // Incrementa o dia UTC

  const ano = data.getUTCFullYear();
  const mes = (data.getUTCMonth() + 1).toString().padStart(2, '0');
  const dia = data.getUTCDate().toString().padStart(2, '0'); // Altere de padStart(1, '0') para padStart(2, '0') para dias como '01'

  return `${ano}-${mes}-${dia}`;
}

const message = useMessage()

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
  monthly_limit: {
    required: true,
    message: 'Por favor, informe o limite mensal'
  }
}

watch(() => props.beneficiaryData, (newValue) => {
  if (newValue && props.editMode) {
    formData.value = {
      name: newValue.name,
      document: newValue.document,
      address: newValue.address,
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
      // Mostra mensagem "Atualizando..."
      const loadingMsg = message.loading('Atualizando beneficiário...', {
        duration: 0 // Não fecha automaticamente
      })
      
      const updatedBeneficiary = await beneficiaryService.update(
        props.beneficiaryData.id,
        beneficiaryData
      )
      
      // Fecha a mensagem de loading
      loadingMsg.destroy()
      
      // Mostra sucesso com detalhes
      message.success(`Beneficiário ${updatedBeneficiary.name} atualizado com sucesso!`)
      emit('update', props.beneficiaryData.id, updatedBeneficiary)
    } else {
      // Mostra mensagem "Cadastrando..."
      const loadingMsg = message.loading('Cadastrando novo beneficiário...', {
        duration: 0 // Não fecha automaticamente
      })
      
      const newBeneficiary = await beneficiaryService.create(beneficiaryData)
      
      // Fecha a mensagem de loading
      loadingMsg.destroy()
      
      // Mostra sucesso com detalhes
      message.success(`Beneficiário ${newBeneficiary.name} cadastrado com sucesso!`)
      emit('submit', newBeneficiary)
    }

    // Adicione feedback sonoro (opcional)
    const audio = new Audio('/sounds/success.mp3')  // Se você tiver um arquivo de som
    audio.play().catch(() => {}) // Ignora erros se o navegador bloquear

    // Fecha o modal com um pequeno atraso para que o usuário veja a confirmação
    setTimeout(() => {
      emit('update:modelValue', false)
      resetForm()
    }, 500)
    
  } catch (error) {
    console.error('Erro detalhado:', error)
    
    // Feedback de erro mais detalhado
    if (error instanceof Error) {
      message.error({
        content: error.message,
        duration: 5000, // 5 segundos
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

const resetForm = () => {
  formData.value = {
    name: '',
    document: '',
    address: '',
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
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>