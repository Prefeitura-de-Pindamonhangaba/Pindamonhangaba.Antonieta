import { Page, expect } from '@playwright/test'

export class DistributionModalOperator {
  constructor(public page: Page) {}

  selectors = {
    modal: '.n-modal:has-text("Distribuição")',
    beneficiarySelect: 'input[placeholder*="beneficiário"]',
    rationTypeSelect: 'input[placeholder*="ração"]',
    amountInput: 'input[type="number"]',
    observationsInput: 'textarea[placeholder*="observação"]',
    saveButton: 'button:has-text("Salvar")',
    cancelButton: 'button:has-text("Cancelar")'
  }

  async isOpen() {
    return await this.page.isVisible(this.selectors.modal)
  }

  async fillForm({ beneficiary, rationType, amount, observations }: { beneficiary: string, rationType: string, amount: number, observations?: string }) {
    await this.page.fill(this.selectors.beneficiarySelect, beneficiary)
    await this.page.fill(this.selectors.rationTypeSelect, rationType)
    await this.page.fill(this.selectors.amountInput, amount.toString())
    if (observations) {
      await this.page.fill(this.selectors.observationsInput, observations)
    }
  }

  async save() {
    await this.page.click(this.selectors.saveButton)
  }

  async cancel() {
    await this.page.click(this.selectors.cancelButton)
  }
}