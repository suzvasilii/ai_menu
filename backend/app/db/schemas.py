from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    login: str

class DishCreate(BaseModel):
    name: str
    local_path: Optional[str] = None

class DishResponse(BaseModel):
    id: int
    name: str
    image_url: str

    class Config:
        from_attributes = True

class BasketItem(BaseModel):
    name: int
    quantity: int

class BasketAdd(BaseModel):
    user_id: int
    items: List[BasketItem]

class OrderItem(BaseModel):
    name: str
    quantity: int

class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    user_id: int
    comment: Optional[str] = None
    dishes: List[OrderItem]
