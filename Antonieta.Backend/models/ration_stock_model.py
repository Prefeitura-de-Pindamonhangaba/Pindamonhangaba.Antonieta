from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class RationStock(Base):
    __tablename__ = 'ration_stock'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ration_type_id = Column(Integer, ForeignKey('ration_type.id'), index=True)
    unit = Column(String, index=True)
    stock = Column(Integer, index=True)
    description = Column(String, index=True)
    distributions = relationship("Distribution", back_populates="ration")
    ration_type = relationship("RationType", back_populates="ration_stocks")