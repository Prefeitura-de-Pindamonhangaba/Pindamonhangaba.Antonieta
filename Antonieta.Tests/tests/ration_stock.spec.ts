import { test, expect } from '@playwright/test'
import { AuthHelper } from '../helpers/authHelper'
import { RationStockPage } from '../pages/RationStockPage'

test.describe('Estoque de Rações - Exibição e Busca', () => {
  let rationStockPage: RationStockPage

  test.beforeEach(async ({ page }) => {
    rationStockPage = new RationStockPage(page)
    const loginSuccess = await AuthHelper.login(page)
    expect(loginSuccess).toBe(true)
    await rationStockPage.navigateToPage()
  })

  test('deve exibir o título da página', async () => {
    await rationStockPage.verifyPageTitle()
  })

  test('deve exibir a tabela de estoques', async () => {
    await rationStockPage.verifyTableExists()
    const headers = await rationStockPage.getTableHeaders()
    expect(headers.join(' ').toLowerCase()).toContain('nome')
    expect(headers.join(' ').toLowerCase()).toContain('estoque')
  })

  test('deve exibir dados na tabela ou mensagem de tabela vazia', async () => {
    await rationStockPage.verifyTableContent()
  })

  test('deve exibir campo de busca', async () => {
    await rationStockPage.verifySearchField()
  })

  test('deve aceitar texto no campo de busca', async () => {
    await rationStockPage.testSearchFunctionality()
  })

  test('deve filtrar resultados ao buscar por nome ou descrição', async () => {
    await rationStockPage.testFilterByNameOrDescription()
  })
})