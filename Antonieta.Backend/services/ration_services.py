from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.ration_model import Ration
from sqlalchemy.orm import Session
from database import get_db
from dtos.create_ration_dto import create_ration_dto
from dtos.update_ration_dto import update_ration_dto

async def get_all_ration_service(skip: int = 0, limit: int = 100) -> Tuple[List[Ration], int]:
    """
    Retorna todos os raçãos do banco de dados.
    Obtém a sessão do DB internamente.

    Returns:
        Uma lista de objetos ration.
    """
    db = next(get_db())
    try:
        query = db.query(Ration)
        ration = query.offset(skip).limit(limit).all()
        total_ration = db.query(func.count(Ration.id)).scalar()
        return ration, total_ration
    finally:
        db.close()

async def get_ration_by_id_service(ration_id: int) -> Optional[Ration]:
    """
    Retorna um ração específico do banco de dados.

    Args:
        ration_id: ID do ração a ser retornado.

    Returns:
        Um objeto ration ou None se não encontrado.
    """
    db = next(get_db())
    try:
        ration = db.query(Ration).filter(Ration.id == ration_id).first()
        return ration
    finally:
        db.close()

async def create_ration_service(ration_dto: create_ration_dto) -> Ration:
    """
    Cria um novo ração no banco de dados.

    Args:
        ration_dto: Dados do ração a ser criado.

    Returns:
        O objeto ration criado.
    """

    db_ration = Ration(**ration_dto.model_dump())

    db = next(get_db())
    try:
        db.add(db_ration)
        db.commit()
        db.refresh(db_ration)
        return db_ration
    finally:
        db.close()

async def update_ration_service(ration_dto: update_ration_dto) -> Optional[Ration]:
    """
    Atualiza um ração existente no banco de dados.

    Args:
        ration_dto: Dados atualizados do ração.

    Returns:
        O objeto ration atualizado ou None se não encontrado.
    """
    db = next(get_db())
    try:
        ration = db.query(Ration).filter(Ration.id == ration_dto.id).first()
        if ration:
            update_data = ration_dto.model_dump(exclude={'id'}, exclude_unset=True)

            for key, value in update_data.items():
                setattr(Ration, key, value)
            db.commit()
            db.refresh(Ration)
        return ration
    finally:
        db.close()

async def delete_ration_service(ration_id: int) -> bool:
    """
    Deleta um ração do banco de dados.

    Args:
        ration_id: ID do ração a ser deletado.

    Returns:
        True se o ração foi deletado, False caso contrário.
    """
    db = next(get_db())
    try:
        ration = db.query(Ration).filter(Ration.id == ration_id).first()
        if not ration:
            return False
        db.delete(Ration)
        db.commit()
        return True
    finally:
        db.close()