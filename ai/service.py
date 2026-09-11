import os
from gigachat import GigaChat
from fastapi import HTTPException, UploadFile, File
from PIL import Image
import io
from dotenv import load_dotenv

from semantic.vector_search import TextClassifier
from cnn.cnn import predict_by_image
from schemas import PromptResponse, ClassifiedResponse

load_dotenv()

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

print(GIGACHAT_API_KEY, "<---- api key")

class AI_Serivce:

    def __init__(self, classifier: TextClassifier):
        self.classifier = classifier

    def ask_officiant(self, request:str):
        try:
            with GigaChat(
                credentials=GIGACHAT_API_KEY,
                model="GigaChat-2",
                verify_ssl_certs=False
            ) as client:
                response = client.chat.create(request)
                return PromptResponse(answer=response.messages[0].content[0].text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_description(self, user_query: str) -> ClassifiedResponse:
        try:
            client = GigaChat(credentials=GIGACHAT_API_KEY, verify_ssl_certs=False)
            request = {
                "model": "GigaChat-2",
                "messages": [
                    {
                        "role": "system",
                        "content":"Твоя задача преобразовать описание блюда"
                                  "в английское короткое релевантное описание, чтобы получилось найти релевантное фото."
                                  "Пример: фунчоза -> glass noodles."
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

    def classify_photo(self, photo: UploadFile) ->ClassifiedResponse:
        try:
            contents = photo.file.read()
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            dish_name = predict_by_image(image)
            category = self.classifier.classify(dish_name)
            return ClassifiedResponse(dish_name=dish_name, category=category)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

