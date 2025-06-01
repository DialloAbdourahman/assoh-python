from pydantic import BaseModel
from typing import Union
from dto.response.product import ProductResponseModel, ProductResponseParser
from models.ordered_product import OrderedProduct 

class OrderedProductResponseModel(BaseModel):
    product: ProductResponseModel 
    price_at_order: float
    quantity: int

class OrderedProductResponseParser:
    @staticmethod
    def parse(ordered_product: Union[OrderedProduct, dict]) -> OrderedProductResponseModel:
        is_dict = isinstance(ordered_product, dict)
        data = ordered_product if is_dict else ordered_product.to_mongo().to_dict()
        
        return OrderedProductResponseModel(
            product=ProductResponseParser.parse(data.get("product")) if is_dict else ProductResponseParser.parse(ordered_product.product),
            price_at_order=data.get("price_at_order"),
            quantity=data.get("quantity"),
        )
