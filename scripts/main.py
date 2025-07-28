#!/usr/bin/env python3
import time
from downloader import AnimeXinDownloader
from processor import VideoProcessor
from tracker import EpisodeTracker
from utilities import send_telegram_notification

def process_episode(url, downloader, processor):
    try:
        print(f"Processing episode: {url}")
        video_path = downloader.download_episode(url)
        if video_path:
            doc_path = processor.convert_to_doc(video_path)
            if doc_path:
                send_telegram_notification(doc_path)
                return True
        return False
    except Exception as e:
        print(f"Error processing episode: {str(e)}")
        return False

def main():
    tracker = EpisodeTracker()
    downloader = AnimeXinDownloader()
    processor = VideoProcessor()
    
    print("Starting AnimeXin Auto-Downloader...")
    while True:
        try:
            new_episodes = downloader.get_all_new_episodes()
            print(f"Found {len(new_episodes)} new episodes")
            
            for ep_url in new_episodes:
                if not tracker.is_processed(ep_url):
                    success = process_episode(ep_url, downloader, processor)
                    tracker.mark_processed(ep_url, success)
                    time.sleep(random.uniform(5, 10))  # Random delay between episodes
            
            # Wait before next check (1 hour)
            time.sleep(2600)
            
        except Exception as e:
            print(f"Main loop error: {str(e)}")
            time.sleep(600)  # Wait 10 minutes after error

if __name__ == "__main__":
    main()
