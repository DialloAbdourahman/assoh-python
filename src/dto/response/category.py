from pydantic import BaseModel, EmailStr

from dto.response.paginated import Paginated
from .address import AddressResponseModel, parse_returned_address
from typing import Optional
from models.category import Category

class CategoryResponseModel(BaseModel):
    id: str
    name: str 
    description: str 

def parse_returned_category(category: Category):
    return CategoryResponseModel(
        id = str(category.id),
        name = category.name, 
        description = category.description, 
    )

def parse_returned_categories(categories: list[Category]):
    return [
        CategoryResponseModel(
            id = str(item.id),
            name = item.name, 
            description = item.description, 
        ) for item in categories
    ]

