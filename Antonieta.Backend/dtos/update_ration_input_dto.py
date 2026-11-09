from pydantic import BaseModel, Field
from datetime import datetime

class update_ration_input_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar registro de entrada de ração.
    """
    id: int
    ration_stock_id: int
    amount: float = Field(gt=0, allow_inf_nan=False)
    date: datetime
    description: str
