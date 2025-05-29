from fastapi import APIRouter, status, Response
from dto.response.category import CategoryResponseModel
from enums.response_codes import EnumResponseCode
from utils.orchestration_result import  OrchestrationResultType
from services.category import CategoryService

router = APIRouter(tags=['Categories'], prefix='/category')

@router.get('/', status_code=status.HTTP_200_OK, response_model=OrchestrationResultType[list[CategoryResponseModel]])
async def get_categories(
    response: Response, 
):
    result: OrchestrationResultType[list[CategoryResponseModel]] = await CategoryService.get_categories()

    if result.get('code') == EnumResponseCode.FAILED.value:
        response.status_code = status.HTTP_400_BAD_REQUEST

    if result.get('code') == EnumResponseCode.SERVER_ERROR.value:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR    
    
    return result