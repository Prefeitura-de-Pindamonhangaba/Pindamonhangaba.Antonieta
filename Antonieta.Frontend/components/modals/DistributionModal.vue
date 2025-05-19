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
      <n-form-item label="Beneficiário" path="beneficiario">
        <n-select
          v-model:value="formData.beneficiario"
          :options="beneficiaryOptions"
          placeholder="Selecione o beneficiário"
          clearable
        />
      </n-form-item>

      <n-form-item label="Quantidade (kg)" path="quantidade">
        <n-input-number
          v-model:value="formData.quantidade"
          :min="1"
          :precision="0"
          placeholder="Informe a quantidade em kg"
        />
      </n-form-item>

      <n-form-item label="Observações" path="observacoes">
        <n-input
          v-model:value="formData.observacoes"
          type="textarea"
          placeholder="Observações adicionais"
        />
      </n-form-item>
    </n-form>

    <template #action>
      <div style="display: flex; justify-content: flex-end; gap: 12px">
        <n-button @click="handleCancel">Cancelar</n-button>
        <n-button type="primary" :loading="loading" @click="handleSubmit">Registrar</n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInst, FormRules } from 'naive-ui'
import { NModal, NForm, NFormItem, NInput, NInputNumber, NButton, NSelect } from 'naive-ui'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', formData: any): void
}>()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)

const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const formData = ref({
  beneficiario: '',
  quantidade: null as number | null,
  observacoes: ''
})

const rules: FormRules = {
  beneficiario: {
    required: true,
    message: 'Por favor, selecione o beneficiário',
    trigger: ['blur', 'change']
  },
  quantidade: {
    required: true,
    type: 'number',
    message: 'Por favor, informe a quantidade',
    trigger: ['blur', 'change']
  }
}

// Exemplo de opções de beneficiários - deve ser substituído por dados reais
const beneficiaryOptions = [
  { label: 'João Santos', value: 'João Santos' },
  { label: 'Maria Silva', value: 'Maria Silva' },
  { label: 'Pedro Souza', value: 'Pedro Souza' }
]

const handleSubmit = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      loading.value = true
      emit('submit', formData.value)
      loading.value = false
      show.value = false
      formRef.value?.restoreValidation()
      formData.value = {
        beneficiario: '',
        quantidade: null,
        observacoes: ''
      }
    }
  })
}

const handleCancel = () => {
  show.value = false
  formRef.value?.restoreValidation()
  formData.value = {
    beneficiario: '',
    quantidade: null,
    observacoes: ''
  }
}
</script>