from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.beneficiary_model import Beneficiary
from sqlalchemy.orm import Session
from database import get_db
from dtos.create_beneficiary_dto import create_beneficiary_dto
from dtos.update_beneficiary_dto import update_beneficiary_dto

async def get_all_beneficiaries_service(skip: int = 0, limit: int = 1000, include_old: bool = False) -> Tuple[List[Beneficiary], int]:
    """
    Retorna todos os beneficiários do banco de dados.
    Obtém a sessão do DB internamente.

    Args:
        skip: Número de registros para pular
        limit: Limite de registros
        include_old: Se True, inclui registros antigos (apenas para gestores)

    Returns:
        Uma lista de objetos Beneficiary.
    """
    db = next(get_db())
    try:
        query = db.query(Beneficiary)
        if not include_old:
            query = query.filter(Beneficiary.old == False)
        beneficiaries = query.offset(skip).limit(limit).all()
        
        count_query = db.query(func.count(Beneficiary.id))
        if not include_old:
            count_query = count_query.filter(Beneficiary.old == False)
        total_beneficiaries = count_query.scalar()
        
        return beneficiaries, total_beneficiaries
    finally:
        db.close()

async def get_beneficiary_by_id_service(beneficiary_id: int) -> Optional[Beneficiary]:
    """
    Retorna um beneficiário específico do banco de dados.

    Args:
        beneficiary_id: ID do beneficiário a ser retornado.

    Returns:
        Um objeto Beneficiary ou None se não encontrado.
    """
    db = next(get_db())
    try:
        beneficiary = db.query(Beneficiary).filter(
            Beneficiary.id == beneficiary_id,
            Beneficiary.old == False
        ).first()
        return beneficiary
    finally:
        db.close()

async def create_beneficiary_service(beneficiary_dto: create_beneficiary_dto) -> Beneficiary:
    """
    Cria um novo beneficiário no banco de dados.

    Args:
        beneficiary_dto: Dados do beneficiário a ser criado.

    Returns:
        O objeto Beneficiary criado.
    """

    db_beneficiary = Beneficiary(**beneficiary_dto.model_dump())

    db = next(get_db())
    try:
        db.add(db_beneficiary)
        db.commit()
        db.refresh(db_beneficiary)
        return db_beneficiary
    finally:
        db.close()

async def update_beneficiary_service(beneficiary_dto: update_beneficiary_dto) -> Optional[Beneficiary]:
    """
    Atualiza um beneficiário existente no banco de dados.

    Args:
        beneficiary_dto: Dados atualizados do beneficiário.

    Returns:
        O objeto Beneficiary atualizado ou None se não encontrado.
    """
    db = next(get_db())
    try:
        beneficiary = db.query(Beneficiary).filter(
            Beneficiary.id == beneficiary_dto.id,
            Beneficiary.old == False
        ).first()
        if beneficiary:
            update_data = beneficiary_dto.model_dump(exclude={'id'}, exclude_unset=True)

            for key, value in update_data.items():
                setattr(beneficiary, key, value)
            db.commit()
            db.refresh(beneficiary)
        return beneficiary
    finally:
        db.close()

async def delete_beneficiary_service(beneficiary_id: int) -> bool:
    """
    Deleta um beneficiário do banco de dados.

    Args:
        beneficiary_id: ID do beneficiário a ser deletado.

    Returns:
        True se o beneficiário foi deletado, False caso contrário.
    """
    db = next(get_db())
    try:
        beneficiary = db.query(Beneficiary).filter(
            Beneficiary.id == beneficiary_id,
            Beneficiary.old == False
        ).first()
        if not beneficiary:
            return False
        db.delete(beneficiary)
        db.commit()
        return True
    finally:
        db.close()