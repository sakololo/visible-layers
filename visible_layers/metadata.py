"""Metadata helpers for Visible Layers character exports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_LAYER_FIELDS = {
    "name": str,
    "file": str,
    "z_index": int,
    "category": str,
    "width": int,
    "height": int,
    "requires_overdraw": bool,
}


def make_character_metadata(
    width: int,
    height: int,
    layers: list[dict[str, Any]],
    *,
    source: str | None = None,
) -> dict[str, Any]:
    data: dict[str, Any] = {
        "format": "visible-layers.character",
        "version": 1,
        "canvas": {"width": width, "height": height},
        "layers": layers,
    }
    if source:
        data["source"] = source
    validate_character_metadata(data)
    return data


def make_layer_record(
    *,
    name: str,
    file: str,
    z_index: int,
    category: str,
    width: int,
    height: int,
    requires_overdraw: bool,
) -> dict[str, Any]:
    return {
        "name": name,
        "file": file.replace("\\", "/"),
        "z_index": z_index,
        "category": category,
        "width": width,
        "height": height,
        "requires_overdraw": requires_overdraw,
    }


def validate_character_metadata(data: dict[str, Any]) -> None:
    errors = list(iter_metadata_errors(data))
    if errors:
        raise ValueError("Invalid character metadata: " + "; ".join(errors))


def iter_metadata_errors(data: dict[str, Any]):
    canvas = data.get("canvas")
    if not isinstance(canvas, dict):
        yield "canvas must be an object"
        return

    for key in ("width", "height"):
        value = canvas.get(key)
        if not isinstance(value, int) or value <= 0:
            yield f"canvas.{key} must be a positive integer"

    layers = data.get("layers")
    if not isinstance(layers, list):
        yield "layers must be a list"
        return

    for index, layer in enumerate(layers):
        if not isinstance(layer, dict):
            yield f"layers[{index}] must be an object"
            continue
        for field, expected_type in REQUIRED_LAYER_FIELDS.items():
            value = layer.get(field)
            if not isinstance(value, expected_type):
                yield f"layers[{index}].{field} must be {expected_type.__name__}"
        for field in ("width", "height"):
            value = layer.get(field)
            if isinstance(value, int) and value <= 0:
                yield f"layers[{index}].{field} must be positive"


def read_metadata(path: str | Path) -> dict[str, Any]:
    metadata_path = Path(path)
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    validate_character_metadata(data)
    return data


def write_metadata(data: dict[str, Any], path: str | Path) -> None:
    validate_character_metadata(data)
    metadata_path = Path(path)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
