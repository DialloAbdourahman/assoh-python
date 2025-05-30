from pydantic import BaseModel, EmailStr

from dto.response.paginated import Paginated
from .address import AddressResponseModel, parse_returned_address
from typing import Optional
from models.category import Category

class CategoryResponseModel(BaseModel):
    id: str
    name: str 
    description: str 
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]

def parse_returned_category(category: Category, private:bool = False):
    return CategoryResponseModel(
        id = str(category.id),
        name = category.name, 
        description = category.description, 
        created_at = str(category.created_at),
        updated_at = str(category.updated_at) if category.updated_at else None,
        deleted_at = str(category.deleted_at) if category.deleted_at else None
    )

def parse_returned_categories(categories: list[Category]):
    return [
        parse_returned_category(category=category) for category in categories
    ]

