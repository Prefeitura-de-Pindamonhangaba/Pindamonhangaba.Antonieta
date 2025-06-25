<template>
  <n-space justify="end">
    <n-button
      quaternary
      class="edit-button"
      @click="$emit('edit')"
    >
      <template #icon>
        <n-icon><IconEdit /></n-icon>
      </template>
    </n-button>
    <n-button
      quaternary
      type="error"
      @click="$emit('delete')"
    >
      <template #icon>
        <n-icon><IconTrash /></n-icon>
      </template>
    </n-button>
  </n-space>
</template>

<script setup>
import { NSpace, NButton, NIcon } from 'naive-ui'
import { IconEdit, IconTrash } from '@tabler/icons-vue'

defineEmits(['edit', 'delete'])
</script>

<style scoped>
.n-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
}

.edit-button {
  color: var(--primary-color);
}

/* Estilos para hover */
.edit-button:hover {
  color: var(--primary-color-hover);
}
</style>