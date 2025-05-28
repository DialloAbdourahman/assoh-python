import math
from dto.response.user import UserResponseModel, parse_returned_paginated_users
from dto.response.user import parse_returned_user
from enums.response_codes import EnumResponseStatusCode
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
                        status_code=EnumResponseStatusCode.ACCOUNT_DELETED_ALREADY,
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
                data=parse_returned_user(user), 
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
                    status_code=EnumResponseStatusCode.ACCOUNT_RESTORED_ALREADY,
                    message='This account has been deleted already.'
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
                data=parse_returned_user(user), 
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

            users: User = User.objects(filters).skip(skip).limit(limit)

            return OrchestrationResult.success(
                data=parse_returned_paginated_users(
                    users=users,
                    total_pages=total_pages,
                    limit=limit,
                    page=page,
                    total_items=total_items
                ), 
                message='Account deleted successfully', 
                status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        