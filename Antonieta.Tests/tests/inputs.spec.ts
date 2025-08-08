import { test, expect } from '@playwright/test'
import { AuthHelper } from '../helpers/authHelper'
import { InputPage } from '../pages/InputPage'

test.describe('Entradas de Ração - Exibição e Busca', () => {
  let inputPage: InputPage

  test.beforeEach(async ({ page }) => {
    inputPage = new InputPage(page)
    const loginSuccess = await AuthHelper.login(page)
    expect(loginSuccess).toBe(true)
    await inputPage.navigateToPage()
  })

  test('deve exibir o título da página', async () => {
    await inputPage.verifyPageTitle()
  })

  test('deve exibir a tabela de entradas', async () => {
    await inputPage.verifyTableExists()
    const headers = await inputPage.getTableHeaders()
    expect(headers.join(' ').toLowerCase()).toContain('tipo')
    expect(headers.join(' ').toLowerCase()).toContain('quantidade')
  })

  test('deve exibir dados na tabela ou mensagem de tabela vazia', async () => {
    await inputPage.verifyTableContent()
  })

  test('deve exibir campo de busca', async () => {
    await inputPage.verifySearchField()
  })

  test('deve aceitar texto no campo de busca', async () => {
    await inputPage.testSearchFunctionality()
  })

  test('deve filtrar resultados ao buscar por tipo de ração', async () => {
    await inputPage.testFilterByRationType()
  })
})