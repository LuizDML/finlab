from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from api.config.settings import settings

class EmbeddingsService:
    def __init__(self):
        self.dense_model = TextEmbedding(settings.dense_model)
        self.sparse_model = SparseTextEmbedding(settings.sparse_model) 
        self.colbert_model = LateInteractionTextEmbedding(settings.colbert_model) 

    def embed_query(self, query: str):
        dense = list(self.dense_model.query_embed([query]))[0].tolist()
        sparse = list(self.sparse_model.query_embed([query]))[0].as_object()
        colbert = list(self.colbert_model.query_embed([query]))[0].tolist()
        return dense, sparse, colbert
    
    
        
    def get_dense_embedding(self, text: str):
        return list(self.dense_model.passage_embed([text]))[0].tolist()

    def get_sparse_embedding(self, text: str):
        return list(self.sparse_model.passage_embed([text]))[0].as_object()

    def get_colbert_embedding(self, text: str):
        return list(self.colbert_model.passage_embed([text]))[0].tolist()