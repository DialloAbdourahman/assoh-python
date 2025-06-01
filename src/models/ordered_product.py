from mongoengine import StringField, EmbeddedDocument, ReferenceField, FloatField, IntField
from .product import Product

class OrderedProduct(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    price_at_order = FloatField(required=False)
    quantity = IntField(required=False)