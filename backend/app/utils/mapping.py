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