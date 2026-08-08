from app.adapters.mock_adapter import MockAdapter
from app.adapters.speech_provider import SpeechProvider
from app.adapters.whisper_adapter import WhisperAdapter
from app.config.settings import settings


def get_speech_provider() -> SpeechProvider:
    if settings.use_mock:
        return MockAdapter()

    return WhisperAdapter(
        model_size=settings.model_size,
    )