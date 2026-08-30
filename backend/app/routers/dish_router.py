from fastapi import APIRouter, Depends, UploadFile, File
from db.schemas import DishCreate, DishResponse
from services.dish_service import DishService
from utils.instances import get_dish_service

router = APIRouter(prefix="/dish", tags=["dishes"])

@router.post("/create_by_name")
def create_dish(dish: DishCreate, service: DishService = Depends(get_dish_service)):
    return service.create(dish)

@router.post("/create_by_photo")
def create_dish_by_photo(file: UploadFile = File(...), service: DishService = Depends(get_dish_service)):
    return service.create_by_photo(file)

@router.get("/get", response_model=list[DishResponse])
def get_all_dishes(service: DishService = Depends(get_dish_service)):
    return service.get_all()

@router.delete("/del/{id}")
def delete_dish(id: int, service: DishService = Depends(get_dish_service)):
    service.delete_dish(id)