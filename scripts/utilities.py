import requests
import os
from telegram import Bot
from telegram.error import TelegramError
import yaml
from urllib.parse import urlparse  # Added for proxy handling

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
            with open(file_path, 'rb') as f:
                bot.send_document(
                    chat_id=channel_id,
                    document=f,
                    caption="New episode available"
                )
        else:
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
    """Get free proxies from multiple sources"""
    proxy_sources = [
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    
    proxies = []
    for source in proxy_sources:
        try:
            response = requests.get(source, timeout=10)
            if response.ok:
                proxies.extend([f"http://{p.strip()}" for p in response.text.split('\n') if p.strip()])
        except:
            continue
    
    return list(set(proxies))[:50]  # Return unique proxies, max 50
