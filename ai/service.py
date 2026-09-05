import os
from gigachat import GigaChat
from fastapi import HTTPException, UploadFile, File
from PIL import Image
import io

from semantic.vector_search import TextClassifier
from cnn.cnn import predict_by_image
from schemas import PromptResponse, ClassifiedResponse

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

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
                response = client.chat.create(
                    messages=[{"role": "user", "content": request.prompt}]
                )
                return PromptResponse(answer=response.choices[0].message.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_description(self, user_query: str) -> ClassifiedResponse:
        try:
            with GigaChat(
                    credentials=GIGACHAT_API_KEY,
                    model="GigaChat-2",
                    verify_ssl_certs=False
            ) as client:
                response = client.chat.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Ты — помощник, который определяет название блюда по описанию пользователя. "
                                "Отвечай только коротким названием блюда до 5-6 слов максимум"
                                "Никаких пояснений, только название на английском языке чтобы нашлась наиболее релевантная картинка. Пример: Фунчоза -> Glass noodles."
                            )
                        },
                        {
                            "role": "user",
                            "content": user_query
                        }
                    ]
                )
                dish_name = response.choices[0].message.content.strip()
                category = self.classifier.classify(dish_name)
                return ClassifiedResponse(dish_name=dish_name, category=category)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def classify_photo(self, file: UploadFile = File(...)) ->ClassifiedResponse:
        try:
            contents = file.file.read()
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            dish_name = predict_by_image(image)
            category = self.classifier.classify(dish_name)
            return ClassifiedResponse(dish_name=dish_name, category=category)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

