from fastapi import APIRouter
from services.distribution_services import get_all_distribution_service, get_distribution_by_id_service, create_distribution_service, update_distribution_service, delete_distribution_service
from dtos.update_distribution_dto import update_distribution_dto
from dtos.create_distribution_dto import create_distribution_dto

router = APIRouter(prefix="/distribution", tags=["distribution"])

@router.get("/")
async def get_all_distribution(include_old: bool = False):
    """
    Retorna todas as distribuições
    
    Args:
        include_old: Se True, inclui registros antigos (apenas para gestores)
    """
    return await get_all_distribution_service(include_old=include_old)

@router.get("/{distribution_id}")
async def get_distribution_by_id(distribution_id: int):
    return await get_distribution_by_id_service(distribution_id=distribution_id)

@router.post("/")
async def create_distribution(distribution_dto: create_distribution_dto):
    return await create_distribution_service(distribution_dto=distribution_dto)

@router.put("/")
async def create_distribution(distribution_dto: update_distribution_dto):
    return await update_distribution_service(distribution_dto=distribution_dto)

@router.delete("/{distribution_id}")
async def create_distribution(distribution_id: int):
    return await delete_distribution_service(distribution_id=distribution_id)