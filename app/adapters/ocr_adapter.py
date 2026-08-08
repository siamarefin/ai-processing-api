from abc import ABC, abstractmethod

import pytesseract
from PIL import Image


class OCRAdapter(ABC):

    @abstractmethod
    def extract_text(
        self,
        image_path: str,
        language: str = "eng",
    ) -> str:
        """Extract text from an image."""
        pass


class TesseractOCRAdapter(OCRAdapter):

    def extract_text(
        self,
        image_path: str,
        language: str = "eng",
    ) -> str:
        image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image,
            lang=language,
        )

        return text.strip()