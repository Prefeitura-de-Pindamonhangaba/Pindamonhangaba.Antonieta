<template>
  <div class="page-wrapper">
    <n-spin :show="loading" description="Carregando...">
      <slot></slot>
    </n-spin>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.page-wrapper {
  padding: 24px;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .page-wrapper {
    padding: 16px;
  }
}
</style>