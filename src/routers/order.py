from fastapi import APIRouter, status, Response, Depends, Path, Query
from dependencies import validate_roles
from dto.request.category import CreateCategoryDto, UpdateCategoryDto
from dto.request.order import CreateOrderDto
from dto.response.category import CategoryResponseModel
from dto.response.order import OrderResponseModel
from dto.response.paginated import Paginated
from enums.order_status_enum import EnumOrderStatus
from enums.response_codes import EnumResponseCode
from dto.response.user import  UserResponseModel
from enums.user_role_enum import EnumUserRole
from utils.orchestration_result import  OrchestrationResultType
from dependencies.validate_roles import validate_roles
from services.order import OrderService
from utils_types.user_info_in_token import UserInfoInToken

router = APIRouter(tags=['Order'], prefix='/order')

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrchestrationResultType[OrderResponseModel])
async def create_order(
    response: Response, 
    order_request:CreateOrderDto,
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.CLIENT.value]))
):
    result: OrchestrationResultType[OrderResponseModel] = await OrderService.create_order(user_info=user_info, data=order_request)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.get('/', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[Paginated[OrderResponseModel]])
async def get_my_orders(
    response: Response, 
    page:int = 1,
    limit:int = 10,
    order_status: EnumOrderStatus = Query(default=None),
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.CLIENT.value]))
):
    result: OrchestrationResultType[Paginated[OrderResponseModel]] = await OrderService.get_my_orders(page=page, limit=limit, user_info=user_info, order_status=order_status)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.post('/cancel/paid/{order_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[OrderResponseModel])
async def cancel_paid_order(
    response: Response, 
    order_id:str,
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.CLIENT.value]))
):
    result: OrchestrationResultType[OrderResponseModel] = await OrderService.cancel_paid_order(user_info=user_info, order_id=order_id)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.post('/cancel/{order_id}', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[OrderResponseModel])
async def cancel_order(
    response: Response, 
    order_id:str,
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.CLIENT.value]))
):
    result: OrchestrationResultType[OrderResponseModel] = await OrderService.cancel_order(user_info=user_info, order_id=order_id)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

