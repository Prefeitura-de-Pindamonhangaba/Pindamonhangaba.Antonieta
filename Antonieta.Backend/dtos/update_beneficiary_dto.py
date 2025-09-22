from pydantic import BaseModel, Field
from typing import Optional

class update_beneficiary_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar um beneficiário.
    O campo 'id' é obrigatório para identificar qual beneficiário atualizar.
    Os demais campos são opcionais para permitir atualizações parciais.
    """
    # id (obrigatório para identificar o beneficiário)
    id: int = Field(..., gt=0, description="ID do beneficiário a ser atualizado")
    
    # Dados pessoais
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo")
    document: Optional[str] = Field(None, min_length=8, max_length=20, description="CPF ou RG")
    contact: Optional[str] = Field(None, min_length=8, max_length=50, description="Telefone ou e-mail")
    
    # Endereço estruturado (substituindo o campo 'address')
    street: Optional[str] = Field(None, min_length=5, max_length=200, description="Rua, Avenida, etc.")
    number: Optional[str] = Field(None, max_length=10, description="Número da residência")
    neighborhood: Optional[str] = Field(None, min_length=2, max_length=100, description="Bairro")
    city: Optional[str] = Field(None, max_length=100, description="Cidade")
    state: Optional[str] = Field(None, max_length=2, description="Estado (sigla)")
    zip_code: Optional[str] = Field(None, max_length=10, description="CEP")
    complement: Optional[str] = Field(None, max_length=100, description="Complemento (apt, casa, etc.)")
    
    # Dados pessoais opcionais
    mother_name: Optional[str] = Field(None, max_length=100, description="Nome da mãe")
    birth_date: Optional[str] = Field(None, description="Data de nascimento (YYYY-MM-DD)")
    
    # Dados dos animais
    qtd_dogs: Optional[int] = Field(None, ge=0, le=50, description="Quantidade de cães")
    qtd_castred_dogs: Optional[int] = Field(None, ge=0, le=50, description="Cães castrados")
    qtd_cats: Optional[int] = Field(None, ge=0, le=50, description="Quantidade de gatos")
    qtd_castred_cats: Optional[int] = Field(None, ge=0, le=50, description="Gatos castrados")
    
    # Benefícios sociais
    government_benefit: Optional[bool] = Field(None, description="Recebe benefício do governo")
    receives_basic_basket: Optional[bool] = Field(None, description="Recebe cesta básica")
    
    # Informações adicionais
    how_did_you_hear: Optional[str] = Field(None, max_length=200, description="Como soube do projeto")
    observations: Optional[str] = Field(None, max_length=500, description="Observações")

    class Config:
        """Configuração do Pydantic."""
        json_schema_extra = {
            "example": {
                "id": 1,  # ✅ ADICIONADO no exemplo
                "name": "João Silva Santos",
                "street": "Rua Nova das Flores",
                "number": "456",
                "neighborhood": "Vila Nova",
                "city": "Pindamonhangaba",
                "state": "SP",
                "zip_code": "12400-001",
                "complement": "Casa dos fundos",
                "contact": "(12) 98888-7777",
                "qtd_dogs": 3,
                "qtd_castred_dogs": 2,
                "government_benefit": True,
                "observations": "Mudou de endereço e aumentou quantidade de animais"
            }
        }