from dto.request.product import CreateProductDto
from dto.response.product import ProductResponseModel, parse_returned_product
from models.address import Address
from dto.request.user import CreateUserRequestDto, LoginUserRequestDto, UpdateUserRequestDto
from dto.response.user import UserResponseModel, LoginResponseModel
from dto.response.user import parse_returned_user, parse_returned_logged_in_user
from enums.response_codes import EnumResponseStatusCode
from models.category import Category
from models.product import Product
from models.user import User
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType
from utils.password_utils import PasswordUtils
from utils.token_utils import TokenUtils
from utils_types.user_info_in_token import UserInfoInToken
from datetime import datetime

class ProductService:
    @staticmethod
    async def create_product(data:CreateProductDto, user_info:UserInfoInToken) -> OrchestrationResultType[ProductResponseModel]:
        try:
            seller = User.objects(id=user_info.id, deleted=False).first()

            if not seller:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.SELLER_NOT_FOUND,
                    message='Seller does not exist'
                )

            category = Category.objects(id=data.category_id, deleted=False).first()
            
            if not category:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.CATEGORY_NOT_FOUND,
                    message='Seller does not exist'
                )


            product: Product = Product(
                name = data.name,
                description = data.description,
                price = data.price,
                seller = seller,
                category = category
            )
            product.save()

            return OrchestrationResult.success(
                data=parse_returned_product(product), 
                message='Product created successfully', 
                status_code=EnumResponseStatusCode.CREATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        