from fastapi import APIRouter, Depends
from services.auth_service import AuthService
from utils.instances import get_auth_service
from utils.jwt import verify_current_user
from schemas.auth import GenerateTokenResponse, GenerateTokenRequest, ExchangeTokenResponse, ExchangeTokenRequest, AuthStatus

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/gen-token", response_model=GenerateTokenResponse)
def generate_token(data: GenerateTokenRequest, service: AuthService = Depends(get_auth_service)):
    token = service.login(data)
    return GenerateTokenResponse(token=token)

@router.post("/verify", response_model=ExchangeTokenResponse)
def verify_token(data: ExchangeTokenRequest, service: AuthService = Depends(get_auth_service)):
    access_token = service.verify(data)
    return ExchangeTokenResponse(access_token=access_token)

@router.post("/verify_user", response_model=AuthStatus)
def verify_user(current_user: str = Depends(verify_current_user)):
    return AuthStatus(status=200, username=current_user)