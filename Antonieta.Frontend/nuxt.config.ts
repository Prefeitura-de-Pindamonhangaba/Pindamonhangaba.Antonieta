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
  },

  app: {
    head: {
      title: 'Gerenciamento de Rações - Projeto Antonieta',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Sistema de controle de distribuição de ração do Projeto Antonieta - Prefeitura de Pindamonhangaba' }
      ],
       link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.ico'
        }
      ]
    }
  },
})