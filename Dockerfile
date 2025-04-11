# Start från en minimal Python-bild
FROM python:3.12-slim

# Skapa arbetskatalog
WORKDIR /app

# Kopiera beroenden först (för cache)
COPY requirements.txt .

# Installera beroenden
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera all kod
COPY . .

# Miljövariabler (du kan även hantera detta via docker-compose)
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Kör appen via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
