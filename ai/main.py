from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from services.ai_service import AI_Serivce
from schemas import PromptRequest, PromptResponse

load_dotenv()
app = FastAPI(title="AI Assistant")

def get_ai_service():
    return AI_Serivce()

@app.post("/ask_officiant", response_model=PromptResponse)
def ask_officiant(request: PromptRequest, service: AI_Serivce = Depends(get_ai_service)):
    return service.ask_officiant(request)

@app.get("/health")
def health():
    return {"status": "ok"}