import { Page, expect } from '@playwright/test'

export class BeneficiaryModalOperator {
  constructor(public page: Page) {}

  selectors = {
    modal: '.n-modal:has-text("Beneficiário")',
    nameInput: 'input[placeholder*="nome"]',
    documentInput: 'input[placeholder*="documento"]',
    addressInput: 'input[placeholder*="endereço"]',
    contactInput: 'input[placeholder*="contato"]',
    limitInput: 'input[placeholder*="limite"]',
    saveButton: 'button:has-text("Salvar")',
    cancelButton: 'button:has-text("Cancelar")'
  }

  async isOpen() {
    return await this.page.isVisible(this.selectors.modal)
  }

  async fillForm({ name, document, address, contact, limit }: { name: string, document: string, address: string, contact: string, limit: number }) {
    await this.page.fill(this.selectors.nameInput, name)
    await this.page.fill(this.selectors.documentInput, document)
    await this.page.fill(this.selectors.addressInput, address)
    await this.page.fill(this.selectors.contactInput, contact)
    await this.page.fill(this.selectors.limitInput, limit.toString())
  }

  async save() {
    await this.page.click(this.selectors.saveButton)
  }

  async cancel() {
    await this.page.click(this.selectors.cancelButton)
  }
}