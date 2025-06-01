from pydantic import BaseModel
from typing import Optional, Union
from models.category import Category

class CategoryResponseModel(BaseModel):
    id: str
    name: str 
    description: str 
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]

class CategoryResponseParser:
    @staticmethod
    def parse(category: Union[Category, dict]) -> CategoryResponseModel:
        is_dict = isinstance(category, dict)
        data = category if is_dict else category.to_mongo().to_dict()
        
        return CategoryResponseModel(
            id=str(data.get("id") or data.get("_id")),
            name=data.get("name"),
            description=data.get("description"),
            created_at=str(data.get("created_at")),
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
            deleted_at=str(data.get("deleted_at")) if data.get("deleted_at") else None
        )

    @staticmethod
    def parse_list(categories: list[Union[Category, dict]], private: bool = False) -> list[CategoryResponseModel]:
        return [CategoryResponseParser.parse(category, private) for category in categories]

