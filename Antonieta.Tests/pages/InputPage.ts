import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class InputPage extends BasePage {
  selectors = {
    pageTitle: 'h1, .n-h1',
    dataTable: '.n-data-table',
    tableHeaders: '.n-data-table thead th',
    tableRows: '.n-data-table tbody tr',
    emptyMessage: '.n-empty, .no-data',
    searchField: 'input[placeholder*="Buscar"]'
  }

  async navigateToPage() {
    await this.navigate('/inputs')
    await this.page.waitForLoadState('domcontentloaded')
    await this.page.waitForSelector(this.selectors.dataTable, { timeout: 15000 })
  }

  async verifyPageTitle() {
    const title = await this.page.locator(this.selectors.pageTitle).first().textContent()
    expect(title?.toLowerCase()).toContain('entrada')
    return title
  }

  async verifyTableExists() {
    const tableVisible = await this.page.isVisible(this.selectors.dataTable)
    expect(tableVisible).toBe(true)
  }

  async getTableHeaders() {
    const headers = await this.page.locator(this.selectors.tableHeaders).allTextContents()
    expect(headers.length).toBeGreaterThan(0)
    return headers
  }

  async verifyTableContent() {
    const rowCount = await this.page.locator(this.selectors.tableRows).count()
    if (rowCount > 0) {
      const firstRow = await this.page.locator(this.selectors.tableRows).first().textContent()
      expect(firstRow).not.toBe('')
      return rowCount
    } else {
      const emptyVisible = await this.page.locator(this.selectors.emptyMessage).isVisible().catch(() => false)
      expect(emptyVisible).toBe(true)
      return 0
    }
  }

  async verifySearchField() {
    const searchField = this.page.locator(this.selectors.searchField)
    expect(await searchField.isVisible()).toBe(true)
    const placeholder = await searchField.getAttribute('placeholder')
    expect(placeholder).toContain('ração')
    return searchField
  }

  async testSearchFunctionality() {
    const searchField = await this.verifySearchField()
    await searchField.fill('teste')
    expect(await searchField.inputValue()).toBe('teste')
    await searchField.fill('')
    expect(await searchField.inputValue()).toBe('')
  }

  async testFilterByRationType() {
    const rowCount = await this.page.locator(this.selectors.tableRows).count()
    if (rowCount > 0) {
      const rationType = await this.page.locator(this.selectors.tableRows + ' td').nth(1).textContent()
      const searchField = this.page.locator(this.selectors.searchField)
      const searchTerm = rationType?.slice(0, 3) || ''
      await searchField.fill(searchTerm)
      await this.page.waitForTimeout(1000)
      const filteredCount = await this.page.locator(this.selectors.tableRows).count()
      expect(filteredCount).toBeLessThanOrEqual(rowCount)
      await searchField.fill('')
      await this.page.waitForTimeout(500)
    }
  }
}