from mongoengine import StringField
from .base import BaseModel

class Category(BaseModel):
    name = StringField(required=True, unique=True)
    description = StringField(required=False, unique=True)