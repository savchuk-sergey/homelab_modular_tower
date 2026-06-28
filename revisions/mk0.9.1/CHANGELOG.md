# mk0.9.1 Changelog

## Overview

Corrective revision after the `mk0.9` engineering review.  The goal is to
fix weight, manufacturability, and serviceability issues without adding new
modules.

## Changes

### Base module

* Removed the massive floor-rib plate from `make_base_frame()`.
* The frame is now a pair of interface rings + corner posts only.
* Added `bottom_grill` and `dust_filter_slot` into the base module assembly.
* Restored `foot_mounts` integration into `make_base_module()`.
* Stiffness is now provided by the frame geometry, M5 rods, and corner posts.

### Roof module

* No major structural change — it was already a light frame.
* Kept the fan mount, top grill, filter slot, and light fan shroud.
* Ensured the exhaust path is not choked.

### Feet

* TPU foot placeholders are now explicitly present in the assembly.
* Foot mounts are integrated into the base module bottom face.
* Target foot clearance: 12 mm (intake gap).

### Rail / carriage subsystem (new)

* Introduced `aluminum_u_channel_rail_placeholder` (15 × 10 × 10 × 2 mm).
* Introduced `pom_c_shoe_placeholder` (Ø8 mm, perpendicular, replaceable).
* `rpi_ssd_carriage` — open-frame, 2 shoes per side (4 total).
* `mini_pc_placeholder_carriage` — open-frame, 3 shoes per side (6 total).
* Both carriages include:
  * front pull lip
  * M3 lock screw clearance
  * rear cable exit
  * large central airflow window
  * shoe sockets with clamp-screw bosses

### Retention philosophy

* M3 clamp screw threads into a PETG heat-set insert boss.
* The screw clamps or stops the POM-C shoe.
* **Forbidden:** threading directly into POM-C, glue-only retention, or PETG
  as the final sliding surface.

### Config updates

* Added `RAIL_*`, `RUNNER_*`, `CARRIAGE_*`, and `FOOT_ENABLED` parameters.
* Weight targets now explicitly defined in `config.py`.

### Documentation

* Created `revisions/mk0.9.1/` with full engineering docs.

## What was removed / deprecated

* Legacy `make_rpi_ssd_tray()` is no longer used by the module assembly.
* Legacy `make_mini_pc_placeholder_tray()` is no longer used by the module
  assembly.
* Legacy 10 × 3 mm flat-bar rail placeholders are kept for backward
  compatibility but are not the recommended path.

## Backward compatibility

* All old functions (`make_rpi_ssd_tray`, `make_rpi_mount_posts`, etc.) are
  still present in the source for reference.
* `part_registry.py` exports them under the `legacy/` category.
