from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.ration_type_model import RationType
from schemas.ration_type_schema import RationTypeCreate, RationTypeUpdate, RationType as RationTypeSchema

router = APIRouter()

@router.post("/", response_model=RationTypeSchema)
def create_ration_type(ration_type: RationTypeCreate, db: Session = Depends(get_db)):
    db_ration_type = RationType(name=ration_type.name, description=ration_type.description)
    db.add(db_ration_type)
    db.commit()
    db.refresh(db_ration_type)
    return db_ration_type

@router.get("/", response_model=List[RationTypeSchema])
def read_ration_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ration_types = db.query(RationType).offset(skip).limit(limit).all()
    return ration_types

@router.get("/{ration_type_id}", response_model=RationTypeSchema)
def read_ration_type(ration_type_id: int, db: Session = Depends(get_db)):
    db_ration_type = db.query(RationType).filter(RationType.id == ration_type_id).first()
    if db_ration_type is None:
        raise HTTPException(status_code=404, detail="Tipo de ração não encontrado")
    return db_ration_type

@router.put("/{ration_type_id}", response_model=RationTypeSchema)
def update_ration_type(ration_type_id: int, ration_type: RationTypeUpdate, db: Session = Depends(get_db)):
    db_ration_type = db.query(RationType).filter(RationType.id == ration_type_id).first()
    if db_ration_type is None:
        raise HTTPException(status_code=404, detail="Tipo de ração não encontrado")
    
    if ration_type.name is not None:
        db_ration_type.name = ration_type.name
    if ration_type.description is not None:
        db_ration_type.description = ration_type.description
    
    db.commit()
    db.refresh(db_ration_type)
    return db_ration_type

@router.delete("/{ration_type_id}")
def delete_ration_type(ration_type_id: int, db: Session = Depends(get_db)):
    db_ration_type = db.query(RationType).filter(RationType.id == ration_type_id).first()
    if db_ration_type is None:
        raise HTTPException(status_code=404, detail="Tipo de ração não encontrado")
    
    db.delete(db_ration_type)
    db.commit()
    return {"message": "Tipo de ração removido com sucesso"}