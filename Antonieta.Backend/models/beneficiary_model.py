from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    document = Column(String, index=True)
    address = Column(String, index=True)
    contact = Column(String, index=True)
    monthly_limit = Column(Integer, default=0)
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