from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class Distribution(Base):
    __tablename__ = 'distribution'
    
    id = Column(Integer, primary_key=True, index=True)
    ration_id = Column(Integer, ForeignKey('ration_stock.id'), index=True)
    beneficiary_id = Column(Integer, ForeignKey('beneficiary.id'), index=True)
    amount = Column(Integer, index=True)
    date = Column(DateTime, nullable=False)
    ration = relationship("RationStock", back_populates="distributions")
    beneficiary = relationship("Beneficiary", back_populates="distributions")
