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
const { validateSession } = useAuth()

onMounted(async () => {
  if (await validateSession()) {
    router.push('/dashboard')
  }
})
</script>