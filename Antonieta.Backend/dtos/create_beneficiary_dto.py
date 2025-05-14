from pydantic import BaseModel

class create_beneficiary_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar um novo beneficiário.
    """
    name: str
    document: str
    address: str
    contact: str