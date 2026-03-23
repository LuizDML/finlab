## Para reprodução:

1 - Instalar uv e usar uv sync para criar o .venv com todas as depéndências;

2 - Não se esqueça de criar um .env com as chaves QGRANT_URL, QDRANT_API_KEY, GROQ_API_KEY

3 - Criar as Collections e seus Índices
Basta rodar backend/ingestion/create-colletion.py e backend/ingestion/create_indexes.py

4 - Faça a ingestão dos dados
Basta rodar backend/ingestion/ingestion.py (SEC) e backend/ingestion/news_ingestion.py (Yahooo Finance)
(passo 4 será modificado futuramente)

5 - Iniciar a API
uvicorn main:app --reload

## Endpoints

Atualmente existem 3, POST /search, POST /rag e POST /agent
No front o /rag e o /agent são utilizados, no caso do /agent é necessário marcar a caixa.