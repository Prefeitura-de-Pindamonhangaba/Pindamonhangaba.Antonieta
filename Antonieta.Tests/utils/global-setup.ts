import { chromium, FullConfig } from '@playwright/test'
import { config } from 'dotenv'

config() // Carregar variáveis de ambiente

async function globalSetup(config: FullConfig) {
  console.log('🚀 Iniciando setup global dos testes E2E...')
  
  const frontendUrl = process.env.FRONTEND_URL || 'http://localhost:3000'
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
  
  console.log(`📱 Frontend: ${frontendUrl}`)
  console.log(`🔗 Backend: ${backendUrl}`)
  
  // Verificar se as aplicações estão rodando
  const browser = await chromium.launch()
  const page = await browser.newPage()
  
  try {
    // Testar frontend
    console.log('🔍 Verificando frontend...')
    await page.goto(frontendUrl, { timeout: 30000 })
    console.log('✅ Frontend está rodando')
    
    // Testar backend - vamos tentar diferentes endpoints
    console.log('🔍 Verificando backend...')
    
    try {
      // Primeiro, tentar endpoint health
      const healthResponse = await page.request.get(`${backendUrl}/health`)
      if (healthResponse.ok()) {
        console.log('✅ Backend está rodando (health endpoint)')
      } else {
        // Se não tem health, tentar endpoint docs
        const docsResponse = await page.request.get(`${backendUrl}/docs`)
        if (docsResponse.ok()) {
          console.log('✅ Backend está rodando (docs endpoint)')
        } else {
          // Se não tem docs, tentar root
          const rootResponse = await page.request.get(`${backendUrl}/`)
          if (rootResponse.status() < 500) {
            console.log('✅ Backend está rodando (root endpoint)')
          } else {
            throw new Error(`Backend não está acessível. Status: ${rootResponse.status()}`)
          }
        }
      }
    } catch (requestError) {
      console.log('⚠️ Não foi possível verificar backend automaticamente')
      console.log('⚠️ Certifique-se que o backend está rodando em:', backendUrl)
      console.log('⚠️ Continuando testes apenas com frontend...')
    }
    
  } catch (error) {
    console.error('❌ Erro no setup:', error)
    throw error
  } finally {
    await browser.close()
  }
  
  console.log('✅ Setup global concluído')
}

export default globalSetup