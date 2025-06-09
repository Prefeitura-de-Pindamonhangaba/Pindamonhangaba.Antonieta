<template>
  <div>
    <auth-login-form />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const router = useRouter()
const { checkAuth } = useAuth()

onMounted(() => {
  if (checkAuth()) {
    router.push('/dashboard')
  }
})
</script>