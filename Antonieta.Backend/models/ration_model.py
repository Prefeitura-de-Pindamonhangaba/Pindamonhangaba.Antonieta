from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ration(Base):
    __tablename__ = 'ration'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rationType = Column(String, index=True)
    unit = Column(String, index=True)
    stock = Column(Integer, index=True)
    description = Column(String, index=True)