import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from ..config import BACKEND_URL

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    username = message.from_user.username
    chat_id = message.chat.id

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/auth/gen-token",
            json={"username": username, "chat_id": chat_id}
        )
    data = response.json()
    token = data.get("token")
    site_url = os.getenv("SITE_URL", "http://localhost:5173")
    link = f"{site_url}?token={token}"

    await message.answer(f"🔗SITE:\n{link}")