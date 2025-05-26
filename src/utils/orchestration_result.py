from typing import Any, TypeVar, Generic, Union
from pydantic import BaseModel
from enums.response_codes import EnumResponseCode, EnumResponseStatusCode 

T = TypeVar("T")

class OrchestrationResultType(BaseModel, Generic[T]):
    code: str
    status_code: str
    message: str
    data: Union[T | None]

class OrchestrationResult:
    @staticmethod
    def success(status_code:EnumResponseStatusCode, message:str, data:Any = None) -> dict:
        return {
            "code": EnumResponseCode.SUCCESS.value,
            "status_code": status_code.value,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def failure(status_code:EnumResponseStatusCode, message:str) -> dict:
        return {
            "code": EnumResponseCode.FAILED.value,
            "status_code": status_code.value,
            "message": message,
            "data": None
        }
    
    @staticmethod
    def server_error() -> dict:
        return {
            "code": EnumResponseCode.SERVER_ERROR.value,
            "status_code": EnumResponseStatusCode.SOMETHING_WENT_WRONG.value,
            "message": "Something went wrong",
            "data": None
        }
    
    @staticmethod
    def unauthorized( message:str, data:Any = None) -> dict:
        return {
            "code": EnumResponseCode.FAILED.value,
            "status_code": EnumResponseStatusCode.UNAUTHORIZED,
            "message": message,
            "data": data
        }