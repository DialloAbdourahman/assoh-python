from pydantic import BaseModel, EmailStr

from dto.response.category import CategoryResponseModel, parse_returned_category
from dto.response.paginated import Paginated
from dto.response.user import UserResponseModel, parse_returned_user
from .address import AddressResponseModel, parse_returned_address
from typing import Optional
from models.product import Product

class ProductResponseModel(BaseModel):
    id: str
    name: str 
    description: str 
    price: float
    profile: Optional[str] = None

    seller: UserResponseModel
    category: CategoryResponseModel

    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]


def parse_returned_product(product: Product):
    return ProductResponseModel(
        id = str(product.id),
        name = product.name, 
        description = product.description, 
        price = product.price,
        picture = product.picture if product.picture else None,

        seller = parse_returned_user(product.seller),
        category= parse_returned_category(product.category),

        created_at = str(product.created_at),
        updated_at = str(product.updated_at) if product.updated_at else None,
        deleted_at = str(product.deleted_at) if product.deleted_at else None
    )

# def parse_returned_product(product: dict) -> ProductResponseModel:
#     return ProductResponseModel(
#         id = product.get('id'),
#         name = product.get('name'),
#         description = product.get('description'),
#         price = product.get('price'),
#         picture = product.get('picture') if product.get('picture') else None,
#         # seller = parse_returned_user(product.get('seller')),
#         # category = parse_returned_category(product.get('category')),
#         created_at = str(product.get('created_at')),
#         updated_at = str(product.get('updated_at')) if product.get('updated_at') else None,
#         deleted_at = str(product.get('deleted_at')) if product.get('deleted_at') else None
#     )

def parse_returned_products(products: list[Product]):
    return [
        parse_returned_product(product) for product in products
    ]

def parse_returned_paginated_products(
        products: list[Product],
        limit: int,
        page: int,
        total_items: int,
        total_pages: int
    ):
    return Paginated[ProductResponseModel](
        items= parse_returned_products(products),
        limit=limit,
        page=page,
        total_items=total_items,
        total_pages=total_pages
    )