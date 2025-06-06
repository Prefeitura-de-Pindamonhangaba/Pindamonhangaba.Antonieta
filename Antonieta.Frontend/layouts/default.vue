<template>
  <n-layout has-sider>
    <n-layout-sider
      v-if="!isLoginPage"
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      :collapsed="collapsed"
      show-trigger
      @collapse="collapsed = true"
      @expand="collapsed = false"
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
    <n-layout-content :style="contentStyle">
      <slot />
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import { h, ref, onMounted } from 'vue'
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
  BarChartOutlined // Add this import
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

const contentStyle = computed(() => ({
  padding: isLoginPage.value ? '0' : '20px'
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
  height: v-bind(collapsed ? '50px' : '120px');
  width: auto;
  transition: all 0.3s ease;
}

.menu-container {
  height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.footer-menu {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

:deep(.n-layout-sider) {
  background-color: #ffffff;
}

:deep(.n-menu) {
  background-color: transparent;
}

:deep(.n-menu-item) {
  color: #263238;
}

:deep(.n-menu-item:hover) {
  color: #f77800;
}

:deep(.n-menu-item--selected) {
  color: #f77800;
  background-color: #fff8e1;
}

:deep(.footer-menu .n-menu-item) {
  margin-bottom: 0;
}
</style>