from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class RationInput(Base):
    __tablename__ = 'ration_input'
    
    id = Column(Integer, primary_key=True, index=True)
    ration_stock_id = Column(Integer, ForeignKey('ration_stock.id'), index=True)
    amount = Column(Integer, index=True)
    date = Column(DateTime, nullable=False)
    description = Column(String, index=True)
    ration_stock = relationship("RationStock", back_populates="inputs")