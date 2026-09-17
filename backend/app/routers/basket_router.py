from fastapi import APIRouter, Depends
from services.basket_service import BasketService
from utils.instances import get_basket_service
from schemas.basket import (
    BasketAdd,
    BasketOut,
    BasketRemovePayload,
    BasketUpdatePayload,
    BasketClearPayload,
)

router = APIRouter(prefix="/basket", tags=["basket"])


@router.post("/add", response_model=BasketOut)
def add(basket_data: BasketAdd, service: BasketService = Depends(get_basket_service)):
    return service.add(basket_data)


@router.get("/get", response_model=BasketOut)
def get_all(user_id: int, service: BasketService = Depends(get_basket_service)):
    return service.get_all(user_id)


@router.post("/remove", response_model=BasketOut)
def remove_item(
    payload: BasketRemovePayload,
    service: BasketService = Depends(get_basket_service),
):
    return service.remove_item(payload.user_id, payload.dish_name)


@router.post("/update", response_model=BasketOut)
def update_item(
    payload: BasketUpdatePayload,
    service: BasketService = Depends(get_basket_service),
):
    return service.update_item_quantity(payload.user_id, payload.dish_name, payload.quantity)


@router.post("/clear", response_model=BasketOut)
def clear(
    payload: BasketClearPayload,
    service: BasketService = Depends(get_basket_service),
):
    return service.clear(payload.user_id)