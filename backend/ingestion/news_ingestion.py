import os
import uuid

from pathlib import Path
from dotenv import load_dotenv
from fastembed import LateInteractionTextEmbedding, SparseTextEmbedding, TextEmbedding
from qdrant_client import QdrantClient, models
from utils.news_client import NewsClient
from utils.simple_chunker import SimpleChunker

# Movi o env na pasta de configurações
env_path = Path(__file__).resolve().parents[1] / "api" / "config" / ".env"
load_dotenv(env_path)

# Definições
DENSE_MODEL = "intfloat/multilingual-e5-large"
# DENSE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SPARSE_MODEL = "Qdrant/bm25"
COLBERT_MODEL = "colbert-ir/colbertv2.0"
COLLECTION_NAME = "financial"
MAX_TOKENS = 500

# Iniciar o cliente do Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Iniciar o cliente de noticiais, passando a empresa a ser analisada e a quantidade limite de notícias
news_client = NewsClient()
news_data = news_client.fetch_news("AAPL", max_stories=10)

chunker = SimpleChunker(max_tokens=MAX_TOKENS)

all_chunks = []

# Converter as notícias em chunks 
for article in news_data:
    chunks = chunker.create_chunks(article["text"])
    for chunk in chunks:
        all_chunks.append({"text": chunk, "metadata": article["metadata"]})

# Setar os modelos
dense_model = TextEmbedding(DENSE_MODEL)
sparse_model = SparseTextEmbedding(SPARSE_MODEL)
colbert_model = LateInteractionTextEmbedding(COLBERT_MODEL)

# Vetorizar
points = []
for chunk_data in all_chunks:
    chunk = chunk_data["text"]
    metadata = chunk_data["metadata"]

    dense_embedding = list(dense_model.passage_embed([chunk]))[0].tolist()
    sparse_embedding = list(sparse_model.passage_embed([chunk]))[0].as_object()
    colbert_embedding = list(colbert_model.passage_embed([chunk]))[0].tolist()

    point = models.PointStruct(
        id=str(uuid.uuid4()),
        vector={
            "dense": dense_embedding,
            "sparse": sparse_embedding,
            "colbert": colbert_embedding,
        },
        payload={"text": chunk, "metadata": metadata},
    )
    points.append(point)

# Upload dos vetores para o qdrant
qdrant.upload_points(collection_name=COLLECTION_NAME, points=points, batch_size=5)