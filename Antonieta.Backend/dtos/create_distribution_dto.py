from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class create_distribution_dto(BaseModel):
    """
    Data Transfer Object (DTO) para registrar nova distribuiÃ§Ã£o.
    """
    ration_id: int
    beneficiary_id: int
    amount: float = Field(gt=0, allow_inf_nan=False)
    date: datetime
    observations: Optional[str] = None