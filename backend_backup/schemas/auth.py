from pydantic import BaseModel

class GenerateTokenRequest(BaseModel):
    username: str
    chat_id: int

class GenerateTokenResponse(BaseModel):
    token: str

class ExchangeTokenRequest(BaseModel):
    token: str

class ExchangeTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthStatus(BaseModel):
    status:int
    username:str