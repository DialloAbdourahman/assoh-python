from typing import Optional
from pydantic import Field, BaseModel
from dto.request.ordered_product import OrderedProductDto

class CreateOrderDto(BaseModel):
    products: list[OrderedProductDto] = Field()
