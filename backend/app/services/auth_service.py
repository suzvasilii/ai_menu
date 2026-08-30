from fastapi import HTTPException

from repositories.auth_repository import AuthRepository
from api.responses import getAuthResult
from utils.decorators import service_handle_errors

class AuthService:

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    @service_handle_errors()
    def reg(self, login: str):
        auth_type = "Registration"
        user = self.repo.reg(login)
        if user:
            return {"status": 200, "detail": getAuthResult(auth_type, True)}
        raise HTTPException(status_code=409, detail="User already exists.")

    @service_handle_errors()
    def login(self, login: str):
        auth_type = "Login"
        user = self.repo.login(login)
        if user:
            return {"status": 200, "detail": getAuthResult(auth_type, True)}
        raise HTTPException(status_code=401, detail="Invalid attempt to enter.")
