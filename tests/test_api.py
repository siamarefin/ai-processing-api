from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_transcription_endpoint_exists():
    response = client.post(
        "/api/v1/transcribe",
    )

    assert response.status_code in [400, 422]


def test_document_endpoint_exists():
    response = client.post(
        "/api/v1/documents/extract",
    )

    assert response.status_code in [400, 422]