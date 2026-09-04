from datetime import datetime, timedelta
from utils.jwt import generate_one_time_token, decode_access_token
from sqlalchemy.orm import Session
from db.models import User

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def login(self, data) -> User | None:
        try:
            user = self.db.query(User).filter(User.username == data.username).first()
            if not user:
                user = User(username=data.username, chat_id=data.chat_id)
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
            token = generate_one_time_token(user.username)
            user.one_time_token = token
            user.token_expires = datetime.now() + timedelta(minutes=10)
            self.db.commit()
            return user
        except Exception as e:
            raise RuntimeError(f"Database error, reg unsuccessfully: {e}")

    def verify(self, data) -> User | None:
        try:
            payload = decode_access_token(data.token)
            username = payload.get("sub")
            user = self.db.query(User).filter(
                User.one_time_token == data.token,
                        User.username == username
                    ).first()
            return user
        except Exception as e:
            raise RuntimeError(f"Database error, verify unsuccessfully: {e}")

    def clear_temp_token(self, user: User) -> User | None:
        user.one_time_token = None
        user.token_expires = None
        self.db.commit()
        self.db.refresh(user)