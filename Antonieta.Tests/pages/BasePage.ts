import { Page, expect, Locator } from '@playwright/test'

export class BasePage {
  protected page: Page
  protected baseURL: string

  constructor(page: Page) {
    this.page = page
    this.baseURL = process.env.FRONTEND_URL || 'http://localhost:3000'
  }

  async navigate(path: string = '/') {
    const url = `${this.baseURL}${path}`
    console.log(`🔗 Navegando para: ${url}`)
    await this.page.goto(url)
    await this.page.waitForLoadState('networkidle')
  }

  async waitForElement(selector: string, timeout = 10000): Promise<Locator> {
    return this.page.waitForSelector(selector, { timeout })
  }

  async clickButton(text: string) {
    await this.page.click(`button:has-text("${text}")`)
  }

  async fillField(selector: string, value: string) {
    await this.page.fill(selector, value)
  }

  async expectToast(message: string, type: 'success' | 'error' | 'warning' | 'info' = 'success') {
    const toastSelector = `.n-message`
    await expect(this.page.locator(toastSelector)).toContainText(message, { timeout: 5000 })
  }

  async expectPageTitle(title: string) {
    await expect(this.page).toHaveTitle(new RegExp(title, 'i'))
  }

  async expectElementVisible(selector: string) {
    await expect(this.page.locator(selector)).toBeVisible()
  }

  async expectElementHidden(selector: string) {
    await expect(this.page.locator(selector)).not.toBeVisible()
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ 
      path: `test-results/screenshots/${name}-${Date.now()}.png`,
      fullPage: true 
    })
  }
}