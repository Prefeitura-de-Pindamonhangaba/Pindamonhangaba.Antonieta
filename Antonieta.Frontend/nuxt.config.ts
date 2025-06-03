// https://nuxt.com/docs/api/configuration/nuxt-config
import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'

export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACK_BASE_URL || 'http://localhost:8000'
    }
  },
  devtools: { enabled: true },
  modules: ['@bg-dev/nuxt-naiveui'],
  ssr: false,
  naiveui: {
    themeConfig: {
      shared: {
        common: {
          primaryColor: '#f77800'
        }
      }
    }
  },
  routeRules: {
    '/': { redirect: '/login' }
  }
})