import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_test_message():
    response = requests.post(
        TELEGRAM_URL,
        data={
            "chat_id": CHAT_ID,
            "text": "ربات Roomspot فعال شد و آماده بررسی آگهی‌های جدید است."
        },
        timeout=20
    )
    response.raise_for_status()

if name == "__main__":
    send_test_message()
