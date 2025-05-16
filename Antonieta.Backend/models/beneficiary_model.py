from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    document = Column(String, index=True)
    address = Column(String, index=True)
    contact = Column(String, index=True)
    distributions = relationship("Distribution", back_populates="beneficiary")
    # TODO - Add limit