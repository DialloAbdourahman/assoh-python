from fastapi import APIRouter, status, Response, Depends, Path, Query
from dependencies import validate_roles
from dto.request.category import CreateCategoryDto, UpdateCategoryDto
from dto.request.product import CreateProductDto
from dto.response.category import CategoryResponseModel
from dto.response.paginated import Paginated
from dto.response.product import ProductResponseModel
from enums.response_codes import EnumResponseCode
from dto.response.user import  UserResponseModel
from enums.user_role_enum import EnumUserRole
from utils.orchestration_result import  OrchestrationResultType
from dependencies.validate_roles import validate_roles
from services.product import ProductService
from utils_types.user_info_in_token import UserInfoInToken

router = APIRouter(tags=['Products'], prefix='/product')

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrchestrationResultType[ProductResponseModel])
async def create_product(
    response: Response, 
    product_request: CreateProductDto,
    user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.SELLER.value]))
):
    result: OrchestrationResultType[ProductResponseModel] = await ProductService.create_product(product_request, user_info)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result
