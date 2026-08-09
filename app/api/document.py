import os
import tempfile

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.adapters.ocr_provider import OCRProvider
from app.dependencies import get_ocr_provider
from app.schemas.response import DocumentExtractionResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/api/v1",
    tags=["Document"],
)


@router.post(
    "/documents/extract",
    response_model=DocumentExtractionResponse,
)
async def extract_document(
    file: UploadFile = File(...),
    language: str = Form(default="eng"),
    ocr_provider: OCRProvider = Depends(get_ocr_provider),
):
    if not file.filename or not file.filename.strip():
        raise HTTPException(
            status_code=400,
            detail="Document file name is required.",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Document file must not be empty.",
        )

    temp_path = None

    try:
        suffix = os.path.splitext(file.filename)[1].lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as document_file:
            document_file.write(contents)
            temp_path = document_file.name

        service = DocumentService(ocr_provider)

        return service.extract_text(
            image_path=temp_path,
            language=language,
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()