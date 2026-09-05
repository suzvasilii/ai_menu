from pydantic import BaseModel

class PromptResponse(BaseModel):
    answer: str

class ClassifiedResponse(BaseModel):
    dish_name:str
    category:str