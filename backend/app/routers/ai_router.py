from fastapi import APIRouter, Depends, UploadFile, File

from services.ai_service import AI_Service
from schemas.ai import ImagesResponse, ClassifyResponse, RetryClassifyRequest
from utils.instances import get_ai_service

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/officiant/{query}")
def ask(query: str, service: AI_Service = Depends(get_ai_service)):
    return service.ask_officiant(query)

@router.get("/get_name/{dish_name}", response_model = ImagesResponse)
def get_name(dish_name: str, service: AI_Service = Depends(get_ai_service)):
    return service.get_dish_name_by_str(dish_name)

@router.post("/retry_get_name", response_model=ImagesResponse)
def retry_get_name(request: RetryClassifyRequest, service: AI_Service=Depends(get_ai_service)):
    return service.retry_get_dish_name_by_str(request.dish_name, request.attempts)

@router.post("/classify_photo", response_model = ClassifyResponse)
def classify_photo(photo: UploadFile = File(...), service: AI_Service = Depends(get_ai_service)):
    return service.classify_by_photo(photo)


