# AI Processing API

A simple, modular backend API for **audio transcription** and **document/lab-report extraction** using FastAPI, Whisper, and Tesseract OCR.

## Features

- Audio transcription using Whisper
- Mock speech provider for development/testing
- Provider abstraction using the Adapter Pattern
- Dependency Injection for speech providers
- Image/document text extraction using Tesseract OCR
- Structured extraction of laboratory report metadata
- Laboratory test result extraction
- Unit normalization
- Reference-range parsing
- Automatic `HIGH` / `LOW` flag calculation
- Pydantic response validation
- Docker support
- Automated API tests

## Architecture

```text
Client
  │
  ▼
FastAPI API Layer
  │
  ├── Audio API
  │     │
  │     ▼
  │   Transcription Service
  │     │
  │     ▼
  │   Speech Provider
  │     ├── Whisper Adapter
  │     └── Mock Adapter
  │
  └── Document API
        │
        ▼
      Document Service
        │
        ▼
      OCR Adapter
        │
        ▼
      Tesseract OCR
```

The application separates API handling, business logic, external AI/OCR providers, schemas, configuration, and validation.

## Project Structure

```text
ai-processing-api/
│
├── app/
│   ├── api/
│   │   ├── audio.py
│   │   └── document.py
│   │
│   ├── services/
│   │   ├── transcription_service.py
│   │   └── document_service.py
│   │
│   ├── adapters/
│   │   ├── speech_provider.py
│   │   ├── whisper_adapter.py
│   │   ├── mock_adapter.py
│   │   └── ocr_adapter.py
│   │
│   ├── schemas/
│   │   ├── request.py
│   │   └── response.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── utils/
│   │   └── validation.py
│   │
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│   └── test_api.py
│
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── DECISIONS.md
```

## Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **faster-whisper**
- **Tesseract OCR**
- **Pillow**
- **python-multipart**
- **Pytest**
- **Docker**

# Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-processing-api
```

## 2. Create virtual environment

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
USE_MOCK=false
MODEL_SIZE=small
```

### Development with Mock Provider

```env
USE_MOCK=true
MODEL_SIZE=small
```

Using the mock provider allows the API flow to be tested without running the actual Whisper model.

# Run Locally

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

# API Endpoints

## Health Check

```http
GET /
```

Response:

```json
{
  "message": "AI Processing API is running"
}
```

## Audio Transcription

```http
POST /api/v1/transcribe
```

### Request

Multipart form-data:

```text
file      → audio file
language  → optional language code
```

Example:

```text
file: audio.wav
language: en
```

### Response

```json
{
  "text": "Hello, my name is Siam Arefin.",
  "language": "en",
  "duration": 9.624,
  "provider": "whisper"
}
```

The speech provider is selected through dependency injection, allowing Whisper and Mock providers to be swapped without changing the API layer.

## Document Extraction

```http
POST /api/v1/documents/extract
```

### Request

Multipart form-data:

```text
file      → document/image
language  → OCR language
```

Example:

```text
file: report.png
language: eng
```

### Response

```json
{
  "meta": {
    "patient_name": "SANTOSH KUMAR HATHI",
    "age": 37,
    "sex": "M",
    "report_date": "2022/08/24",
    "lab_name": "CIVIL SERVICE HOSPITAL",
    "reference_no": null
  },
  "results": [
    {
      "test_name": "Blood Sugar Fasting",
      "value": 302,
      "unit": "mg/dL",
      "reference_range": "60-110",
      "flag": "HIGH",
      "raw_line": "Blood Sugar Fasting 302.0 mg/dl 60-110"
    }
  ]
}
```

The document pipeline performs OCR first and then applies rule-based parsing to convert the extracted text into structured metadata and laboratory results.

# Testing

Run the test suite:

```bash
pytest
```

The tests cover the basic application/API behavior.

# Docker

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Stop the containers:

```bash
docker compose down
```

# Design Principles

The project follows a simple layered architecture.

### API Layer

Responsible for:

- HTTP requests
- File uploads
- Request parameters
- API responses

### Service Layer

Responsible for:

- Transcription workflow
- Document extraction
- Parsing
- Business logic

### Adapter Layer

Responsible for communicating with external providers:

- Whisper
- Mock speech provider
- Tesseract OCR

This keeps external dependencies isolated from business logic.

### Schema Layer

Pydantic models define the expected request and response structures.

### Dependency Injection

FastAPI dependency injection is used to select the speech provider without coupling the API endpoint directly to Whisper.

# Limitations

This project intentionally keeps the implementation simple.

Current limitations include:

- OCR accuracy depends on input image quality.
- OCR can misread decimal values or characters.
- Complex laboratory report layouts may require additional parsing rules.
- Handwritten documents are not specifically optimized.
- The parser does not blindly correct uncertain OCR values.
- Language detection/transcription quality depends on the selected Whisper configuration.
- PDF-specific processing may require additional handling depending on the input format.

# Future Improvements

Possible future improvements include:

- Better OCR preprocessing
- More robust laboratory report parsing
- Additional unit normalization
- Better handling of OCR decimal errors
- PDF text/image extraction
- More comprehensive test coverage
- Authentication
- Rate limiting
- Production logging and monitoring

## License

This project is intended for educational and assignment purposes.
