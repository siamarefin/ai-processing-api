import pytesseract

from app.adapters.ocr_provider import OCRProvider


class TesseractOCRAdapter(OCRProvider):

    def extract_text(
        self,
        image_path: str,
        language: str = "eng",
    ) -> str:
        return pytesseract.image_to_string(
            image_path,
            lang=language,
        )