# Changelog

All notable changes to Visible Layers will be documented in this file.

The project follows a simple semantic versioning style while it is early-stage.

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
