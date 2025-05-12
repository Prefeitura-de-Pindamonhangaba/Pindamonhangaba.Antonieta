from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import func
from models.beneficiary_model import Beneficiary
from sqlalchemy.orm import Session
from database import get_db

async def get_all_beneficiaries(skip: int = 0, limit: int = 100) -> Tuple[List[Beneficiary], int]:
    """
    Retorna todos os beneficiários do banco de dados.
    Obtém a sessão do DB internamente.

    Returns:
        Uma lista de objetos Beneficiary.
    """
    db = next(get_db())
    try:
        query = db.query(Beneficiary)
        beneficiaries = query.offset(skip).limit(limit).all()
        total_beneficiaries = db.query(func.count(Beneficiary.id)).scalar()
        return beneficiaries, total_beneficiaries
    finally:
        db.close()