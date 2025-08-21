from fastapi import APIRouter, UploadFile, File
from src.vectordb.models import StatusResponse
from src.ingestion.service import pdf_ingestion_service

import os
import tempfile

router = APIRouter(prefix="/user_uploads", tags=["User Uploads"])

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    suffix = os.path.splitext(file.filename)[1] # type: ignore
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