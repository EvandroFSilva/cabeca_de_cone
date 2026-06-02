from __future__ import annotations

import os
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

os.environ["YOLO_CONFIG_DIR"] = str(Path(__file__).resolve().parents[1] / ".yolo")

from PIL import Image
from ultralytics import YOLO

DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "anomaly_yolo11n_cls6_1024" / "best.pt"


def get_model_path() -> Path:
    model_path = Path(os.getenv("YOLO_MODEL_PATH", DEFAULT_MODEL_PATH))
    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo treinado nao encontrado em {model_path}. "
            "Copie o best.pt do treino para python-service/models/anomaly_yolo11n_cls6_1024/."
        )
    return model_path


@lru_cache(maxsize=1)
def get_model() -> YOLO:
    return YOLO(str(get_model_path()))


def load_image(image_source: str) -> Image.Image:
    parsed = urlparse(image_source)
    if parsed.scheme in {"http", "https"}:
        with urlopen(image_source) as response:
            image_bytes = response.read()
        return Image.open(BytesIO(image_bytes)).convert("RGB")

    image_path = Path(image_source)
    if not image_path.exists():
        raise FileNotFoundError(f"Imagem nao encontrada: {image_source}")
    return Image.open(image_path).convert("RGB")


def predict_image(image_source: str) -> dict[str, object]:
    image = load_image(image_source)
    model = get_model()
    result = model.predict(source=image, verbose=False)[0]

    class_index = int(result.probs.top1)
    class_name = str(result.names[class_index])
    confidence = float(result.probs.top1conf)
    has_failure = class_name != "ok"

    return {
        "predicted_class": class_name,
        "confidence": confidence,
        "has_failure": has_failure,
        "failure_type": class_name if has_failure else None,
        "model_path": str(get_model_path()),
    }
