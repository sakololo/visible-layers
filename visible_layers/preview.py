"""Preview compositing for exported Visible Layers metadata."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .metadata import read_metadata


def compose_preview(metadata_path: str | Path) -> Image.Image:
    path = Path(metadata_path)
    data = read_metadata(path)
    width = data["canvas"]["width"]
    height = data["canvas"]["height"]

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for layer in sorted(data["layers"], key=lambda item: item["z_index"]):
        layer_path = path.parent / layer["file"]
        if not layer_path.is_file():
            raise FileNotFoundError(f"Layer image not found: {layer_path}")
        layer_image = Image.open(layer_path).convert("RGBA")
        if layer_image.size != canvas.size:
            raise ValueError(
                f"Layer size {layer_image.size} does not match canvas size {canvas.size}: {layer_path}"
            )
        canvas = Image.alpha_composite(canvas, layer_image)

    return canvas


def save_preview(metadata_path: str | Path, output_path: str | Path) -> None:
    preview = compose_preview(metadata_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    preview.save(destination)
