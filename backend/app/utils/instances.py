from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.db import get_db, engine, Base

from services.auth_service import AuthService
from services.basket_service import BasketService
from services.dish_service import DishService
from services.order_service import OrderService

from repositories.auth_repository import AuthRepository
from repositories.basket_repository import BasketRepository
from repositories.dish_repository import DishRepository
from repositories.order_repository import OrderRepository

def init_db_instance():
    Base.metadata.create_all(bind=engine)

def get_auth_service(db: Session = Depends(get_db)):
    repo = AuthRepository(db)
    return AuthService(repo)

def get_basket_service(db: Session = Depends(get_db)):
    repo = BasketRepository(db)
    return BasketService(repo)

def get_dish_service(db: Session = Depends(get_db)):
    repo = DishRepository(db)
    return DishService(repo)

def get_order_service(db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    return OrderService(repo)