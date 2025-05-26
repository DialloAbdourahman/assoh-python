from fastapi import Header, HTTPException, Depends, status
from utils_types.user_info_in_token import UserInfoInToken
from utils.token_utils import TokenUtils
from typing import Annotated

def get_user(authorization: str = Header(None, alias='Authorization')) -> UserInfoInToken:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header is missing'
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Authorization scheme must be Bearer'
            )
        
        return TokenUtils.decode_access_token(token=token)
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or malformed token'
        )

    
user_info_dependency = Annotated[UserInfoInToken, Depends(get_user)]