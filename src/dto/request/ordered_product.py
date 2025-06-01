from pydantic import BaseModel, Field


class OrderedProductDto(BaseModel):
    product_id: str = Field()
    quantity: int = Field(gt=0)