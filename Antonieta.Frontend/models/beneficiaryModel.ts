export default class Beneficiary {
  public id: number = 0
  public name: string = ''
  public document: string = ''
  
  // Endereço estruturado
  public street: string = ''
  public number: string | null = null
  public neighborhood: string = ''
  public city: string = 'Pindamonhangaba'
  public state: string = 'SP'
  public zip_code: string | null = null
  public complement: string | null = null
  

  // full_address como computed property do backend
  public full_address?: string
  
  public contact: string = ''
  public mother_name: string | null = null
  public birth_date: string | null = null
  public qtd_dogs: number = 0
  public qtd_castred_dogs: number = 0
  public qtd_cats: number = 0
  public qtd_castred_cats: number = 0
  public government_benefit: boolean = false
  public receives_basic_basket: boolean = false
  
  // CadÚnico (Cadastro Único)
  public cadunico_code: string | null = null
  public income_range: string | null = null
  
  public how_did_you_hear: string | null = null
  public observations: string | null = null

  // Método para formatar endereço no frontend (backup)
  public getFormattedAddress(): string {
    if (this.full_address) {
      // Se o backend já forneceu o endereço formatado, usar ele
      return this.full_address
    }

    // Caso contrário, formatar no frontend
    const addressParts: string[] = []
    
    if (this.street) {
      addressParts.push(this.street)
    }
    
    if (this.number) {
      addressParts.push(`nº ${this.number}`)
    }
    
    if (this.complement) {
      addressParts.push(`(${this.complement})`)
    }
    
    if (this.neighborhood) {
      addressParts.push(`- ${this.neighborhood}`)
    }
    
    if (this.city && this.city !== "Pindamonhangaba") {
      addressParts.push(`- ${this.city}`)
    }
    
    if (this.state && this.state !== "SP") {
      addressParts.push(`/${this.state}`)
    }
    
    return addressParts.join(' ')
  }

  // Método para validar endereço
  public isAddressValid(): boolean {
    return !!(this.street && this.neighborhood)
  }

  // Método estático para criar instância a partir de dados do backend
  public static fromBackend(data: any): Beneficiary {
    const beneficiary = new Beneficiary()
    
    beneficiary.id = data.id || 0
    beneficiary.name = data.name || ''
    beneficiary.document = data.document || ''
    
    // Endereço estruturado
    beneficiary.street = data.street || ''
    beneficiary.number = data.number || null
    beneficiary.neighborhood = data.neighborhood || ''
    beneficiary.city = data.city || 'Pindamonhangaba'
    beneficiary.state = data.state || 'SP'
    beneficiary.zip_code = data.zip_code || null
    beneficiary.complement = data.complement || null
    beneficiary.full_address = data.full_address || null
    
    beneficiary.contact = data.contact || ''
    beneficiary.mother_name = data.mother_name || null
    beneficiary.birth_date = data.birth_date || null
    beneficiary.qtd_dogs = parseInt(data.qtd_dogs) || 0
    beneficiary.qtd_castred_dogs = parseInt(data.qtd_castred_dogs) || 0
    beneficiary.qtd_cats = parseInt(data.qtd_cats) || 0
    beneficiary.qtd_castred_cats = parseInt(data.qtd_castred_cats) || 0
    beneficiary.government_benefit = Boolean(data.government_benefit)
    beneficiary.receives_basic_basket = Boolean(data.receives_basic_basket)
    beneficiary.how_did_you_hear = data.how_did_you_hear || null
    beneficiary.observations = data.observations || null
    
    return beneficiary
  }

  // Método para converter para formato do backend
  public toBackend(): any {
    return {
      id: this.id,
      name: this.name,
      document: this.document,
      
      // Endereço estruturado
      street: this.street,
      number: this.number,
      neighborhood: this.neighborhood,
      city: this.city,
      state: this.state,
      zip_code: this.zip_code,
      complement: this.complement,
      
      contact: this.contact,
      mother_name: this.mother_name,
      birth_date: this.birth_date,
      qtd_dogs: this.qtd_dogs,
      qtd_castred_dogs: this.qtd_castred_dogs,
      qtd_cats: this.qtd_cats,
      qtd_castred_cats: this.qtd_castred_cats,
      government_benefit: this.government_benefit,
      receives_basic_basket: this.receives_basic_basket,
      how_did_you_hear: this.how_did_you_hear,
      observations: this.observations
    }
  }
}

// Interface para compatibilidade
export interface IBeneficiary {
  id?: number
  name: string
  document: string
  street: string
  number?: string | null
  neighborhood: string
  city?: string
  state?: string
  zip_code?: string | null
  complement?: string | null
  full_address?: string
  contact: string
  mother_name?: string | null
  birth_date?: string | null
  qtd_dogs?: number
  qtd_castred_dogs?: number
  qtd_cats?: number
  qtd_castred_cats?: number
  government_benefit?: boolean
  receives_basic_basket?: boolean
  how_did_you_hear?: string | null
  observations?: string | null
}