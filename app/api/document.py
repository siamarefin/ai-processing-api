from fastapi import APIRouter, Depends, File, Form, UploadFile

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
    contents = await file.read()

    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as document_file:
        document_file.write(contents)

    service = DocumentService(ocr_provider)

    return service.extract_text(
        image_path=temp_path,
        language=language,
    )