FROM python:3.11-slim

# instalar dependências do sistema (AGORA INCLUINDO FFMPEG)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Porta usada pelo Fly.io
ENV PORT=8080

# iniciar o app
CMD ["uvicorn", "app:app",]()
