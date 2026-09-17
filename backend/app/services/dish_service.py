import io
import os
import httpx
from fastapi import UploadFile
from PIL import Image
from dotenv import load_dotenv

from schemas.dish import DishCreate, DishResponse
from repositories.dish_repository import DishRepository
from utils.decorators import service_handle_errors
from utils.saver import save_found_image, save_classified_image
from utils.mapping import get_category_key

load_dotenv()

AI_API_URL=os.getenv("AI_API_URL")

class DishService:

    def __init__(self, repo: DishRepository):
        self.repo = repo

    @service_handle_errors(status_code=500)
    def create_by_name(self, dish: DishCreate) -> DishResponse:
        image_url = dish.image_url or ""
        if image_url.startswith("http"):
            image_url = save_found_image(dish.name, image_url) or ""
        new_dish = self.repo.create_dish(dish.name, dish.category, image_url)
        if dish.category_changed and dish.english_dish_name:
            self._sync_with_classifier(dish.english_dish_name, dish.category)
        return new_dish

    @service_handle_errors(status_code=501)
    def create_by_photo(
            self,
            file: UploadFile,
            name: str,
            category: str,
            english_dish_name: str | None = None,
            category_changed: bool = False,
    ) -> DishResponse:
        file.file.seek(0)
        contents = file.file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_url = save_classified_image(image, name)
        new_dish = self.repo.create_dish(name, category, image_url)
        if category_changed and english_dish_name:
            self._sync_with_classifier(english_dish_name, category)
        return new_dish

    @service_handle_errors(status_code=502)
    def get_all(self) -> list[DishResponse]:
        return self.repo.get_all()

    @service_handle_errors(status_code=503)
    def delete_dish(self, id: int):
        self.repo.delete_dish(id)
        return {"status": 200, "detail": "Dish deleted successfully!"}

    def _sync_with_classifier(self, name: str, ru_category: str) -> None:
        en_category = get_category_key(ru_category)
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{AI_API_URL}/upsert_dish",
                    json={"name": name, "category": en_category},
                    timeout=5.0,
                )
                response.raise_for_status()
        except Exception as e:
            print(f"Failed to sync with classifier for '{name}': {e}")