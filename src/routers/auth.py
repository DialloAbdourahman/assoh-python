from fastapi import APIRouter, status, Response, Depends
from enums.response_codes import EnumResponseCode
from services.auth import AuthService
from dto.request.user import CreateUserRequestDto, LoginUserRequestDto, UpdateUserRequestDto
from dto.response.user import  UserResponseModel, LoginResponseModel
from utils.orchestration_result import  OrchestrationResultType
from dependencies.get_user import user_info_dependency

router = APIRouter(tags=['Authentication'], prefix='/auth')

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrchestrationResultType[UserResponseModel])
async def create_account(response: Response, user_request: CreateUserRequestDto):
    result: OrchestrationResultType[UserResponseModel] = await AuthService.create_account(user_request)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.post('/login', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[LoginResponseModel])
async def login(response: Response, login_request: LoginUserRequestDto):
    result: OrchestrationResultType[LoginResponseModel] = await AuthService.login(login_request)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.get('/profile', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def get_profile(response: Response, user_info:user_info_dependency):
    result: OrchestrationResultType[UserResponseModel] = await AuthService.get_profile(user_info)

    print(f'The result {result}')

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

@router.put('/', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[UserResponseModel])
async def update_account(response: Response, user_info:user_info_dependency, user_request: UpdateUserRequestDto):
    result: OrchestrationResultType[UserResponseModel] = await AuthService.update_account(user_request, user_info)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

# @router.get('/test-validate-role', status_code=status.HTTP_200_OK)
# async def test_validate_role(response: Response,  user_info: UserInfoInToken = Depends(validate_roles([EnumUserRole.SELLER.value]))):
#     return 'Authorized'


