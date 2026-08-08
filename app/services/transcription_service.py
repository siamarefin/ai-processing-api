from app.adapters.speech_provider import SpeechProvider


class TranscriptionService:

    def __init__(self, provider: SpeechProvider):
        self.provider = provider

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> dict:
        return self.provider.transcribe(
            audio_path=audio_path,
            language=language,
        )