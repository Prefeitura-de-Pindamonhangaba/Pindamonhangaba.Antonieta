<template>
  <n-layout style="min-height: 100vh">
    <n-spin :show="loading" description="Carregando...">
      <n-layout-content style="padding: 24px">
        <slot />
      </n-layout-content>
    </n-spin>
  </n-layout>
</template>

<script setup lang="ts">
import { NLayout, NLayoutContent, NSpin } from 'naive-ui'

defineProps<{
  loading: boolean
}>()
</script>