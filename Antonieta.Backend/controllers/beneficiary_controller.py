from fastapi import APIRouter
from services.beneficiary_services import get_all_beneficiaries_service, get_beneficiary_by_id_service, create_beneficiary_service, update_beneficiary_service, delete_beneficiary_service
from dtos.update_beneficiary_dto import update_beneficiary_dto
from dtos.create_beneficiary_dto import create_beneficiary_dto

router = APIRouter(prefix="/beneficiary", tags=["Beneficiary"])

@router.get("/")
async def get_all_beneficiaries():
    
    return await get_all_beneficiaries_service()

@router.get("/{beneficiary_id}")
async def get_beneficiary_by_id(beneficiary_id: int):
    return await get_beneficiary_by_id_service(beneficiary_id=beneficiary_id)

@router.post("/")
async def create_beneficiary(benefeciary_dto: create_beneficiary_dto):
    return await create_beneficiary_service(beneficiary_dto=benefeciary_dto)

@router.put("/")
async def create_beneficiary(beneficiary_dto: update_beneficiary_dto):
    return update_beneficiary_service(beneficiary_dto=beneficiary_dto)

@router.delete("/{beneficiary_id}")
async def create_beneficiary(beneficiary_id: int):
    return delete_beneficiary_service(beneficiary_id=beneficiary_id)