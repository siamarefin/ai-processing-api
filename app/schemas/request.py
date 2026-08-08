from pydantic import BaseModel, Field


class TranscriptionRequest(BaseModel):
    language: str | None = Field(
        default=None,
        description="Language of the audio. If omitted, the model will detect it.",
    )


class DocumentExtractionRequest(BaseModel):
    language: str | None = Field(
        default=None,
        description="Language of the document.",
    )