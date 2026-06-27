# mk0.7.3 Changelog

## Implemented

- Updated current revision label to `mk0.7.3`.
- Moved corner blocks out of the frame mid-plane by using `BOTTOM_CORNER_BLOCK_Z` and `TOP_CORNER_BLOCK_Z`.
- Split top/bottom frame clamping logic so the top frame has the nut seat on the outer top face.
- Added extra rod length allowance and printable M5 rod cap placeholders.
- Made corner-block side service holes available on all four side faces.
- Added sectional side-panel mount rails so panels have a real screw target in rough assembly.
- Added rough rail end mounts and tray support ledges for the module stack.
- Added foot sockets to the assembly and increased socket depth from 3 mm to 6 mm.
- Increased bottom fan cartridge feature overlap from 1.2 mm to 4 mm.
- Added corner filter clips to the bottom filter retainer.
- Split `rear_service_spine`, `rear_service_spine_cover`, `power_bus_panel`, and `power_bus_cover` into printable lower/upper sections.
- Moved the full-height service-spine and power-bus versions to review reference exports.
- Regenerated exports, analysis CSVs, manifests, and review package for `mk0.7.3`.

## Verification

- `python -m compileall cad scripts` passed.
- `conda run -n cadquery python scripts/run_revision_pipeline.py --revision mk0.7.3` passed.
- `printability_check.csv` reports no `printable/plastic` parts exceeding the 256 mm P2S axis-aligned envelope.
- `stl_quality.csv` reports all `printable/plastic` and `printable/tpu` parts as watertight and manifold.

## Remaining Notes

- Thin filter/grille parts still require orientation/support review.
- Placeholder and review geometry may remain nonmanifold; these are not printable production parts.
- Final component-specific geometry remains deferred to mk1.0.
