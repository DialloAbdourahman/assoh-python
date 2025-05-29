from pydantic import Field, BaseModel
from typing import Optional

class CreateCategoryDto(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    description: str = Field(max_length=100)

class UpdateCategoryDto(BaseModel):
    name: Optional[str] = Field(min_length=5, max_length=20, default=None)
    description: Optional[str] = Field(max_length=100, default=None)