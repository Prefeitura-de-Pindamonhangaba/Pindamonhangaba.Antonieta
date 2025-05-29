from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class RationType(Base):
    __tablename__ = 'ration_type'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    ration_stocks = relationship("RationStock", back_populates="ration_type")