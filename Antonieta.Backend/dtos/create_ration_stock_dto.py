from pydantic import BaseModel, Field

class create_ration_stock_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar registro de raÃ§Ãµes.
    """
    name: str
    description: str
    unit: str
    stock: float = Field(ge=0, allow_inf_nan=False)