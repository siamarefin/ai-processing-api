from app.adapters.speech_provider import SpeechProvider


class MockAdapter(SpeechProvider):

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> dict:
        return {
            "text": "This is a mock transcription.",
            "language": language or "en",
            "duration": 0.0,
            "provider": "mock",
        }