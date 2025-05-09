from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ration(Base):
    __tablename__ = 'beneficiaries'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    document = Column(String, index=True)
    address = Column(String, index=True)
    contact = Column(String, index=True)