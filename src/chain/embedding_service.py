from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("thenlper/gte-small")
        
    async def get_embedding(self, text: str):
        embedding = self.embedding_model.encode(text)
        return embedding


embedding_service = EmbeddingService()