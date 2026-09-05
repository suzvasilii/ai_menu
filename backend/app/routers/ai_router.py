from fastapi import APIRouter, Depends

from services.ai_service import AI_Service
from schemas.ai import AssistantRequest, AssistantResponse
from utils.instances import get_ai_service

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/officiant", response_model = AssistantResponse)
def ask(request: AssistantRequest, service: AI_Service = Depends(get_ai_service)):
    return service.ask_officiant(request)
