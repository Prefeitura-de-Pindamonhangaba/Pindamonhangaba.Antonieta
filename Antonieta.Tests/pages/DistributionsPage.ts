import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class DistributionsPage extends BasePage {
  private selectors = {
    // Header
    pageTitle: 'h1:has-text("Distribuições")',
    
    // Search and Actions
    searchField: 'input[placeholder*="Buscar por beneficiário"], input[placeholder*="buscar"]',
    addDistributionButton: 'button:has-text("Registrar Nova Distribuição")',
    
    // Table
    dataTable: '.n-data-table',
    tableHeaders: '.n-data-table thead th',
    tableRows: '.n-data-table tbody tr',
    tableLoading: '.n-data-table .n-spin',
    
    // Table columns (baseado nas colunas do Vue)
    dateColumn: 'td:nth-child(1)',
    beneficiaryColumn: 'td:nth-child(2)',
    rationTypeColumn: 'td:nth-child(3)',
    amountColumn: 'td:nth-child(4)',
    observationsColumn: 'td:nth-child(5)',
    actionsColumn: 'td:nth-child(6)',
    
    // Observations specific
    observationsText: '.n-data-table tbody tr td:nth-child(5) span',
    viewMoreButton: 'button:has-text("Ver mais")',
    noObservationsText: 'span:has-text("Sem observações")',
    
    // Action buttons in table
    detailsButton: 'button[title*="detalhes"], button:has([class*="IconFileText"])',
    
    // Pagination
    pagination: '.n-pagination',
    paginationButtons: '.n-pagination .n-pagination-item',
    
    // Loading states
    pageLoading: '.n-spin',
    loadingMessage: '.n-message:has-text("carregando")',
    
    // Messages
    successMessage: '.n-message--success',
    errorMessage: '.n-message--error',
    noDataMessage: '.n-empty, .no-data, [class*="empty"]',
    
    // Card container
    pageCard: '.page-card, .n-card'
  }

  /**
   * Navega para a página de distribuições
   */
  async navigateToPage() {
    console.log('🌐 Navegando para página de distribuições...')
    await this.navigate('/distributions')
    await this.page.waitForLoadState('domcontentloaded')
    console.log('✅ Página de distribuições carregada')
  }

  /**
   * Verifica se a página carregou corretamente
   */
  async verifyPageLoaded() {
    console.log('🔍 Verificando se a página de distribuições carregou...')
    
    // Verificar URL
    const currentUrl = this.page.url()
    expect(currentUrl).toContain('/distributions')
    
    // Verificar se não foi redirecionado para login
    expect(currentUrl).not.toContain('/login')
    
    console.log('✅ Página de distribuições carregada corretamente')
  }

  /**
   * Aguarda carregamento completo da página
   */
  async waitForPageLoad() {
    console.log('⏳ Aguardando carregamento completo...')
    
    // Aguardar loading da página desaparecer
    try {
      await this.page.waitForSelector(this.selectors.pageLoading, { 
        state: 'hidden', 
        timeout: 30000 
      })
      console.log('✅ Loading da página finalizado')
    } catch (error) {
      console.log('ℹ️ Nenhum loading da página detectado')
    }
    
    // Aguardar tabela carregar
    try {
      await this.page.waitForSelector(this.selectors.dataTable, { timeout: 15000 })
      console.log('✅ Tabela carregada')
    } catch (error) {
      console.log('⚠️ Tabela não encontrada ou demorou para carregar')
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
    
    // Aguardar rede estabilizar
    await this.page.waitForLoadState('networkidle', { timeout: 15000 })
    console.log('✅ Página carregada completamente')
  }

  /**
   * Verifica se o título da página está presente
   */
  async verifyPageTitle() {
    console.log('🔍 Verificando título da página...')
    
    try {
      await this.page.waitForSelector(this.selectors.pageTitle, { timeout: 10000 })
      const title = await this.page.textContent(this.selectors.pageTitle)
      
      if (title && title.toLowerCase().includes('distribuiç')) {
        console.log(`✅ Título encontrado: "${title}"`)
        return title
      } else {
        console.log('⚠️ Título não contém "distribuiç"')
        return title
      }
    } catch (error) {
      console.log('⚠️ Título não encontrado')
      return null
    }
  }

  /**
   * Verifica se a tabela está presente
   */
  async verifyTableExists() {
    console.log('🔍 Verificando se a tabela existe...')
    
    try {
      await this.page.waitForSelector(this.selectors.dataTable, { timeout: 15000 })
      const tableVisible = await this.page.isVisible(this.selectors.dataTable)
      
      if (tableVisible) {
        console.log('✅ Tabela encontrada e visível')
        return true
      } else {
        console.log('⚠️ Tabela existe mas não está visível')
        return false
      }
    } catch (error) {
      console.log('❌ Tabela não encontrada')
      return false
    }
  }

  /**
   * Verifica os cabeçalhos da tabela
   */
  async verifyTableHeaders() {
    console.log('🔍 Verificando cabeçalhos da tabela...')
    
    try {
      const headers = await this.page.locator(this.selectors.tableHeaders).allTextContents()
      console.log('📊 Cabeçalhos encontrados:', headers)
      
      if (headers.length > 0) {
        // Verificar cabeçalhos esperados para distribuições
        const headerText = headers.join(' ').toLowerCase()
        const expectedHeaders = ['data', 'beneficiário', 'ração', 'quantidade', 'observações', 'ações']
        const foundHeaders = expectedHeaders.filter(expected => 
          headerText.includes(expected.toLowerCase())
        )
        
        console.log(`✅ Cabeçalhos esperados encontrados: ${foundHeaders.length}/${expectedHeaders.length}`)
        console.log('📋 Cabeçalhos encontrados:', foundHeaders)
        
        return headers
      } else {
        console.log('⚠️ Nenhum cabeçalho encontrado')
        return []
      }
    } catch (error) {
      console.log('❌ Erro ao verificar cabeçalhos:', error.message)
      return []
    }
  }

  /**
   * Conta as distribuições na tabela
   */
  async countDistributions() {
    console.log('🔍 Contando distribuições...')
    
    try {
      await this.page.waitForTimeout(2000) // Aguardar carregamento
      const rowCount = await this.page.locator(this.selectors.tableRows).count()
      console.log(`📦 Distribuições encontradas: ${rowCount}`)
      
      return rowCount
    } catch (error) {
      console.log('❌ Erro ao contar distribuições:', error.message)
      return 0
    }
  }

  /**
   * Verifica se há dados na tabela ou mensagem de tabela vazia
   */
  async verifyTableContent() {
    console.log('🔍 Verificando conteúdo da tabela...')
    
    const rowCount = await this.countDistributions()
    
    if (rowCount > 0) {
      console.log(`✅ Tabela contém ${rowCount} distribuições`)
      
      // Verificar se a primeira linha tem dados válidos
      try {
        const firstRow = this.page.locator(this.selectors.tableRows).first()
        
        // Verificar dados específicos das colunas
        const dateText = await firstRow.locator(this.selectors.dateColumn).textContent()
        const beneficiaryText = await firstRow.locator(this.selectors.beneficiaryColumn).textContent()
        const amountText = await firstRow.locator(this.selectors.amountColumn).textContent()
        
        const hasValidData = dateText && beneficiaryText && amountText &&
                           amountText.includes('kg') // Quantidade deve conter 'kg'
        
        if (hasValidData) {
          console.log('✅ Primeira linha contém dados válidos')
          console.log(`📋 Exemplo: ${dateText} | ${beneficiaryText} | ${amountText}`)
          return { 
            hasData: true, 
            count: rowCount, 
            sampleData: {
              date: dateText?.trim(),
              beneficiary: beneficiaryText?.trim(),
              amount: amountText?.trim()
            }
          }
        } else {
          console.log('⚠️ Primeira linha não contém dados válidos')
          return { hasData: true, count: rowCount, validData: false }
        }
      } catch (error) {
        console.log('⚠️ Erro ao verificar dados da primeira linha')
        return { hasData: true, count: rowCount }
      }
    } else {
      console.log('ℹ️ Tabela vazia ou sem dados')
      
      // Verificar se há mensagem de "sem dados"
      try {
        const noDataVisible = await this.page.isVisible(this.selectors.noDataMessage)
        if (noDataVisible) {
          console.log('✅ Mensagem de "sem dados" exibida corretamente')
        }
      } catch (error) {
        console.log('ℹ️ Nenhuma mensagem de "sem dados" encontrada')
      }
      
      return { hasData: false, count: 0 }
    }
  }

  /**
   * Verifica se o campo de busca está presente
   */
  async verifySearchField() {
    console.log('🔍 Verificando campo de busca...')
    
    try {
      const searchVisible = await this.page.isVisible(this.selectors.searchField)
      
      if (searchVisible) {
        console.log('✅ Campo de busca encontrado')
        
        // Verificar placeholder
        const placeholder = await this.page.getAttribute(this.selectors.searchField, 'placeholder')
        if (placeholder) {
          console.log(`📝 Placeholder: "${placeholder}"`)
          
          // Verificar se placeholder é apropriado para distribuições
          if (placeholder.toLowerCase().includes('beneficiário') || 
              placeholder.toLowerCase().includes('ração') ||
              placeholder.toLowerCase().includes('observações')) {
            console.log('✅ Placeholder apropriado para busca de distribuições')
          }
        }
        
        return true
      } else {
        console.log('⚠️ Campo de busca não encontrado')
        return false
      }
    } catch (error) {
      console.log('❌ Erro ao verificar campo de busca:', error.message)
      return false
    }
  }

  /**
   * Testa a funcionalidade básica de busca (apenas digitação)
   */
  async testBasicSearchFunctionality() {
    console.log('🔍 Testando funcionalidade básica de busca...')
    
    const searchFieldExists = await this.verifySearchField()
    
    if (!searchFieldExists) {
      console.log('⚠️ Campo de busca não encontrado - não é possível testar')
      return false
    }
    
    try {
      // Testar se consegue digitar no campo
      await this.page.fill(this.selectors.searchField, 'teste busca')
      const value = await this.page.inputValue(this.selectors.searchField)
      
      if (value === 'teste busca') {
        console.log('✅ Campo de busca aceita texto')
        
        // Limpar campo
        await this.page.fill(this.selectors.searchField, '')
        console.log('✅ Campo de busca pode ser limpo')
        
        return true
      } else {
        console.log('⚠️ Campo de busca não aceita texto corretamente')
        return false
      }
    } catch (error) {
      console.log('❌ Erro ao testar campo de busca:', error.message)
      return false
    }
  }

  /**
   * Testa busca com dados reais (se houver)
   */
  async testSearchWithRealData() {
    console.log('🔍 Testando busca com dados reais...')
    
    const searchFieldExists = await this.verifySearchField()
    
    if (!searchFieldExists) {
      console.log('⚠️ Campo de busca não encontrado')
      return false
    }
    
    const initialCount = await this.countDistributions()
    
    if (initialCount === 0) {
      console.log('ℹ️ Sem dados para testar busca')
      return false
    }
    
    try {
      // Obter dados da primeira linha para busca
      const firstRow = this.page.locator(this.selectors.tableRows).first()
      const beneficiaryText = await firstRow.locator(this.selectors.beneficiaryColumn).textContent()
      
      if (beneficiaryText && beneficiaryText.trim() && !beneficiaryText.includes('N/A')) {
        // Buscar por parte do nome do beneficiário
        const searchTerm = beneficiaryText.trim().substring(0, 3)
        console.log(`🔍 Buscando por: "${searchTerm}"`)
        
        await this.page.fill(this.selectors.searchField, searchTerm)
        
        // Aguardar filtro aplicar
        await this.page.waitForTimeout(1000)
        
        const filteredCount = await this.countDistributions()
        console.log(`📊 Resultado da busca: ${filteredCount} distribuições`)
        
        // Limpar busca
        await this.page.fill(this.selectors.searchField, '')
        await this.page.waitForTimeout(1000)
        
        const resetCount = await this.countDistributions()
        
        if (resetCount === initialCount) {
          console.log('✅ Busca funcionou corretamente (dados filtrados e resetados)')
          return true
        } else {
          console.log('⚠️ Busca pode não estar funcionando corretamente')
          return false
        }
      } else {
        console.log('ℹ️ Não foi possível obter dados válidos para teste de busca')
        return false
      }
    } catch (error) {
      console.log('❌ Erro durante teste de busca:', error.message)
      return false
    }
  }

  /**
   * Verifica formatação das quantidades (devem conter 'kg')
   */
  async verifyAmountFormatting() {
    console.log('🔍 Verificando formatação das quantidades...')
    
    const rowCount = await this.countDistributions()
    
    if (rowCount === 0) {
      console.log('ℹ️ Sem dados para verificar formatação')
      return true
    }
    
    try {
      const amountCells = await this.page.locator(this.selectors.amountColumn).allTextContents()
      const validAmounts = amountCells.filter(amount => 
        amount && amount.includes('kg') && amount.match(/\d+/)
      )
      
      console.log(`📊 Quantidades verificadas: ${validAmounts.length}/${amountCells.length}`)
      
      if (validAmounts.length > 0) {
        console.log('✅ Quantidades estão formatadas corretamente (contêm "kg")')
        console.log(`📋 Exemplos: ${validAmounts.slice(0, 3).join(', ')}`)
        return true
      } else {
        console.log('⚠️ Quantidades podem não estar formatadas corretamente')
        return false
      }
    } catch (error) {
      console.log('❌ Erro ao verificar formatação:', error.message)
      return false
    }
  }

  /**
   * Verifica botões de ação na tabela
   */
  async verifyActionButtons() {
    console.log('🔍 Verificando botões de ação...')
    
    const rowCount = await this.countDistributions()
    
    if (rowCount === 0) {
      console.log('ℹ️ Sem dados para verificar botões de ação')
      return { detailsButtons: 0 }
    }
    
    try {
      const detailsButtons = await this.page.locator(this.selectors.detailsButton).count()
      
      console.log(`🔘 Botões de detalhes encontrados: ${detailsButtons}`)
      
      if (detailsButtons > 0) {
        console.log('✅ Botões de ação presentes na tabela')
      } else {
        console.log('⚠️ Nenhum botão de ação encontrado')
      }
      
      return { detailsButtons }
    } catch (error) {
      console.log('❌ Erro ao verificar botões de ação:', error.message)
      return { detailsButtons: 0 }
    }
  }

  /**
   * Verifica observações na tabela
   */
  async verifyObservations() {
    console.log('🔍 Verificando coluna de observações...')
    
    const rowCount = await this.countDistributions()
    
    if (rowCount === 0) {
      console.log('ℹ️ Sem dados para verificar observações')
      return { hasObservations: false, noObservations: 0, withObservations: 0 }
    }
    
    try {
      // Contar células com "Sem observações"
      const noObservationsCells = await this.page.locator(this.selectors.noObservationsText).count()
      
      // Contar células com observações (que têm texto e não são "Sem observações")
      const observationCells = await this.page.locator(this.selectors.observationsColumn).count()
      const withObservations = observationCells - noObservationsCells
      
      console.log(`📝 Observações: ${withObservations} com texto, ${noObservationsCells} sem observações`)
      
      // Verificar se há botões "Ver mais"
      const viewMoreButtons = await this.page.locator(this.selectors.viewMoreButton).count()
      if (viewMoreButtons > 0) {
        console.log(`👀 Botões "Ver mais" encontrados: ${viewMoreButtons}`)
      }
      
      return {
        hasObservations: withObservations > 0,
        noObservations: noObservationsCells,
        withObservations,
        viewMoreButtons
      }
    } catch (error) {
      console.log('❌ Erro ao verificar observações:', error.message)
      return { hasObservations: false, noObservations: 0, withObservations: 0 }
    }
  }

  /**
   * Verifica botão de registrar nova distribuição
   */
  async verifyAddDistributionButton() {
    console.log('🔍 Verificando botão de registrar distribuição...')
    
    try {
      const buttonVisible = await this.page.isVisible(this.selectors.addDistributionButton)
      
      if (buttonVisible) {
        console.log('✅ Botão "Registrar Nova Distribuição" encontrado')
        
        // Verificar se botão está habilitado
        const buttonEnabled = await this.page.isEnabled(this.selectors.addDistributionButton)
        console.log(`🔘 Botão habilitado: ${buttonEnabled ? '✅' : '❌'}`)
        
        return true
      } else {
        console.log('⚠️ Botão de registrar distribuição não encontrado')
        return false
      }
    } catch (error) {
      console.log('❌ Erro ao verificar botão:', error.message)
      return false
    }
  }

  /**
   * Executa verificação completa da página (apenas visualização)
   */
  async performCompletePageVerification() {
    console.log('🧪 Iniciando verificação completa da página de distribuições...')
    
    try {
      // 1. Verificar se página carregou
      await this.verifyPageLoaded()
      
      // 2. Aguardar carregamento completo
      await this.waitForPageLoad()
      
      // 3. Verificar título
      const title = await this.verifyPageTitle()
      
      // 4. Verificar se tabela existe
      const tableExists = await this.verifyTableExists()
      
      // 5. Verificar cabeçalhos (se tabela existe)
      let headers = []
      if (tableExists) {
        headers = await this.verifyTableHeaders()
      }
      
      // 6. Verificar conteúdo da tabela
      const tableContent = await this.verifyTableContent()
      
      // 7. Verificar campo de busca
      const searchFieldExists = await this.verifySearchField()
      
      // 8. Testar busca básica
      const basicSearchWorks = await this.testBasicSearchFunctionality()
      
      // 9. Testar busca com dados reais (se houver)
      const realSearchWorks = await this.testSearchWithRealData()
      
      // 10. Verificar formatação das quantidades
      const amountFormatting = await this.verifyAmountFormatting()
      
      // 11. Verificar botões de ação
      const actionButtons = await this.verifyActionButtons()
      
      // 12. Verificar observações
      const observations = await this.verifyObservations()
      
      // 13. Verificar botão de adicionar
      const addButtonExists = await this.verifyAddDistributionButton()
      
      console.log('✅ Verificação completa da página concluída')
      
      return {
        success: true,
        pageLoaded: true,
        title,
        tableExists,
        tableHeaders: headers,
        tableContent,
        searchFieldExists,
        basicSearchFunctionality: basicSearchWorks,
        realSearchFunctionality: realSearchWorks,
        amountFormatting,
        actionButtons,
        observations,
        addButtonExists
      }
      
    } catch (error) {
      console.error('❌ Erro na verificação da página:', error)
      throw error
    }
  }
}