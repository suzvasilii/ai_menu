from aiogram import Router
from config import TELEGRAM_CHAT_ID_SHEF
from dispatcher import bot
from schemas.order import OrderCreate

router = Router()

async def send_telegram_message(text: str):
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID_SHEF,
        text=text,
        parse_mode="HTML"
    )

def gen_msg_and_send(order: OrderCreate, toUser: bool = False):
    message = ""
    if toUser:
        message += f"<b>Hello, {order.customer_name}, we duplicate your order:</b>\n\n"

    message += f"<b>🛒 NEW ORDER!</b>\n\n"

    if order.customer_name:
        message += f"<b>👤 Name:</b> {order.customer_name}\n\n"
    if order.comment:
        message += f"<b> Order details: {order.comment}\n\n"

    message += "<b>📋 Order structure:</b>\n"
    for item in order.items:
        message += f"  • {item.name} x {item.quantity}\n"

    send_telegram_message(message)