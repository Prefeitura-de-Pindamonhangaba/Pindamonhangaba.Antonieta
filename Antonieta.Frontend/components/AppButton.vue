<!-- filepath: c:\Users\almoreira\Documents\Projetos\Pindamonhangaba.Antonieta\Antonieta.Frontend\components\AppButton.vue -->
<template>
  <n-button
    :type="type"
    :class="['app-button', type]"
    :loading="loading"
    :disabled="disabled"
    :size="size"
    :quaternary="quaternary"
    @click="$emit('click', $event)"
  >
    <template v-if="$slots.icon" #icon>
      <slot name="icon"></slot>
    </template>
    <slot></slot>
  </n-button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'default'
  },
  loading: Boolean,
  disabled: Boolean,
  size: {
    type: String,
    default: 'medium'
  },
  quaternary: Boolean
})

defineEmits(['click'])
</script>

<style scoped>
.app-button {
  font-size: 14px;
  padding: 12px 24px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease;
}

.app-button.primary {
  background-color: var(--primary-color);
  color: var(--primary-text);
}

.app-button.primary:hover {
  background-color: var(--primary-color-hover, #e66e00);
}

.app-button.info {
  background-color: var(--info-color, #2080f0);
}

.app-button.info:hover {
  background-color: var(--info-color-hover, #1060c9);
}

.app-button.success {
  background-color: var(--success-color);
}

.app-button.success:hover {
  background-color: var(--success-color-hover, #0c7a43);
}

.app-button.warning {
  background-color: var(--warning-color);
}

.app-button.warning:hover {
  background-color: var(--warning-color-hover, #d28a18);
}

.app-button.error {
  background-color: var(--error-color);
}

.app-button.error:hover {
  background-color: var(--error-color-hover, #ba2440);
}
</style>