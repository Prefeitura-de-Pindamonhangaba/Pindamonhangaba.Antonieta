<!-- filepath: c:\Users\almoreira\Documents\Projetos\Pindamonhangaba.Antonieta\Antonieta.Frontend\components\AppButton.vue -->
<template>
  <n-button
    :type="type"
    :class="['app-button', type]"
    :loading="loading"
    :disabled="disabled"
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
  disabled: Boolean
})

defineEmits(['click'])
</script>

<style scoped>
.app-button {
  font-size: 14px;
  padding: 12px 24px;
}
.app-button.primary {
  background-color: var(--primary-color);
  color: var(--primary-text);
}
</style>