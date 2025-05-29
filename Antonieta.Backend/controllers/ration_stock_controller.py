from fastapi import APIRouter
from services.ration_stock_services import get_all_ration_stock_service, get_ration_stock_by_id_service, create_ration_stock_service, update_ration_stock_service, delete_ration_stock_service
from dtos.update_ration_stock_dto import update_ration_stock_dto
from dtos.create_ration_stock_dto import create_ration_stock_dto

router = APIRouter(prefix="/ration-stock", tags=["ration-stock"])

@router.get("/")
async def get_all_ration_stock():
    return await get_all_ration_stock_service()

@router.get("/{ration_stock_id}")
async def get_ration_stock_by_id(ration_stock_id: int):
    return await get_ration_stock_by_id_service(ration_stock_id=ration_stock_id)

@router.post("/")
async def create_ration_stock(ration_stock: create_ration_stock_dto):
    return await create_ration_stock_service(ration_stock)

@router.put("/{ration_stock_id}")
async def update_ration_stock(ration_stock_id: int, ration_stock: update_ration_stock_dto):
    return await update_ration_stock_service(ration_stock)

@router.delete("/{ration_stock_id}")
async def delete_ration_stock(ration_stock_id: int):
    return await delete_ration_stock_service(ration_stock_id=ration_stock_id)