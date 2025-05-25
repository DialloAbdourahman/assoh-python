from fastapi import APIRouter, status, Response
from enums.response_codes import EnumResponseCode
from services.auth import AuthService
from dto.request.user import CreateUserRequestDto
from dto.response.user import parse_returned_user, UserResponseModel
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType

router = APIRouter(tags=['Authentication'], prefix='/auth')

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrchestrationResultType[UserResponseModel])
async def create_account(response: Response, user_request: CreateUserRequestDto):
    result: OrchestrationResultType = await AuthService.create_account(user_request)

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result

        
