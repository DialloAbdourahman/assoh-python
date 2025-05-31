from pydantic import BaseModel

from dto.response.category import CategoryResponseModel, CategoryResponseParser
from dto.response.paginated import Paginated
from dto.response.user import UserResponseModel, UserResponseParser
from typing import Optional
from models.product import Product
from typing import Union

class ProductResponseModel(BaseModel):
    id: str
    name: str 
    description: str 
    price: float
    profile: Optional[str] = None
    seller: UserResponseModel
    category: CategoryResponseModel
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]
class ProductResponseParser:
    @staticmethod
    def parse(product: Union[Product, dict]) -> ProductResponseModel:
        is_dict = isinstance(product, dict)
        data = product if is_dict else product.to_mongo().to_dict()

        return ProductResponseModel(
            id=str(data.get("id") or data.get("_id")),
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            picture=data.get("picture") if data.get("picture") else None,

            seller=UserResponseParser.parse(data.get("seller")) if is_dict
                   else UserResponseParser.parse(product.seller),

            category=CategoryResponseParser.parse(data.get("category")) if is_dict
                     else CategoryResponseParser.parse(product.category),

            created_at=str(data.get("created_at")),
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
            deleted_at=str(data.get("deleted_at")) if data.get("deleted_at") else None
        )

    @staticmethod
    def parse_list(products: list[Union[Product, dict]]) -> list[ProductResponseModel]:
        return [ProductResponseParser.parse(product) for product in products]

    @staticmethod
    def parse_paginated(
        products: list[Union[Product, dict]],
        limit: int,
        page: int,
        total_items: int,
        total_pages: int
    ) -> Paginated[ProductResponseModel]:
        return Paginated[ProductResponseModel](
            items=ProductResponseParser.parse_list(products),
            limit=limit,
            page=page,
            total_items=total_items,
            total_pages=total_pages
        )
