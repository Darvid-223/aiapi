# Start från en minimal Python-bild
FROM python:3.12-slim-bookworm

# Uppdatera systemet och installera beroenden
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    libffi-dev \
    libssl-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ange arbetskatalog
WORKDIR /app

# Kopiera beroenden först (för effektiv cache)
COPY requirements.txt .

# Installera Python-beroenden
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kopiera resten av projektet
COPY . .

# Ange kommandot för att köra appen
CMD ["python", "main.py"]
