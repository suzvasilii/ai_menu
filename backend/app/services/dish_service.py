import io
from fastapi import UploadFile
from PIL import Image

from schemas.dish import DishCreate, DishResponse
from repositories.dish_repository import DishRepository
from utils.decorators import service_handle_errors
from utils.saver import save_found_image, save_classified_image


class DishService:

    def __init__(self, repo: DishRepository):
        self.repo = repo

    @service_handle_errors(status_code=500)
    def create_by_name(self, dish: DishCreate) -> DishResponse:
        image_url = dish.image_url or ""
        if image_url.startswith("http"):
            image_url = save_found_image(dish.name, image_url) or ""
        return self.repo.create_dish(dish.name, dish.category, image_url)

    @service_handle_errors(status_code=501)
    def create_by_photo(self, file: UploadFile, name: str, category: str) -> DishResponse:
        file.file.seek(0)
        contents = file.file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        image_url = save_classified_image(image, name)
        return self.repo.create_dish(name, category, image_url)

    @service_handle_errors(status_code=502)
    def get_all(self) -> list[DishResponse]:
        return self.repo.get_all()

    @service_handle_errors(status_code=503)
    def delete_dish(self, id: int):
        self.repo.delete_dish(id)
        return {"status": 200, "detail": "Dish deleted successfully!"}