from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Processing API is running"
    }


def test_transcription_endpoint_exists():
    response = client.post("/audio/transcribe")

    assert response.status_code in [400, 422]


def test_document_endpoint_exists():
    response = client.post("/document/extract")

    assert response.status_code in [400, 422]