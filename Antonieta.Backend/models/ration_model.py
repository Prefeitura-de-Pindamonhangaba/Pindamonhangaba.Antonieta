from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Ration(Base):
    __tablename__ = 'ration'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rationType = Column(String, index=True)
    unit = Column(String, index=True)
    stock = Column(Integer, index=True)
    description = Column(String, index=True)
    distributions = relationship("Distribution", back_populates="ration")