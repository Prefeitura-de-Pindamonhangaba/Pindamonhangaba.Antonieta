export type UserRole = 'comum' | 'gestor' | 'administrador'

export default class User {
  public id: number = 0
  public email: string = ''
  public full_name: string = ''
  public role: UserRole = 'comum'
  public password?: string = ''
  public created_at?: string
  public updated_at?: string

  constructor(data?: Partial<User>) {
    if (data) {
      Object.assign(this, data)
    }
  }

  // Método para obter as iniciais do usuário
  public getInitials(): string {
    const names = this.full_name.split(' ')
    if (names.length >= 2) {
      return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase()
    }
    return this.full_name.substring(0, 2).toUpperCase()
  }

  // Método para obter o nome formatado do role
  public getRoleLabel(): string {
    if (this.role === 'administrador') return 'Administrador'
    if (this.role === 'gestor') return 'Gestor'
    return 'Comum'
  }

  // Método para verificar se é administrador
  public isAdmin(): boolean {
    return this.role === 'administrador'
  }

  // Método para formatar a data de criação
  public getFormattedCreatedAt(): string {
    if (!this.created_at) return '-'
    return new Date(this.created_at).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  // Método para formatar a data de atualização
  public getFormattedUpdatedAt(): string {
    if (!this.updated_at) return '-'
    return new Date(this.updated_at).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }
}
