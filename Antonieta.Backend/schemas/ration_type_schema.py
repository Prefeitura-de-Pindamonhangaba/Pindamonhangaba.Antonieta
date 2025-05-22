from pydantic import BaseModel
from typing import Optional

class RationTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class RationTypeCreate(RationTypeBase):
    pass

class RationTypeUpdate(RationTypeBase):
    name: Optional[str] = None

class RationType(RationTypeBase):
    id: int

    class Config:
        orm_mode = True