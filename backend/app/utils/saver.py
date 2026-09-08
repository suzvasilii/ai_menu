import os
import uuid
import httpx
from fastapi import HTTPException
from PIL import Image
from dotenv import load_dotenv

from api.responses import getFindImageResult
from .decorators import saver_handle_errors

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)
UPLOADS_DIR = os.path.join(APP_DIR, "uploads")

os.makedirs(UPLOADS_DIR, exist_ok=True)

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_URL = "https://api.unsplash.com/search/photos"

@saver_handle_errors
def find_images(name: str) -> list[str] | None:
    with httpx.Client() as client:
        search_resp = client.get(
            UNSPLASH_URL,
            params={"query": name, "per_page": 5},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=10.0
        )
        search_resp.raise_for_status()
        data = search_resp.json()
        if not data.get("results"):
            raise HTTPException(status_code=401, detail=getFindImageResult(False))
        image_urls = [result["urls"]["regular"] for result in data["results"]]
        return image_urls

@saver_handle_errors
def save_found_image(dish_name:str, image_url:str):
    with httpx.Client() as client:
        img_resp = client.get(
            image_url,
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=15.0
        )
        img_resp.raise_for_status()
        unique_id = uuid.uuid4().hex[:10]
        safe_name = f"{dish_name.replace(' ', '_')}_{unique_id}"
        filepath = os.path.join(UPLOADS_DIR, f"{safe_name}.jpg")
        with open(filepath, "wb") as f:
            f.write(img_resp.content)
        return f"/uploads/{safe_name}.jpg"

@saver_handle_errors
def save_classified_image(image: Image, dish_name: str):
    unique_id = uuid.uuid4().hex[:10]
    safe_name = f"{dish_name.replace(' ', '_')}_{unique_id}.jpg"
    filepath = os.path.join(UPLOADS_DIR, safe_name)
    image.save(filepath)
    return f"/uploads/{safe_name}"