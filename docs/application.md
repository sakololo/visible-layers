# Application Notes

Use these snippets when creating the public repository and applying for open-source support. Replace placeholders before submitting.

## Project Name

Visible Layers

## Short Description

An open-source bridge between anime layer decomposition and production-oriented 2D rigging preparation.

## GitHub About

Open-source tooling for inspecting, organizing, and repairing layered character assets before Live2D-style rigging.

## Role

I am the founder and primary maintainer of Visible Layers. I define the roadmap, maintain the repository, write documentation, implement the CLI and core pipeline, triage issues, review pull requests, and manage releases.

## 500-Character Application Text

I aim to build and maintain Visible Layers, an exploratory OSS pipeline that bridges automatic anime layer decomposition and production-oriented 2D rigging preparation. Recent tools can decompose flat images into layers, but Live2D-style workflows still need inspection, hidden-region repair, metadata, naming, and human-in-the-loop correction. I would use Codex for CLI development, tests, docs, examples, issue triage, and release automation.

## Longer Justification

Recent research and tools are making anime layer decomposition, transparent layer generation, and occluded-region inpainting increasingly practical. However, automatic decomposition is not the same as production-ready Live2D preparation. Creators still need artistically meaningful part separation, naming, metadata, layer-order checks, hidden-region repair, preview comparison, and human quality control.

Visible Layers is an early-stage OSS project focused on that gap. It provides an inspectable workflow for layer extraction, metadata export, previewing, gap detection, a built-in synthetic demo, and future imports from decomposition tools or PSD-like exports. The project does not claim to replace artists or riggers. It aims to reduce repetitive preparation work and make each intermediate result easier to inspect, repair, and document.

## Initial GitHub Issues

1. Define the first layer taxonomy for character illustrations.
2. Add a small permissively licensed example workflow.
3. Improve gap detection for thin outlines and partial transparency.
4. Design inpainting prompt templates for hidden-region repair.
5. Add import support for layer folders from decomposition tools.
6. Explore PSD import and export options.
7. Add Live2D-friendly naming presets.
8. Document a full human-in-the-loop workflow.
