from pydantic import BaseModel

class create_ration_stock_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar registro de rações.
    """
    name: str
    description: str
    unit: str
    stock: int