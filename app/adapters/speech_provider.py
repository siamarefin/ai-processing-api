from abc import ABC, abstractmethod


class SpeechProvider(ABC):

    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> dict:
        """Transcribe an audio file into text."""
        pass