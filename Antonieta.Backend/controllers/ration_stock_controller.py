from fastapi import APIRouter, HTTPException
from services.ration_stock_services import get_all_ration_stock_service, get_ration_stock_by_id_service, create_ration_stock_service, update_ration_stock_service, delete_ration_stock_service
from dtos.update_ration_stock_dto import update_ration_stock_dto
from dtos.create_ration_stock_dto import create_ration_stock_dto

router = APIRouter(prefix="/ration-stock", tags=["ration-stock"])

@router.get("/")
async def get_all_ration_stock():
    return await get_all_ration_stock_service()

@router.get("/{ration_stock_id}")
async def get_ration_stock_by_id(ration_stock_id: int):
    record = await get_ration_stock_by_id_service(ration_stock_id=ration_stock_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Ração não encontrada")
    return record

@router.post("/")
async def create_ration_stock(ration_stock: create_ration_stock_dto):
    return await create_ration_stock_service(ration_stock)

@router.put("/{ration_stock_id}")
async def update_ration_stock(ration_stock_id: int, ration_stock: update_ration_stock_dto):
    if ration_stock_id != ration_stock.id:
        raise HTTPException(status_code=400, detail="ID da rota não corresponde ao ID do corpo da requisição")
    record = await update_ration_stock_service(ration_stock)
    if record is None:
        raise HTTPException(status_code=404, detail="Ração não encontrada")
    return record

@router.delete("/{ration_stock_id}")
async def delete_ration_stock(ration_stock_id: int):
    if not await delete_ration_stock_service(ration_stock_id=ration_stock_id):
        raise HTTPException(status_code=404, detail="Ração não encontrada")
    return True