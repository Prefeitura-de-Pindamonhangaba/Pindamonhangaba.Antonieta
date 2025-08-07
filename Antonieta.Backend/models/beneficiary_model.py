from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    document = Column(String, index=True)
    
    street = Column(String, index=True, comment="Rua, Avenida, etc.")
    number = Column(String, nullable=True, comment="Número da residência")
    neighborhood = Column(String, index=True, comment="Bairro")
    city = Column(String, default="Pindamonhangaba", comment="Cidade")
    state = Column(String, default="SP", comment="Estado")
    zip_code = Column(String, nullable=True, comment="CEP")
    complement = Column(String, nullable=True, comment="Complemento (apt, casa, etc.)")
    
    contact = Column(String, index=True)
    
    monthly_limit = Column(Float, default=0.0, comment="Limite mensal em kg")
    
    mother_name = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    qtd_dogs = Column(Integer, default=0)
    qtd_castred_dogs = Column(Integer, default=0)
    qtd_cats = Column(Integer, default=0)
    qtd_castred_cats = Column(Integer, default=0)
    government_benefit = Column(Boolean, default=False)
    receives_basic_basket = Column(Boolean, default=False)
    how_did_you_hear = Column(String, nullable=True)
    observations = Column(String, nullable=True)
    
    # Relationships
    distributions = relationship("Distribution", back_populates="beneficiary")
    
    def __repr__(self):
        return f"<Beneficiary(id={self.id}, name='{self.name}', neighborhood='{self.neighborhood}')>"
    
    @property
    def full_address(self):
        """Retorna o endereço completo formatado"""
        address_parts = []
        
        if self.street:
            address_parts.append(self.street)
        
        if self.number:
            address_parts.append(f"nº {self.number}")
        
        if self.complement:
            address_parts.append(f"({self.complement})")
        
        if self.neighborhood:
            address_parts.append(f"- {self.neighborhood}")
        
        if self.city and self.city != "Pindamonhangaba":
            address_parts.append(f"- {self.city}")
        
        if self.state and self.state != "SP":
            address_parts.append(f"/{self.state}")
        
        return " ".join(address_parts)