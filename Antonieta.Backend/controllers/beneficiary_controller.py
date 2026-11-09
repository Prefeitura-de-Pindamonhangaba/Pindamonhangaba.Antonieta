import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.user_model import User
from services.auth_service import get_current_user
from services.beneficiary_services import (
    get_all_beneficiaries_service, get_beneficiary_by_id_service,
    create_beneficiary_service, update_beneficiary_service, delete_beneficiary_service,
)
from dtos.create_beneficiary_dto import create_beneficiary_dto
from dtos.update_beneficiary_dto import update_beneficiary_dto

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/beneficiary", tags=["Beneficiary"])


@router.get("/")
async def get_all_beneficiaries(skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000)):
    return await get_all_beneficiaries_service(skip, limit)


@router.get("/{beneficiary_id}")
async def get_beneficiary_by_id(beneficiary_id: int):
    record = await get_beneficiary_by_id_service(beneficiary_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Beneficiario nao encontrado")
    return record


@router.post("/")
async def create_beneficiary(beneficiary_dto: create_beneficiary_dto, request: Request, actor: User = Depends(get_current_user)):
    record = await create_beneficiary_service(beneficiary_dto, actor=actor, request=request)
    logger.info("Beneficiary created id=%s", record.id)
    return record


@router.put("/")
async def update_beneficiary(beneficiary_dto: update_beneficiary_dto, request: Request, actor: User = Depends(get_current_user)):
    record = await update_beneficiary_service(beneficiary_dto, actor=actor, request=request)
    if record is None:
        raise HTTPException(status_code=404, detail="Beneficiario nao encontrado")
    logger.info("Beneficiary updated id=%s", record.id)
    return record


@router.delete("/{beneficiary_id}")
async def delete_beneficiary(beneficiary_id: int, request: Request, actor: User = Depends(get_current_user)):
    if not await delete_beneficiary_service(beneficiary_id, actor=actor, request=request):
        raise HTTPException(status_code=404, detail="Beneficiario nao encontrado")
    logger.info("Beneficiary deleted id=%s", beneficiary_id)
    return {"message": "Beneficiario excluido"}


@router.get("/search/neighborhood/{neighborhood}")
async def search_by_neighborhood(neighborhood: str, skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000)):
    records, total = await get_all_beneficiaries_service(skip, limit, neighborhood=neighborhood)
    return {"beneficiaries": records, "total": total}


@router.get("/search/street/{street}")
async def search_by_street(street: str, skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000)):
    records, total = await get_all_beneficiaries_service(skip, limit, street=street)
    return {"beneficiaries": records, "total": total}
