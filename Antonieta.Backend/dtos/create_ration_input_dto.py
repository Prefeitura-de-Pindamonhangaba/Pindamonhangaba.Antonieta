from pydantic import BaseModel, Field
from datetime import datetime

class create_ration_input_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar registro de entrada de ração.
    """
    ration_stock_id: int
    amount: float = Field(gt=0, allow_inf_nan=False)
    date: datetime
    description: str
