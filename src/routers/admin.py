from fastapi import APIRouter, status, Response, Depends, Path, Query
from dependencies import validate_roles
from dto.response.paginated import Paginated
from enums.response_codes import EnumResponseCode
from dto.response.user import  UserResponseModel
from enums.user_role_enum import EnumUserRole
from utils.orchestration_result import  OrchestrationResultType
from dependencies.validate_roles import validate_roles
from services.admin import AdminService
from utils_types.user_info_in_token import UserInfoInToken

router = APIRouter(tags=['Administration'], prefix='/admin')

@router.post('/{user_id}/restore', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def create_account(
    response: Response, 
    user_id:str = Path(),
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[UserResponseModel] = await AdminService.restore_account(user_id, user_info)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.get('/users', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[Paginated[UserResponseModel]])
async def find_users(
    response: Response, 
    page: int = 1,
    limit: int = 10,
    name:str = Query(default=None),
    email:str = Query(default=None),
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[UserResponseModel] = await AdminService.find_users(page, limit, name, email, user_info)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result


@router.delete('/{user_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def create_account(
    response: Response, 
    user_id:str = Path(),
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[UserResponseModel] = await AdminService.delete_account(user_id, user_info)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result
