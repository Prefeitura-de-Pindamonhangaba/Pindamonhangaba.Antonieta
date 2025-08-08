import { Page, expect } from '@playwright/test'

export class RationTypeModalOperator {
  constructor(public page: Page) {}

  selectors = {
    modal: '.n-modal:has-text("Nova Ração")',
    nameInput: 'input[placeholder="Nome do tipo de ração"]',
    descriptionInput: 'input[placeholder="Descrição do tipo de ração"]',
    saveButton: 'button:has-text("Adicionar")',
    cancelButton: 'button:has-text("Cancelar")'
  }

  async isOpen() {
    return await this.page.isVisible(this.selectors.modal)
  }

  async fillForm({ name, description }: { name: string, description: string }) {
    await this.page.fill(this.selectors.nameInput, name)
    await this.page.fill(this.selectors.descriptionInput, description)
  }

  async save() {
    await this.page.click(this.selectors.saveButton)
  }

  async cancel() {
    await this.page.click(this.selectors.cancelButton)
  }
}