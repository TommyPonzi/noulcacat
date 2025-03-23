import requests
import time

# === CONFIG ===
BOT_TOKEN = '7621052158:AAEsxkndRtysQu-tPGXe0-C8XxQEfFO22Nc'
CHAT_ID = '7621052158'
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_message(text):
    try:
        res = requests.post(TELEGRAM_URL, data={'chat_id': CHAT_ID, 'text': text})
        print(f"Sent message: {text} | Response: {res.status_code}")
    except Exception as e:
        print(f"Failed to send message: {e}")

# === Start of bot ===
send_telegram_message("hi from Render bot")

# === Main Loop ===
while True:
    time.sleep(30)  # Wait 30 seconds
    send_telegram_message("Still running...")
