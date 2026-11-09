from pydantic import BaseModel, Field

class update_ration_stock_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar registro de raÃ§Ãµes.
    """
    id: int
    name: str
    description: str
    unit: str
    stock: float = Field(ge=0, allow_inf_nan=False)