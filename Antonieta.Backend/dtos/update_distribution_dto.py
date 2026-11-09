from pydantic import BaseModel, Field
from datetime import datetime

class update_distribution_dto(BaseModel):
    """
    Data Transfer Object (DTO) para registrar uma distribuiÃ§Ã£o.
    """
    id: int
    ration_id: int
    beneficiary_id: int
    amount: float = Field(gt=0, allow_inf_nan=False)
    date: datetime
    observations: str | None = None
