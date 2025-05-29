from pydantic import BaseModel

class update_ration_stock_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar registro de rações.
    """
    id: int
    name: str
    rationType: str
    unit: str
    stock: int
    description: str