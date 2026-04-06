FROM python:3.13-slim-bullseye

WORKDIR /app

ENV PYTHONPATH=/app
# ENV FASTEMBED_CACHE_PATH=/app/models

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baixa modelo durante build - esse modelo dá problema ao baixar direto no Pi
# RUN python -c "from fastembed import LateInteractionTextEmbedding; LateInteractionTextEmbedding('colbert-ir/colbertv2.0')"


COPY . .

# RUN mkdir -p /app/models

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]