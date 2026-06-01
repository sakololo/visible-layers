# Initial Issues

These can be copied into GitHub issues after the repository is created.

## Define Initial Layer Taxonomy

We need a practical first taxonomy for character illustration layers.

Candidate categories:

- body
- face
- hair
- arm
- clothing
- accessory
- part

The goal is not to cover every possible Live2D model. The goal is a useful MVP vocabulary for metadata, validation, and documentation.

## Add a Small Example Workflow

Create one simple example showing:

1. input image
2. masks
3. exported layers
4. `character.json`
5. recomposed preview
6. gap report

The image must be self-created or permissively licensed.

## Improve Gap Detection

The current gap detector marks transparent pixels inside the composited bounding box. This is useful but rough.

Future work:

- ignore intentional internal transparent regions
- handle outline-only art better
- report connected components
- rank gaps by size

## Design Inpainting Prompt Templates

Create prompt templates for hidden-region repair.

Examples:

- forehead behind bangs
- torso behind arms
- face behind glasses
- clothing behind hands

The output should help creators send better masks and prompts to external inpainting tools.

## Explore PSD Export

Investigate PSD export options for Python.

Acceptance criteria:

- preserve layer names
- preserve canvas size
- preserve layer order
- keep transparent PNG layer data intact
