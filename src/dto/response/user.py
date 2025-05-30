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
    updated_at: Optional[str]
    deleted_at: Optional[str]
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
        created_at = str(user.created_at),
        updated_at = str(user.updated_at) if user.updated_at else None,
        deleted_at = str(user.deleted_at) if user.deleted_at else None    
    )

def parse_returned_users(users: list[User]):
    return [
        parse_returned_user(user=user) for user in users
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