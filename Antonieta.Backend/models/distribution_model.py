from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ration(Base):
    __tablename__ = 'distribution'
    
    id = Column(Integer, primary_key=True, index=True)
    ration_id = Column(Integer, ForeignKey('ration.id'), index=True)
    beneficiary_id = Column(Integer, ForeignKey('beneficiaries.id'), index=True)
    amount = Column(Integer, index=True)
    date = Column(DateTime, default=DateTime.datetime.utcnow, nullable=False)

