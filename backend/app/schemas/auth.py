from pydantic import BaseModel

class AuthScheme(BaseModel):
    login: str

class AuthResponse(BaseModel):
    id: int
    login: str