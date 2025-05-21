<template>
  <div class="login-container">
    <div class="logo-container">
      <img src="/assets/logo_projeto_antonieta.svg" alt="Logo Projeto Antonieta" class="logo" />
    </div>
    <n-card class="login-card" title="Bem-vindo">
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
      >
        <n-form-item path="email" label="E-mail">
          <n-input
            v-model:value="formValue.email"
            placeholder="Digite seu e-mail"
            type="email"
          >
            <template #prefix>
              <n-icon><mail-outline /></n-icon>
            </template>
          </n-input>
        </n-form-item>

        <n-form-item path="password" label="Senha">
          <n-input
            v-model:value="formValue.password"
            type="password"
            placeholder="Digite sua senha"
            show-password-on="click"
          >
            <template #prefix>
              <n-icon><lock-closed-outline /></n-icon>
            </template>
          </n-input>
        </n-form-item>

        <div class="flex justify-between items-center">
          <n-checkbox v-model:checked="rememberMe">
            Lembrar-me
          </n-checkbox>
          <n-button text>
            Esqueceu a senha?
          </n-button>
        </div>

        <n-button
          class=""
          type="primary"
          block
          @click="handleSubmit"
          :loading="loading"
        >
          Entrar
        </n-button>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { MailOutline, LockClosedOutline } from '@vicons/ionicons5'

const formRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)
const router = useRouter()
const message = useMessage()

const formValue = ref({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: 'Por favor, digite seu e-mail', trigger: 'blur' },
    { type: 'email', message: 'Por favor, digite um e-mail válido', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Por favor, digite sua senha', trigger: 'blur' },
    { min: 6, message: 'A senha deve ter no mínimo 6 caracteres', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  try {
    if (!formRef.value) return
    await formRef.value.validate()
    
    loading.value = true
    const formData = new URLSearchParams()
    formData.append('username', formValue.value.email)
    formData.append('password', formValue.value.password)
    formData.append('grant_type', 'password')

    const response = await fetch('http://localhost:8000/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Erro ao fazer login')
    }

    const data = await response.json()
    localStorage.setItem('access_token', data.access_token)
    
    message.success('Login realizado com sucesso!')
    router.push('/dashboard')
  } catch (error) {
    message.error(error instanceof Error ? error.message : 'Erro ao fazer login')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff8e1;
}

.logo-container {
  margin-bottom: 2rem;
}

.logo {
  width: 300px;
  height: auto;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 20px;
  background-color: #ffffff;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.n-form {
  margin-top: 20px;
}

:deep(.n-button--primary-type) {
  background-color: #f77800 !important;
}

:deep(.n-button--primary-type:hover) {
  background-color: #e56f00 !important;
}

:deep(.n-button--primary-type:active) {
  background-color: #d36600 !important;
}

:deep(.n-card-header__title) {
  color: #263238;
  font-size: 1.5rem;
  font-weight: 600;
}
</style>