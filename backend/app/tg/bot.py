import os
from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from db.schemas import OrderCreate
from utils.decorators import tg_handle_errors

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

@tg_handle_errors
async def send_telegram_message(text: str):
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text,
        parse_mode=ParseMode.HTML
    )

def gen_msg_and_send(self, order: OrderCreate, toUser=False):
        order_items = []
        message = ""
        if (toUser):
            message += f"<b>Hello, {order.customer_name}, we are duplicate your order:</b>"
        message = f"<b>🛒 NEW ORDER!</b>\n\n"
        if order.customer_name:
            message += f"<b>👤 Name:</b> {order.customer_name}\n\n"
        if order.comment:
            message += f"<b> Order details: {order.comment}\n\n"
        message += "<b>📋 Order structure:</b>\n"
        for item in order.items:
            message += f"  • {item.name} x {item.quantity}\n"
            order_items.append(item.name)
        send_telegram_message(message)