from fastapi import UploadFile, File
from PIL import Image
import io

from api.responses import returnBadrequestError
from schemas.dish import DishCreate, DishResponse
from repositories.dish_repository import DishRepository

from utils.saver import save_classified_image, find_and_save_image
from utils.decorators import service_handle_errors

class DishService:

    def __init__(self, repo: DishRepository):
        self.repo = repo

    @service_handle_errors(status_code=500)
    def create(self, dish: DishCreate, isSemantic=True):
        return None

    @service_handle_errors(status_code=501)
    def create_by_photo(self, file: UploadFile = File(...)):
        return None

    @service_handle_errors(status_code=502)
    def get_all(self) -> list[DishResponse]:
        return self.repo.get_all()

    @service_handle_errors(status_code=503)
    def delete_dish(self, id:int):
        self.repo.delete_dish(id)
        return {"status": 200, "detail": "Dish deleted successfully!"}
