from qdrant_client import AsyncQdrantClient
from typing import Any, Optional
from qdrant_client.http.models import (
    VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue, PointIdsList
)
from src.app_settings import settings
from src.vectordb.models import QdrantItems, QdrantDeleteRequest, QdrantInsertRequest, QdrantSearchRequest

class QdrantClient:
    
    def __init__(self):
        self._url = settings.qdrant_url
        self._port = settings.qdrant_port
        self._api_key = settings.qdrant_api_key
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = AsyncQdrantClient(url=self._url, port=int(self._port), api_key=self._api_key) # type: ignore
        return self._client
        
    async def get_collections(self) -> list[str]:
        response = await self.client.get_collections()
        return [collection.name for collection in response.collections]

    async def create_collection(self, collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
        collections = await self.get_collections()
        if collection_name in collections:
            raise ValueError(f"Collection '{collection_name}' already exists.")
        
        await self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance)
        )

    async def delete_collection(self, collection_name: str):
        collections = await self.get_collections()
        if collection_name not in collections:
            raise ValueError(f"Collection '{collection_name}' does not exist")
        
        await self.client.delete_collection(collection_name=collection_name)

    async def put_items(self, collection_name: str, items: list[QdrantItems]):
        points = [
            PointStruct(
                id=item.id,     
                vector=item.vector,     
                payload=item.payload,   
            )
            for item in items
        ]
        await self.client.upsert(collection_name=collection_name, points=points)

    async def delete_items(self, collection_name: str, ids: list[int]):
        selector = PointIdsList(points=ids) # type: ignore
        await self.client.delete(collection_name=collection_name, points_selector=selector)
    
    async def query_points(
        self,
        collection_name: str,
        query_vectors: list[float],
        limit: int = 10,
        filter_payload: Optional[dict[str, Any]] = None
    ):
        qdrant_filter = None
        if filter_payload:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    ) for key, value in filter_payload.items()
                ]
            )
        response = await self.client.query_points(
            collection_name=collection_name,
            query=query_vectors,
            limit=limit,
            query_filter=qdrant_filter
        )
        return response