from pydantic import BaseModel

class ImageResponse(BaseModel):
    dish_url: str

class ImagesResponse(BaseModel):
    images: list[ImageResponse]
    dish_name: str
    category: str

class ClassifyResponse(BaseModel):
    dish_name: str
    category: str