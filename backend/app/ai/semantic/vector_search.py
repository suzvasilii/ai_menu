import faiss
from sentence_transformers import SentenceTransformer
from googletrans import Translator

FOOD_DATASET = {
    # === СУПЫ (категория: soup) ===
    "borscht": {
        "api_query": "borscht soup",
        "synonyms": ["red beet soup", "ukrainian borscht", "beetroot soup"],
        "category": "soup"
    },
    "chicken noodle soup": {
        "api_query": "chicken noodle soup",
        "synonyms": ["chicken soup", "noodle soup", "chicken broth"],
        "category": "soup"
    },
    "tomato soup": {
        "api_query": "tomato soup",
        "synonyms": ["cream of tomato", "tomato bisque"],
        "category": "soup"
    },
    "mushroom soup": {
        "api_query": "mushroom soup",
        "synonyms": ["cream of mushroom", "mushroom cream soup"],
        "category": "soup"
    },
    "pea soup": {
        "api_query": "pea soup",
        "synonyms": ["split pea soup", "green pea soup"],
        "category": "soup"
    },
    "fish soup": {
        "api_query": "fish soup",
        "synonyms": ["fish broth", "fisherman's soup"],
        "category": "soup"
    },
    "solyanka": {
        "api_query": "solyanka soup",
        "synonyms": ["hodgepodge soup", "russian meat soup"],
        "category": "soup"
    },
    "okroshka": {
        "api_query": "okroshka",
        "synonyms": ["cold russian soup", "kefir soup", "summer soup"],
        "category": "soup"
    },
    "pumpkin soup": {
        "api_query": "pumpkin soup",
        "synonyms": ["pumpkin cream soup", "butternut squash soup"],
        "category": "soup"
    },
    "onion soup": {
        "api_query": "french onion soup",
        "synonyms": ["french onion", "onion broth", "soupe a l'oignon"],
        "category": "soup"
    },
    "beetroot soup": {
        "api_query": "beetroot soup",
        "synonyms": ["cold beetroot soup", "chilled beet soup"],
        "category": "soup"
    },
    "cabbage soup": {
        "api_query": "cabbage soup",
        "synonyms": ["russian cabbage soup", "shchi", "sauerkraut soup"],
        "category": "soup"
    },
    "cheese soup": {
        "api_query": "cheese soup",
        "synonyms": ["cheese chowder", "creamy cheese soup"],
        "category": "soup"
    },
    "noodle soup": {
        "api_query": "asian noodle soup",
        "synonyms": ["ramen", "pho", "noodle broth"],
        "category": "soup"
    },
    "lentil soup": {
        "api_query": "lentil soup",
        "synonyms": ["red lentil soup", "lentil stew"],
        "category": "soup"
    },
    "gazpacho": {
        "api_query": "gazpacho",
        "synonyms": ["cold tomato soup", "spanish soup"],
        "category": "soup"
    },
    "miso soup": {
        "api_query": "miso soup",
        "synonyms": ["miso broth", "japanese soup"],
        "category": "soup"
    },
    "tom yum": {
        "api_query": "tom yum soup",
        "synonyms": ["thai soup", "hot and sour soup"],
        "category": "soup"
    },
    "egg drop soup": {
        "api_query": "egg drop soup",
        "synonyms": ["egg flower soup", "chinese egg soup"],
        "category": "soup"
    },
    "clam chowder": {
        "api_query": "clam chowder",
        "synonyms": ["new england clam chowder", "seafood soup"],
        "category": "soup"
    },

    # === ПИЦЦА (категория: pizza) ===
    "margherita": {
        "api_query": "margherita pizza",
        "synonyms": ["pizza margherita", "classic italian pizza"],
        "category": "pizza"
    },
    "pepperoni": {
        "api_query": "pepperoni pizza",
        "synonyms": ["pizza pepperoni", "spicy sausage pizza"],
        "category": "pizza"
    },
    "quattro formaggi": {
        "api_query": "four cheese pizza",
        "synonyms": ["quattro formaggi", "four cheese pizza"],
        "category": "pizza"
    },
    "hawaiian": {
        "api_query": "hawaiian pizza",
        "synonyms": ["pineapple pizza"],
        "category": "pizza"
    },
    "vegetarian pizza": {
        "api_query": "vegetarian pizza",
        "synonyms": ["veggie pizza", "vegetable pizza"],
        "category": "pizza"
    },
    "diavola": {
        "api_query": "diavola pizza",
        "synonyms": ["diavola", "spicy pizza", "salame piccante"],
        "category": "pizza"
    },
    "capricciosa": {
        "api_query": "capricciosa pizza",
        "synonyms": ["capricciosa", "mixed toppings pizza"],
        "category": "pizza"
    },
    "napoli": {
        "api_query": "napoli pizza",
        "synonyms": ["napoli", "anchovy pizza", "neapolitan pizza"],
        "category": "pizza"
    },
    "prosciutto pizza": {
        "api_query": "prosciutto pizza",
        "synonyms": ["pizza con prosciutto", "ham pizza"],
        "category": "pizza"
    },
    "pizza bianca": {
        "api_query": "white pizza",
        "synonyms": ["bianca", "pizza without tomato"],
        "category": "pizza"
    },

    # === РОЛЛЫ (категория: sushi roll) ===
    "california roll": {
        "api_query": "california roll",
        "synonyms": ["california sushi", "crab roll"],
        "category": "sushi roll"
    },
    "philadelphia roll": {
        "api_query": "philadelphia roll",
        "synonyms": ["salmon roll with cheese"],
        "category": "sushi roll"
    },
    "dragon roll": {
        "api_query": "dragon roll",
        "synonyms": ["dragon sushi", "eel roll"],
        "category": "sushi roll"
    },
    "spicy tuna roll": {
        "api_query": "spicy tuna roll",
        "synonyms": ["spicy tuna sushi"],
        "category": "sushi roll"
    },
    "rainbow roll": {
        "api_query": "rainbow roll",
        "synonyms": ["rainbow sushi", "assorted fish roll"],
        "category": "sushi roll"
    },
    "tempura roll": {
        "api_query": "tempura roll",
        "synonyms": ["tempura sushi"],
        "category": "sushi roll"
    },
    "unagi roll": {
        "api_query": "unagi roll",
        "synonyms": ["unagi sushi", "eel roll"],
        "category": "sushi roll"
    },
    "salmon roll": {
        "api_query": "salmon roll",
        "synonyms": ["salmon sushi"],
        "category": "sushi roll"
    },
    "cucumber roll": {
        "api_query": "cucumber roll",
        "synonyms": ["cucumber sushi", "kappa maki"],
        "category": "sushi roll"
    },
    "avocado roll": {
        "api_query": "avocado roll",
        "synonyms": ["avocado sushi"],
        "category": "sushi roll"
    },

    # === ПАСТА (категория: pasta) ===
    "pasta carbonara": {
        "api_query": "pasta carbonara",
        "synonyms": ["carbonara", "spaghetti carbonara"],
        "category": "pasta"
    },
    "spaghetti bolognese": {
        "api_query": "spaghetti bolognese",
        "synonyms": ["bolognese", "meat sauce pasta"],
        "category": "pasta"
    },
    "lasagna": {
        "api_query": "lasagna",
        "synonyms": ["lasagne", "baked pasta"],
        "category": "pasta"
    },

    # === ВТОРЫЕ БЛЮДА (категория: main dish) ===
    "pilaf": {
        "api_query": "pilaf",
        "synonyms": ["pilav", "rice pilaf", "central asian rice"],
        "category": "main dish"
    },
    "baked chicken": {
        "api_query": "baked chicken",
        "synonyms": ["roast chicken", "whole roasted chicken"],
        "category": "main dish"
    },
    "grilled salmon": {
        "api_query": "grilled salmon",
        "synonyms": ["grilled fish", "salmon fillet"],
        "category": "main dish"
    },
    "steak": {
        "api_query": "grilled steak",
        "synonyms": ["beef steak", "ribeye", "strip loin"],
        "category": "main dish"
    },
    "risotto": {
        "api_query": "risotto",
        "synonyms": ["italian rice", "creamy rice"],
        "category": "main dish"
    },
    "khachapuri": {
        "api_query": "khachapuri",
        "synonyms": ["georgian cheese bread", "stuffed bread", "cheese boat"],
        "category": "main dish"
    },
    "khinkali": {
        "api_query": "khinkali dumplings",
        "synonyms": ["georgian dumplings", "meat dumplings", "stuffed dough"],
        "category": "main dish"
    },
    "schnitzel": {
        "api_query": "schnitzel",
        "synonyms": ["wiener schnitzel", "breaded cutlet"],
        "category": "main dish"
    },
    "chicken kiev": {
        "api_query": "chicken kiev",
        "synonyms": ["chicken cutlet", "stuffed chicken breast"],
        "category": "main dish"
    },
    "stuffed peppers": {
        "api_query": "stuffed peppers",
        "synonyms": ["peppers with meat"],
        "category": "main dish"
    },
    "cabbage rolls": {
        "api_query": "cabbage rolls",
        "synonyms": ["stuffed cabbage", "cabbage leaves with meat"],
        "category": "main dish"
    },
    "sushi": {
        "api_query": "sushi",
        "synonyms": ["japanese sushi", "nigiri", "maki"],
        "category": "main dish"
    },
    "burger": {
        "api_query": "burger",
        "synonyms": ["hamburger", "beef burger", "cheeseburger"],
        "category": "main dish"
    },
    "omelette": {
        "api_query": "omelette",
        "synonyms": ["egg omelet", "french omelet"],
        "category": "main dish"
    },
    "pancakes": {
        "api_query": "russian pancakes",
        "synonyms": ["russian blini", "crepes", "thin pancakes"],
        "category": "main dish"
    },
    "funchoza": {
        "api_query": "glass noodles",
        "synonyms": ["cellophane noodles", "glass noodle salad", "mung bean noodles"],
        "category": "main dish"
    },
    "macaroni with meat": {
        "api_query": "macaroni with minced meat",
        "synonyms": ["navy style macaroni", "pasta with meat", "macaroni with ground beef"],
        "category": "main dish"
    },
    "fried chicken": {
        "api_query": "fried chicken",
        "synonyms": ["crispy chicken", "southern fried chicken"],
        "category": "main dish"
    },
    "meatballs": {
        "api_query": "meatballs",
        "synonyms": ["meatballs in sauce", "swedish meatballs"],
        "category": "main dish"
    },
    "shrimp scampi": {
        "api_query": "shrimp scampi",
        "synonyms": ["shrimp in garlic sauce"],
        "category": "main dish"
    },
    "beef stroganoff": {
        "api_query": "beef stroganoff",
        "synonyms": ["stroganoff", "beef with sour cream"],
        "category": "main dish"
    },

    # === САЛАТЫ (категория: salad) ===
    "caesar salad": {
        "api_query": "caesar salad",
        "synonyms": ["romaine salad"],
        "category": "salad"
    },
    "olivier salad": {
        "api_query": "russian salad",
        "synonyms": ["salad olivier", "russian potato salad"],
        "category": "salad"
    },
    "greek salad": {
        "api_query": "greek salad",
        "synonyms": ["horiatiki", "greek village salad"],
        "category": "salad"
    },
    "caprese": {
        "api_query": "caprese salad",
        "synonyms": ["caprese", "tomato mozzarella salad"],
        "category": "salad"
    },
    "mimosa": {
        "api_query": "mimosa salad",
        "synonyms": ["mimosa", "layered salad"],
        "category": "salad"
    },
    "crab salad": {
        "api_query": "crab salad",
        "synonyms": ["imitation crab salad", "seafood salad"],
        "category": "salad"
    },
    "vinigret": {
        "api_query": "vinigret salad",
        "synonyms": ["russian beet salad", "vegetable salad"],
        "category": "salad"
    },
    "cesar with chicken": {
        "api_query": "chicken caesar salad",
        "synonyms": ["caesar chicken salad"],
        "category": "salad"
    },
    "tuna salad": {
        "api_query": "tuna salad",
        "synonyms": ["tuna fish salad"],
        "category": "salad"
    },
    "warm vegetable salad": {
        "api_query": "warm vegetable salad",
        "synonyms": ["grilled vegetables salad"],
        "category": "salad"
    },

    # === ДЕСЕРТЫ (категория: dessert) ===
    "cheesecake": {
        "api_query": "cheesecake",
        "synonyms": ["new york cheesecake", "cream cheese dessert"],
        "category": "dessert"
    },
    "chocolate cake": {
        "api_query": "chocolate cake",
        "synonyms": ["chocolate torte", "dark chocolate cake"],
        "category": "dessert"
    },
    "fruit tart": {
        "api_query": "fruit tart",
        "synonyms": ["fruit pie", "tarte aux fruits"],
        "category": "dessert"
    },
    "pancakes dessert": {
        "api_query": "dessert pancakes",
        "synonyms": ["stuffed pancakes", "sweet blini"],
        "category": "dessert"
    },
    "ice cream": {
        "api_query": "ice cream",
        "synonyms": ["vanilla ice cream", "gelato"],
        "category": "dessert"
    },
    "panna cotta": {
        "api_query": "panna cotta",
        "synonyms": ["italian cream dessert", "cooked cream"],
        "category": "dessert"
    },
    "creme brulee": {
        "api_query": "creme brulee",
        "synonyms": ["caramel custard", "burnt cream"],
        "category": "dessert"
    },
    "macarons": {
        "api_query": "macarons",
        "synonyms": ["french macaroons", "macaron cookies"],
        "category": "dessert"
    },
    "cupcakes": {
        "api_query": "cupcakes",
        "synonyms": ["fairy cakes", "frosted cupcakes"],
        "category": "dessert"
    },
    "brownie": {
        "api_query": "brownie",
        "synonyms": ["chocolate brownie", "fudge brownie"],
        "category": "dessert"
    },
    "tiramisu": {
        "api_query": "tiramisu",
        "synonyms": ["italian coffee dessert", "mascarpone dessert"],
        "category": "dessert"
    },
    "medovik": {
        "api_query": "medovik cake",
        "synonyms": ["russian honey cake", "honey layer cake", "honey cake"],
        "category": "dessert"
    },
    "napoleon": {
        "api_query": "napoleon cake",
        "synonyms": ["russian napoleon", "layered puff pastry cake", "mille-feuille"],
        "category": "dessert"
    },
    "bird's milk": {
        "api_query": "bird's milk cake",
        "synonyms": ["souffle cake", "chocolate souffle", "ptichye moloko"],
        "category": "dessert"
    },
    "kinder": {
        "api_query": "kinder chocolate",
        "synonyms": ["canvas", "kinder bueno", "kinder chocolate bar", "chocolate with milk"],
        "category": "dessert"
    },

    # === НАПИТКИ (категория: beverage) ===
    "coffee": {
        "api_query": "coffee",
        "synonyms": ["espresso", "cappuccino", "latte", "americano"],
        "category": "beverage"
    },
    "tea": {
        "api_query": "tea",
        "synonyms": ["green tea", "black tea", "herbal tea", "chai"],
        "category": "beverage"
    },
    "fresh juice": {
        "api_query": "fresh juice",
        "synonyms": ["freshly squeezed juice", "orange juice"],
        "category": "beverage"
    },
    "smoothie": {
        "api_query": "smoothie",
        "synonyms": ["fruit smoothie", "berry smoothie", "protein shake"],
        "category": "beverage"
    },
    "milkshake": {
        "api_query": "milkshake",
        "synonyms": ["shake", "ice cream shake"],
        "category": "beverage"
    },
    "lemonade": {
        "api_query": "lemonade",
        "synonyms": ["homemade lemonade", "lemon drink"],
        "category": "beverage"
    },
    "milk": {
        "api_query": "milk",
        "synonyms": ["whole milk", "oat milk", "almond milk"],
        "category": "beverage"
    },
    "hot chocolate": {
        "api_query": "hot chocolate",
        "synonyms": ["hot cocoa", "chocolate drink"],
        "category": "beverage"
    },
    "water": {
        "api_query": "mineral water",
        "synonyms": ["still water", "sparkling water", "mineral water"],
        "category": "beverage"
    },
    "compote": {
        "api_query": "fruit compote",
        "synonyms": ["russian fruit drink", "dried fruit drink", "fruit syrup"],
        "category": "beverage"
    },

    # === ГАРНИРЫ (категория: side dish) ===
    "french fries": {
        "api_query": "french fries",
        "synonyms": ["chips", "fries"],
        "category": "side dish"
    },
    "mashed potatoes": {
        "api_query": "mashed potatoes",
        "synonyms": ["mashed potato", "creamy potatoes"],
        "category": "side dish"
    },
    "rice": {
        "api_query": "steamed rice",
        "synonyms": ["white rice", "jasmine rice", "basmati"],
        "category": "side dish"
    },
    "buckwheat": {
        "api_query": "buckwheat",
        "synonyms": ["kasha", "buckwheat groats", "russian kasha"],
        "category": "side dish"
    },
    "vegetable saute": {
        "api_query": "vegetable saute",
        "synonyms": ["sauteed vegetables", "ratatouille"],
        "category": "side dish"
    },

    # === ЗАКУСКИ (категория: appetizer) ===
    "hummus": {
        "api_query": "hummus",
        "synonyms": ["chickpea dip", "middle eastern dip"],
        "category": "appetizer"
    },
    "guacamole": {
        "api_query": "guacamole",
        "synonyms": ["avocado dip", "mexican dip"],
        "category": "appetizer"
    },
    "olives": {
        "api_query": "olives",
        "synonyms": ["green olives", "black olives", "marinated olives"],
        "category": "appetizer"
    },
    "cheese plate": {
        "api_query": "cheese platter",
        "synonyms": ["assorted cheese", "cheese board"],
        "category": "appetizer"
    },
    "garlic bread": {
        "api_query": "garlic bread",
        "synonyms": ["bread with garlic", "toast"],
        "category": "appetizer"
    },

    # === РАЗНОЕ (категория: other) ===
    "pad thai": {
        "api_query": "pad thai",
        "synonyms": ["thai noodles", "stir-fried noodles"],
        "category": "other"
    },
    "pho": {
        "api_query": "pho soup",
        "synonyms": ["vietnamese soup", "pho bo"],
        "category": "other"
    },
    "paella": {
        "api_query": "paella",
        "synonyms": ["spanish rice", "saffron rice"],
        "category": "other"
    },
    "tacos": {
        "api_query": "tacos",
        "synonyms": ["tacos mexican", "mexican tacos"],
        "category": "other"
    },
    "burrito": {
        "api_query": "burrito",
        "synonyms": ["mexican burrito", "wrapped tortilla"],
        "category": "other"
    },
    "fajitas": {
        "api_query": "fajitas",
        "synonyms": ["mexican fajitas", "grilled meat and vegetables"],
        "category": "other"
    },
    "moussaka": {
        "api_query": "moussaka",
        "synonyms": ["greek moussaka", "eggplant casserole"],
        "category": "other"
    },
    "ceviche": {
        "api_query": "ceviche",
        "synonyms": ["peruvian ceviche", "marinated fish"],
        "category": "other"
    }
}

model = SentenceTransformer('all-MiniLM-L6-v2')
DIMENSION = 384
translator = Translator()

def translate_text(text):
    try:
        result = translator.translate(text, dest='en')
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def get_embedding_text(dish_name: str) -> str:
    dish = FOOD_DATASET[dish_name]
    parts = [
        dish_name,
        *dish.get("synonyms", []),
        dish.get("category", "")
    ]
    return " ".join(parts)

dishes = list(FOOD_DATASET.keys())
embedding_texts = [get_embedding_text(dish) for dish in dishes]
vectors = model.encode(embedding_texts, convert_to_numpy=True).astype('float32')
index = faiss.IndexFlatL2(DIMENSION)
index.add(vectors)

def find_best_api_query(user_query: str) -> str:
    query_en = translate_text(user_query)
    print(f"orig: {user_query} tr:{query_en}")
    query_vector = model.encode([query_en], convert_to_numpy=True).astype('float32')
    distances, indices = index.search(query_vector, k=1)
    best_idx = indices[0][0]
    best_key = dishes[best_idx]
    best_api_query = FOOD_DATASET[best_key]["api_query"]
    best_distance = distances[0][0]
    best_score = 1 / (1 + best_distance)
    print(best_api_query)
    print(best_score)
    if (best_score >= 0.5):
        return best_api_query
    return query_en
