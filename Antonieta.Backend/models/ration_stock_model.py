from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class RationStock(Base):
    __tablename__ = 'ration_stock'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Nome/Tipo da ração
    description = Column(String, index=True)
    unit = Column(String, index=True)
    stock = Column(Float, index=True)
    distributions = relationship("Distribution", back_populates="ration")
    inputs = relationship("RationInput", back_populates="ration_stock")
