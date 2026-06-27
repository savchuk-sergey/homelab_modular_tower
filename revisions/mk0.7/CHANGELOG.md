# mk0.7 Changelog

## Added

- Added `bottom_fan_cartridge` printable part for a removable 120 mm bottom intake fan.
- Added `bottom_filter_frame` and `bottom_filter_retainer` printable parts for future dust-filter support.
- Added `fan_120x120x25_placeholder` non-printable fan reference.
- Added `raspberry_pi_3b_placeholder` device reference with board outline, mounting holes and connector keepouts.
- Added `bottom_intake_open_area_review`.
- Added categorized export registry for printable plastic, metal references, device placeholders, fan placeholders and review geometry.
- Added generated `MANIFEST.md` support for revision exports.

## Changed

- Updated current revision to `mk0.7`.
- Increased foot height from 25 mm to 32 mm for bottom intake clearance.
- Updated assembly to include bottom fan cartridge, fan placeholder and Raspberry Pi 3B placeholder.
- Changed revision export path to `exports/mk0.7/...` with category folders and `assemblies/assembly.step`.

## Verified

- `python -m compileall cad`
- `python -m cad.export --revision mk0.7`
