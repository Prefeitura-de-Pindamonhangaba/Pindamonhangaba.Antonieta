from pydantic import BaseModel

class create_ration_stock_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar registro de rações.
    """
    name: str
    ration_type_id: int
    unit: str
    stock: int
    description: str