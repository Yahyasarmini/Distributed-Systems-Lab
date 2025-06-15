# backend/Dockerfile
FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# System-Dependencies installieren
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App Code kopieren
COPY . .

# Port freigeben
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# App starten
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]