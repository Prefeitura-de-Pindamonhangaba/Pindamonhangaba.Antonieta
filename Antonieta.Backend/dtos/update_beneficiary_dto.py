from pydantic import BaseModel

class update_beneficiary_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar um beneficiário.
    """
    id: int
    name: str
    document: str
    address: str
    contact: str
    monthly_limit: int  # Add monthly_limit field