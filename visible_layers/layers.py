"""Layer extraction from a flat input image and grayscale masks."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageChops

from .metadata import make_character_metadata, make_layer_record, write_metadata


MASK_EXTENSIONS = {".png"}
OVERDRAW_CATEGORIES = {"hair", "arm", "body", "clothing", "accessory", "base"}


def split_layers(input_path: str | Path, masks_dir: str | Path, output_dir: str | Path) -> dict:
    input_image_path = Path(input_path)
    mask_directory = Path(masks_dir)
    output_directory = Path(output_dir)

    if not input_image_path.is_file():
        raise FileNotFoundError(f"Input image not found: {input_image_path}")
    if not mask_directory.is_dir():
        raise FileNotFoundError(f"Mask directory not found: {mask_directory}")

    mask_paths = sorted(
        path for path in mask_directory.iterdir() if path.suffix.lower() in MASK_EXTENSIONS
    )
    if not mask_paths:
        raise ValueError(f"No PNG masks found in: {mask_directory}")

    source_image = Image.open(input_image_path).convert("RGBA")
    width, height = source_image.size

    layers_directory = output_directory / "layers"
    layers_directory.mkdir(parents=True, exist_ok=True)

    layer_records = []
    for index, mask_path in enumerate(mask_paths):
        name = normalize_layer_name(mask_path.stem)
        category = infer_category(name)
        layer_filename = f"{index:02d}_{name}.png"
        layer_path = layers_directory / layer_filename

        extract_layer(source_image, mask_path, layer_path)

        layer_records.append(
            make_layer_record(
                name=name,
                file=f"layers/{layer_filename}",
                z_index=index * 10,
                category=category,
                width=width,
                height=height,
                requires_overdraw=category in OVERDRAW_CATEGORIES,
            )
        )

    metadata = make_character_metadata(
        width,
        height,
        layer_records,
        source=str(input_image_path),
    )
    write_metadata(metadata, output_directory / "character.json")
    return metadata


def extract_layer(source_image: Image.Image, mask_path: str | Path, output_path: str | Path) -> None:
    mask = Image.open(mask_path).convert("L")
    if mask.size != source_image.size:
        raise ValueError(
            f"Mask size {mask.size} does not match input image size {source_image.size}: {mask_path}"
        )

    red, green, blue, alpha = source_image.split()
    masked_alpha = ImageChops.multiply(alpha, mask)
    layer = Image.merge("RGBA", (red, green, blue, masked_alpha))

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    layer.save(destination)


def normalize_layer_name(name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "_", name.strip().lower())
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "layer"


def infer_category(name: str) -> str:
    lowered = name.lower()
    category_keywords = {
        "hair": ("hair", "bang", "fringe"),
        "face": ("face", "head", "eye", "mouth", "nose", "brow"),
        "arm": ("arm", "hand"),
        "body": ("body", "torso", "base", "skin"),
        "clothing": ("shirt", "cloth", "dress", "pants", "skirt", "jacket"),
        "accessory": ("accessory", "hat", "ribbon", "glasses", "patch", "prop"),
    }
    for category, keywords in category_keywords.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "part"
