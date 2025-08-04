from pydantic import BaseModel
from datetime import datetime

class create_distribution_dto(BaseModel):
    """
    Data Transfer Object (DTO) para registrar nova distribuição.
    """
    ration_id: int
    beneficiary_id: int
    amount: float
    date: datetime