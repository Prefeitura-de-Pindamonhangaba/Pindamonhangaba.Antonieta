// https://nuxt.com/docs/api/configuration/nuxt-config
import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@bg-dev/nuxt-naiveui'],
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