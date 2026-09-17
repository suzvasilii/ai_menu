from fastapi import APIRouter, Depends, UploadFile, File, Form
from schemas.dish import DishCreate, DishResponse
from services.dish_service import DishService
from utils.instances import get_dish_service

router = APIRouter(prefix="/dish", tags=["dish"])


@router.post("/create_by_name", response_model=DishResponse)
def create_dish(dish: DishCreate, service: DishService = Depends(get_dish_service)):
    return service.create_by_name(dish)


@router.post("/create_by_photo", response_model=DishResponse)
def create_dish_by_photo(
    file: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(...),
    english_dish_name: str = Form(None),
    category_changed: bool = Form(False),
    service: DishService = Depends(get_dish_service),
):
    return service.create_by_photo(file, name, category, english_dish_name, category_changed)


@router.get("/get", response_model=list[DishResponse])
def get_all_dishes(service: DishService = Depends(get_dish_service)):
    return service.get_all()


@router.delete("/del/{id}")
def delete_dish(id: int, service: DishService = Depends(get_dish_service)):
    service.delete_dish(id)