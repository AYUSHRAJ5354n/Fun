# AnimeXin Auto-Downloader

Automatically downloads new episodes with English hardsubs.

## Setup
```bash
# 1. Install Docker
sudo apt update && sudo apt install -y docker.io docker-compose

# 2. Clone repo
git clone https://github.com/yourusername/animexin-autodl.git
cd animexin-autodl

# 3. Initialize
mkdir -p data/downloads data/temp
touch config/episodes.db

# 4. Configure
nano config/config.yaml  # Set your Telegram details

# 5. Run
docker-compose up -d --build

# View logs
docker-compose logs -f
