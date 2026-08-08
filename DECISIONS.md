# Architecture Decisions

This document records the main technical and architectural decisions made for the AI Processing API.

The project intentionally follows a simple and modular architecture. The goal is to keep the implementation easy to understand, test, maintain, and extend without adding unnecessary complexity.

---

## 1. Why FastAPI?

### Decision

Use **FastAPI** as the backend web framework.

### Reason

FastAPI provides:

- Simple API development
- Automatic OpenAPI documentation
- Swagger UI
- Pydantic integration
- File upload support
- Dependency Injection
- Good performance
- Type-hint based development

It is well suited for an AI-processing API where files need to be uploaded and processed by ML/OCR components.

---

## 2. Why a Layered Architecture?

### Decision

Separate the application into:

```text
API
 ↓
Service
 ↓
Adapter
```

### Reason

Each layer has a clear responsibility.

### API Layer

Handles:

- HTTP requests
- File uploads
- Request parameters
- HTTP responses

### Service Layer

Handles:

- Business logic
- Transcription workflow
- Document extraction
- Parsing
- Normalization

### Adapter Layer

Handles:

- External AI providers
- OCR providers
- Provider-specific implementation details

This separation makes the system easier to test and maintain.

---

## 3. Why the Adapter Pattern?

### Decision

Use adapters for external speech and OCR providers.

Speech providers are represented through:

```text
SpeechProvider
├── WhisperAdapter
└── MockAdapter
```

### Reason

The service layer should not depend directly on a specific speech provider.

For example, the transcription service can work with:

```python
SpeechProvider
```

instead of directly depending on:

```python
WhisperAdapter
```

This makes it easier to replace Whisper with another provider later without rewriting the API or service layer.

---

## 4. Why a Mock Speech Provider?

### Decision

Provide a mock speech implementation.

### Reason

The mock provider allows the application to be tested without:

- Downloading a Whisper model
- Running ML inference
- Depending on external model resources

It is useful for:

- Development
- API testing
- Unit testing
- Faster debugging

The mock provider also verifies that the API and service layers are correctly separated from the actual speech model.

---

## 5. Why Whisper?

### Decision

Use **Whisper/faster-whisper** for speech transcription.

### Reason

Whisper provides a practical local speech-to-text solution and supports multiple languages.

Using a local model also keeps the transcription pipeline independent from an external speech API.

The implementation allows the model configuration to be changed through application settings.

---

## 6. Why Tesseract OCR?

### Decision

Use **Tesseract OCR** for document/image text extraction.

### Reason

Tesseract provides a straightforward OCR engine that can be integrated locally.

It is sufficient for the project's basic document extraction requirements and avoids introducing an external OCR service.

The OCR implementation is isolated inside an adapter so that another OCR provider can be added later if required.

---

## 7. Why Dependency Injection?

### Decision

Use FastAPI Dependency Injection for selecting the speech provider.

### Reason

The API endpoint should not create a specific speech implementation directly.

Instead:

```text
API Endpoint
     ↓
Dependency
     ↓
SpeechProvider
     ↓
Whisper / Mock
```

This provides loose coupling and makes testing easier.

It also allows the provider to be changed through configuration without changing the endpoint implementation.

---

## 8. Why a Service Layer?

### Decision

Keep business logic inside service classes.

Examples:

```text
TranscriptionService
DocumentService
```

### Reason

API endpoints should remain thin.

For example:

```text
Request
 ↓
API endpoint
 ↓
Service
 ↓
Provider
 ↓
Response
```

The service layer contains processing logic rather than mixing that logic with HTTP handling.

This makes the processing logic easier to test independently.

---

## 9. Why Pydantic Response Schemas?

### Decision

Use Pydantic models for API responses.

### Reason

Structured response models provide:

- Type validation
- Consistent API responses
- Automatic OpenAPI documentation
- Clear API contracts
- Easier testing

For document extraction, the response is separated into:

```text
meta
results
```

Each laboratory result contains structured fields such as:

```text
test_name
value
unit
reference_range
flag
raw_line
```

---

## 10. Why Preserve `raw_line`?

### Decision

Keep the original OCR line in every extracted laboratory result.

### Reason

OCR can contain mistakes.

For example:

```text
Potassium (K+) 43 mEq/L 3.5-5.2
```

The OCR system may have incorrectly recognized an original decimal value.

Keeping:

```text
raw_line
```

provides traceability between the structured result and the original OCR output.

The parser therefore avoids silently changing uncertain OCR values.

---

## 11. Why Rule-Based Document Parsing?

### Decision

Use simple rule-based parsing for the initial implementation.

### Reason

The project requires a basic but structured document extraction pipeline.

Rule-based parsing is:

- Easy to understand
- Easy to test
- Lightweight
- Deterministic
- Easy to modify for known report formats

A more advanced NLP/LLM-based extraction layer could be added later if document variability requires it.

---

## 12. Why Normalize Units?

### Decision

Normalize common OCR variations into consistent units.

Examples:

```text
mg/dl  → mg/dL
gm/dl  → g/dL
meq/l  → mEq/L
u/l    → U/L
```

### Reason

OCR output can contain inconsistent capitalization or small formatting variations.

Normalization creates a more consistent structured response while keeping the original OCR line available through `raw_line`.

---

## 13. Why Calculate HIGH/LOW Flags?

### Decision

Calculate a result flag when a numeric value and a valid reference range are available.

Example:

```text
Value: 302
Reference range: 60-110
Flag: HIGH
```

If the value falls inside the reference range:

```text
Flag: null
```

If there is not enough information to determine the flag:

```text
Flag: null
```

### Reason

The flag is derived from the provided reference range rather than from hardcoded medical assumptions.

This keeps the implementation simple and tied to the report's own reference values.

---

## 14. Why Avoid Blind OCR Correction?

### Decision

Do not automatically guess or modify uncertain OCR values.

For example, if OCR returns:

```text
43
```

instead of a possible:

```text
4.3
```

the parser does not automatically change it.

### Reason

Automatically changing uncertain medical report values could introduce incorrect data.

The original OCR value is preserved in:

```text
value
raw_line
```

Further correction can be introduced later using a more reliable validation or domain-specific approach.

---

## 15. Why Docker?

### Decision

Provide Docker and Docker Compose configuration.

### Reason

Docker makes the application environment more reproducible.

It helps package:

- Python dependencies
- Application code
- Runtime configuration
- System-level dependencies

This reduces differences between development and deployment environments.

---

## 16. Why Keep the Initial Scope Small?

### Decision

Avoid unnecessary features in the initial implementation.

### Reason

The primary goal is to demonstrate a clean AI backend architecture rather than build a large production platform.

The current system focuses on:

```text
Audio → Transcription

Image/Document → OCR → Structured Extraction
```

Features such as authentication, rate limiting, advanced monitoring, and complex orchestration can be added later if required.

---

## 17. Known Limitations

The current implementation has several limitations:

- OCR accuracy depends on image quality.
- OCR can misread decimal values.
- Complex laboratory layouts may require additional parsing rules.
- Handwritten documents are not specifically optimized.
- Different report formats may require additional extraction rules.
- Whisper transcription quality depends on the selected model and language configuration.
- PDF-specific processing may require additional handling depending on the input.
- The current parser is rule-based rather than a general-purpose medical document understanding system.

These limitations are accepted for the initial implementation.

---

## 18. Future Improvements

Possible future improvements include:

- Better OCR preprocessing
- More robust document layout detection
- Improved value normalization
- Better handling of OCR decimal errors
- Support for additional document formats
- More comprehensive unit tests
- Authentication
- Rate limiting
- Structured application logging
- Monitoring and observability
- Additional speech/OCR providers
- More advanced document understanding

---

## Summary

The architecture prioritizes:

```text
Simple
   ↓
Modular
   ↓
Testable
   ↓
Replaceable Providers
   ↓
Maintainable
```

The implementation deliberately avoids unnecessary complexity while keeping clear boundaries between API handling, business logic, external providers, configuration, and data validation.
