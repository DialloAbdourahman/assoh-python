from pydantic import BaseModel

from dto.response.category import CategoryResponseModel, CategoryResponseParser
from dto.response.order import OrderResponseModel, OrderResponseParser
from dto.response.ordered_product import OrderedProductResponseModel, OrderedProductResponseParser
from dto.response.paginated import Paginated
from dto.response.user import UserResponseModel, UserResponseParser
from typing import Optional
from enums.refund_status import EnumRefundStatus
from models.refund import Refund
from typing import Union
from enums.order_status_enum import EnumOrderStatus

class RefundResponseModel(BaseModel):
    id: str
    status: EnumRefundStatus
    original_amount: float
    refunded_amount: float
    refund_id:str
    client: UserResponseModel
    order: OrderResponseModel

class RefundResponseParser:
    @staticmethod
    def parse(refund: Union[Refund, dict], url: Optional[str] = None) -> RefundResponseModel:

        is_dict = isinstance(refund, dict)
        data = refund if is_dict else refund.to_mongo().to_dict()

        return RefundResponseModel(
            id=str(data.get("id") or data.get("_id")),
            status=data.get("status"),
            original_amount=data.get("original_amount"),
            refunded_amount=data.get("refunded_amount"),
            refund_id=data.get("refund_id"),

            client=UserResponseParser.parse(data.get("client")) if is_dict
                   else UserResponseParser.parse(refund.client),
            order=OrderResponseParser.parse(data.get("order")) if is_dict
                   else OrderResponseParser.parse(refund.order),

            created_at=str(data.get("created_at")),
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
            deleted_at=str(data.get("deleted_at")) if data.get("deleted_at") else None
        )

    @staticmethod
    def parse_list(refunds: list[Union[Refund, dict]]) -> list[RefundResponseModel]:
        return [RefundResponseParser.parse(refund) for refund in refunds]

    @staticmethod
    def parse_paginated(
        refunds: list[Union[Refund, dict]],
        limit: int,
        page: int,
        total_items: int,
        total_pages: int
    ) -> Paginated[RefundResponseModel]:
        return Paginated[RefundResponseModel](
            items=RefundResponseParser.parse_list(refunds),
            limit=limit,
            page=page,
            total_items=total_items,
            total_pages=total_pages
        )
