from fastapi import FastAPI

app = FastAPI(
    title="AI Processing API",
    description="Audio transcription and document extraction API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "AI Processing API is running"}