from pydantic import BaseModel
from typing import Union

class StatusResponse(BaseModel):
    status: str
    message: str

class CollectionsResponse(StatusResponse):
    collections: list[str]

class SearchResponse(StatusResponse):
    retrieved_vectors: Union[dict, None]

class QdrantItems(BaseModel):
    id: int
    vector: list
    payload: Union[dict, None]

class QdrantSearchRequest(BaseModel):
    collection_name: str
    query_vectors: list[float]    

class QdrantInsertRequest(BaseModel):
    collection_name: str
    items: list[QdrantItems]
class QdrantDeleteRequest(BaseModel):
    collection_name: str
