from pydantic import BaseModel
from typing import List

class BasketItem(BaseModel):
    name: int
    quantity: int

class BasketAdd(BaseModel):
    user_id: int
    items: List[BasketItem]