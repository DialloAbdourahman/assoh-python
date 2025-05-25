from mongoengine import StringField, EmailField, EmbeddedDocumentField
from .base import BaseModel
from src.enums.user_role_enum import EnumUserRole
from .address import Address

class User(BaseModel):
    fullname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = StringField(required=False)
    role = StringField(choices=[e.value for e in EnumUserRole], required=True)
    address = EmbeddedDocumentField(Address, required=False)