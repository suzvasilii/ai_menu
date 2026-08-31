from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from ..db.db import SessionLocal
from db.models import User
from dispatcher import dp
from utils.decorators import tg_handle_errors

router = Router()

@dp.message(Command("start"))
@tg_handle_errors
async def start_command(message: Message):
    username = message.from_user.username
    chat_id = message.chat.id

    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user:
        user = User(username=username, chat_id=chat_id)
        db.add(user)
        db.commit()
        await message.answer("Registration ok!")
    else:
        await message.answer("You are already registered!")
    db.close()

    site_url = "http://localhost:5173"
    link = f"{site_url}?user={username}"

    await message.answer(
        f"🔗 Link:\n{link}\n\n"
        f"👤 Login: <b>{username}</b>",
        parse_mode="HTML"
    )