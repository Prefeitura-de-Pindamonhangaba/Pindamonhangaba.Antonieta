import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class DashboardPage extends BasePage {
  private selectors = {
    // Header e título
    pageTitle: 'h1',
    
    // Action buttons
    actionButtons: {
      registerDistribution: 'button:has-text("Registrar Nova Saída")',
      registerInput: 'button:has-text("Registrar Nova Entrada")',
      addBeneficiary: 'button:has-text("Adicionar Novo Beneficiário")'
    },
    
    // Summary cards
    summaryCards: {
      totalInputs: '.n-card:has(.n-text:has-text("Entrada Total"))',
      totalDistributions: '.n-card:has(.n-text:has-text("Saída Total"))',
      currentStock: '.n-card:has(.n-text:has-text("Estoque Atual"))'
    },
    
    // Statistcs values
    statisticValues: '.n-statistic .n-statistic-value',
    
    // Beneficiaries table
    beneficiariesSection: '.n-card:has-text("Beneficiários e Controle Mensal")',
    searchField: 'input[placeholder*="Buscar por nome de beneficiário"]',
    dataTable: '.n-data-table',
    tableHeaders: '.n-data-table thead th',
    tableRows: '.n-data-table tbody tr',
    
    // Loading states
    pageLoading: '.n-spin',
    tableLoading: '.n-data-table .n-spin'
  }

  /**
   * Navega para a página do dashboard
   */
  async navigateToDashboard() {
    console.log('🌐 Navegando para dashboard...')
    await this.navigate('/dashboard')
    await this.page.waitForLoadState('domcontentloaded')
    console.log('✅ Dashboard carregado')
  }

  /**
   * Verifica se a página do dashboard carregou corretamente
   */
  async verifyDashboardLoaded() {
    console.log('🔍 Verificando se o dashboard carregou...')
    
    // Verificar se estamos na URL correta
    const currentUrl = this.page.url()
    expect(currentUrl).toContain('/dashboard')
    
    // Aguardar o título aparecer
    await this.page.waitForSelector(this.selectors.pageTitle, { timeout: 10000 })
    const title = await this.page.textContent(this.selectors.pageTitle)
    expect(title?.toLowerCase()).toContain('dashboard')
    
    console.log('✅ Dashboard carregado corretamente')
  }

  /**
   * Verifica se os botões de ação estão presentes
   */
  async verifyActionButtons() {
    console.log('🔍 Verificando botões de ação...')
    
    // Verificar botão de registrar distribuição
    const distributionButton = await this.page.isVisible(this.selectors.actionButtons.registerDistribution)
    expect(distributionButton).toBe(true)
    console.log('✅ Botão "Registrar Nova Saída" presente')
    
    // Verificar botão de registrar entrada
    const inputButton = await this.page.isVisible(this.selectors.actionButtons.registerInput)
    expect(inputButton).toBe(true)
    console.log('✅ Botão "Registrar Nova Entrada" presente')
    
    // Verificar botão de adicionar beneficiário
    const beneficiaryButton = await this.page.isVisible(this.selectors.actionButtons.addBeneficiary)
    expect(beneficiaryButton).toBe(true)
    console.log('✅ Botão "Adicionar Novo Beneficiário" presente')
    
    console.log('✅ Todos os botões de ação estão presentes')
  }

  /**
   * Verifica se os cards de resumo estão presentes
   */
  async verifySummaryCards() {
    console.log('🔍 Verificando cards de resumo...')
    
    // Aguardar cards carregarem
    await this.page.waitForSelector(this.selectors.summaryCards.totalInputs, { timeout: 15000 })
    
    // Verificar card de entrada total
    const inputsCard = await this.page.isVisible(this.selectors.summaryCards.totalInputs)
    expect(inputsCard).toBe(true)
    console.log('✅ Card "Entrada Total" presente')
    
    // Verificar card de saída total
    const distributionsCard = await this.page.isVisible(this.selectors.summaryCards.totalDistributions)
    expect(distributionsCard).toBe(true)
    console.log('✅ Card "Saída Total" presente')
    
    // Verificar card de estoque atual
    const stockCard = await this.page.isVisible(this.selectors.summaryCards.currentStock)
    expect(stockCard).toBe(true)
    console.log('✅ Card "Estoque Atual" presente')
    
    console.log('✅ Todos os cards de resumo estão presentes')
  }

  /**
   * Verifica se os valores estatísticos estão sendo exibidos
   */
  async verifyStatisticValues() {
    console.log('🔍 Verificando valores estatísticos...')
    
    // Aguardar valores carregarem
    await this.page.waitForTimeout(3000)
    
    const statisticElements = await this.page.locator(this.selectors.statisticValues).count()
    expect(statisticElements).toBe(3) // Deve ter 3 estatísticas
    
    // Verificar se os valores contêm "kg"
    const statisticValues = await this.page.locator(this.selectors.statisticValues).allTextContents()
    
    for (let i = 0; i < statisticValues.length; i++) {
      const value = statisticValues[i]
      expect(value).toContain('kg')
      console.log(`✅ Estatística ${i + 1}: ${value}`)
    }
    
    console.log('✅ Valores estatísticos estão sendo exibidos corretamente')
    return statisticValues
  }

  /**
   * Verifica se a seção de beneficiários está presente
   */
  async verifyBeneficiariesSection() {
    console.log('🔍 Verificando seção de beneficiários...')
    
    // Verificar se a seção existe
    const beneficiariesSection = await this.page.isVisible(this.selectors.beneficiariesSection)
    expect(beneficiariesSection).toBe(true)
    console.log('✅ Seção "Beneficiários e Controle Mensal" presente')
    
    // Verificar campo de busca
    const searchField = await this.page.isVisible(this.selectors.searchField)
    expect(searchField).toBe(true)
    console.log('✅ Campo de busca presente')
    
    // Verificar tabela
    await this.page.waitForSelector(this.selectors.dataTable, { timeout: 15000 })
    const dataTable = await this.page.isVisible(this.selectors.dataTable)
    expect(dataTable).toBe(true)
    console.log('✅ Tabela de beneficiários presente')
    
    console.log('✅ Seção de beneficiários está completa')
  }

  /**
   * Verifica os cabeçalhos da tabela de beneficiários
   */
  async verifyTableHeaders() {
    console.log('🔍 Verificando cabeçalhos da tabela...')
    
    const headers = await this.page.locator(this.selectors.tableHeaders).allTextContents()
    console.log('📊 Cabeçalhos encontrados:', headers)
    
    // Verificar se tem os cabeçalhos esperados
    const headerText = headers.join(' ').toLowerCase()
    expect(headerText).toContain('nome')
    expect(headerText).toContain('limite')
    expect(headerText).toContain('recebido')
    expect(headerText).toContain('progresso')
    expect(headerText).toContain('status')
    
    console.log('✅ Cabeçalhos da tabela estão corretos')
    return headers
  }

  /**
   * Conta as linhas da tabela de beneficiários
   */
  async countBeneficiaryRows() {
    console.log('🔍 Contando linhas da tabela...')
    
    // Aguardar tabela carregar
    await this.page.waitForTimeout(2000)
    
    const rowCount = await this.page.locator(this.selectors.tableRows).count()
    console.log(`📊 Linhas de beneficiários encontradas: ${rowCount}`)
    
    return rowCount
  }

  /**
   * Testa a funcionalidade de busca
   */
  async testSearchFunctionality() {
    console.log('🔍 Testando funcionalidade de busca...')
    
    // Contar linhas antes da busca
    const initialRowCount = await this.countBeneficiaryRows()
    
    if (initialRowCount > 0) {
      // Obter o nome do primeiro beneficiário
      const firstRowName = await this.page.locator(this.selectors.tableRows).first().locator('td').first().textContent()
      
      if (firstRowName && firstRowName.trim()) {
        // Buscar por parte do nome
        const searchTerm = firstRowName.trim().substring(0, 3)
        await this.page.fill(this.selectors.searchField, searchTerm)
        
        // Aguardar filtro aplicar
        await this.page.waitForTimeout(1000)
        
        // Verificar se ainda há resultados
        const filteredRowCount = await this.countBeneficiaryRows()
        console.log(`🔍 Resultado da busca por "${searchTerm}": ${filteredRowCount} linhas`)
        
        // Limpar busca
        await this.page.fill(this.selectors.searchField, '')
        await this.page.waitForTimeout(1000)
        
        const resetRowCount = await this.countBeneficiaryRows()
        expect(resetRowCount).toBe(initialRowCount)
        
        console.log('✅ Funcionalidade de busca está funcionando')
        return true
      }
    }
    
    console.log('ℹ️ Busca não testada (sem dados ou dados insuficientes)')
    return false
  }

  /**
   * Verifica se a página está carregando dados
   */
  async waitForDataLoad() {
    console.log('⏳ Aguardando carregamento de dados...')
    
    // Aguardar loading desaparecer
    try {
      await this.page.waitForSelector(this.selectors.pageLoading, { 
        state: 'hidden', 
        timeout: 30000 
      })
      console.log('✅ Loading da página finalizado')
    } catch (error) {
      console.log('ℹ️ Nenhum loading da página detectado')
    }
    
    // Aguardar loading da tabela desaparecer
    try {
      await this.page.waitForSelector(this.selectors.tableLoading, { 
        state: 'hidden', 
        timeout: 15000 
      })
      console.log('✅ Loading da tabela finalizado')
    } catch (error) {
      console.log('ℹ️ Nenhum loading da tabela detectado')
    }
    
    // Aguardar estabilização da rede
    await this.page.waitForLoadState('networkidle', { timeout: 15000 })
    console.log('✅ Rede estabilizada')
  }

  /**
   * Executa teste completo do dashboard
   */
  async performCompleteDashboardTest() {
    console.log('🧪 Iniciando teste completo do dashboard...')
    
    try {
      // 1. Navegar para dashboard
      await this.navigateToDashboard()
      
      // 2. Aguardar carregamento
      await this.waitForDataLoad()
      
      // 3. Verificar se página carregou
      await this.verifyDashboardLoaded()
      
      // 4. Verificar botões de ação
      await this.verifyActionButtons()
      
      // 5. Verificar cards de resumo
      await this.verifySummaryCards()
      
      // 6. Verificar valores estatísticos
      const statisticValues = await this.verifyStatisticValues()
      
      // 7. Verificar seção de beneficiários
      await this.verifyBeneficiariesSection()
      
      // 8. Verificar cabeçalhos da tabela
      const headers = await this.verifyTableHeaders()
      
      // 9. Contar beneficiários
      const rowCount = await this.countBeneficiaryRows()
      
      // 10. Testar busca (se houver dados)
      const searchTested = await this.testSearchFunctionality()
      
      console.log('✅ Teste completo do dashboard concluído com sucesso!')
      
      return {
        success: true,
        dashboardLoaded: true,
        actionButtonsPresent: true,
        summaryCardsPresent: true,
        statisticValues,
        beneficiariesSectionPresent: true,
        tableHeaders: headers,
        beneficiaryCount: rowCount,
        searchFunctionality: searchTested
      }
      
    } catch (error) {
      console.error('❌ Erro no teste do dashboard:', error)
      throw error
    }
  }
}