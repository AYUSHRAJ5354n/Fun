import sqlite3
from datetime import datetime

class EpisodeTracker:
    def __init__(self, db_path='config/episodes.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS episodes
            (url TEXT PRIMARY KEY,
             success INTEGER,
             processed_at TIMESTAMP)''')
        self.conn.commit()
    
    def is_processed(self, url):
        cursor = self.conn.execute("SELECT 1 FROM episodes WHERE url=?", (url,))
        return cursor.fetchone() is not None
    
    def mark_processed(self, url, success):
        self.conn.execute('''INSERT OR REPLACE INTO episodes
                          VALUES (?, ?, ?)''',
                          (url, int(success), datetime.now()))
        self.conn.commit()
