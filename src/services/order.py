import math
from typing import Optional
from dto.response.order import OrderResponseModel, OrderResponseParser
from dto.response.paginated import Paginated
from enums.financial_line_status import EnumFinancialLineStatus
from enums.order_status_enum import EnumOrderStatus
from dto.request.order import CreateOrderDto
from enums.refund_status import EnumRefundStatus
from enums.response_codes import EnumResponseStatusCode
from models.financial_line import FinancialLine
from models.order import Order
from models.ordered_product import OrderedProduct
from models.product import Product
from models.refund import Refund
from models.user import User
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType
from utils_types.user_info_in_token import UserInfoInToken
from mongoengine import get_db, Q
from stripe.checkout import Session
from .stripe import StripeService
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
                        status=EnumOrderStatus.PENDING.value,
                        total=total
                    )
                    order.save(session=session)  # Use session-aware save

                    # Update product quantities inside the transaction
                    for ordered_product in ordered_products:
                        product: Product = Product.objects(id=ordered_product.product.id, deleted=False).first()
                        product.quantity -= ordered_product.quantity
                        product.save(session=session)  # Use session-aware save

            # Get the checkout url 
            checkout_session: Session = StripeService.create_checkout_session(order=order)

            print(f'Stripe url === {checkout_session.url}')
                
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
        
    @staticmethod
    async def cancel_order(user_info:UserInfoInToken, order_id:str):
        try:
            order: Order = Order.objects(id=order_id, client=user_info.id).first()

            if not order:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Order not found.'
                )
            
            if order.status != EnumOrderStatus.PENDING.value:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.CAN_ONLY_CANCEL_PENDING_ORDERS,
                        message='Can only cancel pending orders'
                )
            
            cancellation_result: OrchestrationResultType[OrderResponseModel] = OrderService.remove_order_completely_and_set_status(order=order, status=EnumOrderStatus.CANCELLED)

            return cancellation_result
        except Exception as exc: 
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def cancel_paid_order(user_info:UserInfoInToken, order_id:str):
        try:
            # TODO: Add an env and make sure that we can only cancel a paid order just after 30 mins since it has been paid. (maybe use the paid at for that)
            order: Order = Order.objects(id=order_id, client=user_info.id).first()

            if not order:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Order not found.'
                )
            
            if order.status != EnumOrderStatus.PAID.value:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.CAN_ONLY_CANCEL_PAID_ORDERS,
                        message='Can only cancel paid orders'
                )
            
            cancellation_result: OrchestrationResultType[OrderResponseModel] = OrderService.remove_order_completely_and_set_status(order=order, status=EnumOrderStatus.CANCELLED_AFTER_PAYMENT, unset_financial_lines=True, initial_refund=True)

            return cancellation_result
        except Exception as exc: 
            print(exc)
            return OrchestrationResult.server_error()

    # This method will be when:
        # The user wants to cancel an order that has not been paid for.
        # The user wants to cancel an order that has been paid for. 
        # The cron job cancels the order automatically. 
        # We get a timeout from stripe.
    @staticmethod
    def remove_order_completely_and_set_status(order:Order, status:EnumOrderStatus, unset_financial_lines:bool = False, initial_refund:bool = False) -> OrchestrationResultType[OrderResponseModel]:
        try:
            ordered_products: list[OrderedProduct] = order.products

            # Start a session and a transaction
            with get_db().client.start_session() as session:
                with session.start_transaction():
               
                    # Get all financial lines of this order and mark them as cancelled if the order status is not PENDING.
                    if unset_financial_lines:
                        financial_lines: list[FinancialLine] = FinancialLine.objects(order=order)
                        for financial_line in financial_lines:
                            financial_line.status = EnumFinancialLineStatus.CANCELLED.value
                            financial_line.save(session=session)

                    # Initial refund and store it in db. 
                    if initial_refund:
                        # TODO: Initial stripe refund here. 
                        refund = Refund(
                            client = order.client,
                            status = EnumRefundStatus.PENDING.value,
                            order = order,
                            total = order.total # TODO: Include the cancelling percentage here and maybe give a percentage to the seller too.  
                        )
                        refund.save(session=session)

                    # Restore all the product quantities. 
                    for ordered_product in ordered_products:
                        product: Product = Product.objects(id=str(ordered_product.product.id)).first()
                        product.quantity += ordered_product.quantity
                        product.save(session=session)

                    # Update the order status
                    order.status = status.value
                    order.save(session=session)

            return OrchestrationResult.success(
                    data=OrderResponseParser.parse(order), 
                    message='Order cancelled successfully', 
                    status_code=EnumResponseStatusCode.CANCELLED_SUCCESSFULLY
                )
        except Exception as exc: 
            print(exc)
            return OrchestrationResult.server_error()