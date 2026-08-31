from fastapi import APIRouter, Depends
from services.auth_service import AuthService
from utils.instances import get_auth_service
from schemas.auth import AuthScheme

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/reg")
def reg(auth: AuthScheme, service: AuthService = Depends(get_auth_service)):
    return service.reg(auth.login)

@router.post("/login")
def login(auth: AuthScheme, service: AuthService = Depends(get_auth_service)):
    return service.login(auth.login)