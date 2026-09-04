from pydantic import BaseModel
from typing import Optional, List

class OrderItem(BaseModel):
    name: str
    quantity: int

class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    user_id: int
    comment: Optional[str] = None
    dishes: List[OrderItem]
