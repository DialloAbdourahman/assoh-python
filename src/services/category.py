

from dto.response.category import CategoryResponseModel, CategoryResponseParser
from enums.response_codes import EnumResponseStatusCode
from models.category import Category
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType

class CategoryService:
    @staticmethod
    async def get_categories() -> OrchestrationResultType[list[CategoryResponseModel]]:
        try:
            categories: list[Category] = Category.objects(deleted=False)

            return OrchestrationResult.success(
                data=CategoryResponseParser.parse_list(categories=categories), 
                message='Category recovered successfully', 
                status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()