from fastapi import Depends, Request
from services.auth_service import get_current_user
from models.user_model import User
from fastapi import APIRouter, HTTPException, Query
from services.distribution_services import (
    get_all_distribution_service, get_distribution_by_id_service,
    create_distribution_service, update_distribution_service, delete_distribution_service,
)
from dtos.update_distribution_dto import update_distribution_dto
from dtos.create_distribution_dto import create_distribution_dto

router = APIRouter(prefix="/distribution", tags=["distribution"])


@router.get("/")
async def get_all_distribution(skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000)):
    return await get_all_distribution_service(skip, limit)


@router.get("/beneficiary/{beneficiary_id}")
async def get_beneficiary_distributions(beneficiary_id: int, skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000)):
    return await get_all_distribution_service(skip, limit, beneficiary_id=beneficiary_id)


@router.get("/{distribution_id}")
async def get_distribution_by_id(distribution_id: int):
    record = await get_distribution_by_id_service(distribution_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    return record


@router.post("/")
async def create_distribution(distribution_dto: create_distribution_dto, request: Request, actor: User = Depends(get_current_user)):
    return await create_distribution_service(distribution_dto, actor=actor, request=request)


@router.put("/")
async def update_distribution(distribution_dto: update_distribution_dto, request: Request, actor: User = Depends(get_current_user)):
    record = await update_distribution_service(distribution_dto, actor=actor, request=request)
    if record is None:
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    return record


@router.put("/{distribution_id}")
async def update_distribution_by_id(distribution_id: int, distribution_dto: update_distribution_dto, request: Request, actor: User = Depends(get_current_user)):
    if distribution_id != distribution_dto.id:
        raise HTTPException(status_code=400, detail="ID da rota não corresponde ao ID do corpo da requisição")
    return await update_distribution(distribution_dto, actor=actor, request=request)


@router.delete("/{distribution_id}")
async def delete_distribution(distribution_id: int, request: Request, actor: User = Depends(get_current_user)):
    if not await delete_distribution_service(distribution_id, actor=actor, request=request):
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    return True
