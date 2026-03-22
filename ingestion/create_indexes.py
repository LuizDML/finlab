"""Criar índices para melhorar a performance e filtrar apenas itens desejados"""
# Não esquecer de rodar APÓS fazer a ingestão

import os

from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

# Movi o env na pasta de configurações
env_path = Path(__file__).resolve().parents[1] / "api" / "config" / ".env"
load_dotenv(env_path)

# Iniciar o cliente do Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Campos a indexar
fields_to_index =[
    "metadata.ticker",
    "metadata.form_type",
    "metadata.source",
]

for field_name in fields_to_index:
    qdrant.create_payload_index(
        collection_name = "financial",
        field_name=field_name,
        field_schema=models.PayloadSchemaType.KEYWORD,
    )
    print(f"Índice criado para {field_name}")