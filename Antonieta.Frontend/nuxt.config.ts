export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACK_BASE_URL || 'http://localhost:8000'
    }
  },
  devServer: {
    port: Number(process.env.FRONTEND_PORT) || 5000,
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