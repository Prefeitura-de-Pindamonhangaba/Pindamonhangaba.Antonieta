from fastapi import APIRouter, HTTPException
from services.ration_input_services import (
    get_all_ration_input_service,
    get_ration_input_by_id_service,
    create_ration_input_service,
    update_ration_input_service,
    delete_ration_input_service
)
from dtos.create_ration_input_dto import create_ration_input_dto
from dtos.update_ration_input_dto import update_ration_input_dto

router = APIRouter(prefix="/ration-input", tags=["ration-input"])

@router.get("/")
async def get_all_ration_input():
    """
    Retorna todos os registros de entrada de ração.
    """
    return await get_all_ration_input_service()

@router.get("/{ration_input_id}")
async def get_ration_input_by_id(ration_input_id: int):
    """
    Retorna um registro específico de entrada de ração.
    """
    ration_input = await get_ration_input_by_id_service(ration_input_id)
    if not ration_input:
        raise HTTPException(status_code=404, detail="Registro de entrada não encontrado")
    return ration_input

@router.post("/")
async def create_ration_input(ration_input: create_ration_input_dto):
    """
    Cria um novo registro de entrada de ração.
    """
    return await create_ration_input_service(ration_input)

@router.put("/{ration_input_id}")
async def update_ration_input(ration_input_id: int, ration_input: update_ration_input_dto):
    """
    Atualiza um registro existente de entrada de ração.
    """
    if ration_input_id != ration_input.id:
        raise HTTPException(status_code=400, detail="ID da rota não corresponde ao ID do corpo da requisição")
    
    updated_input = await update_ration_input_service(ration_input)
    if not updated_input:
        raise HTTPException(status_code=404, detail="Registro de entrada não encontrado")
    return updated_input

@router.delete("/{ration_input_id}")
async def delete_ration_input(ration_input_id: int):
    """
    Remove um registro de entrada de ração.
    """
    success = await delete_ration_input_service(ration_input_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registro de entrada não encontrado")
    return {"message": "Registro de entrada removido com sucesso"}