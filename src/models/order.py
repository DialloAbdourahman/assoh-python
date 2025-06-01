from mongoengine import ReferenceField, StringField, FloatField, ListField, EmbeddedDocumentField
from enums.order_status_enum import EnumOrderStatus
from .base import BaseModel
from .user import User
from .ordered_product import OrderedProduct

class Order(BaseModel):
    products = ListField(EmbeddedDocumentField(OrderedProduct, required=True))
    client = ReferenceField(User, required=True)
    status = StringField(choices=[e.value for e in EnumOrderStatus], required=True, default=EnumOrderStatus.CREATED.value)
    total = FloatField(required=True)
