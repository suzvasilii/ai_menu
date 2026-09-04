from fastapi import UploadFile, File
from PIL import Image
import io

from api.responses import returnBadrequestError
from schemas.dish import DishCreate, DishResponse
from repositories.dish_repository import DishRepository
from ai.cnn.cnn import predict_by_image
from ai.semantic.vector_search import translate_text, find_best_api_query
from utils.saver import save_classified_image, find_and_save_image
from utils.decorators import service_handle_errors

class DishService:

    def __init__(self, repo: DishRepository):
        self.repo = repo

    @service_handle_errors(status_code=500)
    def create(self, dish: DishCreate, isSemantic=True):
        local_path = None
        if (isSemantic):
            semantic = find_best_api_query(dish.name)
            local_path = find_and_save_image(semantic)
        else:
            local_path = dish.local_path
        dish = self.repo.create_dish(dish.name, local_path)
        if dish:
            return {"status": 200, "detail": "Dish added successfully!"}

    @service_handle_errors(status_code=501)
    def create_by_photo(self, file: UploadFile = File(...)):
        if not file.content_type.startswith("image/"):
            raise  RuntimeError(f"Creating dish error: {returnBadrequestError('File should be an image.')}")
        contents = file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        dish_name = predict_by_image(image)
        translated = translate_text(dish_name, 'ru')
        filepath = save_classified_image(image, dish_name)
        new_dish = DishCreate()
        new_dish.name = translated
        new_dish.filepath = filepath
        return self.create(new_dish)

    @service_handle_errors(status_code=502)
    def get_all(self) -> list[DishResponse]:
        return self.repo.get_all()

    @service_handle_errors(status_code=503)
    def delete_dish(self, id:int):
        self.repo.delete_dish(id)
        return {"status": 200, "detail": "Dish deleted successfully!"}
