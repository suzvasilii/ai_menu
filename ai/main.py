from fastapi import FastAPI, Depends, UploadFile, File
from dotenv import load_dotenv

from schemas import (
    ClassifiedResponse,
    RetryClassifyRequest,
    UpsertDishRequest,
    OfficiantRequest,
    PromptResponse,
)
from service import AI_Serivce
from semantic.vector_search import TextClassifier

load_dotenv()
app = FastAPI(title="AI Assistant")

classifier = TextClassifier()


def get_ai_service():
    return AI_Serivce(classifier)


@app.post("/ask_officiant", response_model=PromptResponse)
def ask_officiant(request: OfficiantRequest, service: AI_Serivce = Depends(get_ai_service)):
    messages = [m.model_dump() for m in request.messages]
    return service.ask_officiant(messages)


@app.get("/get_dish_name_by_str/{dish_name}", response_model=ClassifiedResponse)
def get_dish_name_by_str(dish_name: str, service: AI_Serivce = Depends(get_ai_service)):
    return service.get_description(dish_name)


@app.post("/retry", response_model=ClassifiedResponse)
def retry_get_dish_name_by_str(request: RetryClassifyRequest, service: AI_Serivce = Depends(get_ai_service)):
    return service.retry_get_description(request.dish_name, request.attempts)


@app.post("/classify_photo", response_model=ClassifiedResponse)
def classify_photo(photo: UploadFile = File(...), service: AI_Serivce = Depends(get_ai_service)):
    return service.classify_photo(photo)


@app.post("/upsert_dish")
def upsert_dish(request: UpsertDishRequest, service: AI_Serivce = Depends(get_ai_service)):
    service.upsert_dish(request.name, request.category)
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}