from mongoengine import EmbeddedDocument, ReferenceField, FloatField, IntField
from .product import Product

class OrderedProduct(EmbeddedDocument):
    product = ReferenceField(Product, required=True)
    price_at_order = FloatField(required=True)
    quantity = IntField(required=True)