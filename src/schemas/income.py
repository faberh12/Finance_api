from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class Income(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the Income")
    date: Optional[datetime] = Field(default_factory=datetime.now, title="Date when the income was created")
    description: str = Field(min_length=4, max_length=60, title="description of the expense")
    value: float = Field(title="value of the expense")
    category: str = Field(min_length=4, max_length=60, title="category of the expense")
    owner_id: int = Field(ge=1, title="Owner of the expense")
    
@validator("category")
def validate_type(cls, value):
    if value not in {"pago de nomina", "pago contrato", "pago arriendo", "mesada", "otros"}:
        raise ValueError("Type must be either pago de nomina, pago contrato, pago arriendo, mesada, otros")
    return value
class Config:
    json_schema_extra = {
        "example": {
            "date": "example date",
            "description": "example description",
            "value": 5000,
            "category": "example category",
            "owner_id": 1
        }
    }