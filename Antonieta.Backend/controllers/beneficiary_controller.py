from fastapi import APIRouter
from services.beneficiary_services import get_all_beneficiaries

router = APIRouter(prefix="/beneficiary", tags=["Beneficiary"])

@router.get("/")
async def get_all_beneficiaries_endpoint():
    
    return await get_all_beneficiaries()

@router.get("/{beneficiary_id}")
async def get_beneficiary_by_id(beneficiary_id: int):
    return 

@router.post("/")
async def create_beneficiary():
    return 

@router.put("/{beneficiary_id}")
async def create_beneficiary(beneficiary_id: int):
    return 

@router.delete("/{beneficiary_id}")
async def create_beneficiary(beneficiary_id: int):
    return 