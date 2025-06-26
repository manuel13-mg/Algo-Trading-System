import requests
TELEGRAM_TOKEN = 'TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print(f"Telegram message sent successfully: {message}")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

