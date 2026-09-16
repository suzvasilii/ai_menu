from pydantic import BaseModel
from typing import List


class BasketItemAdd(BaseModel):
    dish_name: str
    quantity: int

class BasketAdd(BaseModel):
    user_id: int
    items: List[BasketItemAdd]


class BasketItemOut(BaseModel):
    dish_name: str
    quantity: int
    image_url: str | None = None

    class Config:
        from_attributes = True

class BasketOut(BaseModel):
    id: int
    user_id: int
    items: List[BasketItemOut] = []

    class Config:
        from_attributes = True