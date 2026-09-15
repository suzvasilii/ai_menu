from sqlalchemy.orm import Session, joinedload
from db.models import Basket, BasketItem

from schemas.basket import BasketAdd, BasketOut

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
            self.db.rollback() 
            raise RuntimeError(f"Database error, unable to save the Basket: {e}")

    def get_all(self, user_id: int) -> BasketOut | None:
        try:
            basket = (
                self.db.query(Basket)
                .options(joinedload(Basket.items))
                .filter(Basket.user_id == user_id)
                .first()
            )
            if not basket:
                return None

            names = [item.dish_name for item in basket.items]
            dishes = (
                self.db.query(Dish)
                .filter(Dish.name.in_(names))
                .all()
            )
            image_by_name = {d.name: d.image_url for d in dishes}

            return BasketOut(
                id=basket.id,
                user_id=basket.user_id,
                items=[
                    BasketItemOut(
                        dish_name=item.dish_name,
                        quantity=item.quantity,
                        image_url=image_by_name.get(item.dish_name)
                    )
                    for item in basket.items
                ]
            )
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Database error, unable to get the Basket: {e}")
