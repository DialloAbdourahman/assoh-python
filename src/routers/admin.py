from fastapi import APIRouter, status, Response, Depends, Path, Query
from dependencies import validate_roles
from dto.request.category import CreateCategoryDto, UpdateCategoryDto
from dto.response.category import CategoryResponseModel
from dto.response.paginated import Paginated
from dto.response.refund import RefundResponseModel
from enums.refund_status import EnumRefundStatus
from enums.response_codes import EnumResponseCode
from dto.response.user import  UserResponseModel
from enums.user_role_enum import EnumUserRole
from utils.orchestration_result import  OrchestrationResultType
from dependencies.validate_roles import validate_roles
from services.admin import AdminService
from utils_types.user_info_in_token import UserInfoInToken

router = APIRouter(tags=['Administration'], prefix='/admin')

@router.post('/users/{user_id}/restore', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def restore_account(
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


@router.delete('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def delete_account(
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

@router.put('/users/{user_id}/change-user-role', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def change_user_role(
    response: Response, 
    user_id:str = Path(),
    role: EnumUserRole = Query(),
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[UserResponseModel] = await AdminService.change_user_role(user_id, role, user_info)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.post('/category', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[CategoryResponseModel])
async def create_category(
    response: Response, 
    category_request:CreateCategoryDto,
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[CategoryResponseModel] = await AdminService.create_category(category_request)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.put('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[CategoryResponseModel])
async def update_category(
    response: Response, 
    category_request:UpdateCategoryDto,
    category_id:str = Path(),
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[CategoryResponseModel] = await AdminService.update_category(category_id, category_request)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.delete('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[CategoryResponseModel])
async def delete_category(
    response: Response, 
    category_id:str = Path(),
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[CategoryResponseModel] = await AdminService.delete_category(category_id)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.post('/category/{category_id}/restore', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[CategoryResponseModel])
async def restore_category(
    response: Response, 
    category_id:str = Path(),
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[CategoryResponseModel] = await AdminService.restore_category(category_id)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.post('/refund/{refund_id}/retry', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[RefundResponseModel])
async def retry_refund(
    response: Response, 
    refund_id:str = Path(),
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[RefundResponseModel] = await AdminService.retry_refund(refund_id)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.get('/refund/{refund_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[RefundResponseModel])
async def get_refund(
    response: Response, 
    refund_id:str = Path(),
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[RefundResponseModel] = await AdminService.get_refund(refund_id)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.get('/refund', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[Paginated[RefundResponseModel]])
async def get_refunds(
    response: Response, 
    status:EnumRefundStatus = Query(),
    page:int = 1,
    limit:int = 10,    
    _: UserInfoInToken = Depends(validate_roles([EnumUserRole.ADMIN.value]))
):
    result: OrchestrationResultType[Paginated[RefundResponseModel]] = await AdminService.get_refunds(page, limit, status)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

