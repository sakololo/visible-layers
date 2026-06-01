# The Occlusion Problem

In a finished character illustration, foreground parts hide background structure.

Examples:

- bangs hide the forehead
- arms hide the torso
- glasses or eye patches hide the face
- clothing hides body lines
- props hide hands or sleeves

For a static image, these hidden regions do not matter. For rigging, they matter a lot. When a foreground part moves, the area behind it may become visible.

## Why This Is Hard

A flat image only stores the final visible pixels. If the forehead is covered by hair, the original forehead pixels are not present in the file. Newer layer-decomposition and inpainting systems can estimate these regions, but the result still needs inspection because the correct answer depends on art style, intended motion, and rigging needs.

That means layer extraction has two separate problems:

1. Separate visible parts into transparent layers.
2. Reconstruct or repair regions that were hidden in the original image.

Visible Layers treats these as separate steps. The first MVP handles extraction, metadata, previewing, and gap detection. Later versions can import decomposition outputs and add inpainting-assisted repair.

## What Gap Detection Does

`detect-gaps` composites all exported layers, finds the visible character bounding box, and marks transparent or low-alpha pixels inside that box.

This does not prove that every marked pixel is a real defect. It is a debug aid. The report helps creators find regions that may need manual repair, mask editing, or inpainting.

## Why Human Inspection Stays Important

Hidden-region reconstruction is not just technical. It is also artistic. The correct solution depends on anatomy, style, line weight, clothing design, and how the character will move.

For that reason, the project favors inspectable intermediate outputs over one-click automation.
