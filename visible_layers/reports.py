"""Validation reports for imported Visible Layers PNG layer folders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from .layers import (
    MASK_EXTENSIONS,
    OVERDRAW_CATEGORIES,
    infer_category,
    normalize_layer_name,
    strip_order_prefix,
)


LOW_VISIBLE_COVERAGE_PERCENT = 0.1


def analyze_layer_folder(layers_dir: str | Path) -> dict[str, Any]:
    """Inspect a transparent PNG layer folder without modifying it."""
    layer_source_directory = Path(layers_dir)

    if not layer_source_directory.is_dir():
        raise FileNotFoundError(f"Layer directory not found: {layer_source_directory}")

    source_paths = sorted(
        path for path in layer_source_directory.iterdir() if path.suffix.lower() in MASK_EXTENSIONS
    )
    if not source_paths:
        raise ValueError(f"No PNG layers found in: {layer_source_directory}")

    canvas_size: tuple[int, int] | None = None
    layers = []
    findings = []

    for source_path in source_paths:
        name = normalize_layer_name(strip_order_prefix(source_path.stem))
        category = infer_category(name)
        layer_findings = []

        with Image.open(source_path) as image:
            layer_image = image.convert("RGBA")
            width, height = layer_image.size
            if canvas_size is None:
                canvas_size = layer_image.size

            if layer_image.size != canvas_size:
                layer_findings.append(
                    make_finding(
                        "error",
                        "SIZE_MISMATCH",
                        (
                            f"Layer {source_path.name} has size {width}x{height} "
                            f"but expected {canvas_size[0]}x{canvas_size[1]}."
                        ),
                        layer=source_path.name,
                    )
                )

            visible_pixels = count_visible_pixels(layer_image)
            total_pixels = width * height
            visible_percentage = (
                round((visible_pixels / total_pixels) * 100, 4) if total_pixels else 0.0
            )

        if visible_pixels == 0:
            layer_findings.append(
                make_finding(
                    "error",
                    "EMPTY_LAYER",
                    f"Layer {source_path.name} contains no visible pixels.",
                    layer=source_path.name,
                )
            )
        elif visible_percentage < LOW_VISIBLE_COVERAGE_PERCENT:
            layer_findings.append(
                make_finding(
                    "warning",
                    "LOW_ALPHA_COVERAGE",
                    f"Layer {source_path.name} has very low visible coverage.",
                    layer=source_path.name,
                )
            )

        if category == "part":
            layer_findings.append(
                make_finding(
                    "warning",
                    "UNKNOWN_CATEGORY",
                    f"Layer {source_path.name} could not be assigned to a known category.",
                    layer=source_path.name,
                )
            )

        requires_overdraw_review = category in OVERDRAW_CATEGORIES
        if requires_overdraw_review:
            layer_findings.append(
                make_finding(
                    "info",
                    "POSSIBLE_OVERDRAW_NEEDED",
                    f"Layer {source_path.name} may require hidden-region repair behind it.",
                    layer=source_path.name,
                )
            )

        findings.extend(layer_findings)
        layers.append(
            {
                "filename": source_path.name,
                "name": name,
                "category": category,
                "width": width,
                "height": height,
                "visible_pixel_count": visible_pixels,
                "visible_pixel_percentage": visible_percentage,
                "requires_overdraw_review": requires_overdraw_review,
                "status": layer_status(layer_findings),
                "findings": layer_findings,
            }
        )

    if canvas_size is None:
        raise ValueError(f"No PNG layers found in: {layer_source_directory}")

    report = {
        "format": "visible-layers.import-report",
        "version": 1,
        "input": str(layer_source_directory),
        "summary": {
            "total_layers": len(layers),
            "canvas_width": canvas_size[0],
            "canvas_height": canvas_size[1],
            "all_sizes_match": not any(finding["code"] == "SIZE_MISMATCH" for finding in findings),
            "preview_generated": False,
            "gap_report_generated": False,
            "info_count": 0,
            "warning_count": 0,
            "error_count": 0,
        },
        "layers": layers,
        "findings": findings,
    }
    refresh_import_report_counts(report)
    return report


def count_visible_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    return image.width * image.height - histogram[0]


def make_finding(severity: str, code: str, message: str, *, layer: str | None = None) -> dict[str, Any]:
    finding = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if layer:
        finding["layer"] = layer
    return finding


def add_import_report_finding(
    report: dict[str, Any],
    severity: str,
    code: str,
    message: str,
    *,
    layer: str | None = None,
) -> None:
    report["findings"].append(make_finding(severity, code, message, layer=layer))
    refresh_import_report_counts(report)


def refresh_import_report_counts(report: dict[str, Any]) -> None:
    findings = report.get("findings", [])
    summary = report["summary"]
    summary["info_count"] = sum(1 for finding in findings if finding["severity"] == "info")
    summary["warning_count"] = sum(1 for finding in findings if finding["severity"] == "warning")
    summary["error_count"] = sum(1 for finding in findings if finding["severity"] == "error")


def layer_status(findings: list[dict[str, Any]]) -> str:
    severities = {finding["severity"] for finding in findings}
    if "error" in severities:
        return "error"
    if "warning" in severities:
        return "warning"
    if "info" in severities:
        return "info"
    return "ok"


def render_import_report_summary(report: dict[str, Any]) -> str:
    summary = report["summary"]
    return "\n".join(
        [
            "Layer Import Report",
            f"Input: {report['input']}",
            f"Total layers: {summary['total_layers']}",
            f"Canvas size: {summary['canvas_width']}x{summary['canvas_height']}",
            f"All layers same size: {yes_no(summary['all_sizes_match'])}",
            f"Preview generated: {yes_no(summary['preview_generated'])}",
            f"Gap report generated: {yes_no(summary['gap_report_generated'])}",
            f"Warnings: {summary['warning_count']}",
            f"Errors: {summary['error_count']}",
        ]
    )


def write_import_report_markdown(report: dict[str, Any], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_import_report_markdown(report), encoding="utf-8")


def write_import_report_json(report: dict[str, Any], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def render_import_report_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Layer Import Report",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Input | {escape_markdown_cell(report['input'])} |",
        f"| Total layers | {summary['total_layers']} |",
        f"| Canvas size | {summary['canvas_width']}x{summary['canvas_height']} |",
        f"| All sizes match | {yes_no(summary['all_sizes_match'])} |",
        f"| Preview generated | {yes_no(summary['preview_generated'])} |",
        f"| Gap report generated | {yes_no(summary['gap_report_generated'])} |",
        f"| Info | {summary['info_count']} |",
        f"| Warnings | {summary['warning_count']} |",
        f"| Errors | {summary['error_count']} |",
        "",
        "## Layers",
        "",
        "| Layer | Category | Size | Visible % | Status |",
        "|---|---|---:|---:|---|",
    ]

    for layer in report["layers"]:
        lines.append(
            "| {filename} | {category} | {width}x{height} | {visible:.4f}% | {status} |".format(
                filename=escape_markdown_cell(layer["filename"]),
                category=escape_markdown_cell(layer["category"]),
                width=layer["width"],
                height=layer["height"],
                visible=layer["visible_pixel_percentage"],
                status=layer["status"].upper(),
            )
        )

    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )
    for severity in ("error", "warning", "info"):
        title = severity.capitalize() + "s"
        lines.extend([f"### {title}", ""])
        severity_findings = [
            finding for finding in report["findings"] if finding["severity"] == severity
        ]
        if severity_findings:
            for finding in severity_findings:
                lines.append(
                    f"- {finding['code']}: {escape_markdown_text(finding['message'])}"
                )
        else:
            lines.append(f"No {severity} findings.")
        lines.append("")

    lines.extend(
        [
            "## Suggested Next Steps",
            "",
        ]
    )
    lines.extend(suggest_next_steps(report))
    lines.append("")
    return "\n".join(lines)


def suggest_next_steps(report: dict[str, Any]) -> list[str]:
    summary = report["summary"]
    codes = {finding["code"] for finding in report["findings"]}
    steps = []
    if summary["error_count"]:
        steps.append("- Fix error findings before using these layers for preview or rigging prep.")
    if "UNKNOWN_CATEGORY" in codes:
        steps.append("- Rename unknown layers with clearer part names such as body, face, hair, or arm.")
    if "POSSIBLE_OVERDRAW_NEEDED" in codes:
        steps.append("- Review possible overdraw layers for hidden-region repair needs.")
    if not steps:
        steps.append("- Inspect the generated preview and gap report before continuing.")
    return steps


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def escape_markdown_text(value: str) -> str:
    return value.replace("\n", " ")
