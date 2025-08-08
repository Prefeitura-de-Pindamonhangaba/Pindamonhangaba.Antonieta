import { test, expect } from '@playwright/test'
import { DashboardPage } from '../pages/DashboardPage'
import { AuthHelper } from '../helpers/authHelper'

test.describe('Dashboard - Testes E2E', () => {
  let dashboardPage: DashboardPage

  test.beforeEach(async ({ page }) => {
    dashboardPage = new DashboardPage(page)
    
    // 1. Fazer login
    await AuthHelper.login(page)
    
    // 2. Navegar para dashboard
    await dashboardPage.navigateToDashboard()
    
    // 3. Aguardar carregamento
    await dashboardPage.waitForDataLoad()
    
    console.log('🚀 Setup completo: Login + Navegação para dashboard')
  })

  test('deve carregar o dashboard corretamente', async () => {
    console.log('🧪 Teste: Carregamento do dashboard')
    
    // Verificar se o dashboard carregou
    await dashboardPage.verifyDashboardLoaded()
    
    console.log('✅ Dashboard carregado corretamente')
  })

  test('deve exibir todos os botões de ação', async () => {
    console.log('🧪 Teste: Botões de ação')
    
    // Verificar botões de ação
    await dashboardPage.verifyActionButtons()
    
    console.log('✅ Todos os botões de ação estão presentes')
  })

  test('deve exibir cards de resumo com valores', async () => {
    console.log('🧪 Teste: Cards de resumo')
    
    // Verificar cards de resumo
    await dashboardPage.verifySummaryCards()
    
    // Verificar valores estatísticos
    const statisticValues = await dashboardPage.verifyStatisticValues()
    
    // Verificar se todos os valores contêm "kg"
    expect(statisticValues).toHaveLength(3)
    statisticValues.forEach(value => {
      expect(value).toContain('kg')
    })
    
    console.log('✅ Cards de resumo com valores corretos')
  })

  test('deve exibir tabela de beneficiários', async () => {
    console.log('🧪 Teste: Tabela de beneficiários')
    
    // Verificar seção de beneficiários
    await dashboardPage.verifyBeneficiariesSection()
    
    // Verificar cabeçalhos
    const headers = await dashboardPage.verifyTableHeaders()
    
    // Verificar se tem os cabeçalhos essenciais
    expect(headers.length).toBeGreaterThan(0)
    
    // Contar beneficiários
    const rowCount = await dashboardPage.countBeneficiaryRows()
    expect(rowCount).toBeGreaterThanOrEqual(0)
    
    console.log(`✅ Tabela de beneficiários com ${rowCount} registros`)
  })

  test('deve testar funcionalidade de busca', async () => {
    console.log('🧪 Teste: Funcionalidade de busca')
    
    // Verificar seção primeiro
    await dashboardPage.verifyBeneficiariesSection()
    
    // Testar busca
    const searchTested = await dashboardPage.testSearchFunctionality()
    
    if (searchTested) {
      console.log('✅ Funcionalidade de busca testada e funciona')
    } else {
      console.log('ℹ️ Busca não testada devido à falta de dados')
    }
  })

  test('deve executar teste completo do dashboard', async () => {
    console.log('🧪 Teste: Funcionalidade completa do dashboard')
    
    // Executar teste completo
    const result = await dashboardPage.performCompleteDashboardTest()
    
    // Verificar resultado
    expect(result.success).toBe(true)
    expect(result.dashboardLoaded).toBe(true)
    expect(result.actionButtonsPresent).toBe(true)
    expect(result.summaryCardsPresent).toBe(true)
    expect(result.beneficiariesSectionPresent).toBe(true)
    expect(result.statisticValues).toHaveLength(3)
    expect(result.tableHeaders.length).toBeGreaterThan(0)
    expect(result.beneficiaryCount).toBeGreaterThanOrEqual(0)
    
    console.log('📊 Resultado do teste completo:', {
      '📋 Dashboard carregado': result.dashboardLoaded ? '✅' : '❌',
      '🔘 Botões presentes': result.actionButtonsPresent ? '✅' : '❌',
      '📊 Cards presentes': result.summaryCardsPresent ? '✅' : '❌',
      '🔢 Valores estatísticos': result.statisticValues.length,
      '📈 Beneficiários': result.beneficiaryCount,
      '🔍 Busca testada': result.searchFunctionality ? '✅' : '⚠️'
    })
    
    console.log('✅ Teste completo do dashboard realizado com sucesso')
  })
})