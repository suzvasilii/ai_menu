from pydantic import BaseModel

class DishCreate(BaseModel):
    name: str

class DishResponse(BaseModel):
    id: int
    name: str
    image_url: str

    class Config:
        from_attributes = True