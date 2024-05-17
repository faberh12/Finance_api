from pydantic import BaseModel, Field, validator, model_validator
from typing import Optional

class Income(BaseModel):
    date: str
    description: str
    value: float
    category: str