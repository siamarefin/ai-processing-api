from fastapi import FastAPI

from app.api.audio import router as audio_router
from app.api.document import router as document_router


app = FastAPI(
    title="AI Processing API",
    description="Audio transcription and document extraction API",
    version="1.0.0",
)


app.include_router(audio_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {"message": "AI Processing API is running"}