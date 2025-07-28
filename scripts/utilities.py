import requests
import os
from telegram import Bot
from telegram.error import TelegramError
import yaml

def load_config():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

def send_telegram_notification(file_path):
    """Send file to Telegram channel"""
    try:
        config = load_config()
        bot_token = config['telegram']['bot_token']
        channel_id = config['telegram']['channel_id']
        
        bot = Bot(token=bot_token)
        
        # Check file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # in MB
        max_size = config['telegram'].get('max_file_size', 50)
        
        if file_size > max_size:
            # Send as document if too large
            with open(file_path, 'rb') as f:
                bot.send_document(
                    chat_id=channel_id,
                    document=f,
                    caption="New episode available"
                )
        else:
            # Send as video if within size limit
            with open(file_path, 'rb') as f:
                bot.send_video(
                    chat_id=channel_id,
                    video=f,
                    caption="New episode available"
                )
        return True
        
    except TelegramError as e:
        print(f"Telegram error: {str(e)}")
        return False
    except Exception as e:
        print(f"Notification error: {str(e)}")
        return False

def get_free_proxies():
    """Alternative free proxy scraper"""
    try:
        url = "https://www.proxy-list.download/api/v1/get"
        params = {
            'type': 'https',
            'anon': 'elite',
            'country': 'US,UK,CA'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.ok:
            return [f"http://{p}" for p in response.text.split('\r\n') if p]
        return []
    except:
        return []
