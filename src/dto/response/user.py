from pydantic import BaseModel, EmailStr

from dto.response.paginated import Paginated
from .address import AddressResponseModel, AddressResponseParser
from typing import Optional, Union
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

class UserResponseParser:
    @staticmethod
    def parse(user: Union[User, dict]) -> UserResponseModel:
        is_dict = isinstance(user, dict)
        data = user if is_dict else user.to_mongo().to_dict()
        
        return UserResponseModel(
            id=str(data.get("id") or data.get("_id")),
            fullname=data.get("fullname"),
            email=data.get("email"),
            address=AddressResponseParser.parse(data.get("address")) if data.get("address") else None,
            role=data.get("role"),
            created_at=str(data.get("created_at")),
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
            deleted_at=str(data.get("deleted_at")) if data.get("deleted_at") else None    
        )

    @staticmethod
    def parse_list(users: list[Union[User, dict]]) -> list[UserResponseModel]:
        return [UserResponseParser.parse(user) for user in users]

    @staticmethod
    def parse_paginated(
        users: list[Union[User, dict]],
        limit: int,
        page: int,
        total_items: int,
        total_pages: int
    ) -> Paginated[list[UserResponseModel]]:
        return Paginated[UserResponseModel](
            items=UserResponseParser.parse_list(users),
            limit=limit,
            page=page,
            total_items=total_items,
            total_pages=total_pages
        )
    
    def parse_logged_in_user(user: User, access_token: str, refresh_token: str = None) -> LoginResponseModel:
        return LoginResponseModel(
            user = UserResponseParser.parse(user),
            access_token =  access_token, 
            refresh_token = refresh_token if refresh_token else 'Coming soon'
        )

