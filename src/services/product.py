import json
import math

from bson import ObjectId
from dto.request.product import CreateProductDto, UpdateProductDto
from dto.response.paginated import Paginated
from dto.response.product import ProductResponseModel, ProductResponseParser
from enums.response_codes import EnumResponseStatusCode
from models.category import Category
from models.product import Product
from models.user import User
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType
from utils_types.user_info_in_token import UserInfoInToken
from datetime import datetime
from mongoengine import Q

class ProductService:
    @staticmethod
    async def create_product(data:CreateProductDto, user_info:UserInfoInToken) -> OrchestrationResultType[ProductResponseModel]:
        try:
            seller = User.objects(id=user_info.id, role=user_info.role, deleted=False).first()

            if not seller:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
                    message='Seller does not exist'
                )

            category = Category.objects(id=data.category_id, deleted=False).first()
            
            if not category:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.CATEGORY_NOT_FOUND,
                    message='Category does not exist'
                )

            product: Product = Product(
                name = data.name,
                description = data.description,
                price = data.price,
                seller = seller,
                category = category
            )
            product.save()

            return OrchestrationResult.success(
                data=ProductResponseParser.parse(product), 
                message='Product created successfully', 
                status_code=EnumResponseStatusCode.CREATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    # @staticmethod
    # async def search_product(
    #     page:int,
    #     limit:int,
    #     product_name: str,
    #     seller_id: str,
    #     category_id: str,
    #     min_price: float,
    #     max_price: float,
    # ) -> OrchestrationResultType[Paginated[ProductResponseModel]]:
    #     try:
    #         filter_query = Q(deleted=False)

    #         if seller_id is not None:
    #             seller = User.objects(id=seller_id, deleted=False).first()
    #             if not seller:
    #                 return OrchestrationResult.unauthorized(
    #                     status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
    #                     message='Seller does not exist'
    #             )
    #             filter_query &= Q(seller=seller)

    #         if category_id is not None:
    #             category = Category.objects(id=category_id, deleted=False).first()
    #             if not category:
    #                 return OrchestrationResult.unauthorized(
    #                     status_code=EnumResponseStatusCode.CATEGORY_NOT_FOUND,
    #                     message='Category does not exist'
    #                 )
    #             filter_query &= Q(category=category)

    #         if product_name is not None:
    #             filter_query &= Q(name__icontains=product_name)

    #         if min_price is not None:
    #             filter_query &= Q(price__gte=min_price)

    #         if max_price is not None:
    #             filter_query &= Q(price__lte=max_price)

    #         skip = (page - 1) * limit
    #         total_items = Product.objects(filter_query).count()
    #         total_pages = math.ceil(total_items / limit)

    #         products: list[Product] = Product.objects(filter_query).skip(skip).limit(limit)

    #         return OrchestrationResult.success(
    #             data=ProductResponseParser.parse_paginated(
    #                 products=products,
    #                 total_pages=total_pages,
    #                 limit=limit,
    #                 page=page,
    #                 total_items=total_items
    #             ), 
    #             message='Recovered successfully successfully', 
    #             status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
    #         )
    #     except Exception as exc:
    #         print(exc)
    #         return OrchestrationResult.server_error()

    @staticmethod
    async def search_product(
        page:int,
        limit:int,
        product_name: str,
        seller_id: str,
        category_id: str,
        min_price: float,
        max_price: float,
    ) -> OrchestrationResultType[Paginated[ProductResponseModel]]:
        try:
            initial_match_query = {
                "deleted": False,
            }
            if seller_id:
                initial_match_query['seller'] = ObjectId(seller_id)
            if category_id:
                initial_match_query['category'] = ObjectId(category_id)
            if min_price:
                initial_match_query['price'] = {"$gte": min_price}
            if max_price:
                initial_match_query['price'] = {"$lte":max_price}
            if product_name:
                initial_match_query['name'] = {
                    "$regex": product_name,
                    "$options": "i"
                }

            deleted_match_query = {}
            if seller_id:
                deleted_match_query['seller.deleted'] = False
            if category_id:
                deleted_match_query['category.deleted'] = False

            skip = (page - 1) * limit

            pipeline = [
                {
                    "$match": initial_match_query
                },
                {
                    "$lookup": {
                        "from": "category",
                        "localField": "category",
                        "foreignField": "_id",
                        "as": "category"
                    }
                },
                {
                    "$unwind": "$category"
                },
                {
                    "$lookup": {
                        "from": "user",
                        "localField": "seller",
                        "foreignField": "_id",
                        "as": "seller"
                    }
                },
                {
                    "$unwind": "$seller"
                },
                {
                    "$match": deleted_match_query
                },
                {
                    "$set": {
                        "category.id": { "$toString": "$category._id" },
                        "seller.id": { "$toString": "$seller._id" },
                        "id": { "$toString": "$_id" },
                    }
                },
                {
                    "$unset": ["seller._id", "category._id", "_id"]
                }
            ]

            count_pipeline = pipeline.copy()
            pipeline.extend(
                [
                    {
                        "$skip": skip
                    },
                    {
                        "$limit": limit
                    }
                ]
            )
            count_pipeline.append({"$count": "total"})

            products: list[dict] = list(Product.objects.aggregate(*pipeline))
            count_result = list(Product.objects.aggregate(*count_pipeline))
            
            print(f'pipeline {pipeline}')
            print(f'count pipeline {count_pipeline}')
            
            total_items = count_result[0]["total"] if count_result else 0            
            total_pages = math.ceil(total_items / limit)

            return OrchestrationResult.success(
                data=ProductResponseParser.parse_paginated(
                    products=products,
                    total_pages=total_pages,
                    limit=limit,
                    page=page,
                    total_items=total_items
                ), 
                message='Recovered successfully successfully', 
                status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def delete_product(product_id:str, user_info:UserInfoInToken) -> OrchestrationResultType[ProductResponseModel]:
        try:
            seller = User.objects(id=user_info.id, deleted=False).first()
            if not seller:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
                    message='Seller does not exist'
            )
            
            product: Product = Product.objects(id=product_id, seller=seller).first()

            if product is None:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Product does not exist.'
                    )
            
            if product.deleted == True:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.DELETED_ALREADY,
                        message='This product has been deleted already.'
                    )

            product.deleted = True
            product.deleted_at = datetime.utcnow()               
            
            product.save()

            return OrchestrationResult.success(
                data=ProductResponseParser.parse(product), 
                message='Product deleted successfully', 
                status_code=EnumResponseStatusCode.DELETED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def restore_product(product_id:str, user_info:UserInfoInToken) -> OrchestrationResultType[ProductResponseModel]:
        try:
            seller = User.objects(id=user_info.id, deleted=False).first()
            if not seller:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
                    message='Seller does not exist'
            )
            
            product: Product = Product.objects(id=product_id, seller=seller).first()
            if product is None:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='User does not exist.'
                )
            
            if product.deleted == False:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.RESTORED_ALREADY,
                    message='This product has been restored already.'
                )

            product.deleted = False
            product.deleted_at = None               
            
            product.save()

            return OrchestrationResult.success(
                data=ProductResponseParser.parse(product), 
                message='Product deleted successfully', 
                status_code=EnumResponseStatusCode.RESTORED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def update_product(product_id:str, data:UpdateProductDto, user_info:UserInfoInToken) -> OrchestrationResultType[ProductResponseModel]:
        try:
            seller = User.objects(id=user_info.id, deleted=False).first()
            if not seller:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
                    message='Seller does not exist'
            )
            
            product: Product = Product.objects(id=product_id, seller=seller).first()
            if product is None:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='User does not exist.'
                )
            
            if data.name is not None:
                product.name = data.name

            if data.description is not None:
                product.description = data.description

            if data.price is not None:
                product.price = data.price

            if data.category_id is not None:
                category: Category = Category.objects(id=data.category_id, deleted=False).first()
                if not category:
                    return OrchestrationResult.failure(
                            status_code=EnumResponseStatusCode.NOT_FOUND,
                            message='Category does not exist.'
                    )
                product.category = category

            product.updated_at = datetime.utcnow()               
            product.save()

            return OrchestrationResult.success(
                data=ProductResponseParser.parse(product), 
                message='Product updated successfully', 
                status_code=EnumResponseStatusCode.UPDATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        