from pydantic import BaseModel, EmailStr
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

def parse_returned_user(user: User):
    # print(f'The returned user:  {user.to_json()}')

    return UserResponseModel(
        id = str(user.id),
        fullname = user.fullname, 
        email = user.email, 
        address = parse_returned_address(user.address) if user.address else None,
        role = user.role,
        created_at = str(user.created_at)
    )