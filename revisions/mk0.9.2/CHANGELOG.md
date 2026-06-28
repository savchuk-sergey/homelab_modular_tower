# mk0.9.2 Changelog

## Fixed

- Fixed the `make_pom_c_shoe_clamp()` geometry blocker that prevented
  `make_rpi_ssd_carriage()`, `make_mini_pc_placeholder_carriage()`,
  `build_assembly()`, export, and render generation.
- Removed the same fragile chamfer pattern from `make_rail_end_clip()`.
- Fixed the export registry entry for the aluminum U-channel placeholder by
  giving it an explicit rail length factory.

## Added

- Parameterized rail pocket carrier and rail end stop dimensions.
- Parameterized carriage clamp, pull lip, shoe spacing, rib allowance, and
  Mini PC support pad dimensions.
- Printable rail pocket carrier geometry in the active RPi/SSD and Mini PC
  placeholder module shells.
- `mk0.9.2` analysis CSVs and review package.
- Full render evidence under `renders/mk0.9.2/`.

## Removed

- Empty stray top-level directory `revisionsmk0.9.1/`.

## Not changed

- No final Mini PC geometry.
- No power distribution geometry.
- No router or UPS module.
- No full Rear Service Spine implementation.
