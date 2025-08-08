import { Page, expect } from '@playwright/test'

export class DistributionDetailsModalOperator {
  constructor(public page: Page) {}

  selectors = {
    modal: '.n-modal:has-text("Detalhes da Distribuição")',
    closeButton: 'button:has-text("Fechar")'
  }

  async isOpen() {
    return await this.page.isVisible(this.selectors.modal)
  }

  async close() {
    await this.page.click(this.selectors.closeButton)
  }
}