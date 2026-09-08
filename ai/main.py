from fastapi import FastAPI, Depends, UploadFile, File
from dotenv import load_dotenv

from schemas import ClassifiedResponse
from service import AI_Serivce
from semantic.vector_search import TextClassifier
load_dotenv()
app = FastAPI(title="AI Assistant")

classifier = TextClassifier()

def get_ai_service():
    return AI_Serivce(classifier)

@app.get("/ask_officiant/{query}")
def ask_officiant(query: str, service: AI_Serivce = Depends(get_ai_service)):
    return service.ask_officiant(query)

@app.get("/get_dish_name_by_str/{dish_name}", response_model = ClassifiedResponse)
def get_dish_name_by_str(dish_name: str, service: AI_Serivce = Depends(get_ai_service)):
    return service.get_description(dish_name)

@app.post("/classify_photo", response_model = ClassifiedResponse)
def classify_photo(
    file: UploadFile = File(...),
    service: AI_Serivce = Depends(get_ai_service)
):
    return service.classify_photo(file)

@app.get("/health")
def health():
    return {"status": "ok"}