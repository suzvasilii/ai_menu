import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID_SHEF = os.getenv("TELEGRAM_CHAT_ID_SHEF")


def _send_message(chat_id: int, text: str) -> None:
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set, skipping notification")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    httpx.post(
        url,
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=5.0,
    )


def _build_shef_message(order_data) -> str:
    message = "<b>🛒 NEW ORDER!</b>\n\n"
    if order_data.customer_name:
        message += f"<b>👤 Name:</b> {order_data.customer_name}\n\n"
    if order_data.comment:
        message += f"<b>Order details:</b> {order_data.comment}\n\n"
    message += "<b>📋 Order structure:</b>\n"
    for item in order_data.dishes:
        message += f"  • {item.name} x {item.quantity}\n"
    return message


def _build_user_message(order_data) -> str:
    message = "<b>✅ Ваш заказ принят!</b>\n\n"
    if order_data.comment:
        message += f"<b>Комментарий:</b> {order_data.comment}\n\n"
    message += "<b>📋 Состав заказа:</b>\n"
    for item in order_data.dishes:
        message += f"  • {item.name} x {item.quantity}\n"
    message += "\nМы свяжемся с вами в ближайшее время."
    return message


def notify_shef(order_data) -> None:
    if not TELEGRAM_CHAT_ID_SHEF:
        print("TELEGRAM_CHAT_ID_SHEF not set, skipping shef notification")
        return
    try:
        _send_message(int(TELEGRAM_CHAT_ID_SHEF), _build_shef_message(order_data))
    except Exception as e:
        print(f"Failed to notify shef: {e}")


def notify_user(order_data, chat_id: int | None) -> None:
    if not chat_id:
        print(f"No chat_id for user {order_data.user_id}, skipping user notification")
        return
    try:
        _send_message(chat_id, _build_user_message(order_data))
    except Exception as e:
        print(f"Failed to notify user {chat_id}: {e}")