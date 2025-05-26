from datetime import datetime, timedelta, timezone
from jose import jwt

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
     