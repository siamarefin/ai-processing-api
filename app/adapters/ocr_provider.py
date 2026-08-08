from abc import ABC, abstractmethod


class OCRProvider(ABC):
    @abstractmethod
    def extract_text(
        self,
        image_path: str,
        language: str = "eng",
    ) -> str:
        """Extract text from an image/document."""
        raise NotImplementedError