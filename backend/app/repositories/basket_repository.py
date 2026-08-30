from sqlalchemy.orm import Session
from db.models import Basket, BasketItem

from db.schemas import BasketAdd

class BasketRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, basket_data: BasketAdd) -> Basket | None:
        try:
            basket = self.db.query(Basket).filter(Basket.user_id == basket_data.user_id).first()
            if not basket:
                basket = Basket(user_id=basket_data.user_id)
                self.db.add(basket)
                self.db.flush()
            for new_item in basket_data.items:
                existing = self.db.query(BasketItem).filter(
                    BasketItem.basket_id == basket.id,
                    BasketItem.dish_name == new_item.name
                ).first()

                if existing:
                    existing.quantity += new_item.quantity
                else:
                    new_basket_item = BasketItem(
                        basket_id=basket.id,
                        dish_name=new_item.name,
                        quantity=new_item.quantity
                    )
                    self.db.add(new_basket_item)

            self.db.commit()
            self.db.refresh(basket)
            return basket
        except Exception as e:
            RuntimeError(f"Database error, unable to save the Basket: {e}")

    def get_all(self, id: int) -> Basket | None:
        try:
            return self.db.query(Basket).filter(user_id=id).first()
        except Exception as e:
            raise RuntimeError(f"Database error, unable to get the Basket: {e}")

