from app.adapters.ocr_provider import OCRProvider


class MockOCRAdapter(OCRProvider):

    def extract_text(
        self,
        image_path: str,
        language: str = "eng",
    ) -> str:
        return """
        CIVIL SERVICE HOSPITAL
        Name: SANTOSH KUMAR HATHI
        Age/Gender: 37 YEAR/ M
        Sample Registered Date: 2022/08/24
        Blood Sugar Fasting 302.0 mg/dl 60-110
        Blood Urea 33.0 mg/dl 8-45
        """