import { test, expect } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'

test.describe('Login - Testes E2E', () => {
  let loginPage: LoginPage

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page)
    
    // Navegar para a página de login
    await loginPage.navigateToLoginPage()
  })

  test('deve carregar a página de login corretamente', async () => {
    console.log('🧪 Teste: Carregamento da página de login')
    
    // Verificar se a página carregou
    await loginPage.verifyLoginPageLoaded()
    
    // Verificar se os elementos do formulário estão presentes
    await loginPage.verifyLoginFormElements()
    
    console.log('✅ Página de login carregada e elementos presentes')
  })

  test('deve permitir login com credenciais válidas', async () => {
    console.log('🧪 Teste: Login com credenciais válidas')
    
    // Verificar elementos primeiro
    await loginPage.verifyLoginFormElements()
    
    // Realizar login válido
    const result = await loginPage.testValidLogin()

    console.log(result)
    
    expect(result.success).toBe(true)
    expect(result.error).toBeNull()
    
    console.log('✅ Login com credenciais válidas funciona')
  })

  test('deve rejeitar login com credenciais inválidas', async () => {
    console.log('🧪 Teste: Login com credenciais inválidas')
    
    // Verificar elementos primeiro
    await loginPage.verifyLoginFormElements()
    
    // Realizar login inválido
    const result = await loginPage.testInvalidLogin()
    
    expect(result.success).toBe(false)
    expect(result.error).toBeTruthy()
    
    console.log('✅ Login com credenciais inválidas falha corretamente')
  })

  test('deve validar campos obrigatórios', async () => {
    console.log('🧪 Teste: Validação de campos obrigatórios')
    
    // Tentar fazer login sem preencher nada
    await loginPage.clickLoginButton()
    
    // Verificar se permanece na página de login
    const currentUrl = loginPage.page.url()
    expect(currentUrl).toContain('/login')
    
    console.log('✅ Validação de campos obrigatórios funciona')
  })

  test('deve preencher e limpar campos corretamente', async () => {
    console.log('🧪 Teste: Preenchimento e limpeza de campos')
    
    // Preencher campos
    await loginPage.fillLoginForm('test@example.com', 'testpassword')
    
    // Verificar se os campos foram preenchidos
    const emailValue = await loginPage.page.inputValue('input[type="email"], input[name="email"]')
    const passwordValue = await loginPage.page.inputValue('input[type="password"], input[name="password"]')
    
    expect(emailValue).toBe('test@example.com')
    expect(passwordValue).toBe('testpassword')
    
    console.log('✅ Campos preenchidos corretamente')
    
    // Limpar campos
    await loginPage.page.fill('input[type="email"], input[name="email"]', '')
    await loginPage.page.fill('input[type="password"], input[name="password"]', '')
    
    // Verificar se os campos foram limpos
    const clearedEmailValue = await loginPage.page.inputValue('input[type="email"], input[name="email"]')
    const clearedPasswordValue = await loginPage.page.inputValue('input[type="password"], input[name="password"]')
    
    expect(clearedEmailValue).toBe('')
    expect(clearedPasswordValue).toBe('')
    
    console.log('✅ Campos limpos corretamente')
  })
})