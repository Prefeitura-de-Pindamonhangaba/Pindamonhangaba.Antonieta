from pydantic import BaseModel

class update_beneficiary_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar um novo beneficiário.
    """
    id: int
    name: str
    document: str
    address: str
    contact: str