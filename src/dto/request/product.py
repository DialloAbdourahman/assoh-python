from pydantic import Field, BaseModel

class CreateProductDto(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    description: str = Field(max_length=100)
    price: float = Field(min=0)
    category_id:str = Field()
