import os
from dotenv import load_dotenv
from airflow.models import Variable

load_dotenv()

TELEGRAM_CONFIG = {
    'BOT_TOKEN': Variable.get('TELEGRAM_BOT_TOKEN', default_var=os.getenv('TELEGRAM_BOT_TOKEN', '')),
    'CHAT_ID': Variable.get('TELEGRAM_CHAT_ID', default_var=os.getenv('TELEGRAM_CHAT_ID', '')),
    'CHANNEL_ID': Variable.get('TELEGRAM_CHANNEL_ID', default_var=os.getenv('TELEGRAM_CHANNEL_ID', '')),
    'API_URL': 'https://api.telegram.org/bot'
}

if __name__ == '__main__':
    print(TELEGRAM_CONFIG)