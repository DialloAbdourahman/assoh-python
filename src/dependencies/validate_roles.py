from fastapi import HTTPException, status
from .get_user import user_info_dependency

def validate_roles(roles:list[str]):
    def dependency(user_info:user_info_dependency):
        if user_info.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return user_info
    return dependency


    
    
