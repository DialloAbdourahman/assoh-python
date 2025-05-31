from pydantic import BaseModel
from typing import Optional, Union
from models.address import Address 

class AddressResponseModel(BaseModel):
    country: Optional[str] 
    city: Optional[str]
    street_name: Optional[str] 
    street_number: Optional[str] 
    postal_code : Optional[str] 


class AddressResponseParser:
    @staticmethod
    def parse(address: Union[Address, dict]) -> AddressResponseModel:
        is_dict = isinstance(address, dict)
        data = address if is_dict else address.to_mongo().to_dict()
        
        return AddressResponseModel(
            country=data.get("country"),
            city=data.get("city"),
            street_name=data.get("street_name"),
            street_number=data.get("street_number"),
            postal_code=data.get("postal_code"),
        )
