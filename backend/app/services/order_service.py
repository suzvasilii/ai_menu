from collections import Counter

from schemas.order import OrderCreate
from repositories.order_repository import OrderRepository
from db.models import Order
from utils.decorators import service_handle_errors
from tg.bot import gen_msg_and_send

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    @service_handle_errors()
    def create(self, order_data: OrderCreate):
        self.repo.create(order_data)
        gen_msg_and_send(order_data)
        gen_msg_and_send(order_data, toUser=True)
        return {"status":200, "detail":"order created successfully"}

    @service_handle_errors()
    def get_recommendations(self, user_id: int, current_dish: str, top_k: int = 3):
        orders = self.repo.get_orders_by_user(user_id)
        all_orders = self.repo.get_all()

        local_statistic, global_statistic  = self.__get_statistic(current_dish, orders), self.__get_statistic(current_dish, all_orders)
        local_counter, local_total = local_statistic["counter"], local_statistic["total"]
        global_counter, global_total = global_statistic["counter"], global_statistic["total"]

        alpha = 5
        smoothed = {}
        all_dishes = set(local_counter.keys()) | set(global_counter.keys())
        for dish in all_dishes:
            local_count = local_counter.get(dish, 0)
            global_count = global_counter.get(dish, 0)
            global_prob = global_count / global_total if global_total > 0 else 0
            smoothed[dish] = (local_count + alpha * global_prob) / (local_total + alpha)

        return sorted(smoothed.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def __get_statistic(self, current_dish: str, orders: list[Order]):
        paired_dishes = []
        for order in orders:
            dishes = order.dishes.split(",")
            if current_dish in dishes:
                paired_dishes.extend([d for d in dishes if d != current_dish])
        counter = Counter(paired_dishes)
        total = sum(counter.values())
        return {
            "counter": counter,
            "total": total
        }
