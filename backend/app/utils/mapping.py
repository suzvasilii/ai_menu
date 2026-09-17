from functools import lru_cache
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='ru')

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

@lru_cache(maxsize=512)
def get_ru_name(en_name: str) -> str:
    if not en_name:
        return ""
    try:
        return translator.translate(en_name)
    except Exception as e:
        print(f"Translation failed for '{en_name}': {e}")
        return en_name