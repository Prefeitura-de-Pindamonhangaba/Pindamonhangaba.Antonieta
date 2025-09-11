import { Page, expect } from '@playwright/test'

export class InputModalOperator {
  constructor(public page: Page) {}

  selectors = {
    modal: '.n-modal:has-text("Nova Entrada")',
    rationTypeSelect: 'input[placeholder*="tipo de ração"]',
    amountInput: 'input[type="number"]',
    dateInput: 'input[type="date"]',
    saveButton: 'button:has-text("Salvar")',
    cancelButton: 'button:has-text("Cancelar")'
  }

  async isOpen() {
    return await this.page.isVisible(this.selectors.modal)
  }

  async fillForm({ rationType, amount, date }: { rationType: string, amount: number, date: string }) {
    await this.page.fill(this.selectors.rationTypeSelect, rationType)
    await this.page.fill(this.selectors.amountInput, amount.toString())
    await this.page.fill(this.selectors.dateInput, date)
  }

  async save() {
    await this.page.click(this.selectors.saveButton)
  }

  async cancel() {
    await this.page.click(this.selectors.cancelButton)
  }
}