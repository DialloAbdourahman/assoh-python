from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class Paginated(BaseModel, Generic[T]):
    items: list[T]
    total_items: int 
    total_pages: int
    page: int
    limit: int
