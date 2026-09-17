from repositories.basket_repository import BasketRepository
from schemas.basket import BasketAdd, BasketOut, BasketItemOut
from utils.decorators import service_handle_errors


class BasketService:
    def __init__(self, repo: BasketRepository):
        self.repo = repo

    def _to_out(self, basket, user_id: int) -> BasketOut:
        if basket is None:
            return BasketOut(id=0, user_id=user_id, items=[])
        return BasketOut(
            id=basket.id,
            user_id=basket.user_id,
            items=[
                BasketItemOut(
                    dish_name=i.dish_name,
                    quantity=i.quantity,
                    image_url=None,
                )
                for i in basket.items
            ],
        )

    @service_handle_errors()
    def add(self, basket_data: BasketAdd) -> BasketOut:
        basket = self.repo.add(basket_data)
        return self._to_out(basket, basket_data.user_id)

    @service_handle_errors()
    def get_all(self, user_id: int) -> BasketOut:
        basket = self.repo.get_all(user_id)
        return self._to_out(basket, user_id)

    @service_handle_errors()
    def remove_item(self, user_id: int, dish_name: str) -> BasketOut:
        basket = self.repo.remove_item(user_id, dish_name)
        return self._to_out(basket, user_id)

    @service_handle_errors()
    def update_item_quantity(self, user_id: int, dish_name: str, quantity: int) -> BasketOut:
        basket = self.repo.update_item_quantity(user_id, dish_name, quantity)
        return self._to_out(basket, user_id)

    @service_handle_errors()
    def clear(self, user_id: int) -> BasketOut:
        basket = self.repo.clear(user_id)
        return self._to_out(basket, user_id)