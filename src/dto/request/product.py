from typing import Optional
from pydantic import Field, BaseModel

class CreateProductDto(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    description: str = Field(max_length=100)
    price: float = Field(min=0)
    quantity: int = Field(min=0)
    category_id:str = Field()

class UpdateProductDto(BaseModel):
    name: Optional[str] = Field(min_length=5, max_length=20, default=None)
    description: Optional[str] = Field(max_length=100, default=None)
    quantity: Optional[int] = Field(min=0, default=None)
    price: Optional[float] = Field(min=0, default=None)
    category_id:Optional[str] = Field(default=None)
