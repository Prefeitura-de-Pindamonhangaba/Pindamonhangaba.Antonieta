from fastapi import APIRouter

router = APIRouter()

@router.get("/beneficiary")
async def get_all_beneficiaries():
    return 

@router.get("/beneficiary/{beneficiary_id}")
async def get_beneficiary_by_id(beneficiary_id: int):
    return 

@router.post("/beneficiary")
async def create_beneficiary():
    return 

@router.put("/beneficiary")
async def create_beneficiary(beneficiary_id: int):
    return 

@router.delete("/beneficiary/{beneficiary_id}")
async def create_beneficiary(beneficiary_id: int):
    return 