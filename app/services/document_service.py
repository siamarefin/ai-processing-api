import re

from app.adapters.ocr_provider import OCRProvider


class DocumentService:

    def __init__(self, ocr_provider: OCRProvider):
        self.ocr_provider = ocr_provider

    def extract_text(self, image_path: str, language: str = "eng"):
        raw_text = self.ocr_provider.extract_text(
            image_path=image_path,
            language=language,
        )

        meta = self._extract_metadata(raw_text)
        results = self._extract_results(raw_text)

        return {
            "meta": meta,
            "results": results,
        }

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def _extract_metadata(self, text: str) -> dict:
        return {
            "patient_name": self._extract_patient_name(text),
            "age": self._extract_age(text),
            "sex": self._extract_sex(text),
            "report_date": self._extract_report_date(text),
            "lab_name": self._extract_lab_name(text),
            "reference_no": self._extract_reference_no(text),
        }

    def _extract_patient_name(self, text: str):
        match = re.search(
            r"Name\s*:\s*([A-Za-z .'-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

        return None

    def _extract_age(self, text: str):
        match = re.search(
            r"Age\s*/?\s*Gender\s*:\s*(\d+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return int(match.group(1))

        return None

    def _extract_sex(self, text: str):
        match = re.search(
            r"Age\s*/?\s*Gender\s*:\s*\d+\s*(?:YEAR)?\s*/\s*([MF])",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).upper()

        return None

    def _extract_report_date(self, text: str):
        match = re.search(
            r"Sample\s+Registered\s+Date\s*:\s*"
            r"(\d{4}/\d{2}/\d{2})",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None

    def _extract_lab_name(self, text: str):
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines[:10]:
            if "HOSPITAL" in line.upper():
                return line.strip()

        return None

    def _extract_reference_no(self, text: str):
        match = re.search(
            r"Patient\s+ID\s*:\s*([A-Za-z0-9-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None

    # ---------------------------------------------------------
    # Lab Results
    # ---------------------------------------------------------

    def _extract_results(self, text: str) -> list[dict]:
        results = []

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            result = self._parse_result_line(line)

            if result:
                results.append(result)

        return results

    def _parse_result_line(self, line: str):
        pattern = re.compile(
            r"^(?P<test_name>[A-Za-z][A-Za-z0-9 ()+\-/'.]+?)"
            r"\s+"
            r"(?P<value>[<>]?\s*\d[\d,]*(?:\.\d+)?)"
            r"\s+"
            r"(?P<unit>[A-Za-z%µμ/]+(?:/[A-Za-z]+)?)"
            r"(?:\s+"
            r"(?P<reference_range>[<>]?\s*\d[\d,.]*"
            r"(?:\s*-\s*[<>]?\s*\d[\d,.]*)?))?"
            r"\s*$",
            re.IGNORECASE,
        )

        match = pattern.match(line)

        if not match:
            return None

        test_name = match.group("test_name").strip()
        raw_value = match.group("value").strip()
        unit = self._normalize_unit(match.group("unit"))
        reference_range = match.group("reference_range")

        value = self._normalize_value(raw_value)

        if value is None:
            return None

        if reference_range:
            reference_range = reference_range.strip()

        flag = self._calculate_flag(
            value=value,
            reference_range=reference_range,
        )

        return {
            "test_name": test_name,
            "value": value,
            "unit": unit,
            "reference_range": reference_range,
            "flag": flag,
            "raw_line": line,
        }

    # ---------------------------------------------------------
    # Value Normalization
    # ---------------------------------------------------------

    def _normalize_value(self, value: str):
        value = value.strip()
        value = value.replace(",", "")

        if value.startswith("<"):
            value = value[1:].strip()

        if value.startswith(">"):
            value = value[1:].strip()

        try:
            return float(value)
        except ValueError:
            return None

    # ---------------------------------------------------------
    # Unit Normalization
    # ---------------------------------------------------------

    def _normalize_unit(self, unit: str) -> str:
        normalized = unit.strip().lower()

        unit_map = {
            "mg/dl": "mg/dL",
            "mg/di": "mg/dL",
            "gm/dl": "g/dL",
            "gm/di": "g/dL",
            "g/dl": "g/dL",
            "meq/l": "mEq/L",
            "meq/i": "mEq/L",
            "u/l": "U/L",
            "u/t": "U/L",
            "%": "%",
            "cells/cumm": "cells/cumm",
            "cells/curm": "cells/cumm",
        }

        return unit_map.get(normalized, unit.strip())

    # ---------------------------------------------------------
    # Flag
    # ---------------------------------------------------------

    def _calculate_flag(
        self,
        value: float,
        reference_range: str | None,
    ):
        if not reference_range:
            return None

        match = re.match(
            r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$",
            reference_range,
        )

        if not match:
            return None

        lower = float(match.group(1))
        upper = float(match.group(2))

        if value < lower:
            return "LOW"

        if value > upper:
            return "HIGH"

        return None