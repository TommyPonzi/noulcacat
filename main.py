import requests
import time

# CONFIG
HELIUS_API_KEY = '7d0d5554-0327-4b6a-836f-1f6e6c7c6748'
BOT_TOKEN = '7621052158:AAEsxkndRtysQu-tPGXe0-C8XxQEfFO22Nc'
CHAT_ID = '7621052158'
API_URL = 'https://api.helius.xyz/v0/addresses/TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA/transactions?api-key=' + HELIUS_API_KEY

SEEN_TOKENS = set()
last_no_token_message_time = time.time()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def fetch_new_tokens():
    try:
        res = requests.get(API_URL)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Failed to fetch tokens: {e}")
    return []

def extract_token_mints(transactions):
    mints = []
    for tx in transactions:
        transfers = tx.get("tokenTransfers", [])
        for transfer in transfers:
            mint = transfer.get("mint")
            if mint and mint not in SEEN_TOKENS:
                SEEN_TOKENS.add(mint)
                mints.append(mint)
    return mints

# STARTUP MESSAGE
send_telegram_message("hi")

while True:
    txs = fetch_new_tokens()
    new_mints = extract_token_mints(txs)

    if new_mints:
        for mint in new_mints:
            send_telegram_message(f"New token mint: {mint}")
    else:
        if time.time() - last_no_token_message_time > 1800:  # 30 minutes
            send_telegram_message("no tokens found")
            last_no_token_message_time = time.time()

    time.sleep(1)
