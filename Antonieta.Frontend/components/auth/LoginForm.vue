<template>
  <div class="login-container">
    <n-space vertical align="center" justify="center" style="min-height: 100vh; width: 100%">
      <n-space vertical align="center" :size="24">
        <n-space justify="center">
          <img
            src="/assets/logo_projeto_antonieta.svg"
            alt="Logo Projeto Antonieta"
            width="200px"
          />
        </n-space>
        <n-card
          class="login-card"
          :bordered="true"
          :shadow="false"
        >
          <n-form 
            ref="formRef" 
            :model="formValue" 
            :rules="rules"
            @keydown.enter.prevent="handleSubmit"
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
              <!-- TODO - Implementar esqueceu a senha -->
              <!-- <n-checkbox v-model:checked="rememberMe"> Lembrar-me </n-checkbox> -->
              <!-- <n-button text> Esqueceu a senha? </n-button> -->
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
      </n-space>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useMessage } from "naive-ui";
import { MailOutline, LockClosedOutline } from "@vicons/ionicons5";
import { authService } from "~/services/authService";
import { useAuth } from "~/composables/useAuth";

const formRef = ref(null);
const loading = ref(false);
const router = useRouter();
const message = useMessage();
const { setUser, setToken } = useAuth();

const formValue = ref({
  email: "",
  password: "",
});

const rules = {
  email: [
    {
      required: true,
      message: "Por favor, digite seu e-mail",
      trigger: "blur",
    },
    {
      type: "email",
      message: "Por favor, digite um e-mail válido",
      trigger: "blur",
    },
  ],
  password: [
    { required: true, message: "Por favor, digite sua senha", trigger: "blur" },
    {
      min: 6,
      message: "A senha deve ter no mínimo 6 caracteres",
      trigger: "blur",
    },
  ],
};

const handleSubmit = async () => {
  try {
    if (!formRef.value) return;
    await formRef.value.validate();

    loading.value = true;
    const { access_token, user } = await authService.login(
      formValue.value.email,
      formValue.value.password
    );

    // Atualizar o estado global do useAuth
    setToken(access_token);
    setUser(user);
    
    message.success("Login realizado com sucesso!");
    await router.push({
      path: "/dashboard",
      query: { loading: "true" }
    });
  } catch (error) {
    message.error(
      error instanceof Error ? error.message : "Erro ao fazer login"
    );
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  background-color: var(--background-light);
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
