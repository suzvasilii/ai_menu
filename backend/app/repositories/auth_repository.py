from sqlalchemy.orm import Session
from db.models import User

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def reg(self, login: str) -> User | None:
        try:
            is_user_exists = self.db.query(User).filter(User.login == login).first()
            if is_user_exists:
                return None
            new_user = User(login=login)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as e:
            raise RuntimeError(f"Database error, reg unsuccessfully: {e}")

    def login(self, login:str)->User | None:
        try:
            return self.db.query(User).filter(User.login == login).first()
        except Exception as e:
            raise RuntimeError(f"Database error, login unsuccessfully: {e}")