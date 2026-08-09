from pathlib import Path

from fastapi import HTTPException, UploadFile


ALLOWED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".ogg",
}

ALLOWED_AUDIO_CONTENT_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/x-m4a",
    "audio/flac",
    "audio/ogg",
}

MAX_AUDIO_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


def validate_audio_file(file: UploadFile) -> None:
    # ---------------------------------------------------------
    # Filename validation
    # ---------------------------------------------------------

    if not file.filename or not file.filename.strip():
        raise HTTPException(
            status_code=400,
            detail="Audio file name is required.",
        )

    filename = Path(file.filename).name

    if filename != file.filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid audio file name.",
        )

    # ---------------------------------------------------------
    # Extension validation
    # ---------------------------------------------------------

    extension = Path(filename).suffix.lower()

    if not extension:
        raise HTTPException(
            status_code=400,
            detail="Audio file extension is required.",
        )

    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {extension}",
        )

    # ---------------------------------------------------------
    # Content type validation
    # ---------------------------------------------------------

    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="Audio content type is required.",
        )

    if file.content_type not in ALLOWED_AUDIO_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported content type: {file.content_type}",
        )

    # ---------------------------------------------------------
    # File size validation
    # ---------------------------------------------------------

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Audio file must not be empty.",
        )

    if file_size > MAX_AUDIO_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Audio file size must not exceed 25 MB.",
        )