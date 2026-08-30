from fastapi import APIRouter, Depends
from services.auth_service import BasketService
from utils.instances import get_basket_service

from db.schemas import BasketAdd

router = APIRouter(prefix="/basket", tags=["auth"])

@router.post("/add")
def add(basket_data: BasketAdd, service: BasketService = Depends(get_basket_service)):
    return service.add(basket_data)

@router.get("/get")
def get_all(user_id: int, service: BasketService = Depends(get_basket_service)):
    return service.get_all(user_id)