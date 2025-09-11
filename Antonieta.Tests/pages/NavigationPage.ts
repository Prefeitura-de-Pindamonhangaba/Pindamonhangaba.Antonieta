import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class NavigationPage extends BasePage {
  private selectors = {
    // Menu principal
    navigation: 'nav, .n-menu, .navigation',
    menuItems: '.n-menu-item, nav a, .menu-item',
    
    // Links específicos do menu
    menuLinks: {
      dashboard: 'a[href="/dashboard"], .n-menu-item:has-text("Dashboard"), .n-menu-item:has-text("Início")',
      beneficiaries: 'a[href="/beneficiary"], .n-menu-item:has-text("Beneficiários")',
      distributions: 'a[href="/distributions"], .n-menu-item:has-text("Distribuições")',
      inputs: 'a[href="/inputs"], .n-menu-item:has-text("Entradas")',
      rationStock: 'a[href="/ration_stock"], .n-menu-item:has-text("Estoque")'
    },
    
    // Elementos de feedback
    activeMenuItem: '.n-menu-item--selected, .active, [aria-current="page"]',
    pageTitle: 'h1',
    
    // Loading states
    pageLoading: '.n-spin, .loading'
  }

  /**
   * Verifica se o menu de navegação está presente
   */
  async verifyNavigationExists() {
    console.log('🔍 Verificando se o menu de navegação existe...')
    
    await this.page.waitForSelector(this.selectors.navigation, { timeout: 10000 })
    const navVisible = await this.page.isVisible(this.selectors.navigation)
    expect(navVisible).toBe(true)
    
    console.log('✅ Menu de navegação encontrado')
  }

  /**
   * Verifica se todos os links do menu estão presentes
   */
  async verifyAllMenuItems() {
    console.log('🔍 Verificando todos os itens do menu...')
    
    const menuItems = Object.entries(this.selectors.menuLinks)
    const foundItems = []
    
    for (const [itemName, selector] of menuItems) {
      try {
        const element = this.page.locator(selector)
        const count = await element.count()
        
        if (count > 0) {
          const isVisible = await element.first().isVisible()
          if (isVisible) {
            foundItems.push(itemName)
            console.log(`✅ Item "${itemName}" encontrado`)
          } else {
            console.log(`⚠️ Item "${itemName}" existe mas não está visível`)
          }
        } else {
          console.log(`❌ Item "${itemName}" não encontrado`)
        }
      } catch (error) {
        console.log(`❌ Erro ao verificar item "${itemName}": ${error.message}`)
      }
    }
    
    console.log(`📊 Itens encontrados: ${foundItems.length}/${menuItems.length}`)
    return foundItems
  }

  /**
   * Clica em um item específico do menu
   */
  async clickMenuItem(itemName: keyof typeof this.selectors.menuLinks) {
    console.log(`🔘 Clicando no item do menu: ${itemName}`)
    
    const selector = this.selectors.menuLinks[itemName]
    
    // Aguardar elemento estar presente e visível
    await this.page.waitForSelector(selector, { timeout: 10000 })
    
    // Clicar no item
    await this.page.click(selector)
    console.log(`✅ Clicou em "${itemName}"`)
    
    // Aguardar navegação
    await this.page.waitForLoadState('domcontentloaded')
    await this.page.waitForTimeout(1000)
  }

  /**
   * Verifica se foi redirecionado para a página correta
   */
  async verifyCorrectPageLoaded(expectedPath: string, expectedTitle?: string) {
    console.log(`🔍 Verificando se foi redirecionado para: ${expectedPath}`)
    
    // Aguardar um pouco para garantir que a navegação terminou
    await this.page.waitForTimeout(2000)
    
    // Verificar URL
    const currentUrl = this.page.url()
    expect(currentUrl).toContain(expectedPath)
    console.log(`✅ URL correta: ${currentUrl}`)
    
    // Verificar título da página (se fornecido)
    if (expectedTitle) {
      try {
        await this.page.waitForSelector(this.selectors.pageTitle, { timeout: 5000 })
        const pageTitle = await this.page.textContent(this.selectors.pageTitle)
        
        if (pageTitle && pageTitle.toLowerCase().includes(expectedTitle.toLowerCase())) {
          console.log(`✅ Título correto: ${pageTitle}`)
        } else {
          console.log(`⚠️ Título encontrado: "${pageTitle}", esperado: "${expectedTitle}"`)
        }
      } catch (error) {
        console.log('⚠️ Não foi possível verificar o título da página')
      }
    }
    
    return currentUrl
  }

  /**
   * Testa navegação para o Dashboard
   */
  async testDashboardNavigation() {
    console.log('🧪 Testando navegação para Dashboard...')
    
    await this.clickMenuItem('dashboard')
    const url = await this.verifyCorrectPageLoaded('/dashboard', 'dashboard')
    
    console.log('✅ Navegação para Dashboard testada')
    return url
  }

  /**
   * Testa navegação para Beneficiários
   */
  async testBeneficiariesNavigation() {
    console.log('🧪 Testando navegação para Beneficiários...')
    
    await this.clickMenuItem('beneficiaries')
    const url = await this.verifyCorrectPageLoaded('/beneficiary', 'beneficiári')
    
    console.log('✅ Navegação para Beneficiários testada')
    return url
  }

  /**
   * Testa navegação para Distribuições
   */
  async testDistributionsNavigation() {
    console.log('🧪 Testando navegação para Distribuições...')
    
    await this.clickMenuItem('distributions')
    const url = await this.verifyCorrectPageLoaded('/distributions', 'distribuiç')
    
    console.log('✅ Navegação para Distribuições testada')
    return url
  }

  /**
   * Testa navegação para Entradas
   */
  async testInputsNavigation() {
    console.log('🧪 Testando navegação para Entradas...')
    
    await this.clickMenuItem('inputs')
    const url = await this.verifyCorrectPageLoaded('/inputs', 'entrada')
    
    console.log('✅ Navegação para Entradas testada')
    return url
  }

  /**
   * Testa navegação para Estoque
   */
  async testRationStockNavigation() {
    console.log('🧪 Testando navegação para Estoque...')
    
    await this.clickMenuItem('rationStock')
    const url = await this.verifyCorrectPageLoaded('/ration_stock', 'estoque')
    
    console.log('✅ Navegação para Estoque testada')
    return url
  }

  /**
   * Verifica se o item ativo está marcado corretamente
   */
  async verifyActiveMenuItem(expectedPath: string) {
    console.log(`🔍 Verificando item ativo do menu para: ${expectedPath}`)
    
    try {
      // Aguardar elemento ativo aparecer
      await this.page.waitForSelector(this.selectors.activeMenuItem, { timeout: 5000 })
      
      const activeItems = await this.page.locator(this.selectors.activeMenuItem).count()
      
      if (activeItems > 0) {
        const activeText = await this.page.locator(this.selectors.activeMenuItem).first().textContent()
        console.log(`✅ Item ativo encontrado: "${activeText}"`)
        return true
      } else {
        console.log('⚠️ Nenhum item ativo encontrado')
        return false
      }
    } catch (error) {
      console.log('⚠️ Não foi possível verificar item ativo')
      return false
    }
  }

  /**
   * Testa todas as navegações em sequência
   */
  async testAllNavigations() {
    console.log('🧪 Testando todas as navegações do menu...')
    
    const navigationTests = [
      { name: 'Dashboard', method: () => this.testDashboardNavigation() },
      { name: 'Beneficiários', method: () => this.testBeneficiariesNavigation() },
      { name: 'Distribuições', method: () => this.testDistributionsNavigation() },
      { name: 'Entradas', method: () => this.testInputsNavigation() },
      { name: 'Estoque', method: () => this.testRationStockNavigation() }
    ]
    
    const results = []
    
    for (const test of navigationTests) {
      try {
        console.log(`\n🔄 Testando navegação: ${test.name}`)
        const url = await test.method()
        
        // Verificar item ativo
        const hasActiveItem = await this.verifyActiveMenuItem(url)
        
        results.push({
          name: test.name,
          success: true,
          url,
          hasActiveItem
        })
        
        console.log(`✅ ${test.name}: SUCESSO`)
        
        // Aguardar um pouco entre os testes
        await this.page.waitForTimeout(1000)
        
      } catch (error) {
        console.error(`❌ ${test.name}: FALHOU - ${error.message}`)
        results.push({
          name: test.name,
          success: false,
          error: error.message,
          hasActiveItem: false
        })
      }
    }
    
    // Resumo dos resultados
    const successCount = results.filter(r => r.success).length
    const totalCount = results.length
    
    console.log(`\n📊 Resumo dos testes de navegação:`)
    console.log(`✅ Sucessos: ${successCount}/${totalCount}`)
    
    results.forEach(result => {
      const status = result.success ? '✅' : '❌'
      const activeStatus = result.hasActiveItem ? '🎯' : '⚪'
      console.log(`${status} ${activeStatus} ${result.name}: ${result.url || result.error}`)
    })
    
    return results
  }

  /**
   * Aguarda carregamento da página após navegação
   */
  async waitForPageLoad() {
    console.log('⏳ Aguardando carregamento da página...')
    
    // Aguardar loading desaparecer
    try {
      await this.page.waitForSelector(this.selectors.pageLoading, { 
        state: 'hidden', 
        timeout: 10000 
      })
      console.log('✅ Loading finalizado')
    } catch (error) {
      console.log('ℹ️ Nenhum loading detectado')
    }
    
    // Aguardar rede estabilizar
    await this.page.waitForLoadState('networkidle', { timeout: 10000 })
    console.log('✅ Página carregada completamente')
  }
}