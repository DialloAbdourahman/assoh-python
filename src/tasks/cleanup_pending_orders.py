from datetime import datetime, timedelta
from enums.order_status_enum import EnumOrderStatus
from models.order import Order
from services.order import OrderService
from utils.config import max_pending_or_failed_order_time_in_minutes

async def cleanup_pending_orders():
    orders: list[Order] = Order.objects(status__in=[EnumOrderStatus.PENDING.value, EnumOrderStatus.PAYMENT_ERROR.value])
    
    for order in orders:
        if datetime.utcnow() - order.created_at > timedelta(minutes=int(max_pending_or_failed_order_time_in_minutes)):
            await OrderService.remove_order_completely_and_set_status(order=order, status=EnumOrderStatus.CANCELLED_AUTOMATICALLY)

