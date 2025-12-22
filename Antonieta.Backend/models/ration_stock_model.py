from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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
    
    # Audit fields
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
