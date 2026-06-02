from __future__ import annotations

import argparse
import csv
import random
import shutil
from dataclasses import dataclass
from pathlib import Path


CLASS_NAMES = {
    0: "ok",
    1: "anomaly",
}


@dataclass(frozen=True)
class Sample:
    filename: str
    class_id: int

    @property
    def class_name(self) -> str:
        return CLASS_NAMES[self.class_id]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cria a estrutura YOLO de classificacao a partir de dataset/train.csv."
    )
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "dataset",
        help="Pasta raiz do dataset original.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "dataset" / "yolo_cls",
        help="Pasta de saida da estrutura YOLO.",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Proporcao de validacao por classe.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Semente para o split reproduzivel.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove a pasta de saida antes de recriar.",
    )
    return parser.parse_args()


def load_samples(train_csv: Path) -> list[Sample]:
    samples: list[Sample] = []
    with train_csv.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            filename = row["filename"].strip()
            class_id = int(row["anomaly"])
            if class_id not in CLASS_NAMES:
                raise ValueError(f"Classe desconhecida para {filename}: {class_id}")
            samples.append(Sample(filename=filename, class_id=class_id))
    return samples


def split_samples(samples: list[Sample], val_ratio: float, seed: int) -> tuple[list[Sample], list[Sample]]:
    grouped: dict[int, list[Sample]] = {class_id: [] for class_id in CLASS_NAMES}
    for sample in samples:
        grouped[sample.class_id].append(sample)

    random_generator = random.Random(seed)
    train_split: list[Sample] = []
    val_split: list[Sample] = []

    for class_id, class_samples in grouped.items():
        random_generator.shuffle(class_samples)
        val_count = max(1, round(len(class_samples) * val_ratio))
        val_split.extend(class_samples[:val_count])
        train_split.extend(class_samples[val_count:])

    random_generator.shuffle(train_split)
    random_generator.shuffle(val_split)
    return train_split, val_split


def clear_output(output_root: Path) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)


def ensure_layout(output_root: Path) -> None:
    for split_name in ("train", "val"):
        for class_name in CLASS_NAMES.values():
            (output_root / split_name / class_name).mkdir(parents=True, exist_ok=True)
    (output_root / "predict" / "test").mkdir(parents=True, exist_ok=True)


def copy_samples(samples: list[Sample], source_dir: Path, destination_root: Path, split_name: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for sample in samples:
        source_path = source_dir / sample.filename
        if not source_path.exists():
            raise FileNotFoundError(f"Arquivo nao encontrado: {source_path}")

        destination_path = destination_root / split_name / sample.class_name / sample.filename
        shutil.copy2(source_path, destination_path)
        records.append(
            {
                "filename": sample.filename,
                "class_id": str(sample.class_id),
                "class_name": sample.class_name,
                "split": split_name,
                "source_path": str(source_path),
                "target_path": str(destination_path),
            }
        )
    return records


def copy_test_images(test_dir: Path, destination_root: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    target_dir = destination_root / "predict" / "test"
    for image_path in sorted(test_dir.glob("*.png")):
        destination_path = target_dir / image_path.name
        shutil.copy2(image_path, destination_path)
        records.append(
            {
                "filename": image_path.name,
                "class_id": "",
                "class_name": "",
                "split": "predict/test",
                "source_path": str(image_path),
                "target_path": str(destination_path),
            }
        )
    return records


def write_manifest(records: list[dict[str, str]], output_root: Path) -> None:
    manifest_path = output_root / "splits.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["filename", "class_id", "class_name", "split", "source_path", "target_path"],
        )
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    args = parse_args()
    dataset_root: Path = args.dataset_root
    output_root: Path = args.output_root
    train_csv = dataset_root / "train.csv"
    train_dir = dataset_root / "train"
    test_dir = dataset_root / "test"

    if not train_csv.exists():
        raise FileNotFoundError(f"CSV de treino nao encontrado: {train_csv}")
    if not train_dir.exists():
        raise FileNotFoundError(f"Pasta de treino nao encontrada: {train_dir}")
    if not test_dir.exists():
        raise FileNotFoundError(f"Pasta de teste nao encontrada: {test_dir}")

    if args.overwrite:
        clear_output(output_root)

    ensure_layout(output_root)

    samples = load_samples(train_csv)
    train_split, val_split = split_samples(samples, args.val_ratio, args.seed)

    records: list[dict[str, str]] = []
    records.extend(copy_samples(train_split, train_dir, output_root, "train"))
    records.extend(copy_samples(val_split, train_dir, output_root, "val"))
    records.extend(copy_test_images(test_dir, output_root))
    write_manifest(records, output_root)

    print(f"Dataset YOLO criado em: {output_root}")
    print(f"Treino: {len(train_split)} imagens")
    print(f"Validacao: {len(val_split)} imagens")
    print(f"Teste: {len(list(test_dir.glob('*.png')))} imagens")


if __name__ == "__main__":
    main()
