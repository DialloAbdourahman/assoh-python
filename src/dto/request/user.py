from pydantic import BaseModel, Field, EmailStr
from .address import AddressDto
from typing import Optional

class CreateUserRequestDto(BaseModel):
    fullname: str = Field(min_length=5, max_length=30)
    email: EmailStr = Field()
    password: str = Field(min_length=10, max_length=20)
    address: Optional[AddressDto] = None

class LoginUserRequestDto(BaseModel):
    email: EmailStr
    password: str
