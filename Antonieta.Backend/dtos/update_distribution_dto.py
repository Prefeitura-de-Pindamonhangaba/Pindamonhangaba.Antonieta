from pydantic import BaseModel
from datetime import datetime

class update_distribution_dto(BaseModel):
    """
    Data Transfer Object (DTO) para registrar uma distribuição.
    """
    id: int
    ration_id: int
    beneficiary_id: int
    amount: int
    date: datetime