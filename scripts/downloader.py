import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent
import yaml
import os
from urllib.parse import urlparse, urljoin
from utilities import get_free_proxies

class AnimeXinDownloader:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.last_request = {}
        self.load_config()
        
    def load_config(self):
        with open('config/config.yaml') as f:
            self.config = yaml.safe_load(f)
    
    def make_request(self, url):
        """Smart request with rate limiting and proxy rotation"""
        domain = urlparse(url).netloc
        delay = self.config['request_intervals'].get(
            'dailymotion' if 'dailymotion' in domain else
            'okru' if 'ok.ru' in domain else
            'default', 3.0
        )
        
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            if elapsed < delay:
                time.sleep(delay - elapsed)
        
        proxies = get_free_proxies()
        headers = {'User-Agent': self.ua.random}
        
        for attempt in range(3):
            try:
                proxy = random.choice(proxies) if proxies else None
                response = self.session.get(
                    url,
                    headers=headers,
                    proxies={'http': proxy, 'https': proxy} if proxy else None,
                    timeout=15
                )
                response.raise_for_status()
                self.last_request[domain] = time.time()
                return response
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {str(e)}")
                time.sleep(random.uniform(2, 5))
        return None
    
    def get_all_new_episodes(self):
        """Scrape AnimeXin for all new episodes"""
        try:
            response = self.make_request("https://animexin.dev/")
            if not response:
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            episodes = []
            
            for item in soup.select('.episode-item a'):
                ep_url = urljoin("https://animexin.dev/", item['href'])
                if '/episode-' in ep_url.lower():
                    episodes.append(ep_url)
            
            return sorted(list(set(episodes)), key=lambda x: int(x.split('-')[-1]), reverse=True)
            
        except Exception as e:
            print(f"Error scraping new episodes: {str(e)}")
            return []
    
    def download_episode(self, episode_url):
        """Download episode from preferred server"""
        try:
            # Implementation to find and download from preferred servers
            # Returns path to downloaded file
            return "/tmp/test.mp4"  # Temporary placeholder
        except Exception as e:
            print(f"Download failed: {str(e)}")
            return None
