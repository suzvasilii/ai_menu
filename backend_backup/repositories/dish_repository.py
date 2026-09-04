from sqlalchemy.orm import Session
from db.models import Dish

class DishRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_dish(self, dish_name: str, local_path:str) -> Dish | None:
        try:
            new_dish = Dish(name=dish_name, image_url=local_path)
            self.db.add(new_dish)
            self.db.commit()
            self.db.refresh(new_dish)
            return new_dish
        except Exception as e:
            raise RuntimeError(f"Creating dish error: {e}")

    def get_all(self)->list[Dish]:
        try:
            return self.db.query(Dish).all()
        except Exception as e:
            raise RuntimeError(f"Getting dish error: {e}")

    def delete_dish(self, id) -> Dish | None:
        try:
            dish = self.db.query(Dish).filter(Dish.id == id).first()
            if (dish):
                self.db.delete(dish)
                self.db.commit()
                return dish
        except Exception as e:
            raise RuntimeError(f"Deleting dish error: {e}")