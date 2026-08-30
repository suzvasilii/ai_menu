from fastapi import APIRouter, Depends
from services.auth_service import AuthService
from utils.instances import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/reg")
def reg(login: str, service: AuthService = Depends(get_auth_service)):
    return service.reg(login)

@router.post("/login")
def login(login: str, service: AuthService = Depends(get_auth_service)):
    return service.login(login)