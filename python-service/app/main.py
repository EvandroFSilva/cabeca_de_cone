from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.model_loader import get_model, predict_image


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_model()
    yield


app = FastAPI(title="Detector de Falhas em Parafusos", lifespan=lifespan)


class DetectionRequest(BaseModel):
    image_url: str | None = None
    screw_id: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
def detect_failure(request: DetectionRequest):
    if not request.image_url:
        raise HTTPException(status_code=400, detail="image_url e obrigatorio.")

    prediction = predict_image(request.image_url)
    return {
        "screw_id": request.screw_id,
        "has_failure": prediction["has_failure"],
        "confidence": prediction["confidence"],
        "failure_type": prediction["failure_type"],
        "predicted_class": prediction["predicted_class"],
        "model_path": prediction["model_path"],
    }
