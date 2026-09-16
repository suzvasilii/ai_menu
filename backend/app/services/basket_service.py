from repositories.basket_repository import BasketRepository

from schemas.basket import BasketAdd, BasketOut

from utils.decorators import service_handle_errors

class BasketService:

    def __init__(self, repo: BasketRepository):
        self.repo = repo

    @service_handle_errors()
    def add(self, basket_data: BasketAdd):
        if (self.repo.add(basket_data)):
            return {"status":200, "detail":"Basket saved!"}

    @service_handle_errors()
    def get_all(self, user_id: int) -> BasketOut:
        basket = self.repo.get_all(user_id)
        if basket is None:
            return BasketOut(id=0, user_id=user_id, items=[])
        return basket
