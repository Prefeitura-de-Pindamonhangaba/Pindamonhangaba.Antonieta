from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class update_distribution_dto(BaseModel):
    """
    Data Transfer Object (DTO) para registrar uma distribuição.
    """
    id: int
    ration_id: int
    beneficiary_id: int
    amount: float = Field(gt=0, allow_inf_nan=False)
    date: datetime
    observations: Optional[str] = None
