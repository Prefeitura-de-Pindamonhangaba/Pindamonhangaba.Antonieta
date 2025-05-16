<template>
  <n-config-provider>
    <n-message-provider>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { darkTheme, NConfigProvider, NMessageProvider } from 'naive-ui'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Montserrat', sans-serif;
}
</style>
