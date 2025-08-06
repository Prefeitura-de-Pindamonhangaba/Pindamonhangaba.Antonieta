export const testData = {
  beneficiaries: {
    valid: {
      name: 'João Silva E2E',
      document: '123.456.789-00',
      address: 'Rua das Flores, 123',
      contact: '(12) 99999-9999',
      monthlyLimit: 4.0,
      motherName: 'Maria Silva',
      birthDate: '1990-01-15'
    },
    
    withDecimals: {
      name: 'Ana Costa Decimal E2E',
      document: '987.654.321-00',
      address: 'Av. Principal, 456',
      contact: '(12) 88888-8888',
      monthlyLimit: 7.25 // ✅ Valor decimal crítico
    }
  }
}