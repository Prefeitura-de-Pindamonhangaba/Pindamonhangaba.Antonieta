export default class Beneficiary {
  public id: number = 0
  public name: string = ''
  public document: string = ''
  public address: string = ''
  public contact: string = ''
  public monthly_limit: number = 0
  public mother_name: string | null = null
  public birth_date: string | null = null
  public qtd_dogs: number = 0
  public qtd_castred_dogs: number = 0
  public qtd_cats: number = 0
  public qtd_castred_cats: number = 0
  public government_benefit: boolean = false
  public receives_basic_basket: boolean = false
  public how_did_you_hear: string | null = null
  public observations: string | null = null
}