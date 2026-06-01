"""Transparent gap detection for composited layer previews."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .preview import compose_preview


def detect_gaps(
    metadata_path: str | Path,
    output_dir: str | Path,
    *,
    alpha_threshold: int = 8,
) -> dict:
    if alpha_threshold < 0 or alpha_threshold > 255:
        raise ValueError("alpha_threshold must be between 0 and 255")

    composed = compose_preview(metadata_path)
    alpha = composed.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > alpha_threshold else 0).getbbox()

    output_directory = Path(output_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    gap_mask = Image.new("L", composed.size, 0)
    gap_pixels = 0

    if bbox:
        alpha_pixels = alpha.load()
        gap_pixels_map = gap_mask.load()
        left, top, right, bottom = bbox
        for y in range(top, bottom):
            for x in range(left, right):
                if alpha_pixels[x, y] <= alpha_threshold:
                    gap_pixels_map[x, y] = 255
                    gap_pixels += 1

    mask_path = output_directory / "transparent_gaps.png"
    report_path = output_directory / "report.md"
    gap_mask.save(mask_path)

    report = {
        "bbox": bbox,
        "gap_pixels": gap_pixels,
        "mask": str(mask_path),
        "report": str(report_path),
    }
    write_gap_report(report, report_path, alpha_threshold)
    return report


def write_gap_report(report: dict, report_path: str | Path, alpha_threshold: int) -> None:
    bbox = report["bbox"]
    bbox_text = "none" if bbox is None else f"{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}"
    text = "\n".join(
        [
            "# Gap Detection Report",
            "",
            f"- Alpha threshold: {alpha_threshold}",
            f"- Character bounding box: {bbox_text}",
            f"- Transparent or low-alpha pixels inside bounding box: {report['gap_pixels']}",
            f"- Debug mask: {Path(report['mask']).name}",
            "",
            "White pixels in the debug mask mark transparent regions inside the composited character bounding box.",
            "These regions are candidates for manual inspection or inpainting-assisted overdraw.",
            "",
        ]
    )
    Path(report_path).write_text(text, encoding="utf-8")
