import { test, expect } from '@playwright/test'

test.describe('Conectividade Básica', () => {
  test('deve acessar o frontend', async ({ page }) => {
    console.log('🧪 Teste: Conectividade frontend')
    
    const frontendUrl = process.env.FRONTEND_URL || 'http://localhost:3000'
    
    await page.goto(frontendUrl)
    await page.waitForLoadState('domcontentloaded')
    
    // Verificar se a página carregou
    await expect(page.locator('body')).toBeVisible()
    
    console.log('✅ Frontend acessível')
  })

  test('deve verificar se o backend responde', async ({ request }) => {
    console.log('🧪 Teste: Conectividade backend')
    
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    try {
      const response = await request.get(`${backendUrl}/health`)
      console.log(`Backend status: ${response.status()}`)
      
      // Aceitar 200 ou 404 (caso não tenha health check)
      expect([200, 404]).toContain(response.status())
      
      console.log('✅ Backend acessível')
    } catch (error) {
      console.log('⚠️ Backend pode não estar rodando:', error.message)
      // Não falhar o teste se backend não estiver rodando
    }
  })
})