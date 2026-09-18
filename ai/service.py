import os
from gigachat import GigaChat
from fastapi import HTTPException, UploadFile, File
from PIL import Image
import io
from dotenv import load_dotenv

from semantic.vector_search import TextClassifier
from cnn.cnn import predict_by_image
from schemas import PromptResponse, ClassifiedResponse
from prompts import GET_DISH_NAME_PROMPT, RETRY_GET_DISH_NAME_PROMPT, OFFICIANT_PROMPT

load_dotenv()

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

class AI_Serivce:

    def __init__(self, classifier: TextClassifier):
        self.classifier = classifier

    def ask_officiant(self, messages: list[dict]) -> PromptResponse:
        try:
            with GigaChat(
                    credentials=GIGACHAT_API_KEY,
                    model="GigaChat-2",
                    verify_ssl_certs=False,
            ) as client:
                request = {
                    "model": "GigaChat-2",
                    "messages": [
                        {"role": "system", "content": OFFICIANT_PROMPT},
                        *messages,
                    ],
                }
                response = client.chat.create(request)
                return PromptResponse(answer=response.messages[0].content[0].text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_description(self, user_query: str, request = None) -> ClassifiedResponse:
        try:
            client = GigaChat(credentials=GIGACHAT_API_KEY, verify_ssl_certs=False)
            if request is None:
                request = {
                    "model": "GigaChat-2",
                    "messages": [
                        {
                            "role": "system",
                            "content": GET_DISH_NAME_PROMPT
                        },
                        {
                            "role": "user",
                            "content": user_query
                        }
                    ],
                }
            response = client.chat.create(request)
            dish_name = response.messages[0].content[0].text
            category = self.classifier.classify(dish_name)
            return ClassifiedResponse(dish_name=dish_name, category=category)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def retry_get_description(self, dish_name: str, prev_attempts: list[str]):
        try:
            prompt = RETRY_GET_DISH_NAME_PROMPT + ', '.join(prev_attempts)
            request = {
                "model": "GigaChat-2",
                "messages": [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": dish_name
                    }
                ],
            }
            return self.get_description(dish_name, request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    def classify_photo(self, photo: UploadFile) ->ClassifiedResponse:
        try:
            contents = photo.file.read()
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            dish_name = predict_by_image(image)
            category = self.classifier.classify(dish_name)
            return ClassifiedResponse(dish_name=dish_name, category=category)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def upsert_dish(self, name: str, category: str) -> None:
        self.classifier.upsert_item(name, category)
