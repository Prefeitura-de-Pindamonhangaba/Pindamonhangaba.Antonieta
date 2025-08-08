import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class LoginPage extends BasePage {
  private selectors = {
    // Campos do formulário
    emailInput: 'input[type="email"], input[name="email"], input[placeholder*="email" i]',
    passwordInput: 'input[type="password"], input[name="password"], input[placeholder*="senha" i]',
    loginButton: 'button[type="submit"], button:has-text("Entrar"), button:has-text("Login")',
    
    // Elementos da página
    pageTitle: 'h1, h2, .login-title',
    loginForm: 'form, .login-form',
    
    // Mensagens
    errorMessage: '.error, .alert, .message, [data-testid="error"]',
    loadingSpinner: '.loading, .spinner, [data-testid="loading"]'
  }

  /**
   * Navega para a página de login
   */
  async navigateToLoginPage() {
    console.log('🌐 Navegando para página de login...')
    await this.navigate('/login')
    await this.page.waitForLoadState('domcontentloaded')
    console.log('✅ Página de login carregada')
  }

  /**
   * Verifica se a página de login carregou corretamente
   */
  async verifyLoginPageLoaded() {
    console.log('🔍 Verificando se a página de login carregou...')
    
    // Verificar se estamos na URL correta
    const currentUrl = this.page.url()
    expect(currentUrl).toContain('/login')
    
    // Verificar se o formulário de login existe
    await this.page.waitForSelector(this.selectors.loginForm, { timeout: 10000 })
    const formVisible = await this.page.isVisible(this.selectors.loginForm)
    expect(formVisible).toBe(true)
    
    console.log('✅ Página de login carregada corretamente')
  }

  /**
   * Verifica se os elementos do formulário estão presentes
   */
  async verifyLoginFormElements() {
    console.log('🔍 Verificando elementos do formulário de login...')
    
    // Verificar campo de email
    await this.page.waitForSelector(this.selectors.emailInput, { timeout: 10000 })
    const emailVisible = await this.page.isVisible(this.selectors.emailInput)
    expect(emailVisible).toBe(true)
    console.log('✅ Campo de email presente')
    
    // Verificar campo de senha
    const passwordVisible = await this.page.isVisible(this.selectors.passwordInput)
    expect(passwordVisible).toBe(true)
    console.log('✅ Campo de senha presente')
    
    // Verificar botão de login
    const loginButtonVisible = await this.page.isVisible(this.selectors.loginButton)
    expect(loginButtonVisible).toBe(true)
    console.log('✅ Botão de login presente')
    
    console.log('✅ Todos os elementos do formulário estão presentes')
  }

  /**
   * Preenche o formulário de login
   */
  async fillLoginForm(email: string, password: string) {
    console.log('📝 Preenchendo formulário de login...')
    
    // Preencher email
    await this.page.fill(this.selectors.emailInput, email)
    console.log(`✅ Email preenchido: ${email}`)
    
    // Preencher senha
    await this.page.fill(this.selectors.passwordInput, password)
    console.log('✅ Senha preenchida')
  }

  /**
   * Clica no botão de login
   */
  async clickLoginButton() {
    console.log('🔘 Clicando no botão de login...')
    await this.page.click(this.selectors.loginButton)
    console.log('✅ Botão de login clicado')
  }

  /**
   * Verifica se ocorreu redirecionamento de forma mais robusta
   * @returns objeto com informações detalhadas do redirecionamento
   */
  async checkLoginResult(): Promise<{ redirected: boolean, currentUrl: string, onLoginPage: boolean }> {
    console.log('🔍 Verificando resultado do login...')
    
    // Aguardar um tempo para processar
    await this.page.waitForTimeout(3000)
    
    let redirected = false
    const currentUrl = this.page.url()
    
    console.log(`📍 URL atual: ${currentUrl}`)
    
    // ✅ MÚLTIPLAS VERIFICAÇÕES para detectar redirecionamento bem-sucedido
    const conditions = {
      containsDashboard: currentUrl.includes('/dashboard'),
      notLoginPage: !currentUrl.includes('/login'),
      hasLoadingParam: currentUrl.includes('loading=true'),
      isLocalhost: currentUrl.includes('localhost')
    }
    
    console.log('🔍 Condições de verificação:')
    console.log(`   - Contém 'dashboard': ${conditions.containsDashboard}`)
    console.log(`   - Não é página de login: ${conditions.notLoginPage}`)
    console.log(`   - Tem parâmetro loading: ${conditions.hasLoadingParam}`)
    console.log(`   - É localhost correto: ${conditions.isLocalhost}`)
    
    // ✅ Login bem-sucedido se contém dashboard E não é página de login
    redirected = conditions.containsDashboard && conditions.notLoginPage
    
    console.log(`🔄 Redirecionamento detectado: ${redirected}`)
    
    return {
      redirected,
      currentUrl,
      onLoginPage: currentUrl.includes('/login')
    }
  }

  /**
   * Verifica se há mensagem de erro
   */
  async verifyErrorMessage() {
    console.log('🔍 Verificando mensagem de erro...')
    
    // Aguardar um pouco para a mensagem aparecer
    await this.page.waitForTimeout(2000)
    
    const errorElements = await this.page.locator(this.selectors.errorMessage).count()
    
    if (errorElements > 0) {
      const errorText = await this.page.textContent(this.selectors.errorMessage)
      console.log(`❌ Mensagem de erro encontrada: ${errorText}`)
      return errorText
    } else {
      console.log('ℹ️ Nenhuma mensagem de erro encontrada')
      return null
    }
  }

  /**
   * Realiza login completo com verificação robusta
   */
  async performLogin(email: string, password: string) {
    console.log(`🔐 Realizando login com: ${email}`)
    
    await this.fillLoginForm(email, password)
    await this.clickLoginButton()
    
    // Verificar resultado do login
    const loginResult = await this.checkLoginResult()
    
    if (loginResult.redirected && !loginResult.onLoginPage) {
      console.log('✅ Login realizado com sucesso')
      return { 
        success: true, 
        error: null,
        redirected: true,
        currentUrl: loginResult.currentUrl
      }
    } else {
      // Login falhou - verificar mensagem de erro
      const errorMessage = await this.verifyErrorMessage()
      console.log('❌ Login falhou')
      return { 
        success: false, 
        error: errorMessage || 'Login falhou - não houve redirecionamento',
        redirected: false,
        currentUrl: loginResult.currentUrl,
        onLoginPage: loginResult.onLoginPage
      }
    }
  }

  /**
   * Testa login com credenciais válidas
   */
  async testValidLogin() {
    console.log('🧪 Testando login com credenciais válidas...')
    
    const result = await this.performLogin('admin@test.com', 'admin123')
    
    if (!result.success) {
      console.error('❌ ERRO: Login válido deveria ter funcionado!')
      console.error('Resultado:', result)
    }
    
    return result
  }

  /**
   * Testa login com credenciais inválidas
   */
  async testInvalidLogin() {
    console.log('🧪 Testando login com credenciais inválidas...')
    
    const result = await this.performLogin('invalid@test.com', 'wrongpassword')
    
    if (result.success) {
      console.error('❌ ERRO: Login inválido não deveria ter funcionado!')
      console.error('Resultado:', result)
    } else {
      console.log('✅ Login inválido foi rejeitado corretamente')
      console.log(`Motivo: ${result.error}`)
      console.log(`Permaneceu na página de login: ${result.onLoginPage}`)
    }
    
    return result
  }
}