from pydantic import BaseModel, EmailStr

from dto.response.paginated import Paginated
from .address import AddressResponseModel, parse_returned_address
from typing import Optional
from models.user import User

class UserResponseModel(BaseModel):
    id: str
    fullname: str 
    email: EmailStr 
    address: Optional[AddressResponseModel] = None
    role: str
    created_at: str

class LoginResponseModel(BaseModel):
    user: UserResponseModel
    access_token: str 
    refresh_token: str 


def parse_returned_user(user: User):
    return UserResponseModel(
        id = str(user.id),
        fullname = user.fullname, 
        email = user.email, 
        address = parse_returned_address(user.address) if user.address else None,
        role = user.role,
        created_at = str(user.created_at)
    )

def parse_returned_users(users: list[User]):
    return [
        UserResponseModel(
            id = str(item.id),
            fullname = item.fullname, 
            email = item.email, 
            address = parse_returned_address(item.address) if item.address else None,
            role = item.role,
            created_at = str(item.created_at)
        ) for item in users
    ]

def parse_returned_logged_in_user(user: User, access_token: str, refresh_token: str = None) -> LoginResponseModel:
    return LoginResponseModel(
        user = parse_returned_user(user),
        access_token =  access_token, 
        refresh_token = refresh_token if refresh_token else 'Coming soon'
    )

def parse_returned_paginated_users(
        users: list[User],
        limit: int,
        page: int,
        total_items: int,
        total_pages: int
    ):
    return Paginated[UserResponseModel](
        items= parse_returned_users(users),
        limit=limit,
        page=page,
        total_items=total_items,
        total_pages=total_pages
    )