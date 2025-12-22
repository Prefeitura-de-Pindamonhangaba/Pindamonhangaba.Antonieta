<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 600px">
    <template #header>
      <div class="modal-header">
        <h3>{{ props.editMode ? 'Editar Usuário' : 'Cadastrar Novo Usuário' }}</h3>
      </div>
    </template>
    <div class="modal-content">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-form-item label="Nome Completo" path="full_name">
          <n-input 
            v-model:value="formData.full_name" 
            clearable 
            placeholder="Digite o nome completo"/>
        </n-form-item>

        <n-form-item label="E-mail" path="email">
          <n-input 
            v-model:value="formData.email" 
            clearable 
            type="email"
            placeholder="usuario@email.com"/>
        </n-form-item>

        <n-form-item label="Nível de Acesso" path="role">
          <n-select
            v-model:value="formData.role"
            :options="roleOptions"
            placeholder="Selecione o nível de acesso"
          />
        </n-form-item>

        <n-form-item label="Senha" path="password">
          <n-input 
            v-model:value="formData.password" 
            clearable 
            type="password"
            show-password-on="click"
            :placeholder="props.editMode ? 'Deixe em branco para manter a senha atual' : 'Digite uma senha'"/>
        </n-form-item>

        <n-form-item v-if="!props.editMode" label="Confirmar Senha" path="confirmPassword">
          <n-input 
            v-model:value="formData.confirmPassword" 
            clearable 
            type="password"
            show-password-on="click"
            placeholder="Digite a senha novamente"/>
        </n-form-item>
      </n-form>
    </div>
    <template #action>
      <n-space justify="end">
        <app-button @click="$emit('update:modelValue', false)">
          Cancelar
        </app-button>
        <app-button type="primary" @click="handleSubmit" :loading="loading">
          {{ props.editMode ? 'Atualizar' : 'Cadastrar' }}
        </app-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { NModal, NForm, NFormItem, NInput, NSelect, NSpace, useMessage, type FormInst, type FormRules } from 'naive-ui'
import User, { type UserRole } from '~/models/userModel'
import AppButton from '~/components/AppButton.vue'

const props = defineProps<{
  modelValue: boolean
  editMode?: boolean
  user?: User
}>()

const emit = defineEmits(['update:modelValue', 'submit'])
const message = useMessage()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)

const roleOptions = [
  { label: 'Comum', value: 'comum' },
  { label: 'Administrador', value: 'administrador' }
]

const formData = ref<User & { confirmPassword?: string }>({
  id: 0,
  full_name: '',
  email: '',
  role: 'comum',
  password: '',
  confirmPassword: ''
})

const rules: FormRules = {
  full_name: [
    { required: true, message: 'Nome completo é obrigatório', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'E-mail é obrigatório', trigger: 'blur' },
    { type: 'email', message: 'E-mail inválido', trigger: ['blur', 'input'] }
  ],
  role: [
    { required: true, message: 'Nível de acesso é obrigatório', trigger: 'blur' }
  ],
  password: [
    {
      required: !props.editMode,
      message: 'Senha é obrigatória',
      trigger: 'blur'
    },
    {
      validator: (_rule: any, value: string) => {
        if (value && value.length < 6) {
          return new Error('Senha deve ter no mínimo 6 caracteres')
        }
        return true
      },
      trigger: ['blur', 'input']
    }
  ],
  confirmPassword: [
    {
      validator: (_rule: any, value: string) => {
        // Só validar se houver senha preenchida
        if (formData.value.password && value !== formData.value.password) {
          return new Error('As senhas não coincidem')
        }
        return true
      },
      trigger: ['blur', 'input']
    }
  ]
}

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    if (props.editMode && props.user) {
      formData.value = {
        ...props.user,
        password: '',
        confirmPassword: ''
      }
    } else {
      formData.value = {
        id: 0,
        full_name: '',
        email: '',
        role: 'comum',
        password: '',
        confirmPassword: ''
      }
    }
  }
})

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    loading.value = true

    const userData: any = {
      full_name: formData.value.full_name,
      email: formData.value.email,
      role: formData.value.role
    }

    // Só incluir senha se foi preenchida
    if (formData.value.password) {
      userData.password = formData.value.password
    }

    emit('submit', userData)
  } catch (error) {
    console.error('Validation error:', error)
    message.error('Por favor, preencha todos os campos obrigatórios')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-header h3 {
  margin: 0;
  color: #f77800;
}

.modal-content {
  padding: 20px 0;
}
</style>
