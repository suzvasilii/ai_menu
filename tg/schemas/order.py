from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    name: str
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    comment: str | None = None
    items: List[OrderItem]