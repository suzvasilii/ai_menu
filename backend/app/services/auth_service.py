from fastapi import HTTPException
from repositories.auth_repository import AuthRepository
from utils.decorators import service_handle_errors
from schemas.auth import AuthResponse

class AuthService:

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    @service_handle_errors()
    def reg(self, login: str):
        user = self.repo.reg(login)
        if user:
            return AuthResponse(id=user.id, login=user.login)
        raise HTTPException(status_code=409, detail="User already exists.")

    @service_handle_errors()
    def login(self, login: str):
        user = self.repo.login(login)
        if user:
            return AuthResponse(id=user.id, login=user.login)
        raise HTTPException(status_code=401, detail="Invalid attempt to enter.")
