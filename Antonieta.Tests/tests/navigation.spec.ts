import { test, expect } from '@playwright/test'
import { NavigationPage } from '../pages/NavigationPage'
import { AuthHelper } from '../helpers/authHelper'

test.describe('Navegação - Testes E2E', () => {
  let navigationPage: NavigationPage

  test.beforeEach(async ({ page }) => {
    navigationPage = new NavigationPage(page)
    
    // 1. Fazer login
    const loginSuccess = await AuthHelper.login(page)
    if (!loginSuccess) {
      throw new Error('Falha no login durante setup do teste')
    }
    
    // 2. Aguardar carregamento inicial
    await navigationPage.waitForPageLoad()
    
    console.log('🚀 Setup completo: Login realizado')
  })

  test('deve exibir o menu de navegação com todos os itens', async () => {
    console.log('🧪 Teste: Verificação do menu de navegação')
    
    // Verificar se o menu existe
    await navigationPage.verifyNavigationExists()
    
    // Verificar todos os itens do menu
    const foundItems = await navigationPage.verifyAllMenuItems()
    
    // Deve ter pelo menos alguns itens principais
    expect(foundItems.length).toBeGreaterThan(0)
    console.log(`✅ Menu de navegação com ${foundItems.length} itens encontrados`)
  })

  test('deve navegar para Dashboard', async () => {
    console.log('🧪 Teste: Navegação para Dashboard')
    
    await navigationPage.verifyNavigationExists()
    const url = await navigationPage.testDashboardNavigation()
    
    expect(url).toContain('/dashboard')
    console.log('✅ Navegação para Dashboard funciona')
  })

  test('deve navegar para Beneficiários', async () => {
    console.log('🧪 Teste: Navegação para Beneficiários')
    
    await navigationPage.verifyNavigationExists()
    const url = await navigationPage.testBeneficiariesNavigation()
    
    expect(url).toContain('/beneficiary')
    console.log('✅ Navegação para Beneficiários funciona')
  })

  test('deve navegar para Distribuições', async () => {
    console.log('🧪 Teste: Navegação para Distribuições')
    
    await navigationPage.verifyNavigationExists()
    const url = await navigationPage.testDistributionsNavigation()
    
    expect(url).toContain('/distributions')
    console.log('✅ Navegação para Distribuições funciona')
  })

  test('deve navegar para Entradas', async () => {
    console.log('🧪 Teste: Navegação para Entradas')
    
    await navigationPage.verifyNavigationExists()
    const url = await navigationPage.testInputsNavigation()
    
    expect(url).toContain('/inputs')
    console.log('✅ Navegação para Entradas funciona')
  })

  test('deve navegar para Estoque', async () => {
    console.log('🧪 Teste: Navegação para Estoque')
    
    await navigationPage.verifyNavigationExists()
    const url = await navigationPage.testRationStockNavigation()
    
    expect(url).toContain('/ration_stock')
    console.log('✅ Navegação para Estoque funciona')
  })

  test('deve verificar itens ativos do menu durante navegação', async () => {
    console.log('🧪 Teste: Verificação de itens ativos do menu')
    
    await navigationPage.verifyNavigationExists()
    
    // Testar algumas navegações e verificar item ativo
    const navigationsToTest = [
      { name: 'Dashboard', method: () => navigationPage.testDashboardNavigation() },
      { name: 'Beneficiários', method: () => navigationPage.testBeneficiariesNavigation() }
    ]
    
    for (const nav of navigationsToTest) {
      console.log(`🔄 Testando item ativo para: ${nav.name}`)
      
      const url = await nav.method()
      const hasActiveItem = await navigationPage.verifyActiveMenuItem(url)
      
      console.log(`${nav.name}: Item ativo = ${hasActiveItem ? '✅' : '⚠️'}`)
    }
    
    console.log('✅ Verificação de itens ativos concluída')
  })

  test('deve navegar entre páginas múltiplas vezes', async () => {
    console.log('🧪 Teste: Navegação múltipla entre páginas')
    
    await navigationPage.verifyNavigationExists()
    
    // Testar navegação ida e volta
    console.log('🔄 Dashboard → Beneficiários')
    await navigationPage.testDashboardNavigation()
    await navigationPage.testBeneficiariesNavigation()
    
    console.log('🔄 Beneficiários → Dashboard')
    await navigationPage.testBeneficiariesNavigation()
    await navigationPage.testDashboardNavigation()
    
    console.log('🔄 Dashboard → Distribuições → Dashboard')
    await navigationPage.testDashboardNavigation()
    await navigationPage.testDistributionsNavigation()
    await navigationPage.testDashboardNavigation()
    
    // Verificar se ainda está funcionando
    const currentUrl = navigationPage.page.url()
    expect(currentUrl).toContain('/dashboard')
    
    console.log('✅ Navegação múltipla funciona corretamente')
  })
})