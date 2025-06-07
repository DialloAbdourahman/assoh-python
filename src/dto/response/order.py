from pydantic import BaseModel

from dto.response.category import CategoryResponseModel, CategoryResponseParser
from dto.response.ordered_product import OrderedProductResponseModel, OrderedProductResponseParser
from dto.response.paginated import Paginated
from dto.response.user import UserResponseModel, UserResponseParser
from typing import Optional
from models.order import Order
from typing import Union
from enums.order_status_enum import EnumOrderStatus

class OrderResponseModel(BaseModel):
    id: str
    client: UserResponseModel
    total: float 
    status: EnumOrderStatus 
    products: list[OrderedProductResponseModel]
    url: Optional[str]

class OrderResponseParser:
    @staticmethod
    def parse(order: Union[Order, dict], url: Optional[str] = None) -> OrderResponseModel:
        is_dict = isinstance(order, dict)
        data = order if is_dict else order.to_mongo().to_dict()

        return OrderResponseModel(
            id=str(data.get("id") or data.get("_id")),
            total=data.get("total"),
            status=data.get("status"),

            client=UserResponseParser.parse(data.get("client")) if is_dict
                   else UserResponseParser.parse(order.client),
            products= [OrderedProductResponseParser.parse(product) for product in data.get("products")] if is_dict
                     else [OrderedProductResponseParser.parse(product) for product in order.products],

            url=url if url else None,

            created_at=str(data.get("created_at")),
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
            deleted_at=str(data.get("deleted_at")) if data.get("deleted_at") else None
        )

    @staticmethod
    def parse_list(orders: list[Union[Order, dict]]) -> list[OrderResponseModel]:
        return [OrderResponseParser.parse(order) for order in orders]

    @staticmethod
    def parse_paginated(
        orders: list[Union[Order, dict]],
        limit: int,
        page: int,
        total_items: int,
        total_pages: int
    ) -> Paginated[OrderResponseModel]:
        return Paginated[OrderResponseModel](
            items=OrderResponseParser.parse_list(orders),
            limit=limit,
            page=page,
            total_items=total_items,
            total_pages=total_pages
        )
