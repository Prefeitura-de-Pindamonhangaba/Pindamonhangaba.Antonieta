<!-- filepath: c:\Users\almoreira\Documents\Projetos\Pindamonhangaba.Antonieta\Antonieta.Frontend\components\SearchField.vue -->
<template>
  <n-input
    v-model:value="inputValue"
    :placeholder="placeholder"
    clearable
    class="search-field"
    @update:value="handleInput"
  >
    <template #prefix>
      <n-icon><IconSearch /></n-icon>
    </template>
  </n-input>
</template>

<script setup>
import { ref, watch } from 'vue'
import { NInput, NIcon } from 'naive-ui'
import { IconSearch } from '@tabler/icons-vue'

const props = defineProps({
  value: String,
  placeholder: {
    type: String,
    default: 'Buscar...'
  }
})

const emit = defineEmits(['update:value', 'search'])

const inputValue = ref(props.value || '')

const handleInput = (value) => {
  emit('update:value', value)
  emit('search', value)
}

watch(() => props.value, (newValue) => {
  if (newValue !== inputValue.value) {
    inputValue.value = newValue
  }
})
</script>

<style scoped>
.search-field {
  width: 300px;
}
</style>