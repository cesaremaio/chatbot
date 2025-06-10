from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

from src.vectordb.service import qdrant_service
import asyncio




class ChainService:
    def __init__(self):
        self.collection_name="chatbot_qdrant"
    
    async def get_embedding(self, user_message: str):
        embedding_model = SentenceTransformer("thenlper/gte-small")
        embeddings = embedding_model.encode(user_message)
        return embeddings

    async def retrieve(self, user_message: str) -> list[str]:
        query_vectors = await self.get_embedding(user_message)
        
        if hasattr(query_vectors, "tolist"):
            query_vectors = query_vectors.tolist()

        retrieved_documents = await qdrant_service.retrieve_points(
            collection_name=self.collection_name, 
            query_vectors=query_vectors,
            limit=10)

        return retrieved_documents
    
    async def rerank(self, user_message: str, retrieved_documents: list[str], top_k: int = 1):
        rerank_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

        ranks = rerank_model.rank(query=user_message, documents=retrieved_documents, top_k=top_k, return_documents=True)

        for rank in ranks:
            print(f"- #{rank['corpus_id']} ({rank['score']:.2f}): {rank['text']}")
        
        return ranks








async def main():
    chain_service = ChainService()
    # embedding = await chain_service.get_embedding("ciao")
    # print(f"embedding: {type(embedding)}")
    # print(f"embedding: {embedding.shape}")

    retrieved_documents = await chain_service.retrieve("ciao")
    print(f"retrieved_documents: {retrieved_documents}")

if __name__ == "__main__":
    asyncio.run(main())