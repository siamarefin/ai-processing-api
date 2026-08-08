from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.adapters.speech_provider import SpeechProvider
from app.dependencies import get_speech_provider
from app.schemas.response import TranscriptionResponse
from app.services.transcription_service import TranscriptionService
from app.utils.validation import validate_audio_file


router = APIRouter(
    prefix="/audio",
    tags=["Audio"],
)


@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str | None = Form(default=None),
    provider: SpeechProvider = Depends(get_speech_provider),
):
    validate_audio_file(file)

    service = TranscriptionService(provider)

    contents = await file.read()

    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as audio_file:
        audio_file.write(contents)

    return service.transcribe(
        audio_path=temp_path,
        language=language,
    )