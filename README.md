# Visible Layers

Visible Layers is an open-source pipeline for turning flat character illustrations and automatic layer-decomposition outputs into inspectable assets for 2D avatar and rigging workflows.

The project starts with a practical MVP: manual masks in, transparent PNG layers and metadata out. This keeps the first version useful while leaving room for future imports from tools such as anime layer decomposition models, PSD exporters, and inpainting workflows.

## Motivation

Modern image generation models and recent layer-decomposition tools can produce or recover increasingly useful layers. However, Live2D-style workflows still need production-oriented checks that are not solved by decomposition alone. A creator often needs:

- separated parts such as hair, face, arms, body, clothing, and accessories
- predictable layer ordering
- transparent PNG assets
- overdraw behind foreground parts
- a way to inspect gaps before rigging

A flat image can look complete while being structurally incomplete. An automatically decomposed image can also still need inspection, cleanup, naming, overdraw repair, and rigging-aware organization. Visible Layers focuses on that gap.

## Prior Art And Positioning

Research and tools such as LayerDiffuse, See-through, and Live2D's own material-separation tooling show that transparent layer generation, anime layer decomposition, occluded-region inpainting, and assisted material separation are progressing quickly.

Visible Layers is not trying to deny or replace that work. The project is positioned as the bridge after decomposition:

- import or create layers
- normalize names, categories, and metadata
- preview and compare layer stacks
- detect likely gaps and missing overdraw
- prepare repair masks and reports
- keep the human review loop explicit

In other words, the project is less "one-click Image-to-Live2D" and more "inspectable preparation tooling between automatic decomposition and production rigging."

## Current MVP

The first version provides:

- `split`: create transparent PNG layers from a source image and grayscale masks
- `import-layers`: import existing transparent PNG layers from external tools or manual workflows
- `preview`: composite exported layers in `z_index` order
- `detect-gaps`: find transparent regions inside the composited character bounding box
- `demo`: generate a complete synthetic sample workflow
- `character.json`: a simple metadata format for layer assets
- tests for metadata, layer extraction, preview compositing, gap detection, and demo generation

This is intentionally human-in-the-loop. The goal is not to pretend the hard artistic parts are solved. The goal is to make each step visible, testable, and replaceable.

## Quick Start

Install the project locally:

```bash
python -m pip install -e .
```

Try the built-in demo:

```bash
visible-layers demo --output demo-output
```

The demo creates a synthetic flat character image, grayscale masks, exported layers, a recomposed preview, and a gap report.

Import existing layers from another tool or manual workflow:

```bash
visible-layers import-layers --layers path/to/png-layers --output output
```

This copies the PNG layers into `output/layers/`, writes `output/character.json`, creates `output/preview.png`, and runs gap detection into `output/gaps/`.

Prepare:

```text
input.png
masks/
  body_base.png
  face_base.png
  front_hair.png
  left_arm.png
```

Each mask should be a grayscale PNG with the same size as `input.png`. White pixels become visible in the exported layer. Black pixels become transparent.

Create layers:

```bash
visible-layers split --input input.png --masks masks --output output
```

Create a recomposed preview:

```bash
visible-layers preview --metadata output/character.json --output output/preview.png
```

Detect likely missing regions:

```bash
visible-layers detect-gaps --metadata output/character.json --output output/gaps
```

## Output

```text
output/
  character.json
  layers/
    00_body_base.png
    01_face_base.png
    02_front_hair.png
    03_left_arm.png
  gaps/
    transparent_gaps.png
    report.md
```

Example metadata:

```json
{
  "format": "visible-layers.character",
  "version": 1,
  "canvas": {
    "width": 2048,
    "height": 2048
  },
  "layers": [
    {
      "name": "front_hair",
      "file": "layers/02_front_hair.png",
      "z_index": 20,
      "category": "hair",
      "width": 2048,
      "height": 2048,
      "requires_overdraw": true
    }
  ]
}
```

## Project Direction

The long-term research question is:

> Can constraints, masks, staged generation, and difference extraction make AI-generated illustrations more useful for riggable layered assets?

Future versions may add:

- richer importers for PSD-like exports from decomposition tools
- segmentation-assisted mask creation
- inpainting prompt generation for hidden regions
- before and after comparison tools
- PSD export experiments
- Live2D-friendly naming presets
- small benchmark examples for occlusion-aware asset preparation

## Non-Goals

Visible Layers does not aim to fully replace professional Live2D artists or riggers.

The first goal is preparation support:

- layer extraction
- metadata
- preview inspection
- gap detection
- documentation
- repeatable workflows

Rigging, final art direction, and quality control remain human-centered.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

Run tests:

```bash
python -m unittest discover -s tests
```

Run the CLI without installing:

```bash
python -m visible_layers.cli split --input input.png --masks masks --output output
```

Import existing layers without installing:

```bash
python -m visible_layers.cli import-layers --layers path/to/png-layers --output output
```

Generate the demo without installing:

```bash
python -m visible_layers.cli demo --output demo-output
```

## License

MIT License.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
