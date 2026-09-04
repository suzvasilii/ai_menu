import os

from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from utils.instances import init_db_instance

from routers import auth_router, dish_router, order_router, basket_router
app = FastAPI(title="Dishes API")

FRONTEND_URL = os.getenv("FRONTEND_URL")
TG_BOT_URL = os.getenv("TG_BOT_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
init_db_instance()

@app.get("/")
def root():
    return {"message": "Dishes API is running!"}

app.include_router(auth_router.router)
app.include_router(basket_router.router)
app.include_router(dish_router.router)
app.include_router(order_router.router)



