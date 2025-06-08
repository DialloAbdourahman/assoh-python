from mongoengine import get_db
from enums.financial_line_status import EnumFinancialLineStatus
from enums.order_status_enum import EnumOrderStatus
from enums.refund_status import EnumRefundStatus
from models.order import Order
from models.ordered_product import OrderedProduct
from models.financial_line import FinancialLine
from datetime import datetime

from models.refund import Refund

class WebhookService:
    @staticmethod
    def checkout_success(order_id:str, payment_intent_id:str):
        if not order_id or not payment_intent_id:
            raise ValueError("Missing order_id or payment_intent_id")

        order: Order = Order.objects(id=order_id, deleted=False).first()

        if order is None:
            raise ValueError("Order does not exist")
        
        # Make this function more idempotent and make sure that the event is not treated twice. 
        if order.status != EnumOrderStatus.PENDING.value:
            return
        
        products: list[OrderedProduct] = order.products

        # Start a session and a transaction
        with get_db().client.start_session() as session:
            with session.start_transaction():
                # Create a financial line for each product ordered
                for product in products:
                    financial_line = FinancialLine(
                        seller=product.product.seller,
                        product=product.product,
                        status=EnumFinancialLineStatus.PENDING.value,
                        price=product.price_at_order,
                        quantity=product.quantity,
                        order=order,
                        total=product.price_at_order * product.quantity
                    )
                    financial_line.save(session=session)

                # Update the order status
                order.status = EnumOrderStatus.PAID.value
                order.payment_intent_id = payment_intent_id
                order.paid_at = datetime.utcnow()
                order.save(session=session)
            

    @staticmethod
    def handle_refund_created(refund_id:str):
        if not refund_id:
            raise ValueError("Missing refund_id or payment_intent_id")

        refund: Refund = Refund.objects(refund_id=refund_id, deleted=False).first()

        if refund is None:
            raise ValueError("Refund does not exist")
        
        # Make this function more idempotent and make sure that the event is not treated twice. 
        if refund.status != EnumRefundStatus.CREATED.value:
            return
        
        refund.status = EnumRefundStatus.INITIATED.value 
        refund.save()

    @staticmethod
    def handle_refund_succeeded(refund_id:str):
        if not refund_id:
            raise ValueError("Missing refund_id or payment_intent_id")

        refund: Refund = Refund.objects(refund_id=refund_id, deleted=False).first()

        if refund is None:
            raise ValueError("Refund does not exist")
        
        # Make this function more idempotent and make sure that the event is not treated twice. 
        if refund.status != EnumRefundStatus.INITIATED.value:
            return
        
        refund.status = EnumRefundStatus.SUCCESS.value
        refund.save() 

    @staticmethod
    def handle_refund_failed(refund_id:str):
        if not refund_id:
            raise ValueError("Missing refund_id or payment_intent_id")

        refund: Refund = Refund.objects(refund_id=refund_id, deleted=False).first()

        if refund is None:
            raise ValueError("Refund does not exist")
        
        # Make this function more idempotent and make sure that the event is not treated twice. 
        if refund.status != EnumRefundStatus.INITIATED.value:
            return
        
        refund.status = EnumRefundStatus.FAILED.value
        refund.save()
            


        
        

        
        
