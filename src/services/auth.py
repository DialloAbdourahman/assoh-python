from dto.request.user import CreateUserRequestDto, LoginUserRequestDto
from dto.response.user import UserResponseModel, LoginResponseModel
from dto.response.user import parse_returned_user, parse_returned_logged_in_user
from enums.response_codes import EnumResponseStatusCode
from models.user import User
from utils.orchestration_result import OrchestrationResult, OrchestrationResultType
from utils.password_utils import PasswordUtils
from utils.token_utils import TokenUtils
from utils_types.user_info_in_token import UserInfoInToken

class AuthService:
    @staticmethod
    async def create_account(data:CreateUserRequestDto) -> OrchestrationResultType[UserResponseModel]:
        try:
            existing_user = User.objects(email=data.email).first()
            if existing_user:
                if existing_user.deleted == True:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.ACCOUNT_DELETED,
                        message='You account has been deleted, please contact an admin to restore it. '
                    )                
                else:
                    return OrchestrationResult.failure(
                        status_code=EnumResponseStatusCode.EXISTS_ALREADY,
                        message='User with this email exists already'
                    )
            
            user = User(**data.model_dump())
            user.password = PasswordUtils.hash_password(data.password)
            user.save()

            return OrchestrationResult.success(
                data=parse_returned_user(user), 
                message='Account created successfully', 
                status_code=EnumResponseStatusCode.CREATED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()
        
    @staticmethod
    async def login(data:LoginUserRequestDto) -> OrchestrationResultType[LoginResponseModel]:
        try:
            found_user = User.objects(email=data.email).first()

            if not found_user:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.NOT_FOUND,
                    message='User with this email does not exist'
                )
            
            if found_user.deleted == True:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.ACCOUNT_DELETED,
                    message='You account has been deleted, please contact an admin to restore it. '
                )
            
            if not PasswordUtils.verify_password(plane_password=data.password, hashed_password=found_user.password):
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.INVALID_CREDENTIALS,
                    message='Invalid credentials'
                )
            
            access_token = TokenUtils.create_access_token(user=found_user)

            return OrchestrationResult.success(
                data=parse_returned_logged_in_user(user=found_user,
                access_token=access_token), 
                message='Logged in successfully', 
                status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()

    @staticmethod
    async def get_profile(user_info:UserInfoInToken) -> OrchestrationResultType[UserResponseModel]:
        try:
            found_user = User.objects(id=user_info.id, deleted=False).first()

            if not found_user:
                return OrchestrationResult.unauthorized(
                    status_code=EnumResponseStatusCode.NOT_FOUND,
                    message='User with this email does not exist'
                )

            return OrchestrationResult.success(
                data=parse_returned_user(found_user), 
                message='Profile retrieved successfully', 
                status_code=EnumResponseStatusCode.RECOVERED_SUCCESSFULLY
            )
        except Exception as exc:
            print(exc)
            return OrchestrationResult.server_error()