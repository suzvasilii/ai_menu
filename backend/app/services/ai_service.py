import os
import httpx
from utils.decorators import service_handle_errors
from utils.saver import find_images
from schemas.ai import AssistantRequest, AssistantResponse, ImagesResponse

AI_API_URL = os.getenv("AI_API_URL")

class AI_Service:

    @service_handle_errors()
    def ask_officiant(self, query):
        with httpx.Client() as client:
            response = client.post(
                f"http://{AI_API_URL}/ask_officiant",
                params={"query": query}
            )
            return AssistantRequest(response=response)

    @service_handle_errors()
    def get_dish_name_by_str(self, dish_name):
        with httpx.Client() as client:
            response = client.post(
                f"http://{AI_API_URL}/get_dish_name_by_str",
                params={"dish_name": dish_name}
            )
            llm_dish_name, category = response["dish_name"], response["category"]
            images = find_images(llm_dish_name)
            return ImagesResponse(images=images, category=category)

    @service_handle_errors()
    def classify_by_photo(self, photo):
        with httpx.Client() as client:
            response = client.post(
                f"http://{AI_API_URL}/classify_photo",
                files={"photo": photo}
            )
            dish_name, category = response["dish_name"], response["category"]

            return AssistantRequest(response=response)