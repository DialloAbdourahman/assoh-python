import math
from typing import Optional
from dto.response.order import OrderResponseModel, OrderResponseParser
from dto.response.paginated import Paginated
from enums.order_status_enum import EnumOrderStatus
from models.address import Address
from dto.request.user import CreateUserRequestDto, LoginUserRequestDto, UpdateUserRequestDto
from dto.response.user import UserResponseModel, LoginResponseModel
from dto.request.order import CreateOrderDto
from enums.response_codes import EnumResponseStatusCode
from models.order import Order
from models.ordered_product import OrderedProduct
from models.product import Product
from models.user import User
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType
from utils.password_utils import PasswordUtils
from utils.token_utils import TokenUtils
from utils_types.user_info_in_token import UserInfoInToken
from datetime import datetime
from mongoengine import get_db, Q

class OrderService:
    @staticmethod
    async def create_order(user_info:UserInfoInToken, data:CreateOrderDto) -> OrchestrationResultType[OrderResponseModel]:
        try:
            # Get the client 
            client = User.objects(id=user_info.id, deleted=False).first()
            if client is None:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Client does not exist.'
                    )

            # Build the ordered products list 
            print(f'Building the ordered products:: {data.products}')
            ordered_products: list[OrderedProduct] = []

            for product in data.products:
                existing_product: Product = Product.objects(id=product.product_id, deleted=False).first()

                if existing_product is None:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.PRODUCT_NOT_FOUND,
                        message='Product does not exist.'
                    )
                
                if (existing_product.quantity - product.quantity) < 0:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.PRODUCT_QUANTITY_MISMATCH,
                        message='Not enough product.'
                    )
                
                if existing_product.seller.deleted == True:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
                        message='Seller not found.'
                    )
                
                ordered_product = OrderedProduct(
                    product=existing_product,
                    price_at_order=existing_product.price,
                    quantity=product.quantity
                )

                ordered_products.append(ordered_product)

            # Start a session and a transaction
            with get_db().client.start_session() as session:
                with session.start_transaction():
                    # Calculate total
                    total = sum(
                        ordered_product.price_at_order * ordered_product.quantity 
                        for ordered_product in ordered_products
                    )

                    # Create and save the order inside the transaction
                    order = Order(
                        products=ordered_products,
                        client=client,
                        status=EnumOrderStatus.CREATED.value,
                        total=total
                    )
                    order.save(session=session)  # Use session-aware save

                    # Update product quantities inside the transaction
                    for ordered_product in ordered_products:
                        product: Product = Product.objects(id=ordered_product.product.id, deleted=False).first()
                        product.quantity -= ordered_product.quantity
                        product.save(session=session)  # Use session-aware save
                
            return OrchestrationResult.success(
                data=OrderResponseParser.parse(order), 
                message='Order created successfully', 
                status_code=EnumResponseStatusCode.CREATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def get_my_orders(page:int, limit:int, user_info:UserInfoInToken, order_status:Optional[EnumOrderStatus]) -> OrchestrationResultType[Paginated[OrderResponseModel]]:
        try:
            client = User.objects(id=user_info.id, deleted=False).first()

            if client is None:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Client does not exist.'
                    )

            filter_query = Q(deleted=False, client=client)

            if order_status is not None:
                filter_query &= Q(status=order_status.value)
                
            skip = (page - 1) * limit
            total_items = Order.objects(filter_query).count()
            total_pages = math.ceil(total_items / limit)

            orders: list[Order] = Order.objects(filter_query).skip(skip).limit(limit)

            return OrchestrationResult.success(
                data=OrderResponseParser.parse_paginated(
                    orders=orders,
                    total_pages=total_pages,
                    limit=limit,
                    page=page,
                    total_items=total_items
                ), 
                message='Recovered successfully successfully', 
                status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()