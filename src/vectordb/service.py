from src.vectordb.client import QdrantClient
from src.vectordb.models import QdrantItems, QdrantBaseRequest, QdrantInsertRequest, QdrantSearchRequest

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

    async def query_points(self, collection_name: str, query_vectors: list[float], limit: int = 10):
        try:
            response = await self.client.query_points(
                    collection_name=collection_name,
                    query_vectors=query_vectors, 
                    limit=limit
                )
            
            return response.model_dump()
        except Exception as e:
            raise e

    async def retrieve_points(self, collection_name: str, query_vectors: list[float], limit: int = 10):
        response = await self.query_points(collection_name, query_vectors)
        points = response["result"]["points"]

        retrieved_documents = []
        for point in points: 
            retrieved_documents.append(point["payload"]["full_text"])
        return retrieved_documents



    async def delete_collection(self, collection_name: str):
        try:
            await self.client.delete_collection(collection_name=collection_name)
        except Exception as e:
            raise e
    

qdrant_service = QdrantService()