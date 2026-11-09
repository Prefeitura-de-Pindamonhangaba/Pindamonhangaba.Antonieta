from pydantic import BaseModel, Field


class UpdateRationMetadata(BaseModel):
    id: int
    name: str = Field(min_length=1)
    description: str
