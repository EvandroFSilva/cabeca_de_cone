from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Detector de Falhas em Parafusos")


class DetectionRequest(BaseModel):
    image_url: str | None = None
    screw_id: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
def detect_failure(request: DetectionRequest):
    return {
        "screw_id": request.screw_id,
        "has_failure": False,
        "confidence": 0.0,
        "failure_type": None,
    }
