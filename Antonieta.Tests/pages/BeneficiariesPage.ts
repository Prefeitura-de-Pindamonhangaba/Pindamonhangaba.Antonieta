import { Page, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export interface BeneficiaryData {
  name: string
  document: string
  address: string
  contact: string
  monthlyLimit: number
  motherName?: string
  birthDate?: string
}

export class BeneficiariesPage extends BasePage {
  // Seletores básicos - ajuste conforme sua aplicação
  private selectors = {
    // Navegação
    title: 'h1',
    addButton: 'button:has-text("Novo"), button:has-text("Adicionar"), button:has-text("Cadastrar")',
    
    // Tabela
    table: 'table, [data-testid*="table"], .n-data-table',
    
    // Modal
    modal: '.n-modal, [role="dialog"]',
    
    // Formulário (seletores genéricos que funcionam com Naive UI)
    form: {
      name: 'input[placeholder*="nome" i], input[placeholder*="Nome" i]',
      document: 'input[placeholder*="documento" i], input[placeholder*="cpf" i], input[placeholder*="rg" i]',
      address: 'input[placeholder*="endereço" i], input[placeholder*="endereco" i]',
      contact: 'input[placeholder*="contato" i], input[placeholder*="telefone" i]',
      monthlyLimit: 'input[placeholder*="limite" i], input[placeholder*="mensal" i]',
      motherName: 'input[placeholder*="mãe" i], input[placeholder*="mae" i]',
      birthDate: 'input[type="date"], .n-date-picker input',
      submitButton: 'button:has-text("Salvar"), button:has-text("Confirmar"), button[type="submit"]',
      cancelButton: 'button:has-text("Cancelar")'
    }
  }

  async navigateToPage() {
    await this.navigate('/beneficiary')
    await this.page.waitForLoadState('domcontentloaded')
    console.log('✅ Navegou para página de beneficiários')
  }

  async openAddModal() {
    console.log('🔍 Procurando botão de adicionar...')
    await this.page.click(this.selectors.addButton)
    await this.page.waitForSelector(this.selectors.modal, { timeout: 5000 })
    console.log('✅ Modal de criação aberto')
  }

  async fillBeneficiaryForm(data: BeneficiaryData) {
    console.log('📝 Preenchendo formulário...', data)
    
    // Campos obrigatórios
    await this.page.fill(this.selectors.form.name, data.name)
    await this.page.fill(this.selectors.form.document, data.document)
    await this.page.fill(this.selectors.form.address, data.address)
    await this.page.fill(this.selectors.form.contact, data.contact)
    
    // ✅ CAMPO CRÍTICO: monthly_limit
    await this.page.fill(this.selectors.form.monthlyLimit, data.monthlyLimit.toString())
    console.log(`💰 Monthly limit preenchido: ${data.monthlyLimit}`)
    
    // Campos opcionais
    if (data.motherName) {
      await this.page.fill(this.selectors.form.motherName, data.motherName)
    }
    
    if (data.birthDate) {
      await this.page.fill(this.selectors.form.birthDate, data.birthDate)
    }
    
    console.log('✅ Formulário preenchido')
  }

  async submitForm() {
    console.log('📤 Submetendo formulário...')
    await this.page.click(this.selectors.form.submitButton)
  }

  async expectBeneficiaryInTable(name: string) {
    console.log(`🔍 Procurando beneficiário na tabela: ${name}`)
    await expect(this.page.locator(this.selectors.table)).toContainText(name, { timeout: 10000 })
    console.log('✅ Beneficiário encontrado na tabela')
  }

  async expectMonthlyLimitInTable(name: string, expectedLimit: number) {
    console.log(`🔍 Verificando limite mensal na tabela: ${expectedLimit}`)
    const tableRow = this.page.locator(`tr:has-text("${name}")`)
    await expect(tableRow).toContainText(expectedLimit.toString(), { timeout: 5000 })
    console.log('✅ Limite mensal correto na tabela')
  }
}