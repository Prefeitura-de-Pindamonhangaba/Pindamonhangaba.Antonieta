import { test, expect } from '@playwright/test'
import { BeneficiariesPage, BeneficiaryData } from '../pages/BeneficiariesPage'
import { testData } from '../fixtures/testData'

test.describe('Beneficiários - Testes E2E', () => {
  let beneficiariesPage: BeneficiariesPage

  test.beforeEach(async ({ page }) => {
    beneficiariesPage = new BeneficiariesPage(page)
  })

  test('deve carregar a página de beneficiários', async ({ page }) => {
    console.log('🧪 Teste: Carregar página de beneficiários')
    
    await beneficiariesPage.navigateToPage()
    
    // Verificações básicas
    await expect(page).toHaveURL(/beneficiary/)
    await beneficiariesPage.expectElementVisible('h1')
    
    // Screenshot para debug
    await beneficiariesPage.takeScreenshot('pagina-beneficiarios-carregada')
    
    console.log('✅ Página carregada com sucesso')
  })

  test('🔥 CRÍTICO: deve criar beneficiário com valor decimal', async ({ page }) => {
    console.log('🧪 Teste: Criar beneficiário com decimal')
    
    const beneficiaryData: BeneficiaryData = {
      ...testData.beneficiaries.withDecimals,
      name: `Teste Decimal ${Date.now()}` // Nome único
    }

    try {
      // Navegar para página
      await beneficiariesPage.navigateToPage()
      
      // Screenshot inicial
      await beneficiariesPage.takeScreenshot('antes-criar-beneficiario')

      // Abrir modal
      await beneficiariesPage.openAddModal()
      await beneficiariesPage.takeScreenshot('modal-aberto')

      // Preencher formulário
      await beneficiariesPage.fillBeneficiaryForm(beneficiaryData)
      await beneficiariesPage.takeScreenshot('formulario-preenchido')

      // Submeter
      await beneficiariesPage.submitForm()

      // Aguardar processamento
      await page.waitForTimeout(2000)

      // Verificar sucesso
      await beneficiariesPage.expectToast('sucesso')
      
      // Screenshot final
      await beneficiariesPage.takeScreenshot('beneficiario-criado')

      // ✅ VERIFICAÇÃO CRÍTICA: Valor decimal preservado
      await beneficiariesPage.expectBeneficiaryInTable(beneficiaryData.name)
      await beneficiariesPage.expectMonthlyLimitInTable(beneficiaryData.name, beneficiaryData.monthlyLimit)

      console.log('✅ Beneficiário criado com valor decimal preservado!')
      
    } catch (error) {
      await beneficiariesPage.takeScreenshot('erro-criar-beneficiario')
      throw error
    }
  })

  test('deve validar que a página existe', async ({ page }) => {
    console.log('🧪 Teste: Validação básica de existência')
    
    await beneficiariesPage.navigateToPage()
    
    // Verificação mínima
    await expect(page.locator('body')).toBeVisible()
    
    console.log('✅ Página existe e é acessível')
  })
})