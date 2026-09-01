import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")
TELEGRAM_CHAT_ID_SHEF = os.getenv("TELEGRAM_CHAT_ID_SHEF")