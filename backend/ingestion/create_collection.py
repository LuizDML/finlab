import os

from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

# Movi o env na pasta de configurações
env_path = Path(__file__).resolve().parents[1] / "api" / "config" / ".env"
load_dotenv(env_path)

COLLECTION_NAME = "financial"

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Deleta a collection
# qdrant.delete_collection(COLLECTION_NAME)

# Na criação da collection usar on_disk=True para cada vetor ocupar 1KB ao invés de 4KB
# no geral quantização só é necessário quando houver mais de 1 milhão de vetores
qdrant.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={
        "dense": models.VectorParams(
            size=1024, 
            distance=models.Distance.COSINE, 
            on_disk=True,), 
        "colbert": models.VectorParams(
            size=128,
            distance=models.Distance.COSINE,
            multivector_config=models.MultiVectorConfig(
                comparator=models.MultiVectorComparator.MAX_SIM
            ),
        ),
    },
    sparse_vectors_config={"sparse": models.SparseVectorParams()},
    quantization_config=models.ScalarQuantization(
        scalar=models.ScalarQuantizationConfig(
            type=models.ScalarType.INT8, # transforma para tipo inteiro
            quantile = 0.99, # exclui outliers extremos
            always_ram=True, # mantem os vetores QUANTIZADOS em ram, os originais ficam em disco
        )
    )    
)