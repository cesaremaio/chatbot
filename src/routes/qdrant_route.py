from fastapi import APIRouter, HTTPException, Request
from typing import Any
from src.vectordb.models import StatusResponse, CollectionsResponse, QdrantDeleteRequest, QdrantInsertRequest, QdrantSearchRequest
from src.vectordb.service import qdrant_service

router = APIRouter(prefix="/qdrant", tags=["qdrant"])

# @router.post("/search")
# async def search_qdrant(request: QdrantSearchRequest):
#     # TODO: Implement Qdrant search logic here
#     # Example: query = body.get("query")
#     # result = qdrant_client.search(query)
#     return {"message": "Search endpoint called", "body": body}

@router.post("/upsert", response_model=StatusResponse)
async def upsert_qdrant(request: QdrantInsertRequest):
    try:
        await qdrant_service.put_items(collection_name=request.collection_name, items=request.items)
        return StatusResponse(status="success", message="Uploaded item")
    except Exception as e:
        return StatusResponse(status="failed", message=f"Unable to upload item. Exception: {e}")

@router.get("/get-collections", response_model=CollectionsResponse)
async def get_collections():
    try:
        collections = await qdrant_service.get_collections()
        return CollectionsResponse(status="success", message="retrieved collections", collections=collections)
    except Exception as e:
        return StatusResponse(status="failed", message=f"error fetching collections. Exception: {e}")
    
@router.delete("/delete-collection", response_model=StatusResponse)
async def delete_qdrant(request: QdrantDeleteRequest):
    try:
        await qdrant_service.delete_collection(request.collection_name)
        return StatusResponse(status="success", message=f"deleted collection {request.collection_name}")
    except Exception as e:
        return StatusResponse(status="failed", message=f"unable to delete collection {request.collection_name}. Exception: {e}")    
