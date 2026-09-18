from pydantic import BaseModel

class ImageResponse(BaseModel):
    data_url: str

class ImagesResponse(BaseModel):
    images: list[ImageResponse]
    dish_name: str
    english_dish_name: str
    category: str

class RetryClassifyRequest(BaseModel):
    dish_name: str
    attempts: list[str]

class ClassifyResponse(BaseModel):
    dish_name: str
    category: str

class OfficiantMessage(BaseModel):
    role: str
    content: str

class OfficiantRequest(BaseModel):
    messages: list[OfficiantMessage]