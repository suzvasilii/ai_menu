from pydantic import BaseModel
from typing import Optional

class DishCreate(BaseModel):
    name: str
    category: str
    image_url: Optional[str] = None
    english_dish_name: Optional[str] = None
    category_changed: bool = False

class DishResponse(BaseModel):
    id: int
    name: str
    category: str
    image_url: str

    class Config:
        from_attributes = True