import math
from dto.request.category import CreateCategoryDto, UpdateCategoryDto
from dto.response.category import CategoryResponseModel, CategoryResponseParser
from dto.response.user import UserResponseModel, UserResponseParser 
from dto.response.user import UserResponseParser 
from enums.response_codes import EnumResponseStatusCode
from enums.user_role_enum import EnumUserRole
from models.category import Category
from models.user import User
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType
from datetime import datetime
from mongoengine import Q

from utils_types.user_info_in_token import UserInfoInToken

class AdminService:
    @staticmethod
    async def delete_account(user_id:str, user_info:UserInfoInToken) -> OrchestrationResultType[UserResponseModel]:
        try:
            user: User = User.objects(id=user_id).first()

            if user is None:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='User does not exist.'
                    )
            
            if user.deleted == True:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.DELETED_ALREADY,
                        message='This account has been deleted already.'
                    )
                        
            if str(user.id) == user_info.id:
                 return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.CANNOT_DELETE_YOU_SELF,
                        message='You cannot delete your own account.'
                    )

            user.deleted = True
            user.deleted_at = datetime.utcnow()               
            
            user.save()

            return OrchestrationResult.success(
                data=UserResponseParser.parse(user), 
                message='Account deleted successfully', 
                status_code=EnumResponseStatusCode.DELETED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def restore_account(user_id:str, user_info:UserInfoInToken) -> OrchestrationResultType[UserResponseModel]:
        try:
            user: User = User.objects(id=user_id).first()

            if user is None:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='User does not exist.'
                )
            
            if user.deleted == False:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.RESTORED_ALREADY,
                    message='This account has been restored already.'
                )
                        
            if str(user.id) == user_info.id:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.CANNOT_RESTORE_YOU_SELF,
                    message='You cannot delete your own account.'
                )

            user.deleted = False
            user.deleted_at = None               
            
            user.save()

            return OrchestrationResult.success(
                data=UserResponseParser.parse(user), 
                message='Account deleted successfully', 
                status_code=EnumResponseStatusCode.RESTORED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
    
    @staticmethod
    async def find_users(page:int, limit:int, name:str, email:str, user_info:UserInfoInToken) -> OrchestrationResultType[UserResponseModel]:
        try:
            filters = Q(
                deleted=False, 
                # id__ne=str(user_info.id)
            )

            if name is not None:
                filters &= Q(fullname__icontains=name)
            
            if email is not None:
                filters &= Q(email=email)

            skip = (page - 1) * limit
            total_items = User.objects(filters).count()
            total_pages = math.ceil(total_items / limit)

            users: list[User] = User.objects(filters).skip(skip).limit(limit)

            return OrchestrationResult.success(
                data=UserResponseParser.parse_paginated(
                    users=users,
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
    async def change_user_role(user_id:str, role:EnumUserRole, user_info:UserInfoInToken) -> OrchestrationResultType[UserResponseModel]:
        try:
            user: User = User.objects(id=user_id, deleted=False).first()

            if user is None:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='User does not exist.'
                )
            
            if user.role == role:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.USER_HAS_THIS_ROLE_ALREADY,
                    message='This user has this role already.'
                )
                        
            if str(user.id) == user_info.id:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.CANNOT_CHANGE_YOUR_OWN_ROLE,
                    message='You cannot change your own role.'
                )

            user.role = role.value
            user.updated_at = datetime.utcnow()               
            
            user.save()

            return OrchestrationResult.success(
                data=UserResponseParser.parse(user), 
                message='Account deleted successfully', 
                status_code=EnumResponseStatusCode.UPDATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()

    @staticmethod
    async def create_category(category_request:CreateCategoryDto) -> OrchestrationResultType[CategoryResponseModel]:
        try:
            category: Category = Category(**category_request.model_dump())
            category.save()

            return OrchestrationResult.success(
                data=CategoryResponseParser.parse(category=category), 
                message='Category created successfully', 
                status_code=EnumResponseStatusCode.CREATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def update_category(category_id:str, category_request:UpdateCategoryDto) -> OrchestrationResultType[CategoryResponseModel]:
        try:
            category: Category = Category.objects(id=category_id, deleted=False).first()

            if not category:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Category does not exist.'
                )
            
            category.name = category_request.name if category_request.name else category.name
            category.description = category_request.description if category_request.description else category.description
            category.save()

            return OrchestrationResult.success(
                data=CategoryResponseParser.parse(category=category), 
                message='Category updated successfully', 
                status_code=EnumResponseStatusCode.UPDATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def delete_category(category_id:str) -> OrchestrationResultType[CategoryResponseModel]:
        try:
            category: Category = Category.objects(id=category_id).first()

            if not category:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Category does not exist.'
                )
            
            if category.deleted == True:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.DELETED_ALREADY,
                        message='This category has been deleted already.'
                    )
            
            category.deleted = True
            category.deleted_at = datetime.utcnow()
            category.save()

            return OrchestrationResult.success(
                data=CategoryResponseParser.parse(category=category), 
                message='Category deleted successfully', 
                status_code=EnumResponseStatusCode.DELETED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def restore_category(category_id:str) -> OrchestrationResultType[CategoryResponseModel]:
        try:
            category: Category = Category.objects(id=category_id).first()

            if not category:
                return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.NOT_FOUND,
                        message='Category does not exist.'
                )
            
            if category.deleted == False:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.RESTORED_ALREADY,
                    message='This category has been restored already.'
                )
            
            category.deleted = False
            category.deleted_at = None
            category.save()

            return OrchestrationResult.success(
                data=CategoryResponseParser.parse(category=category), 
                message='Category restored successfully', 
                status_code=EnumResponseStatusCode.RESTORED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
