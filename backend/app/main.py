import os
import httpx
import uuid

from pydantic import BaseModel

from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from dotenv import load_dotenv

import db
import tg
import ai
from db.db import engine, get_db, Base
from db.models import Dish
from db.schemas import DishCreate, DishResponse
from tg.bot import send_telegram_message

from ai.semantic.vector_search import find_best_api_query

load_dotenv()

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Dishes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderItem(BaseModel):
    name: str
    quantity: int

class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    comment: Optional[str] = None
    items: List[OrderItem]

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_URL = "https://api.unsplash.com/search/photos"


def find_and_save_image(name: str) -> str | None:
    try:
        with httpx.Client() as client:
            search_resp = client.get(
                UNSPLASH_URL,
                params={"query": name, "per_page": 1},
                headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
                timeout=10.0
            )
            search_resp.raise_for_status()
            data = search_resp.json()

            if not data.get("results"):
                print(f"❌ Нет результатов для: '{name}'")
                return None

            image_url = data["results"][0]["urls"]["regular"]

            img_resp = client.get(image_url, timeout=15.0)
            img_resp.raise_for_status()
            unique_id = uuid.uuid4().hex[:10]
            safe_name = f"{name.replace(' ', '_')}_{unique_id}"
            filepath = os.path.join("uploads", f"{safe_name}.jpg")

            with open(filepath, "wb") as f:
                f.write(img_resp.content)

            return f"/uploads/{safe_name}.jpg"

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP ошибка: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

@app.get("/api/dishes", response_model=list[DishResponse])
def get_all_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).all()


@app.post("/api/dishes", response_model=DishResponse)
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    if db.query(Dish).filter(Dish.name == dish.name).first():
        raise HTTPException(status_code=400, detail="Блюдо уже есть")
    try:
        semantic = find_best_api_query(dish.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail = e)
    local_path = find_and_save_image(semantic)
    if not local_path:
        raise HTTPException(status_code=401, detail="Картинка не найдена")
    new_dish = Dish(name=dish.name, image_url=local_path)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish
@app.get("/")
def root():
    return {"message": "Dishes API is running!"}

@app.get("/api/dishes", response_model=list[DishResponse])
def get_all_dishes(db: Session = Depends(get_db)):
    dishes = db.query(Dish).all()
    return dishes

@app.post("/api/orders")
async def create_order(order: OrderCreate):
    message = f"<b>🛒 НОВЫЙ ЗАКАЗ</b>\n\n"
    if order.customer_name:
        message += f"<b>👤 Имя:</b> {order.customer_name}\n\n"
    if order.comment:
        message += f"<b>Уточнение по заказу: {order.comment}\n\n"
    message += "<b>📋 Состав:</b>\n"
    for item in order.items:
        message += f"  • {item.name} x {item.quantity}\n"
    success = await send_telegram_message(message)

    if not success:
        raise HTTPException(status_code=500, detail="Не удалось отправить уведомление")

    return {"status": "success", "message": "Заказ отправлен!"}

@app.delete("/api/del/{id}")
async def delete_dish(id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == id).first()
    if (dish):
        try:
            db.delete(dish)
            db.commit()
            return Response(status_code=204)
        except Exception as e:
            print(f"Ошибка удаления: {e}")
            raise HTTPException(status_code=500, detail="Ошибка сервера")