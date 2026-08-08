from faster_whisper import WhisperModel

from app.adapters.speech_provider import SpeechProvider


class WhisperAdapter(SpeechProvider):

    def __init__(self, model_size: str = "small"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> dict:
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
        )

        text = " ".join(segment.text.strip() for segment in segments)

        return {
            "text": text,
            "language": info.language,
            "duration": info.duration,
            "provider": "whisper",
        }