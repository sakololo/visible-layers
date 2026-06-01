# Roadmap

## Phase 0: Repository Foundation

- [x] Create package structure
- [x] Add CLI skeleton
- [x] Add metadata format
- [x] Add unit tests
- [x] Add docs and application materials
- [x] Add built-in synthetic demo command

## Phase 1: MVP

- [x] Load a flat character image
- [x] Load manual grayscale masks
- [x] Export transparent PNG layers
- [x] Generate `character.json`
- [x] Composite layers into a preview image
- [x] Detect transparent gaps inside the character bounding box
- [x] Generate a synthetic demo workflow without external artwork
- [ ] Add a small permissively licensed example image
- [ ] Add visual documentation with screenshots

## Phase 2: Occlusion Recovery

- [ ] Generate inpainting masks for likely hidden regions
- [ ] Generate category-specific inpainting prompts
- [ ] Add before and after comparison views
- [ ] Add overdraw quality checks

## Phase 3: Decomposition Tool Interop

- [ ] Import layer folders from external decomposition tools
- [ ] Explore PSD import for layer names, size, and order
- [ ] Normalize categories and `z_index` from imported layers
- [ ] Generate reports comparing imported layers with expected rigging-prep metadata

## Phase 4: Assisted Masking

- [ ] Add segmentation-assisted mask import
- [ ] Support common segmentation tool outputs
- [ ] Add mask cleanup helpers
- [ ] Add interactive review ideas

## Phase 5: Rigging-Oriented Output

- [ ] Add Live2D-friendly naming presets
- [ ] Add PSD export experiments
- [ ] Add chibi, bust-up, and full-body templates
- [ ] Add validation reports for layer order and missing regions

## Phase 6: Evaluation

- [ ] Create small benchmark examples
- [ ] Measure manual editing time reduction
- [ ] Evaluate hidden-region repair quality
- [ ] Publish case studies and workflow notes
