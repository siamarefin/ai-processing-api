from app.adapters.ocr_adapter import OCRAdapter


class DocumentService:

    def __init__(self, ocr_provider: OCRAdapter):
        self.ocr_provider = ocr_provider

    def extract_text(
        self,
        image_path: str,
        language: str = "eng",
    ) -> dict:
        text = self.ocr_provider.extract_text(
            image_path=image_path,
            language=language,
        )

        return {
            "text": text,
            "provider": "ocr",
        }