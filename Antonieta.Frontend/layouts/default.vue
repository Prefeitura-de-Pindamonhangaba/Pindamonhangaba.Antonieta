<template>
  <n-layout has-sider>
    <n-layout-sider
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
      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
      />
    </n-layout-sider>
    <n-layout-content>
      <slot />
    </n-layout-content>
  </n-layout>
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import type { Component } from 'vue'
import type { MenuOption } from 'naive-ui'
import { NLayout, NLayoutSider, NLayoutContent, NMenu, NIcon } from 'naive-ui'
import {
  DashboardOutlined,
  SettingOutlined,
  UserOutlined,
  HistoryOutlined
} from '@ant-design/icons-vue'

const collapsed = ref(false)

const menuOptions: MenuOption[] = [
  {
    label: 'Dashboard',
    key: 'dashboard',
    icon: renderIcon(DashboardOutlined),
    path: '/dashboard'
  },
  {
    label: 'Beneficiários',
    key: 'beneficiarios',
    icon: renderIcon(UserOutlined),
    path: '/beneficiarios'
  },
  {
    label: 'Histórico',
    key: 'historico',
    icon: renderIcon(HistoryOutlined),
    path: '/historico'
  },
  {
    label: 'Configurações',
    key: 'configuracoes',
    icon: renderIcon(SettingOutlined),
    path: '/configuracoes'
  }
]

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
</script>

<style scoped>
.logo-container {
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.logo {
  height: 40px;
  width: auto;
  transition: all 0.3s ease;
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
</style>