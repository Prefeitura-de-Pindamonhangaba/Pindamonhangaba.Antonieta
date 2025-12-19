from pydantic import BaseModel, Field
from typing import Optional

class create_beneficiary_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar um novo beneficiário.
    Atualizado para usar endereço estruturado em campos separados.
    """
    # Dados pessoais obrigatórios
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do beneficiário")
    document: str = Field(..., min_length=8, max_length=20, description="CPF ou RG")
    contact: str = Field(..., min_length=8, max_length=50, description="Telefone ou e-mail")
    
    # Endereço estruturado (campos obrigatórios)
    street: str = Field(..., min_length=5, max_length=200, description="Rua, Avenida, etc.")
    neighborhood: str = Field(..., min_length=2, max_length=100, description="Bairro")
    
    # Endereço estruturado (campos opcionais)
    number: Optional[str] = Field(None, max_length=10, description="Número da residência")
    complement: Optional[str] = Field(None, max_length=100, description="Complemento (apt, casa, etc.)")
    city: str = Field(default="Pindamonhangaba", max_length=100, description="Cidade")
    state: str = Field(default="SP", max_length=2, description="Estado (sigla)")
    zip_code: Optional[str] = Field(None, max_length=10, description="CEP")
    
    # Dados pessoais opcionais
    mother_name: Optional[str] = Field(None, max_length=100, description="Nome da mãe")
    birth_date: Optional[str] = Field(None, description="Data de nascimento (YYYY-MM-DD)")
    
    # Dados dos animais
    qtd_dogs: int = Field(default=0, ge=0, le=50, description="Quantidade de cães")
    qtd_castred_dogs: int = Field(default=0, ge=0, le=50, description="Cães castrados")
    qtd_cats: int = Field(default=0, ge=0, le=50, description="Quantidade de gatos")
    qtd_castred_cats: int = Field(default=0, ge=0, le=50, description="Gatos castrados")
    
    # Benefícios sociais
    government_benefit: bool = Field(default=False, description="Recebe benefício do governo")
    receives_basic_basket: bool = Field(default=False, description="Recebe cesta básica")
    
    # CadÚnico (Cadastro Único)
    cadunico_code: Optional[str] = Field(None, max_length=50, description="Código familiar do CadÚnico")
    income_range: Optional[str] = Field(None, max_length=100, description="Faixa de renda familiar per capita")
    
    # Informações adicionais
    how_did_you_hear: Optional[str] = Field(None, max_length=200, description="Como soube do projeto")
    observations: Optional[str] = Field(None, max_length=500, description="Observações")

    class Config:
        """Configuração do Pydantic."""
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "document": "123.456.789-00",
                "contact": "(12) 99999-9999",
                "street": "Rua das Flores",
                "number": "123",
                "neighborhood": "Centro",
                "city": "Pindamonhangaba",
                "state": "SP",
                "zip_code": "12400-000",
                "complement": "Casa 2",
                "mother_name": "Maria Silva",
                "birth_date": "1990-01-15",
                "qtd_dogs": 2,
                "qtd_castred_dogs": 1,
                "qtd_cats": 1,
                "qtd_castred_cats": 0,
                "government_benefit": False,
                "receives_basic_basket": True,
                "how_did_you_hear": "Indicação de vizinho",
                "observations": "Família em situação de vulnerabilidade"
            }
        }