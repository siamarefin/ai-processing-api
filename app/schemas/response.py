from typing import Optional

from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    duration: float
    provider: str


class DocumentMeta(BaseModel):
    patient_name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    report_date: Optional[str] = None
    lab_name: Optional[str] = None
    reference_no: Optional[str] = None


class LabResult(BaseModel):
    test_name: str
    value: Optional[float] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    flag: Optional[str] = None
    raw_line: str


class DocumentExtractionResponse(BaseModel):
    meta: DocumentMeta
    results: list[LabResult]