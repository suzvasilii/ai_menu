from fastapi import APIRouter, Depends
from schemas.order import OrderCreate
from services.order_service import OrderService
from utils.instances import get_order_service

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/create_order")
def create_order(order: OrderCreate, service: OrderService = Depends(get_order_service)):
    return service.create(order)

@router.get("/rec")
def get_recommendations(
    user_id: int,
    dish_name: str,
    service: OrderService = Depends(get_order_service)
):
    return service.get_recommendations(user_id, dish_name)