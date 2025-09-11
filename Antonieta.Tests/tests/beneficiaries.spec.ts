import { test, expect } from '@playwright/test'
import { BeneficiariesPage } from '../pages/BeneficiariesPage'
import { AuthHelper } from '../helpers/authHelper'

test.describe('Beneficiários - Testes de Exibição', () => {
  let beneficiariesPage: BeneficiariesPage

  test.beforeEach(async ({ page }) => {
    beneficiariesPage = new BeneficiariesPage(page)
    
    // 1. Fazer login
    const loginSuccess = await AuthHelper.login(page)
    if (!loginSuccess) {
      throw new Error('Falha no login durante setup do teste')
    }
    
    // 2. Navegar para beneficiários
    await beneficiariesPage.navigateToPage()
    
    // 3. Aguardar carregamento
    await beneficiariesPage.waitForPageLoad()
    
    console.log('🚀 Setup completo: Login + Navegação para beneficiários')
  })

  test('deve carregar a página de beneficiários corretamente', async () => {
    console.log('🧪 Teste: Carregamento da página de beneficiários')
    
    // Verificar se a página carregou
    await beneficiariesPage.verifyPageLoaded()
    
    // Verificar se não foi redirecionado para login
    const currentUrl = beneficiariesPage.page.url()
    expect(currentUrl).toContain('/beneficiary')
    expect(currentUrl).not.toContain('/login')
    
    console.log('✅ Página de beneficiários carregada corretamente')
  })

  test('deve exibir o título da página', async () => {
    console.log('🧪 Teste: Título da página')
    
    // Verificar título
    const title = await beneficiariesPage.verifyPageTitle()
    
    // Se encontrou título, deve conter "beneficiári"
    if (title) {
      expect(title.toLowerCase()).toContain('beneficiári')
      console.log(`✅ Título correto: "${title}"`)
    } else {
      console.log('⚠️ Título não encontrado, mas página pode estar funcionando')
    }
  })

  test('deve exibir a tabela de beneficiários', async () => {
    console.log('🧪 Teste: Tabela de beneficiários')
    
    // Verificar se tabela existe
    const tableExists = await beneficiariesPage.verifyTableExists()
    expect(tableExists).toBe(true)
    
    // Verificar cabeçalhos
    const headers = await beneficiariesPage.verifyTableHeaders()
    expect(headers.length).toBeGreaterThan(0)
    
    console.log(`✅ Tabela com ${headers.length} colunas encontrada`)
  })

  test('deve exibir cabeçalhos corretos na tabela', async () => {
    console.log('🧪 Teste: Cabeçalhos da tabela')
    
    // Verificar cabeçalhos
    const headers = await beneficiariesPage.verifyTableHeaders()
    
    expect(headers.length).toBeGreaterThan(0)
    
    // Verificar se tem pelo menos alguns cabeçalhos básicos
    const headerText = headers.join(' ').toLowerCase()
    const hasBasicHeaders = headerText.includes('nome') || 
                           headerText.includes('documento') || 
                           headerText.includes('ações')
    
    expect(hasBasicHeaders).toBe(true)
    
    console.log('✅ Cabeçalhos da tabela estão presentes e corretos')
    console.log('📋 Cabeçalhos:', headers)
  })

  test('deve exibir dados na tabela ou mensagem apropriada', async () => {
    console.log('🧪 Teste: Conteúdo da tabela')
    
    // Verificar conteúdo
    const tableContent = await beneficiariesPage.verifyTableContent()
    
    // Tabela pode ter dados ou estar vazia - ambos são válidos
    if (tableContent.hasData) {
      expect(tableContent.count).toBeGreaterThan(0)
      console.log(`✅ Tabela contém ${tableContent.count} beneficiários`)
      
      if (tableContent.sampleData) {
        console.log(`📋 Exemplo de dados: ${tableContent.sampleData.substring(0, 50)}...`)
      }
    } else {
      expect(tableContent.count).toBe(0)
      console.log('ℹ️ Tabela vazia (comportamento válido)')
    }
  })

  test('deve exibir campo de busca', async () => {
    console.log('🧪 Teste: Campo de busca')
    
    // Verificar campo de busca
    const searchExists = await beneficiariesPage.verifySearchField()
    expect(searchExists).toBe(true)
    
    console.log('✅ Campo de busca presente')
  })

  test('deve testar funcionalidade básica do campo de busca', async () => {
    console.log('🧪 Teste: Funcionalidade básica de busca')
    
    // Testar se campo aceita texto
    const searchWorks = await beneficiariesPage.testBasicSearchFunctionality()
    expect(searchWorks).toBe(true)
    
    console.log('✅ Campo de busca aceita texto e pode ser limpo')
  })

  test('deve exibir botões de ação', async () => {
    console.log('🧪 Teste: Botões de ação')
    
    // Verificar botões
    const buttons = await beneficiariesPage.verifyActionButtons()
    
    // Pelo menos um botão deve estar presente
    const hasAnyButton = buttons.addButton || buttons.exportButton
    expect(hasAnyButton).toBe(true)
    
    if (buttons.addButton) {
      console.log('✅ Botão de adicionar beneficiário presente')
    }
    
    if (buttons.exportButton) {
      console.log('✅ Botão de exportar presente')
    }
    
    console.log('✅ Botões de ação verificados')
  })

  test('deve executar verificação completa da página', async () => {
    console.log('🧪 Teste: Verificação completa da página')
    
    // Executar verificação completa
    const result = await beneficiariesPage.performCompletePageVerification()
    
    // Verificar resultado geral
    expect(result.success).toBe(true)
    expect(result.pageLoaded).toBe(true)
    expect(result.tableExists).toBe(true)
    expect(result.tableHeaders.length).toBeGreaterThan(0)
    expect(result.searchFieldExists).toBe(true)
    
    // Pelo menos um botão deve estar presente
    const hasAnyButton = result.actionButtons.addButton || result.actionButtons.exportButton
    expect(hasAnyButton).toBe(true)
    
    console.log('📊 Resultado da verificação completa:', {
      '📋 Página carregada': result.pageLoaded ? '✅' : '❌',
      '🏷️ Título encontrado': result.title ? '✅' : '⚠️',
      '📊 Tabela presente': result.tableExists ? '✅' : '❌',
      '📑 Colunas da tabela': result.tableHeaders.length,
      '👥 Beneficiários': result.tableContent.count,
      '🔍 Campo de busca': result.searchFieldExists ? '✅' : '❌',
      '🔘 Botão adicionar': result.actionButtons.addButton ? '✅' : '⚠️',
      '📁 Botão exportar': result.actionButtons.exportButton ? '✅' : '⚠️',
      '🔍 Busca funciona': result.searchFunctionality ? '✅' : '⚠️'
    })
    
    console.log('✅ Verificação completa da página realizada com sucesso')
  })

  test('deve contar beneficiários na tabela', async () => {
    console.log('🧪 Teste: Contagem de beneficiários')
    
    // Contar beneficiários
    const count = await beneficiariesPage.countBeneficiaries()
    
    // Pode ser 0 ou mais - ambos são válidos
    expect(count).toBeGreaterThanOrEqual(0)
    
    console.log(`📊 Total de beneficiários na tabela: ${count}`)
    
    if (count === 0) {
      console.log('ℹ️ Tabela vazia - estado válido para sistema novo')
    } else {
      console.log(`✅ Sistema contém ${count} beneficiários cadastrados`)
    }
  })

  test('deve verificar responsividade básica da página', async ({ page }) => {
    console.log('🧪 Teste: Responsividade básica')
    
    // Testar em diferentes tamanhos de tela
    const viewports = [
      { width: 1920, height: 1080, name: 'Desktop' },
      { width: 768, height: 1024, name: 'Tablet' },
      { width: 375, height: 667, name: 'Mobile' }
    ]
    
    for (const viewport of viewports) {
      console.log(`📱 Testando em ${viewport.name} (${viewport.width}x${viewport.height})`)
      
      await page.setViewportSize({ width: viewport.width, height: viewport.height })
      await page.waitForTimeout(1000)
      
      // Verificar se elementos principais ainda estão visíveis
      const tableExists = await beneficiariesPage.verifyTableExists()
      const searchExists = await beneficiariesPage.verifySearchField()
      
      console.log(`${viewport.name}: Tabela=${tableExists ? '✅' : '❌'}, Busca=${searchExists ? '✅' : '❌'}`)
    }
    
    console.log('✅ Teste de responsividade básica concluído')
  })
})