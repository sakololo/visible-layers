# Initial Layer Taxonomy

The MVP uses a small taxonomy so exported layers can be inspected and processed consistently.

## Categories

- `base`: main body or base surface
- `body`: torso, skin, body shape
- `face`: face, eyes, mouth, brows, nose
- `hair`: front hair, side hair, back hair, bangs
- `arm`: arms and hands
- `clothing`: shirts, jackets, pants, skirts, dresses
- `accessory`: hats, glasses, ribbons, props, eye patches
- `part`: fallback for unknown parts

## Suggested Z Order

This is only a starting point:

```text
00 body_base
10 face_base
20 back_hair
30 clothing
40 arms
50 face_parts
60 front_hair
70 accessories
```

The MVP assigns `z_index` from mask file order. Creators can rename masks with numeric prefixes to control ordering.

## Overdraw

Some categories often need hidden-region repair:

- hair
- arms
- body
- clothing
- accessories
- base

The metadata field `requires_overdraw` marks layers that commonly need inspection.
