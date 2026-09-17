import os
import httpx
from dotenv import load_dotenv
from utils.decorators import service_handle_errors
from utils.saver import find_images
from utils.mapping import get_category
from schemas.ai import ImageResponse, ImagesResponse, ClassifyResponse

load_dotenv()

AI_API_URL = os.getenv("AI_API_URL")

class AI_Service:

    @service_handle_errors()
    def ask_officiant(self, query):
        with httpx.Client() as client:
            response = client.get(f"{AI_API_URL}/ask_officiant/{query}")
            response.raise_for_status()
            data = response.json()
            return {"answer": data["answer"]}

    @service_handle_errors()
    def get_dish_name_by_str(self, dish_name: str):
        with httpx.Client() as client:
            response = client.get(f"{AI_API_URL}/get_dish_name_by_str/{dish_name}")
            response.raise_for_status()
            data = response.json()
            llm_dish_name = data["dish_name"]
            category = data["category"]

            raw_urls = find_images(llm_dish_name) or []
            images = [ImageResponse(data_url=url) for url in raw_urls]

            return ImagesResponse(
                images=images,
                dish_name=dish_name,
                english_dish_name=llm_dish_name,
                category=get_category(category),
            )

    @service_handle_errors()
    def retry_get_dish_name_by_str(self, dish_name: str, attempts: list[str]):
        with httpx.Client() as client:
            payload = {"dish_name": dish_name, "attempts": attempts}
            response = client.post(f"{AI_API_URL}/retry", json=payload)
            response.raise_for_status()
            data = response.json()
            llm_dish_name = data["dish_name"]
            category = data["category"]

            raw_urls = find_images(llm_dish_name) or []
            images = [ImageResponse(data_url=url) for url in raw_urls]

            return ImagesResponse(
                images=images,
                dish_name=dish_name,
                english_dish_name=llm_dish_name,
                category=get_category(category),
            )

    @service_handle_errors()
    def classify_by_photo(self, photo):
        photo.file.seek(0)
        photo_bytes = photo.file.read()
        with httpx.Client() as client:
            response = client.post(
                f"{AI_API_URL}/classify_photo",
                files={"photo": (photo.filename, photo_bytes, photo.content_type)},
            )
            response.raise_for_status()
            data = response.json()
            return ClassifyResponse(
                dish_name=data["dish_name"],
                category=get_category(data["category"]),
            )