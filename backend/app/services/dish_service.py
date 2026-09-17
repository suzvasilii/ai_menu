import os
import io
import uuid
from fastapi import UploadFile
from PIL import Image

from schemas.dish import DishCreate, DishResponse
from repositories.dish_repository import DishRepository
from utils.decorators import service_handle_errors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


class DishService:

    def __init__(self, repo: DishRepository):
        self.repo = repo

    @service_handle_errors(status_code=500)
    def create_by_name(self, dish: DishCreate) -> DishResponse:
        return self.repo.create_dish(dish.name, dish.category, dish.image_url or "")

    @service_handle_errors(status_code=501)
    def create_by_photo(self, file: UploadFile, name: str, category: str) -> DishResponse:
        file.file.seek(0)
        contents = file.file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        unique_id = uuid.uuid4().hex[:10]
        safe_name = f"{name.replace(' ', '_')}_{unique_id}.jpg"
        filepath = os.path.join(UPLOADS_DIR, safe_name)
        image.save(filepath)

        image_url = f"/uploads/{safe_name}"
        return self.repo.create_dish(name, category, image_url)

    @service_handle_errors(status_code=502)
    def get_all(self) -> list[DishResponse]:
        return self.repo.get_all()

    @service_handle_errors(status_code=503)
    def delete_dish(self, id: int):
        self.repo.delete_dish(id)
        return {"status": 200, "detail": "Dish deleted successfully!"}