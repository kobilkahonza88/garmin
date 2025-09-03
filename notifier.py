import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") # volitelné


def _send_telegram(text: str):
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
return
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
requests.post(url, data=data, timeout=15)


def _send_discord(text: str):
if not DISCORD_WEBHOOK_URL:
return
requests.post(DISCORD_WEBHOOK_URL, json={"content": text}, timeout=15)


def notify(text: str):
_send_telegram(text)
_send_discord(text)
