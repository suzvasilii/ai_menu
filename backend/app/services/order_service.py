from collections import Counter

from schemas.order import OrderCreate, RecommendationItem
from repositories.order_repository import OrderRepository
from db.models import Order
from utils.decorators import service_handle_errors
from services.notify_service import notify_shef, notify_user


class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    @service_handle_errors()
    def create(self, order_data: OrderCreate):
        self.repo.create(order_data)
        user_chat_id = self.repo.get_user_chat_id(order_data.user_id)
        notify_shef(order_data)
        notify_user(order_data, user_chat_id)
        return {"status": 200, "detail": "order created successfully"}

    @service_handle_errors()
    def get_recommendations(
        self,
        user_id: int,
        current_dish: str,
        top_k: int = 3,
        threshold: float = 0.6,
    ) -> list[RecommendationItem]:
        orders = self.repo.get_orders_by_user(user_id)
        all_orders = self.repo.get_all()

        local_stat = self.__get_statistic(current_dish, orders)
        global_stat = self.__get_statistic(current_dish, all_orders)

        local_counter, local_total = local_stat["counter"], local_stat["total"]
        global_counter, global_total = global_stat["counter"], global_stat["total"]

        alpha = 5
        smoothed = {}
        all_dishes = set(local_counter.keys()) | set(global_counter.keys())

        for dish in all_dishes:
            local_count = local_counter.get(dish, 0)
            global_count = global_counter.get(dish, 0)
            global_prob = global_count / global_total if global_total > 0 else 0
            smoothed[dish] = (local_count + alpha * global_prob) / (local_total + alpha)

        total = sum(smoothed.values())
        if total == 0:
            return []

        probabilities = {k: v / total for k, v in smoothed.items()}
        filtered = {k: v for k, v in probabilities.items() if v >= threshold}

        sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:top_k]
        names = [name for name, _ in sorted_items]

        dishes = self.repo.get_dishes_by_names(names)
        image_by_name = {d.name: d.image_url for d in dishes}

        result = []
        for name in names:
            if name in image_by_name:
                result.append(RecommendationItem(name=name, image_url=image_by_name[name]))
        return result

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
            "total": total,
        }