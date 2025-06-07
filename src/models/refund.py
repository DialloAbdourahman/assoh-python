from mongoengine import StringField, ReferenceField, FloatField

from enums.financial_line_status import EnumFinancialLineStatus
from enums.refund_status import EnumRefundStatus
from models.order import Order
from .base import BaseModel
from .user import User

class Refund(BaseModel):
    client = ReferenceField(User, required=True)
    status = StringField(choices=[e.value for e in EnumFinancialLineStatus], required=True, default=EnumRefundStatus.CREATED.value)
    order = ReferenceField(Order, required=True)
    original_amount = FloatField(required=True)
    refunded_amount = FloatField(required=True)
    refund_id = StringField()

