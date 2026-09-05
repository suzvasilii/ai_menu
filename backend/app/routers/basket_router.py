from fastapi import APIRouter, Depends
from services.basket_service import BasketService
from utils.instances import get_basket_service
from schemas.basket import BasketAdd

router = APIRouter(prefix="/basket", tags=["basket"])

@router.post("/add")
def add(basket_data: BasketAdd, service: BasketService = Depends(get_basket_service)):
    return service.add(basket_data)

@router.get("/get")
def get_all(user_id: int, service: BasketService = Depends(get_basket_service)):
    return service.get_all(user_id)