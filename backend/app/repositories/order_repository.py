from backend.app.db import Order
from schemas.order import OrderCreate

class OrderRepository:
    def __init__(self, db):
        self.db = db

    def create(self, login: str, order: OrderCreate) -> Order | None:
        try:
            dishes = ''.join(order.dishes)
            new_order = self.db.add(user_id=order.user_id, dishes=dishes)
            self.db.commit()
            self.db.refresh(new_order)
        except Exception as e:
            raise RuntimeError(f"Error of saving order: {e}")

    def get_orders_by_user(self, user_id: int) -> list[Order] | None:
        try:
            return self.db.query(Order).filter(Order.user_id == user_id).all()
        except  Exception as e:
            raise RuntimeError(f"Error of getting orders for user: {e}")

    def get_all(self) -> list[Order] | None:
        try:
            return self.db.query(Order).all()
        except  Exception as e:
            raise RuntimeError(f"Error of getting orders for all users: {e}")