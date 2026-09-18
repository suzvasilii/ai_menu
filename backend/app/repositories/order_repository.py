from db.models import Order, Dish, User
from schemas.order import OrderCreate


class OrderRepository:
    def __init__(self, db):
        self.db = db

    def create(self, order: OrderCreate) -> Order | None:
        try:
            dishes = ",".join(item.name for item in order.dishes)
            new_order = Order(user_id=order.user_id, dishes=dishes)
            self.db.add(new_order)
            self.db.commit()
            self.db.refresh(new_order)
            return new_order
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Error of saving order: {e}")

    def get_orders_by_user(self, user_id: int) -> list[Order] | None:
        try:
            return self.db.query(Order).filter(Order.user_id == user_id).all()
        except Exception as e:
            raise RuntimeError(f"Error of getting orders for user: {e}")

    def get_all(self) -> list[Order] | None:
        try:
            return self.db.query(Order).all()
        except Exception as e:
            raise RuntimeError(f"Error of getting orders for all users: {e}")

    def get_dishes_by_names(self, names: list[str]) -> list[Dish]:
        if not names:
            return []
        try:
            return self.db.query(Dish).filter(Dish.name.in_(names)).all()
        except Exception as e:
            raise RuntimeError(f"Error of getting dishes by names: {e}")

    def get_user_chat_id(self, user_id: int) -> int | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        return user.chat_id if user else None