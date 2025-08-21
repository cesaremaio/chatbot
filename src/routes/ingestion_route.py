from fastapi import APIRouter, UploadFile, File
from src.vectordb.models import StatusResponse, QdrantBaseRequest, QdrantInsertRequest
from src.vectordb.service import qdrant_service
from src.ingestion.service import pdf_ingestion_service

import os
import tempfile

from loguru import logger

router = APIRouter(prefix="/user_uploads", tags=["User Uploads"])


@router.post("/create-collection", response_model=StatusResponse)
async def create_collection(request: QdrantBaseRequest):
    collections = await qdrant_service.get_collections()
    if request.collection_name in collections:
        return StatusResponse(status="failed", message=f"Collection {request.collection_name} already exists.")

    try:
        await qdrant_service.create_collection(collection_name=request.collection_name, vector_size=384)
        return StatusResponse(status="success", message=f"Collection {request.collection_name} successfully created")
    except Exception as e:
        return StatusResponse(status="failed", message=f"Unable to create collection {request.collection_name} . Exception: {e}")
    

@router.post("/upsert", response_model=StatusResponse)
async def upsert_qdrant(request: QdrantInsertRequest):
    try:
        await qdrant_service.put_items(collection_name=request.collection_name, items=request.items)
        return StatusResponse(status="success", message="Uploaded item")
    except Exception as e:
        return StatusResponse(status="failed", message=f"Unable to upload item. Exception: {e}")
    

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Start ingestion
        await pdf_ingestion_service.ingestion(tmp_path)

        return {
            "filename": file.filename,
            "ready_for_chat": True
        }
    finally:
        os.remove(tmp_path)  # cleanup
    
    






    
    # Respond with JSON (frontend expects JSON and checks for `ready_for_chat`)
    return {
        "filename": file.filename,
        "size": len(contents),
        "ready_for_chat": True
    }
