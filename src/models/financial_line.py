from mongoengine import StringField, ReferenceField, FloatField, IntField

from enums.financial_line_status import EnumFinancialLineStatus
from models.order import Order
from .base import BaseModel
from .user import User
from .product import Product

class FinancialLine(BaseModel):
    seller = ReferenceField(User, required=True)
    product = ReferenceField(Product, required=True)
    status = StringField(choices=[e.value for e in EnumFinancialLineStatus], required=True, default=EnumFinancialLineStatus.CREATED.value)
    price = FloatField(required=True)
    quantity = IntField(required=True)
    order = ReferenceField(Order, required=True)
    total = FloatField(required=True)

