from pydantic import BaseModel, Field, validator
from typing import Optional, Union
from datetime import datetime

class Report(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the report")
    date_created: Optional[datetime] = Field(default_factory=datetime.now, title="Date when the report was created")
    type: str = Field(title="Type of the report", description="The type can be either 'basic' or 'extended'")
    description: Union[dict, None] = Field(default=None, title="Description of the report", description="Detailed information of the report")

    @validator("type")
    def validate_type(cls, value):
        if value not in {"basic", "extended"}:
            raise ValueError("Type must be either basic or extended")
        return value

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "date_created": "2024-05-19T15:30:00",
                "type": "basic",
                "description": {
                    "incomes": {
                        "category1": {},
                        "category2": {}
                    },
                    "expenses": {
                        "category1": {},
                        "category2": {}
                    }
                }
            }
        }
