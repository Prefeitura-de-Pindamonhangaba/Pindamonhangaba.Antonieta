from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Distribution(Base):
    __tablename__ = 'distribution'
    
    id = Column(Integer, primary_key=True, index=True)
    ration_id = Column(Integer, ForeignKey('ration_stock.id'), index=True)
    beneficiary_id = Column(Integer, ForeignKey('beneficiary.id'), index=True)
    amount = Column(Float, index=True)
    date = Column(DateTime, nullable=False)
    ration = relationship("RationStock", back_populates="distributions")
    beneficiary = relationship("Beneficiary", back_populates="distributions")
    observations = Column(String, nullable=True)
    
    # Audit fields
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
