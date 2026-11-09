from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.beneficiary_model import Beneficiary
from sqlalchemy.orm import Session
import database
from services import transaction_audit
from fastapi import HTTPException
from models.distribution_model import Distribution
from dtos.create_beneficiary_dto import create_beneficiary_dto
from dtos.update_beneficiary_dto import update_beneficiary_dto

async def get_all_beneficiaries_service(skip: int = 0, limit: int = 1000, neighborhood: str = None, street: str = None) -> Tuple[List[Beneficiary], int]:
    """
    Retorna todos os beneficiários do banco de dados.
    Obtém a sessão do DB internamente.

    Returns:
        Uma lista de objetos Beneficiary.
    """
    db = database.SessionLocal()
    try:
        query = db.query(Beneficiary).filter(Beneficiary.old == False)
        if neighborhood is not None:
            query = query.filter(Beneficiary.neighborhood.ilike(f"%{neighborhood}%"))
        if street is not None:
            query = query.filter(Beneficiary.street.ilike(f"%{street}%"))
        beneficiaries = query.order_by(Beneficiary.id).offset(skip).limit(limit).all()
        total_beneficiaries = query.count()
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
    db = database.SessionLocal()
    try:
        beneficiary = db.query(Beneficiary).filter(
            Beneficiary.id == beneficiary_id,
            Beneficiary.old == False
        ).first()
        return beneficiary
    finally:
        db.close()

async def create_beneficiary_service(beneficiary_dto: create_beneficiary_dto, actor=None, request=None) -> Beneficiary:
    """
    Cria um novo beneficiário no banco de dados.

    Args:
        beneficiary_dto: Dados do beneficiário a ser criado.

    Returns:
        O objeto Beneficiary criado.
    """

    db_beneficiary = Beneficiary(**beneficiary_dto.model_dump())

    db = database.SessionLocal()
    try:
        db.add(db_beneficiary)
        transaction_audit.record_change(db, "CREATE", db_beneficiary, actor, request, beneficiary_dto.model_dump(exclude_unset=True).keys())
        db.commit()
        db.refresh(db_beneficiary)
        return db_beneficiary
    finally:
        db.close()

async def update_beneficiary_service(beneficiary_dto: update_beneficiary_dto, actor=None, request=None) -> Optional[Beneficiary]:
    """
    Atualiza um beneficiário existente no banco de dados.

    Args:
        beneficiary_dto: Dados atualizados do beneficiário.

    Returns:
        O objeto Beneficiary atualizado ou None se não encontrado.
    """
    db = database.SessionLocal()
    try:
        beneficiary = db.query(Beneficiary).filter(
            Beneficiary.id == beneficiary_dto.id,
            Beneficiary.old == False
        ).first()
        if beneficiary:
            update_data = beneficiary_dto.model_dump(exclude={'id'}, exclude_unset=True)

            for key, value in update_data.items():
                setattr(beneficiary, key, value)
            transaction_audit.record_change(db, "UPDATE", beneficiary, actor, request, beneficiary_dto.model_dump(exclude_unset=True).keys())
            db.commit()
            db.refresh(beneficiary)
        return beneficiary
    finally:
        db.close()

async def delete_beneficiary_service(beneficiary_id: int, actor=None, request=None) -> bool:
    """
    Deleta um beneficiário do banco de dados.

    Args:
        beneficiary_id: ID do beneficiário a ser deletado.

    Returns:
        True se o beneficiário foi deletado, False caso contrário.
    """
    db = database.SessionLocal()
    try:
        beneficiary = db.query(Beneficiary).filter(
            Beneficiary.id == beneficiary_id,
            Beneficiary.old == False
        ).with_for_update().first()
        if not beneficiary:
            return False
        if db.query(Distribution).filter_by(beneficiary_id=beneficiary_id).first():
            raise HTTPException(status_code=409, detail="Beneficiário possui distribuições vinculadas")
        db.delete(beneficiary)
        transaction_audit.record_change(db, "DELETE", beneficiary, actor, request, ())
        db.commit()
        return True
    finally:
        db.close()
