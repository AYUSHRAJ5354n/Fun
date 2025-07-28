FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files
COPY scripts/ scripts/
COPY config/ config/

VOLUME /data
VOLUME /app/config

CMD ["python", "-u", "scripts/main.py"]
