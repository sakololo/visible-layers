"""Command line interface for Visible Layers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .demo import create_demo
from .gaps import detect_gaps
from .layers import split_layers
from .preview import save_preview


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="visible-layers",
        description="Prepare flat character illustrations as inspectable layered assets.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Create transparent layers from masks.")
    split_parser.add_argument("--input", required=True, help="Path to a PNG input image.")
    split_parser.add_argument("--masks", required=True, help="Directory containing grayscale PNG masks.")
    split_parser.add_argument("--output", required=True, help="Output directory.")

    preview_parser = subparsers.add_parser("preview", help="Composite exported layers in z-index order.")
    preview_parser.add_argument("--metadata", required=True, help="Path to character.json.")
    preview_parser.add_argument("--output", required=True, help="Path for preview.png.")

    gaps_parser = subparsers.add_parser("detect-gaps", help="Find transparent regions inside the character bbox.")
    gaps_parser.add_argument("--metadata", required=True, help="Path to character.json.")
    gaps_parser.add_argument("--output", required=True, help="Directory for gap masks and report.")
    gaps_parser.add_argument(
        "--alpha-threshold",
        type=int,
        default=8,
        help="Pixels at or below this alpha are treated as transparent.",
    )

    demo_parser = subparsers.add_parser("demo", help="Generate a complete synthetic demo workflow.")
    demo_parser.add_argument("--output", required=True, help="Directory for generated demo files.")
    demo_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the output directory if it already contains files.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "split":
            metadata = split_layers(args.input, args.masks, args.output)
            print(f"Wrote {len(metadata['layers'])} layers to {Path(args.output) / 'layers'}")
            print(f"Wrote metadata to {Path(args.output) / 'character.json'}")
            return 0
        if args.command == "preview":
            save_preview(args.metadata, args.output)
            print(f"Wrote preview to {args.output}")
            return 0
        if args.command == "detect-gaps":
            report = detect_gaps(args.metadata, args.output, alpha_threshold=args.alpha_threshold)
            print(f"Wrote gap mask to {report['mask']}")
            print(f"Wrote report to {report['report']}")
            return 0
        if args.command == "demo":
            result = create_demo(args.output, overwrite=args.overwrite)
            print(f"Wrote demo input to {result['input']}")
            print(f"Wrote {result['layer_count']} layers to {result['layers']}")
            print(f"Wrote preview to {result['preview']}")
            print(f"Wrote gap report to {result['gap_report']}")
            return 0
    except Exception as exc:  # pragma: no cover - exercised through CLI usage.
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
