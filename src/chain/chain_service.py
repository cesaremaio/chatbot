from sentence_transformers import CrossEncoder
from src.vectordb.service import qdrant_service
from loguru import logger
from src.chain.embedding_service import embedding_service
from src.app_settings import settings



class ChainService:
    def __init__(self):
        pass
    
    async def retrieve(self, user_message: str) -> list[str]:
        query_vectors = await embedding_service.get_embedding(user_message)
        
        if hasattr(query_vectors, "tolist"):
            query_vectors = query_vectors.tolist() # type: ignore

        retrieved_documents = await qdrant_service.retrieve_points(
            collection_name=settings.qdrant_collection,  # type: ignore
            query_vectors=query_vectors,
            limit=10)
        
        logger.info(f"Retrieved {len(retrieved_documents)} documents.")
        return retrieved_documents
    
    async def rerank(self, user_message: str, retrieved_documents: list[str], top_k: int = 1):
        rerank_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

        ranks = rerank_model.rank(
            query=user_message, 
            documents=retrieved_documents, 
            top_k=top_k, 
            return_documents=True
        )

        # for rank in ranks:
        #     print(f"rank.keys(): {rank.keys()}")
            # print(f"- #{rank['corpus_id']} ({rank['score']:.2f}): {rank['text']}")

        logger.info("Rerank done.")
        return ranks

    async def full_retrieve(self, user_message: str) -> str:
        retrieved_documents = await self.retrieve(user_message=user_message)
        reranked_documents = await self.rerank(
            user_message=user_message,                 
            retrieved_documents=retrieved_documents,
            top_k=1
        )

        top_document = reranked_documents[0]
        score = top_document["score"]
        logger.info(f"top_document score : {score}")

        if float(score) > 0.000005:
            text=top_document["text"]
        else: 
            text=""
        
        return text # type: ignore

chain_service = ChainService()




# async def main():
    
#     # embedding = await chain_service.get_embedding("ciao")
#     # print(f"embedding: {type(embedding)}")
#     # print(f"embedding: {embedding.shape}")
#     user_message = "what work experience does Cesare have?"

    
#     # print(f"retrieved_documents: {retrieved_documents}")
#     print("\n\n")
#     reranked_documents = await chain_service.rerank(
#         user_message=user_message,                 
#         retrieved_documents=retrieved_documents,
#         top_k=1
#     )
#     for reranked_document in reranked_documents:
#         print(f"\n\nreranked_document: {reranked_document}")

#     top_document = reranked_documents[0]
#     score = top_document["score"]

#     if float(score) > 0.5:
#         text=top_document["text"]
#     else: 
#         text=""
    
#     PROMPT = f"""
#     {text} \n
#     {user_message}
#     """

# if __name__ == "__main__":
#     asyncio.run(main())