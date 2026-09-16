from pydantic import BaseModel
from typing import Optional

class DishCreate(BaseModel):
    name: str
    category: str
    local_path: Optional[str] = None

class DishResponse(BaseModel):
    id: int
    name: str
    category: str
    image_url: str

    class Config:
        from_attributes = True