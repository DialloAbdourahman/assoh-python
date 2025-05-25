from pydantic import Field, BaseModel
from typing import Optional

class AddressDto(BaseModel):
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    street_name: Optional[str] = Field(default=None)
    street_number: Optional[str] = Field(default=None)
    postal_code : Optional[str] = Field(default=None)