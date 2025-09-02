from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class create_distribution_dto(BaseModel):
    """
    Data Transfer Object (DTO) para registrar nova distribuição.
    """
    ration_id: int
    beneficiary_id: int
    amount: float
    date: datetime
    observations: Optional[str] = None