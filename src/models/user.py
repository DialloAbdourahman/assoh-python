from mongoengine import StringField, EmailField, EmbeddedDocumentField
from .base import BaseModel
from enums.user_role_enum import EnumUserRole
from .address import Address
class User(BaseModel):
    fullname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_picture = StringField(required=False)
    role = StringField(choices=[e.value for e in EnumUserRole], required=True, default=EnumUserRole.CLIENT.value)
    address = EmbeddedDocumentField(Address, required=False)