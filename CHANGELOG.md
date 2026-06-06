# Changelog

All notable changes to Visible Layers will be documented in this file.

The project follows a simple semantic versioning style while it is early-stage.

## v0.1.1 - Import Validation Reports

Adds validation reports for imported PNG layer folders.

### Added

- `import-layers` now writes a human-readable Markdown report to `import-report.md`.
- `import-layers` now writes a machine-readable JSON report to `import-report.json`.
- Added import checks for empty layers, mismatched canvas sizes, very low visible pixel coverage, unknown layer categories, and possible hidden-region repair needs.
- Added `--report-md` and `--report-json` options for custom report output paths.
- Added tests for import report analysis, Markdown output, JSON output, and invalid import handling.

### Changed

- README now documents the import validation report workflow and expected output files.
- `import-layers` now stops before metadata export when validation finds structural errors, while still writing the report files for inspection.

### Validation

- `python -m unittest discover -s tests`
- 18 tests passing locally

## v0.1.0 - Manual Mask And Layer Import MVP

Initial public MVP.

### Added

- `split` command for creating transparent PNG layers from a source image and grayscale masks.
- `import-layers` command for importing existing transparent PNG layer folders.
- `preview` command for compositing layers in `z_index` order.
- `detect-gaps` command for finding transparent regions inside a composited character bounding box.
- `demo` command for generating a complete synthetic workflow without external artwork.
- `character.json` metadata format with canvas and layer records.
- Layer category inference and `requires_overdraw` metadata.
- Gap detection report and debug mask output.
- Unit tests for metadata, layer extraction, layer import, preview compositing, gap detection, CLI behavior, and demo generation.
- Documentation for project positioning, occlusion problems, human-in-the-loop workflows, layer taxonomy, roadmap, and application notes.

### Notes

This release is intentionally human-in-the-loop. It does not attempt to replace artists, riggers, or existing layer-decomposition research. It provides inspectable preparation tooling that can sit between automatic decomposition and production rigging workflows.

### Validation

- `python -m unittest discover -s tests`
- 14 tests passing locally
