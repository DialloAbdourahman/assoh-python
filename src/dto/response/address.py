from pydantic import BaseModel
from typing import Optional
from models.address import Address 

class AddressResponseModel(BaseModel):
    country: Optional[str] 
    city: Optional[str]
    street_name: Optional[str] 
    street_number: Optional[str] 
    postal_code : Optional[str] 

def parse_returned_address(address: Address):
    return AddressResponseModel(
        country= address.country, 
        city= address.city,
        street_name= address.street_name,
        street_number= address.street_number,
        postal_code = address.postal_code,
    )
