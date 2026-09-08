from fastapi import APIRouter, Depends, UploadFile, File

from services.ai_service import AI_Service
from schemas.ai import AssistantRequest, AssistantResponse, ImagesResponse
from utils.instances import get_ai_service

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/officiant")
def ask(request: str, service: AI_Service = Depends(get_ai_service)):
    return service.ask_officiant(request)

@router.post("/get_name", response_model = ImagesResponse)
def get_name(dish_name: str, service: AI_Service = Depends(get_ai_service)):
    return service.get_dish_name_by_str(dish_name)

@router.post("/classify_photo", response_model = AssistantResponse)
def classify_photo(photo: UploadFile = File(...), service: AI_Service = Depends(get_ai_service)):
    return service.classify_by_photo(photo)


