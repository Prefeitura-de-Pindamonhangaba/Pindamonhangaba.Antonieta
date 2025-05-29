from pydantic import BaseModel
from datetime import datetime

class create_ration_input_dto(BaseModel):
    """
    Data Transfer Object (DTO) para criar registro de entrada de ração.
    """
    ration_stock_id: int
    amount: int
    date: datetime
    description: str