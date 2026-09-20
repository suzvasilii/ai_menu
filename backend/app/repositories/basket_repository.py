from sqlalchemy.orm import Session, joinedload
from db.models import Basket, BasketItem, Dish

from schemas.basket import BasketAdd


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
                    BasketItem.dish_name == new_item.dish_name,
                ).first()

                if existing:
                    existing.quantity += new_item.quantity
                else:
                    new_basket_item = BasketItem(
                        basket_id=basket.id,
                        dish_name=new_item.dish_name,
                        quantity=new_item.quantity,
                    )
                    self.db.add(new_basket_item)

            self.db.commit()
            self.db.refresh(basket)
            return basket
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Database error, unable to save the Basket: {e}")

    def get_all(self, user_id: int) -> Basket | None:
        return (
            self.db.query(Basket)
            .options(joinedload(Basket.items))
            .filter(Basket.user_id == user_id)
            .first()
        )

    def remove_item(self, user_id: int, dish_name: str) -> Basket | None:
        try:
            basket = (
                self.db.query(Basket)
                .filter(Basket.user_id == user_id)
                .first()
            )
            if not basket:
                return None

            self.db.query(BasketItem).filter(
                BasketItem.basket_id == basket.id,
                BasketItem.dish_name == dish_name,
            ).delete(synchronize_session=False)

            self.db.commit()
            self.db.refresh(basket)
            return basket
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Database error, unable to remove item: {e}")

    def update_item_quantity(self, user_id: int, dish_name: str, quantity: int) -> Basket | None:
        try:
            basket = (
                self.db.query(Basket)
                .filter(Basket.user_id == user_id)
                .first()
            )
            if not basket:
                return None

            item = (
                self.db.query(BasketItem)
                .filter(
                    BasketItem.basket_id == basket.id,
                    BasketItem.dish_name == dish_name,
                )
                .first()
            )
            if not item:
                return basket

            if quantity <= 0:
                self.db.delete(item)
            else:
                item.quantity = quantity

            self.db.commit()
            self.db.refresh(basket)
            return basket
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Database error, unable to update item: {e}")

    def clear(self, user_id: int) -> Basket | None:
        try:
            basket = (
                self.db.query(Basket)
                .filter(Basket.user_id == user_id)
                .first()
            )
            if not basket:
                return None

            self.db.query(BasketItem).filter(
                BasketItem.basket_id == basket.id,
            ).delete(synchronize_session=False)

            self.db.commit()
            self.db.refresh(basket)
            return basket
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Database error, unable to clear basket: {e}")

    def get_images_by_names(self, names: list[str]) -> dict[str, str]:
        if not names:
            return {}
        dishes = self.db.query(Dish).filter(Dish.name.in_(names)).all()
        return {d.name: d.image_url for d in dishes}