from __future__ import annotations

import os
import argparse
import csv
from pathlib import Path

os.environ["YOLO_CONFIG_DIR"] = str(Path(__file__).resolve().parents[1] / ".yolo")

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera o CSV de previsao para as imagens de teste.")
    parser.add_argument(
        "--weights",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "models" / "anomaly_yolo11n_cls6_1024" / "best.pt",
        help="Pesos treinados.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "dataset" / "yolo_cls" / "predict" / "test",
        help="Pasta com as imagens de teste.",
    )
    parser.add_argument(
        "--sample-submit",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "dataset" / "sample_submit.csv",
        help="Arquivo modelo para manter a ordem do envio.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "dataset" / "predictions.csv",
        help="CSV de saida.",
    )
    return parser.parse_args()


def load_order(sample_submit: Path, source: Path) -> list[str]:
    if sample_submit.exists():
        with sample_submit.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            return [row["id"].strip() for row in reader]
    return [path.name for path in sorted(source.glob("*.png"))]


def main() -> None:
    args = parse_args()

    if not args.weights.exists():
        raise FileNotFoundError(f"Pesos nao encontrados: {args.weights}")
    if not args.source.exists():
        raise FileNotFoundError(f"Pasta de teste nao encontrada: {args.source}")

    model = YOLO(str(args.weights))
    order = load_order(args.sample_submit, args.source)

    predictions: dict[str, int] = {}
    results = model.predict(source=str(args.source), verbose=False)
    for result in results:
        image_name = Path(result.path).name
        class_index = int(result.probs.top1)
        class_name = result.names[class_index]
        predictions[image_name] = 1 if class_name == "anomaly" else 0

    missing = [filename for filename in order if filename not in predictions]
    if missing:
        raise RuntimeError(f"Predicoes ausentes para: {missing[:5]}")

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "Predicted"])
        for filename in order:
            writer.writerow([filename, predictions[filename]])

    print(f"CSV gerado em: {args.output}")


if __name__ == "__main__":
    main()
