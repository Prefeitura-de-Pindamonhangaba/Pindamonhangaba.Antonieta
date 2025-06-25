<template>
  <template v-if="isLoginPage">
    <slot />
  </template>
  <n-layout v-else has-sider style="height: 100vh; overflow: hidden;">
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
      style="position: fixed; z-index: 100;"
    >
      <div class="logo-container">
        <img
          src="~/assets/logo_projeto_antonieta.svg"
          alt="Logo Projeto Antonieta"
          class="logo"
        />
      </div>
      <div class="menu-container">
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="mainMenuOptions"
          @update:value="handleMenuClick"
          class="main-menu"
        />
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="footerMenuOptions"
          @update:value="handleMenuClick"
          class="footer-menu"
        />
      </div>
    </n-layout-sider>
    <n-layout-content 
      :style="contentStyleComputed"
    >
      <slot />
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import { h, ref, onMounted, computed } from 'vue'
import type { Component } from 'vue'
import type { MenuOption } from 'naive-ui'
import { NLayout, NLayoutSider, NLayoutContent, NMenu, NIcon } from 'naive-ui'
import { useRouter, useRoute } from '#app'
import {
  DashboardOutlined,
  UserOutlined,
  GiftOutlined,
  InboxOutlined,
  LogoutOutlined,
  StockOutlined // Add this import
} from '@ant-design/icons-vue'
import { useAuth } from '~/composables/useAuth' // Adjust the import based on your project structure

const { checkAuth, clearToken } = useAuth()
const router = useRouter()
const route = useRoute()

const collapsed = ref(false)

const mainMenuOptions: MenuOption[] = [
  {
    label: 'Dashboard',
    key: 'dashboard',
    icon: renderIcon(DashboardOutlined),
    path: '/dashboard'
  },
  {
    label: 'Beneficiários',
    key: 'beneficiary',
    icon: renderIcon(UserOutlined),
    path: '/beneficiary'
  },
  {
    label: 'Distribuições',
    key: 'distributions',
    icon: renderIcon(GiftOutlined),
    path: '/distributions'
  },
  {
    label: 'Entradas',
    key: 'inputs',
    icon: renderIcon(InboxOutlined),
    path: '/inputs'
  },
  {
    label: 'Estoques',
    key: 'ration-stocks',
    icon: renderIcon(StockOutlined), // Changed from InboxOutlined to StockOutlined
    path: '/ration_stock'
  }
]

const footerMenuOptions: MenuOption[] = [
  {
    label: 'Sair',
    key: 'logout',
    icon: renderIcon(LogoutOutlined)
  }
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const isLoginPage = computed(() => route.path === '/login')

const contentStyleComputed = computed(() => ({
  padding: '20px',
  marginLeft: collapsed.value ? '64px' : '240px',
  transition: 'margin-left 0.3s ease',
  height: '100vh',
  overflowY: 'auto'
}))

const menuStyle = computed(() => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between'
}))

// Check authentication on layout mount
onMounted(() => {
  if (!checkAuth() && route.path !== '/login') {
    router.push('/login')
  }
})

async function handleMenuClick(key: string) {
  if (key === 'logout') {
    clearToken()
    await router.push('/login')
    return
  }

  const selectedOption = mainMenuOptions.find(option => option.key === key)
  if (selectedOption?.path) {
    router.push(selectedOption.path)
  }
}
</script>

<style scoped>
.logo-container {
  padding: v-bind(collapsed ? '0.1rem' : '1rem');
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.logo {
  height: v-bind(collapsed ? '50px' : '100px'); /* Reduzi um pouco a altura do logo */
  width: auto;
  transition: all 0.3s ease;
}

.menu-container {
  height: calc(100vh - 120px); /* Ajustado para o tamanho do logo reduzido */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.main-menu {
  flex: 1;
  overflow-y: auto; /* Permite rolagem apenas no menu principal se necessário */
  padding-bottom: 8px;
  max-height: calc(100vh - 240px); /* Garante que o menu principal não empurre o menu de rodapé para fora */
}

.footer-menu {
  flex-shrink: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding: 8px 0;
  margin-bottom: 0;
  position: sticky;
  bottom: 0;
  background-color: #ffffff; /* Garante que o fundo seja opaco */
  z-index: 10; /* Garante que fique acima do conteúdo principal */
}

:deep(.n-layout-sider) {
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  height: 100vh; /* Usa a altura total da viewport */
  position: fixed; /* Fixa o sidebar */
  left: 0;
}

:deep(.n-menu) {
  background-color: transparent;
}

:deep(.n-menu-item) {
  color: #263238;
}

:deep(.n-menu-item:hover) {
  color: var(--primary-color-hover);
}

:deep(.n-menu-item--selected) {
  color: var(--primary-color);
  background-color: #fff8e1;
}

:deep(.n-layout-sider-scroll-container) {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden; /* Impede qualquer overflow */
}

/* Ajuste para o conteúdo principal */
:deep(.n-layout) {
  height: 100vh;
  overflow: hidden; /* Impede overflow na tela principal */
}

:deep(.n-layout-content) {
  height: 100vh;
  overflow-y: auto; /* Permite rolagem apenas no conteúdo */
  margin-left: v-bind(collapsed ? '64px' : '240px'); /* Ajusta a margem baseado no estado do sidebar */
  transition: margin-left 0.3s ease;
}
</style>