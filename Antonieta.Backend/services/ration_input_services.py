from typing import List, Optional, Tuple
from sqlalchemy import func
from models.ration_input_model import RationInput
from models.ration_stock_model import RationStock
from database import get_db
from dtos.create_ration_input_dto import create_ration_input_dto
from dtos.update_ration_input_dto import update_ration_input_dto

async def get_all_ration_input_service(skip: int = 0, limit: int = 100) -> Tuple[List[RationInput], int]:
    """
    Retorna todos os registros de entrada de ração do banco de dados.
    """
    db = next(get_db())
    try:
        query = db.query(RationInput)
        ration_inputs = query.offset(skip).limit(limit).all()
        total_ration_inputs = db.query(func.count(RationInput.id)).scalar()
        return ration_inputs, total_ration_inputs
    finally:
        db.close()

async def get_ration_input_by_id_service(ration_input_id: int) -> Optional[RationInput]:
    """
    Retorna um registro de entrada de ração específico.
    """
    db = next(get_db())
    try:
        return db.query(RationInput).filter(RationInput.id == ration_input_id).first()
    finally:
        db.close()

async def create_ration_input_service(ration_input_dto: create_ration_input_dto) -> RationInput:
    """
    Cria um novo registro de entrada de ração e atualiza o estoque.
    """
    db = next(get_db())
    try:
        # Criar o registro de entrada
        db_ration_input = RationInput(**ration_input_dto.model_dump())
        db.add(db_ration_input)
        
        # Atualizar o estoque
        ration_stock = db.query(RationStock).filter(
            RationStock.id == ration_input_dto.ration_stock_id
        ).first()
        if ration_stock:
            ration_stock.stock += ration_input_dto.amount
        
        db.commit()
        db.refresh(db_ration_input)
        return db_ration_input
    finally:
        db.close()

async def update_ration_input_service(ration_input_dto: update_ration_input_dto) -> Optional[RationInput]:
    """
    Atualiza um registro de entrada de ração e ajusta o estoque.
    """
    db = next(get_db())
    try:
        # Buscar o registro atual
        current_input = db.query(RationInput).filter(
            RationInput.id == ration_input_dto.id
        ).first()
        
        if not current_input:
            return None
            
        # Calcular a diferença na quantidade
        amount_difference = ration_input_dto.amount - current_input.amount
        
        # Atualizar o registro
        for key, value in ration_input_dto.model_dump(exclude={'id'}).items():
            setattr(current_input, key, value)
        
        # Atualizar o estoque
        ration_stock = db.query(RationStock).filter(
            RationStock.id == current_input.ration_stock_id
        ).first()
        if ration_stock:
            ration_stock.stock += amount_difference
        
        db.commit()
        db.refresh(current_input)
        return current_input
    finally:
        db.close()

async def delete_ration_input_service(ration_input_id: int) -> bool:
    """
    Deleta um registro de entrada de ração e ajusta o estoque.
    """
    db = next(get_db())
    try:
        ration_input = db.query(RationInput).filter(
            RationInput.id == ration_input_id
        ).first()
        
        if not ration_input:
            return False
            
        # Atualizar o estoque antes de deletar
        ration_stock = db.query(RationStock).filter(
            RationStock.id == ration_input.ration_stock_id
        ).first()
        if ration_stock:
            ration_stock.stock -= ration_input.amount
        
        db.delete(ration_input)
        db.commit()
        return True
    finally:
        db.close()