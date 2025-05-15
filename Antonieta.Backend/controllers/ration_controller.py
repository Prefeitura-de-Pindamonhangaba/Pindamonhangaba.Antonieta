from fastapi import APIRouter
from services.ration_services import get_all_ration_service, get_ration_by_id_service, create_ration_service, update_ration_service, delete_ration_service
from dtos.update_ration_dto import update_ration_dto
from dtos.create_ration_dto import create_ration_dto

router = APIRouter(prefix="/ration", tags=["ration"])

@router.get("/")
async def get_all_ration():
    return await get_all_ration_service()

@router.get("/{ration_id}")
async def get_ration_by_id(ration_id: int):
    return await get_ration_by_id_service(ration_id=ration_id)

@router.post("/")
async def create_ration(ration_dto: create_ration_dto):
    return await create_ration_service(ration_dto=ration_dto)

@router.put("/")
async def create_ration(ration_dto: update_ration_dto):
    return await update_ration_service(ration_dto=ration_dto)

@router.delete("/{ration_id}")
async def create_ration(ration_id: int):
    return await delete_ration_service(ration_id=ration_id)