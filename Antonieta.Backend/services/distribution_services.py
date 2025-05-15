from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.distribution_model import Distribution
from sqlalchemy.orm import Session
from database import get_db
from dtos.create_distribution_dto import create_distribution_dto
from dtos.update_distribution_dto import update_distribution_dto

async def get_all_distribution_service(skip: int = 0, limit: int = 100) -> Tuple[List[Distribution], int]:
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
    Cria um novo ração no banco de dados.

    Args:
        distribution_dto: Dados do ração a ser criado.

    Returns:
        O objeto distribution criado.
    """

    db_distribution = Distribution(**distribution_dto.model_dump())

    db = next(get_db())
    try:
        db.add(db_distribution)
        db.commit()
        db.refresh(db_distribution)
        return db_distribution
    finally:
        db.close()

async def update_distribution_service(distribution_dto: update_distribution_dto) -> Optional[Distribution]:
    """
    Atualiza um ração existente no banco de dados.

    Args:
        distribution_dto: Dados atualizados do ração.

    Returns:
        O objeto distribution atualizado ou None se não encontrado.
    """
    db = next(get_db())
    try:
        distribution = db.query(Distribution).filter(Distribution.id == distribution_dto.id).first()
        if distribution:
            update_data = distribution_dto.model_dump(exclude={'id'}, exclude_unset=True)

            for key, value in update_data.items():
                setattr(Distribution, key, value)
            db.commit()
            db.refresh(Distribution)
        return distribution
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