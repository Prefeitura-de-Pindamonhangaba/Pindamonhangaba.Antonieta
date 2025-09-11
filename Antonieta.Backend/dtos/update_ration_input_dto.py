from pydantic import BaseModel
from datetime import datetime

class update_ration_input_dto(BaseModel):
    """
    Data Transfer Object (DTO) para atualizar registro de entrada de ração.
    """
    id: int
    ration_stock_id: int
    amount: float
    date: datetime
    description: str