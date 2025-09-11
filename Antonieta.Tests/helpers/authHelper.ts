import { Page } from '@playwright/test'

export class AuthHelper {
  private static readonly DEFAULT_CREDENTIALS = {
    email: 'admin@test.com',
    password: 'admin123'
  }

  private static readonly SELECTORS = {
    emailInput: 'input[type="email"], input[name="email"], input[placeholder*="email" i]',
    passwordInput: 'input[type="password"], input[name="password"], input[placeholder*="senha" i]',
    loginButton: 'button[type="submit"], button:has-text("Entrar"), button:has-text("Login")',
    errorMessage: '.n-message--error, .error-message, .alert-error, [class*="error"]'
  }

  /**
   * Realiza login via interface do usuário
   */
  static async login(page: Page, credentials = AuthHelper.DEFAULT_CREDENTIALS): Promise<boolean> {
    console.log('🔐 Realizando login...')
    
    try {
      // 1. Navegar para a página de login
      await page.goto('/login')
      console.log('🌐 Navegou para /login')
      
      // 2. Aguardar elementos de login carregarem
      await page.waitForSelector(AuthHelper.SELECTORS.emailInput, { timeout: 10000 })
      console.log('📋 Formulário de login carregado')
      
      // 3. Preencher credenciais
      await page.fill(AuthHelper.SELECTORS.emailInput, credentials.email)
      await page.fill(AuthHelper.SELECTORS.passwordInput, credentials.password)
      console.log(`✉️ Credenciais preenchidas: ${credentials.email}`)
      
      // 4. Clicar no botão de login
      await page.click(AuthHelper.SELECTORS.loginButton)
      console.log('🔘 Botão de login clicado')
      
      // 5. Aguardar processamento e verificar resultado
      const loginSuccess = await AuthHelper.waitForLoginResult(page)
      
      if (loginSuccess) {
        console.log('✅ Login realizado com sucesso')
        return true
      } else {
        console.log('❌ Login falhou')
        return false
      }
      
    } catch (error) {
      console.error('❌ Erro durante o login:', error)
      return false
    }
  }

  /**
   * Aguarda o resultado do login (redirecionamento ou erro)
   */
  private static async waitForLoginResult(page: Page): Promise<boolean> {
    console.log('⏳ Aguardando resultado do login...')
    
    try {
      // Aguardar redirecionamento para dashboard (com query parameters)
      await page.waitForURL('**/dashboard*', { timeout: 10000 })
      
      const currentUrl = page.url()
      if (currentUrl.includes('/dashboard')) {
        console.log(`✅ Redirecionado para: ${currentUrl}`)
        return true
      }
    } catch (error) {
      // Se não redirecionou, verificar se há erro ou se permaneceu no login
      console.log('⚠️ Não houve redirecionamento - verificando erro...')
    }
    
    // Aguardar um pouco mais para mensagens de erro aparecerem
    await page.waitForTimeout(3000)
    
    const currentUrl = page.url()
    
    // Se ainda está na página de login, o login falhou
    if (currentUrl.includes('/login')) {
      console.log('❌ Permaneceu na página de login - login falhou')
      
      // Verificar se há mensagem de erro
      const errorMessage = await AuthHelper.checkForErrorMessage(page)
      if (errorMessage) {
        console.log(`📢 Mensagem de erro: ${errorMessage}`)
      }
      
      return false
    }
    
    // Se redirecionou para outra página (não login), considerar sucesso
    console.log(`✅ Redirecionado para: ${currentUrl}`)
    return true
  }

  /**
   * Verifica se há mensagem de erro na página
   */
  private static async checkForErrorMessage(page: Page): Promise<string | null> {
    try {
      const errorElements = await page.locator(AuthHelper.SELECTORS.errorMessage).count()
      
      if (errorElements > 0) {
        const errorText = await page.locator(AuthHelper.SELECTORS.errorMessage).first().textContent()
        return errorText?.trim() || 'Erro detectado (sem texto)'
      }
      
      return null
    } catch (error) {
      return null
    }
  }

  /**
   * Verifica se o usuário está logado
   */
  static async isLoggedIn(page: Page): Promise<boolean> {
    const currentUrl = page.url()
    const notOnLoginPage = !currentUrl.includes('/login')
    
    console.log(`🔍 Verificando login - URL: ${currentUrl}, Logado: ${notOnLoginPage}`)
    return notOnLoginPage
  }

  /**
   * Faz logout se estiver logado
   */
  static async logout(page: Page): Promise<boolean> {
    console.log('🚪 Tentando fazer logout...')
    
    try {
      // Seletores comuns para botões de logout
      const logoutSelectors = [
        'button:has-text("Sair")',
        'button:has-text("Logout")', 
        '[data-testid="logout"]',
        '.logout-button',
        'button[title*="sair" i]'
      ]
      
      for (const selector of logoutSelectors) {
        const logoutButton = page.locator(selector)
        const count = await logoutButton.count()
        
        if (count > 0) {
          await logoutButton.click()
          console.log(`🔘 Clicou no botão de logout: ${selector}`)
          
          // Aguardar redirecionamento para login
          await page.waitForURL('**/login', { timeout: 5000 })
          console.log('✅ Logout realizado com sucesso')
          return true
        }
      }
      
      console.log('⚠️ Botão de logout não encontrado')
      return false
      
    } catch (error) {
      console.log('⚠️ Erro durante logout:', error.message)
      return false
    }
  }

  /**
   * Login com diferentes tipos de usuário
   */
  static async loginAs(page: Page, userType: 'admin' | 'user'): Promise<boolean> {
    const credentials = {
      admin: { 
        email: process.env.ADMIN_EMAIL || 'admin@test.com', 
        password: process.env.ADMIN_PASSWORD || 'admin123' 
      },
      user: { 
        email: process.env.USER_EMAIL || 'user@test.com', 
        password: process.env.USER_PASSWORD || 'user123' 
      }
    }

    console.log(`🔐 Fazendo login como: ${userType}`)
    return await AuthHelper.login(page, credentials[userType])
  }

  /**
   * Verifica se o login é necessário e faz automaticamente
   */
  static async ensureLoggedIn(page: Page): Promise<boolean> {
    console.log('🔍 Verificando se login é necessário...')
    
    const isAlreadyLoggedIn = await AuthHelper.isLoggedIn(page)
    
    if (isAlreadyLoggedIn) {
      console.log('✅ Usuário já está logado')
      return true
    }
    
    console.log('🔐 Login necessário - realizando...')
    return await AuthHelper.login(page)
  }

  /**
   * Força uma nova sessão de login (logout + login)
   */
  static async forceNewLogin(page: Page, credentials = AuthHelper.DEFAULT_CREDENTIALS): Promise<boolean> {
    console.log('🔄 Forçando nova sessão de login...')
    
    // Tentar logout primeiro
    await AuthHelper.logout(page)
    
    // Aguardar um pouco
    await page.waitForTimeout(1000)
    
    // Fazer novo login
    return await AuthHelper.login(page, credentials)
  }

  /**
   * Testa credenciais específicas
   */
  static async testCredentials(page: Page, email: string, password: string): Promise<{ success: boolean, error?: string }> {
    console.log(`🧪 Testando credenciais: ${email}`)
    
    try {
      const success = await AuthHelper.login(page, { email, password })
      
      if (success) {
        return { success: true }
      } else {
        const errorMessage = await AuthHelper.checkForErrorMessage(page)
        return { 
          success: false, 
          error: errorMessage || 'Login falhou sem mensagem específica' 
        }
      }
    } catch (error) {
      return { 
        success: false, 
        error: `Erro durante teste: ${error.message}` 
      }
    }
  }
}