CATEGORY_LABELS = {
    "dessert": "Десерты",
    "soup": "Супы",
    "meat": "Стейки",
    "pasta": "Пасты",
    "rice": "Блюда из риса",
    "pizza": "Пиццы",
    "sushi": "Суши",
    "hamburger": "Бургеры",
    "hot_dog": "Хот доги",
    "fried_food": "Жареные продукты",
    "seafood": "Морепродукты",
    "salad": "Салаты",
    "cold_drink": "Холодные напитки",
    "hot_drink": "Горячие напитки",
}

def get_category(en_lbl: str) -> str:
    return CATEGORY_LABELS.get(en_lbl, en_lbl)

CATEGORY_KEYS = {v: k for k, v in CATEGORY_LABELS.items()}

def get_category_key(ru_category: str) -> str:
    return CATEGORY_KEYS.get(ru_category, ru_category)