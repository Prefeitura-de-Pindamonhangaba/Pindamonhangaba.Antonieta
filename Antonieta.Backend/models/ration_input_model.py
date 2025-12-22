from sqlalchemy import Column, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class RationInput(Base):
    __tablename__ = 'ration_input'
    
    id = Column(Integer, primary_key=True, index=True)
    ration_stock_id = Column(Integer, ForeignKey('ration_stock.id'), index=True)
    amount = Column(Float, index=True)
    date = Column(DateTime, nullable=False)
    description = Column(String, index=True)
    ration_stock = relationship("RationStock", back_populates="inputs")
    
    # Audit fields
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())