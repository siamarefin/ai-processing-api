from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    text: str
    language: str | None = None
    duration: float | None = None
    provider: str


class DocumentExtractionResponse(BaseModel):
    text: str
    provider: str