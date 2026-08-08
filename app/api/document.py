from fastapi import APIRouter, File, Form, UploadFile

from app.adapters.ocr_adapter import TesseractOCRAdapter
from app.schemas.response import DocumentExtractionResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/document",
    tags=["Document"],
)


@router.post(
    "/extract",
    response_model=DocumentExtractionResponse,
)
async def extract_document(
    file: UploadFile = File(...),
    language: str = Form(default="eng"),
):
    contents = await file.read()

    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as document_file:
        document_file.write(contents)

    ocr_provider = TesseractOCRAdapter()
    service = DocumentService(ocr_provider)

    return service.extract_text(
        image_path=temp_path,
        language=language,
    )