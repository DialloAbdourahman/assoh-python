from mongoengine import ReferenceField, StringField, FloatField, ListField, EmbeddedDocumentField, DateTimeField
from enums.order_status_enum import EnumOrderStatus
from .base import BaseModel
from .user import User
from .ordered_product import OrderedProduct

class Order(BaseModel):
    products = ListField(EmbeddedDocumentField(OrderedProduct, required=True))
    client = ReferenceField(User, required=True)
    status = StringField(choices=[e.value for e in EnumOrderStatus], required=True, default=EnumOrderStatus.PENDING.value)
    total = FloatField(required=True)
    payment_intent_id = StringField(required=False)
    paid_at = DateTimeField(required=False)
