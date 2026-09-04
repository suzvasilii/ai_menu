from fastapi import HTTPException
from datetime import datetime, timedelta
from repositories.auth_repository import AuthRepository
from utils.decorators import service_handle_errors
from utils.jwt import create_access_token

class AuthService:

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    @service_handle_errors()
    def login(self, data):
        user = self.repo.login(data)
        if user:
            return user.one_time_token
        raise HTTPException(409, "User already exists.")

    @service_handle_errors()
    def verify(self, data):
        user = self.repo.verify(data)
        if not user or user.token_expires < datetime.now():
            raise HTTPException(401, "Invalid or expired token")
        self.repo.clear_temp_token(user)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(days=40)
        )
        return access_token