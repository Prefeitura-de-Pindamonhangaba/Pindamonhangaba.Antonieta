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
html, body {
  margin: 0;
  padding: 0;
}
</style>
