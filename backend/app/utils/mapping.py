CATEGORY_LABELS = {
    "desert": "Десерты",
    "soup": "Супы",
    "main_dish": "Основные блюда",
    "pizza": "Пицца",
    "roll": "Роллы",
    "cold_drink": "Холодные напитки",
    "hot_drink": "Горячие напитки",
}

def get_category(en_lbl: str) -> str:
    return CATEGORY_LABELS.get(en_lbl, en_lbl)

CATEGORY_KEYS = {v: k for k, v in CATEGORY_LABELS.items()}

def get_category_key(ru_category: str) -> str:
    return CATEGORY_KEYS.get(ru_category, ru_category)