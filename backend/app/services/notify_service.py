import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID_SHEF = os.getenv("TELEGRAM_CHAT_ID_SHEF")


def notify_shef(order_data) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID_SHEF:
        print("Telegram env vars are not set, skipping notification")
        return

    message = "<b>🛒 NEW ORDER!</b>\n\n"

    if order_data.customer_name:
        message += f"<b>👤 Name:</b> {order_data.customer_name}\n\n"
    if order_data.comment:
        message += f"<b>Order details:</b> {order_data.comment}\n\n"

    message += "<b>📋 Order structure:</b>\n"
    for item in order_data.dishes:
        message += f"  • {item.name} x {item.quantity}\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    httpx.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID_SHEF,
            "text": message,
            "parse_mode": "HTML",
        },
        timeout=5.0,
    )