from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.distribution_model import Distribution
from sqlalchemy.orm import Session
from database import get_db
from dtos.create_distribution_dto import create_distribution_dto
from dtos.update_distribution_dto import update_distribution_dto
from models.ration_stock_model import RationStock

async def get_all_distribution_service(skip: int = 0, limit: int = 1000) -> Tuple[List[Distribution], int]:
    """
    Retorna todos os raçãos do banco de dados.
    Obtém a sessão do DB internamente.

    Returns:
        Uma lista de objetos distribution.
    """
    db = next(get_db())
    try:
        query = db.query(Distribution)
        distribution = query.offset(skip).limit(limit).all()
        total_distribution = db.query(func.count(Distribution.id)).scalar()
        return distribution, total_distribution
    finally:
        db.close()

async def get_distribution_by_id_service(distribution_id: int) -> Optional[Distribution]:
    """
    Retorna um ração específico do banco de dados.

    Args:
        distribution_id: ID do ração a ser retornado.

    Returns:
        Um objeto distribution ou None se não encontrado.
    """
    db = next(get_db())
    try:
        distribution = db.query(Distribution).filter(Distribution.id == distribution_id).first()
        return distribution
    finally:
        db.close()

async def create_distribution_service(distribution_dto: create_distribution_dto) -> Distribution:
    """
    Cria uma nova distribuição e atualiza o estoque.
    """
    db = next(get_db())
    try:
        # Verificar e atualizar o estoque
        ration_stock = db.query(RationStock).filter(
            RationStock.id == distribution_dto.ration_id
        ).first()
        
        if not ration_stock:
            raise HTTPException(
                status_code=404,
                detail="Ração não encontrada"
            )
            
        if ration_stock.stock < distribution_dto.amount:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente"
            )
            
        # Deduzir do estoque
        ration_stock.stock -= distribution_dto.amount
        
        # Criar a distribuição
        db_distribution = Distribution(**distribution_dto.model_dump())
        db.add(db_distribution)
        db.commit()
        db.refresh(db_distribution)
        return db_distribution
    finally:
        db.close()

async def update_distribution_service(distribution_dto: update_distribution_dto) -> Optional[Distribution]:
    """
    Atualiza uma distribuição e ajusta o estoque.
    """
    db = next(get_db())
    try:
        # Buscar distribuição atual
        current_distribution = db.query(Distribution).filter(
            Distribution.id == distribution_dto.id
        ).first()
        
        if not current_distribution:
            return None
            
        # Calcular diferença na quantidade
        amount_difference = distribution_dto.amount - current_distribution.amount
        
        # Verificar e atualizar estoque
        ration_stock = db.query(RationStock).filter(
            RationStock.id == current_distribution.ration_id
        ).first()
        
        if ration_stock.stock < amount_difference:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente"
            )
            
        # Atualizar estoque
        ration_stock.stock -= amount_difference
        
        # Atualizar distribuição
        for key, value in distribution_dto.model_dump(exclude={'id'}).items():
            setattr(current_distribution, key, value)
            
        db.commit()
        db.refresh(current_distribution)
        return current_distribution
    finally:
        db.close()

async def delete_distribution_service(distribution_id: int) -> bool:
    """
    Deleta um ração do banco de dados.

    Args:
        distribution_id: ID do ração a ser deletado.

    Returns:
        True se o ração foi deletado, False caso contrário.
    """
    db = next(get_db())
    try:
        distribution = db.query(Distribution).filter(Distribution.id == distribution_id).first()
        if not distribution:
            return False
        db.delete(Distribution)
        db.commit()
        return True
    finally:
        db.close()