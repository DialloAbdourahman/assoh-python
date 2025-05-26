from datetime import datetime, timedelta, timezone
from jose import jwt
from utils_types.user_info_in_token import UserInfoInToken
from models.user import User
from .config import access_token_secret_key, algorithm, access_token_duration_in_minutes

class TokenUtils:
    @staticmethod
    def create_access_token(user: User) -> str:
        data = {
            "id":str(user.id),
            "email":user.email,
            "role":user.role
        }

        now = datetime.now(timezone.utc)

        payload = {
            "user": data,
            "iat": now,
            "exp": now + timedelta(minutes=int(access_token_duration_in_minutes)),
            "sub": data.get('id')
        }

        return jwt.encode(payload, access_token_secret_key, algorithm=algorithm)
     
    @staticmethod
    def decode_access_token(token:str) -> UserInfoInToken:
        payload = jwt.decode(token, access_token_secret_key, algorithm)

        decoded_user = payload.get("user", {})

        user_info = UserInfoInToken(
            id=decoded_user.get("id"),
            email=decoded_user.get("email"),
            role=decoded_user.get("role")
        )

        return user_info