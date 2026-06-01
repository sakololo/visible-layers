# Human-in-the-Loop Workflow

Visible Layers is designed around inspectable steps.

## Phase 1: Manual Mask MVP

1. Prepare a finished character image.
2. Create masks for major parts.
3. Run `visible-layers split`.
4. Inspect `output/layers`.
5. Run `visible-layers preview`.
6. Check whether the recomposed image still matches the source.
7. Run `visible-layers detect-gaps`.
8. Repair masks or hidden regions as needed.

This workflow is simple, but it gives the project a solid base. AI-generated masks, layer-decomposition imports, inpainting, and PSD export can be added later without changing the core idea.

## Phase 2: Assisted Repair

Future versions can add helper outputs for inpainting tools and decomposition outputs:

- masks for missing forehead, torso, clothing, or face regions
- prompts based on layer category
- before and after comparisons
- overdraw quality reports
- imports from layer folders or PSD-style exports

The creator still decides whether the repair is acceptable.

## Phase 3: Rigging-Oriented Export

Once extraction and repair are stable, the project can add:

- Live2D-friendly naming presets
- PSD export experiments
- template layer taxonomies
- asset validation reports

The guiding principle is the same: make each stage visible before asking creators to trust it.
