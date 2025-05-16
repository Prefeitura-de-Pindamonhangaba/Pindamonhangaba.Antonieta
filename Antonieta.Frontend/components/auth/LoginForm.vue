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
import { MailOutline, LockClosedOutline } from '@vicons/ionicons5'

const formRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

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

const handleSubmit = () => {
  loading.value = true
  // Aqui será implementada a lógica de autenticação
  setTimeout(() => {
    loading.value = false
  }, 1000)
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