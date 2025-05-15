from pydantic import BaseModel

class create_ration_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar registro de rações.
    """
    name: str
    rationType: str
    unit: str
    stock: int
    description: str