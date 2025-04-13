# 🐍 Använd en lättviktig Python-bild
FROM python:3.12-slim

# 🧰 Installera nödvändiga systempaket
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 📁 Sätt arbetskatalog
WORKDIR /app

# 📦 Kopiera och installera Python-dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 📄 Kopiera all annan kod
COPY . .

# 🌍 Miljövariabler (kan också sättas via Render Dashboard)
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# 🚀 Startkommandot (använd Render's förväntade port 10000)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "main:app"]
