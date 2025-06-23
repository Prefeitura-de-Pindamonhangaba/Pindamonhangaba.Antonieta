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
  NButton, NGrid, NGridItem, NSwitch, NDatePicker 
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
  monthly_limit: null as number | null,
  mother_name: null as string | null,
  birth_date: null as string | null,
  qtd_dogs: 0,
  qtd_castred_dogs: 0,
  qtd_cats: 0,
  qtd_castred_cats: 0,
  government_benefit: false,
  receives_basic_basket: false,
  how_did_you_hear: null as string | null,
  observations: null as string | null
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

watch(() => props.beneficiaryData, (newValue) => {
  if (newValue && props.editMode) {
    formData.value = {
      name: newValue.name,
      document: newValue.document,
      address: newValue.address,
      contact: newValue.contact,
      monthly_limit: newValue.monthly_limit,
      mother_name: newValue.mother_name,
      birth_date: newValue.birth_date,
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
      name: formData.value.name,
      document: formData.value.document,
      address: formData.value.address,
      contact: formData.value.contact,
      monthly_limit: formData.value.monthly_limit || 0
    }

    if (props.editMode && props.beneficiaryData) {
      const updatedBeneficiary = await beneficiaryService.update(
        props.beneficiaryData.id,
        beneficiaryData
      )
      window.$message?.success('Beneficiário atualizado com sucesso!')
      emit('update', props.beneficiaryData.id, updatedBeneficiary)
    } else {
      const newBeneficiary = await beneficiaryService.create(beneficiaryData)
      window.$message?.success('Beneficiário cadastrado com sucesso!')
      emit('submit', newBeneficiary)
    }

    emit('update:modelValue', false)
    resetForm()
  } catch (error) {
    if (error instanceof Error) {
      window.$message?.error(error.message)
    } else {
      window.$message?.error(props.editMode ? 'Erro ao atualizar beneficiário' : 'Erro ao cadastrar beneficiário')
    }
    console.error('Error:', error)
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