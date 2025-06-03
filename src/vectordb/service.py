from src.vectordb.client import QdrantClient
from src.vectordb.models import QdrantItems, QdrantDeleteRequest, QdrantInsertRequest, QdrantSearchRequest

class QdrantService:
    def __init__(self):
        self.client = QdrantClient()

    async def create_collection(self, collection_name: str, vector_size: int):
        return await self.client.create_collection(
            collection_name=collection_name,
            vector_size=vector_size,
        )

    async def get_collections(self):
        return await self.client.get_collections()

    async def put_items(self, collection_name: str, items: list[QdrantItems]):
        return await self.client.put_items(
            collection_name=collection_name,
            items=items
        )

    # async def search(self, collection_name: str, query_vector: list, top_k: int = 5):
    #     return await self.client.search(
    #         collection_name=collection_name,
    #         query_vector=query_vector,
    #         top_k=top_k
    #     )

    async def delete_collection(self, collection_name: str):
        try:
            await self.client.delete_collection(collection_name=collection_name)
        except Exception as e:
            return 

    # async def get_collection_info(self, collection_name: str):
    #     return await self.client.get_collection_info(collection_name=collection_name)
    

qdrant_service = QdrantService()