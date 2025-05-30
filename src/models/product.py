from mongoengine import StringField, ReferenceField, FloatField
from .base import BaseModel
from .user import User
from .category import Category

class Product(BaseModel):
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    picture = StringField(required=False)

    category = ReferenceField(Category, required=True)
    seller = ReferenceField(User, required=True)