from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.ration_stock_model import RationStock
from sqlalchemy.orm import Session
import database
from services import transaction_audit
from fastapi import HTTPException
from models.ration_input_model import RationInput
from models.distribution_model import Distribution
from dtos.create_ration_stock_dto import create_ration_stock_dto
from dtos.update_ration_stock_dto import update_ration_stock_dto

async def get_all_ration_stock_service(skip: int = 0, limit: int = 1000) -> Tuple[List[RationStock], int]:
    """
    Retorna todos os estoques de ração do banco de dados.
    Obtém a sessão do DB internamente.

    Returns:
        Uma lista de objetos ration_stock.
    """
    db = database.SessionLocal()
    try:
        query = db.query(RationStock)
        ration_stock = query.offset(skip).limit(limit).all()
        total_ration_stock = db.query(func.count(RationStock.id)).scalar()
        return ration_stock, total_ration_stock
    finally:
        db.close()

async def get_ration_stock_by_id_service(ration_stock_id: int) -> Optional[RationStock]:
    """
    Retorna um estoque de ração específico do banco de dados.

    Args:
        ration_stock_id: ID do estoque de ração a ser retornado.

    Returns:
        Um objeto ration_stock ou None se não encontrado.
    """
    db = database.SessionLocal()
    try:
        ration_stock = db.query(RationStock).filter(RationStock.id == ration_stock_id).first()
        return ration_stock
    finally:
        db.close()

async def create_ration_stock_service(ration_stock_dto: create_ration_stock_dto, actor=None, request=None) -> RationStock:
    """
    Cria um novo estoque de ração no banco de dados.

    Args:
        ration_stock_dto: Dados do estoque de ração a ser criado.

    Returns:
        O objeto ration_stock criado.
    """

    db_ration_stock = RationStock(**ration_stock_dto.model_dump())

    db = database.SessionLocal()
    try:
        db.add(db_ration_stock)
        transaction_audit.record_change(db, "CREATE", db_ration_stock, actor, request, ration_stock_dto.model_dump(exclude_unset=True).keys())
        db.commit()
        db.refresh(db_ration_stock)
        return db_ration_stock
    finally:
        db.close()

async def update_ration_stock_service(ration_stock_dto: update_ration_stock_dto, actor=None, request=None) -> Optional[RationStock]:
    """
    Atualiza um estoque de ração existente no banco de dados.

    Args:
        ration_stock_dto: Dados atualizados do estoque de ração.

    Returns:
        O objeto ration_stock atualizado ou None se não encontrado.
    """
    db = database.SessionLocal()
    try:
        ration_stock = db.query(RationStock).filter(RationStock.id == ration_stock_dto.id).with_for_update().first()
        if ration_stock:
            update_data = ration_stock_dto.model_dump(exclude={'id'}, exclude_unset=True)

            for key, value in update_data.items():
                setattr(ration_stock, key, value)
            transaction_audit.record_change(db, "UPDATE", ration_stock, actor, request, ration_stock_dto.model_dump(exclude_unset=True).keys())
            db.commit()
            db.refresh(ration_stock)
        return ration_stock
    finally:
        db.close()

async def delete_ration_stock_service(ration_stock_id: int, actor=None, request=None) -> bool:
    """
    Deleta um estoque de ração do banco de dados.

    Args:
        ration_stock_id: ID do estoque de ração a ser deletado.

    Returns:
        True se o estoque de ração foi deletado, False caso contrário.
    """
    db = database.SessionLocal()
    try:
        ration_stock = db.query(RationStock).filter(RationStock.id == ration_stock_id).with_for_update().first()
        if not ration_stock:
            return False
        if db.query(RationInput).filter_by(ration_stock_id=ration_stock_id).first() or db.query(Distribution).filter_by(ration_id=ration_stock_id).first():
            raise HTTPException(status_code=409, detail="Ração possui movimentações vinculadas")
        db.delete(ration_stock)
        transaction_audit.record_change(db, "DELETE", ration_stock, actor, request, ())
        db.commit()
        return True
    finally:
        db.close()
