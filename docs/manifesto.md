# Manifesto: Why Visible Layers Exists

AI image generation has become very good at producing finished images. Recent layer-decomposition tools are also becoming much better at recovering transparent layers from anime-style images.

But finished images are not always useful images.

For animation, rigging, editing, and game production, creators often need structure: layers, masks, hidden regions, and editable parts. A flat illustration can look complete while being structurally incomplete.

Visible Layers starts from a simple observation:

> AI can draw the final picture, but the final picture does not contain every structure needed for motion.

If a workflow is optimized for visible pixels alone, hidden regions are easy to lose. The forehead behind bangs, the torso behind an arm, the face behind an accessory, or the continuation of a hidden outline may be missing, noisy, or unsuitable for motion.

Human artists work differently when they prepare assets for motion. They separate parts, preserve bases, overdraw hidden regions, and organize layers. These constraints are not only limitations. They create useful structure.

This project explores whether similar constraints can make AI-assisted and layer-decomposition workflows more useful:

- What if the output must be inspectable?
- What if each layer has metadata?
- What if missing regions are detected before rigging?
- What if inpainting is guided by masks, layer categories, and reports?
- What if the final output is not only beautiful, but editable?

The goal is not to imitate human process for nostalgia. The goal is to discover which constraints make generated or decomposed layers more controllable, repairable, and reusable.
