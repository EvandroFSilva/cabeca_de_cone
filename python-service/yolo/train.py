from __future__ import annotations

import os
import argparse
from pathlib import Path

os.environ["YOLO_CONFIG_DIR"] = str(Path(__file__).resolve().parents[1] / ".yolo")

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Treina o modelo YOLO para classificacao binaria.")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "dataset" / "yolo_cls",
        help="Pasta raiz do dataset de classificacao.",
    )
    parser.add_argument(
        "--weights",
        type=str,
        default="yolo11n-cls.pt",
        help="Checkpoint base. Use yolo11n-cls.pt para classificacao.",
    )
    parser.add_argument("--imgsz", type=int, default=224, help="Tamanho da imagem.")
    parser.add_argument("--epochs", type=int, default=50, help="Numero de epocas.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument("--device", type=str, default="0", help="Dispositivo de treino.")
    parser.add_argument("--workers", type=int, default=4, help="Workers do dataloader.")
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parent / "runs")
    parser.add_argument("--name", type=str, default="anomaly_yolo11n_cls")
    parser.add_argument("--patience", type=int, default=20, help="Early stopping.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    model = YOLO(args.weights)
    model.train(
        data=str(args.data),
        imgsz=args.imgsz,
        epochs=args.epochs,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        project=str(args.project),
        name=args.name,
        patience=args.patience,
    )


if __name__ == "__main__":
    main()
