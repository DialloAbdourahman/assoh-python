from datetime import datetime
from dto.request.user import CreateUserRequestDto
from dto.response.user import parse_returned_user
from enums.response_codes import EnumResponseStatusCode
from models.user import User
from models.address import Address
from utils.orchestration_result import OrchestrationResult

class AuthService:
    @staticmethod
    async def create_account(data:CreateUserRequestDto) -> User:
        try:
            existing_user = User.objects(email=data.email).first()
            if existing_user:
                return OrchestrationResult.failure(
                    status_code=EnumResponseStatusCode.EXISTS_ALREADY,
                    message='User with this email exists already'
                )

            user = User(**data.model_dump())
            user.save()

            return OrchestrationResult.success(
                data=parse_returned_user(user), 
                message='Account created successfully', 
                status_code=EnumResponseStatusCode.CREATED_SUCCESSFULLY
            )
        except Exception as exc:
            return OrchestrationResult.server_error()
