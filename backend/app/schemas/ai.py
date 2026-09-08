from pydantic import BaseModel

class AssistantRequest(BaseModel):
    query: str

class ImageResponse(BaseModel):
    dish_url: str
    dish_name: str

class ImagesResponse(BaseModel):
    images: list[ImageResponse]
    category: str

class AssistantResponse(BaseModel):
    response: str