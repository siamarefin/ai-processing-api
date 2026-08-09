import os
import tempfile

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.adapters.speech_provider import SpeechProvider
from app.dependencies import get_speech_provider
from app.schemas.response import TranscriptionResponse
from app.services.transcription_service import TranscriptionService
from app.utils.validation import validate_audio_file


router = APIRouter(
    prefix="/api/v1",
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

    temp_path = None

    try:
        contents = await file.read()

        if not contents:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=400,
                detail="Audio file must not be empty.",
            )

        suffix = os.path.splitext(file.filename or "")[1].lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as audio_file:
            audio_file.write(contents)
            temp_path = audio_file.name

        return service.transcribe(
            audio_path=temp_path,
            language=language,
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()