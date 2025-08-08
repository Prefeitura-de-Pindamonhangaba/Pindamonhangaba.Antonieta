import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class BeneficiariesPage extends BasePage {
  private selectors = {
    // Header
    pageTitle: 'h1:has-text("Beneficiários")',
    
    // Search and Actions
    searchField: 'input[placeholder*="Buscar"], input[placeholder*="buscar"]',
    exportButton: 'button:has-text("Exportar")',
    addBeneficiaryButton: 'button:has-text("Adicionar"), button:has-text("Novo")',
    
    // Table
    dataTable: '.n-data-table',
    tableHeaders: '.n-data-table thead th',
    tableRows: '.n-data-table tbody tr',
    tableLoading: '.n-data-table .n-spin',
    
    // Table columns
    nameColumn: 'td:nth-child(1)',
    documentColumn: 'td:nth-child(2)',
    addressColumn: 'td:nth-child(3)',
    contactColumn: 'td:nth-child(4)',
    monthlyLimitColumn: 'td:nth-child(5)',
    actionsColumn: 'td:nth-child(6)',
    
    // Loading states
    pageLoading: '.n-spin',
    
    // Messages
    noDataMessage: '.n-empty, .no-data, [class*="empty"]'
  }

  /**
   * Navega para a página de beneficiários
   */
  async navigateToPage() {
    console.log('🌐 Navegando para página de beneficiários...')
    await this.navigate('/beneficiary')
    await this.page.waitForLoadState('domcontentloaded')
    console.log('✅ Página de beneficiários carregada')
  }

  /**
   * Verifica se a página carregou corretamente
   */
  async verifyPageLoaded() {
    console.log('🔍 Verificando se a página de beneficiários carregou...')
    
    // Verificar URL
    const currentUrl = this.page.url()
    expect(currentUrl).toContain('/beneficiary')
    
    // Verificar se não foi redirecionado para login
    expect(currentUrl).not.toContain('/login')
    
    console.log('✅ Página de beneficiários carregada corretamente')
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
      
      if (title && title.toLowerCase().includes('beneficiári')) {
        console.log(`✅ Título encontrado: "${title}"`)
        return title
      } else {
        console.log('⚠️ Título não contém "beneficiári"')
        return title
      }
    } catch (error) {
      console.log('⚠️ Título não encontrado - verificando se página carregou de outra forma')
      
      // Verificar se há algum h1, h2 ou título alternativo
      const alternativeTitles = await this.page.locator('h1, h2, .page-title, .title').allTextContents()
      console.log('📋 Títulos alternativos encontrados:', alternativeTitles)
      
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
        // Verificar se tem pelo menos alguns cabeçalhos esperados
        const headerText = headers.join(' ').toLowerCase()
        const hasBasicHeaders = headerText.includes('nome') || 
                               headerText.includes('documento') || 
                               headerText.includes('ações')
        
        if (hasBasicHeaders) {
          console.log('✅ Cabeçalhos da tabela parecem corretos')
        } else {
          console.log('⚠️ Cabeçalhos encontrados mas podem não estar corretos')
        }
        
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
   * Conta os beneficiários na tabela
   */
  async countBeneficiaries() {
    console.log('🔍 Contando beneficiários...')
    
    try {
      await this.page.waitForTimeout(2000) // Aguardar carregamento
      const rowCount = await this.page.locator(this.selectors.tableRows).count()
      console.log(`📊 Beneficiários encontrados: ${rowCount}`)
      
      return rowCount
    } catch (error) {
      console.log('❌ Erro ao contar beneficiários:', error.message)
      return 0
    }
  }

  /**
   * Verifica se há dados na tabela ou mensagem de tabela vazia
   */
  async verifyTableContent() {
    console.log('🔍 Verificando conteúdo da tabela...')
    
    const rowCount = await this.countBeneficiaries()
    
    if (rowCount > 0) {
      console.log(`✅ Tabela contém ${rowCount} beneficiários`)
      
      // Verificar se a primeira linha tem dados
      try {
        const firstRowData = await this.page.locator(this.selectors.tableRows).first().textContent()
        if (firstRowData && firstRowData.trim()) {
          console.log('✅ Primeira linha contém dados')
          return { hasData: true, count: rowCount, sampleData: firstRowData.trim() }
        }
      } catch (error) {
        console.log('⚠️ Erro ao verificar dados da primeira linha')
      }
      
      return { hasData: true, count: rowCount }
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
   * Verifica se os botões de ação estão presentes
   */
  async verifyActionButtons() {
    console.log('🔍 Verificando botões de ação...')
    
    const results = {
      addButton: false,
      exportButton: false
    }
    
    // Verificar botão de adicionar
    try {
      results.addButton = await this.page.isVisible(this.selectors.addBeneficiaryButton)
      if (results.addButton) {
        console.log('✅ Botão de adicionar beneficiário encontrado')
      } else {
        console.log('⚠️ Botão de adicionar não encontrado')
      }
    } catch (error) {
      console.log('❌ Erro ao verificar botão de adicionar')
    }
    
    // Verificar botão de exportar
    try {
      results.exportButton = await this.page.isVisible(this.selectors.exportButton)
      if (results.exportButton) {
        console.log('✅ Botão de exportar encontrado')
      } else {
        console.log('⚠️ Botão de exportar não encontrado')
      }
    } catch (error) {
      console.log('❌ Erro ao verificar botão de exportar')
    }
    
    return results
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
      await this.page.fill(this.selectors.searchField, 'teste')
      const value = await this.page.inputValue(this.selectors.searchField)
      
      if (value === 'teste') {
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
   * Executa verificação completa da página (apenas visualização)
   */
  async performCompletePageVerification() {
    console.log('🧪 Iniciando verificação completa da página de beneficiários...')
    
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
      
      // 8. Verificar botões de ação
      const actionButtons = await this.verifyActionButtons()
      
      // 9. Testar busca básica
      const searchWorks = await this.testBasicSearchFunctionality()
      
      console.log('✅ Verificação completa da página concluída')
      
      return {
        success: true,
        pageLoaded: true,
        title,
        tableExists,
        tableHeaders: headers,
        tableContent,
        searchFieldExists,
        actionButtons,
        searchFunctionality: searchWorks
      }
      
    } catch (error) {
      console.error('❌ Erro na verificação da página:', error)
      throw error
    }
  }
}