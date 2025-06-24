<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { NConfigProvider, NMessageProvider } from 'naive-ui'

const themeOverrides = {
    common: {
      primaryColor: '#f77800',
      primaryColorHover: "#d46700",
      primaryColorPressed: "#f77800", 
      fontFamily: "'Montserrat', sans-serif",
    },
  }
</script>

<style>

:root {
  --primary-color: #f77800;
  --primary-text: white;
  --success-color: #18a058;
  --warning-color: #f0a020;
  --error-color: #d03050;
  --background-light: #f5f5f5;
  --text-dark: #263238;
  --divider-color: #f77800;
}

html, body {
  margin: 0;
  padding: 0;
}

/* Estilos globais para aplicar a todos os cards */
.page-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Estilo para cabeçalhos de página */
.page-header {
  margin-bottom: 24px;
}
.page-header h1 {
  color: var(--primary-color);
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}
.page-header .divider {
  width: 100px; 
  margin: 8px 0 0 0; 
  background-color: var(--divider-color);
  height: 3px;
}

/* Reset e base */
* {
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  margin: 0;
  padding: 0;
  color: var(--text-dark);
  background-color: var(--background-light);
}

/* Espaçamento consistente */
.section-spacing {
  margin-bottom: 24px;
}

.card-content {
  padding: 16px;
}

/* Estilos para tabelas */
.data-table-container {
  overflow-x: auto;
  border-radius: 8px;
}

/* Estilos para formulários */
.form-item {
  margin-bottom: 16px;
}

/* Estilos para modais */
.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.modal-content {
  padding: 24px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Status e tags */
.status-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.success {
  background-color: var(--success-color);
  color: white;
}

.status-tag.warning {
  background-color: var(--warning-color);
  color: white;
}

.status-tag.error {
  background-color: var(--error-color);
  color: white;
}
</style>
