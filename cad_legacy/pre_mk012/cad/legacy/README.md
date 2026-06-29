# cad/legacy — Legacy and Experimental Code

## What "legacy" means here

This directory documents files in the repository that belong to earlier,
cancelled, or superseded workflows. These files are **preserved for reference
only**. They are not the active source for new mk0.11 work.

**Do not:**
- build new mk0.11 parts on top of the full-tower assembly assumptions in the legacy files;
- continue iterating the mk0.10 SVG drawing-first workflow;
- copy geometry from legacy device-specific modules (UPS, RPi, MikroTik, Mini PC) into the generic module design without an explicit engineering decision.

**You may:**
- read legacy files for dimensional reference;
- check historical engineering decisions in `revisions/`;
- treat legacy exports in `exports/mk0.7–mk0.9.3/` as reference artifacts only.

History is preserved, not deleted. All files remain importable.

---

## Physical location of legacy files

All legacy Python part and assembly files have been physically moved here:

```
cad/legacy/
  parts/          ← legacy full-tower part source files
  assembly/       ← legacy full-tower assembly
  scripts/        ← legacy generate_architecture_drawings.py (mk0.10)
  drawings/
    mk0.10/       ← legacy SVG planning drawings (mk0.10, cancelled)
```

The original locations in `cad/parts/` and `cad/assembly/` contain thin
**backward-compatibility stubs** that re-export from the legacy location.
This ensures all existing importers (part_registry.py, tower_assembly.py,
coupons.py, compatibility shims) continue to work without any changes.

---

## Legacy file classification

### Legacy full-tower CAD parts (moved to cad/legacy/parts/)

These files belong to the mk0.7–mk0.9.3 full-tower-first workflow.

| Legacy location | Original location (now stub) | Reason |
|---|---|---|
| `cad/legacy/parts/base_module.py` | `cad/parts/base_module.py` ← stub | mk0.9 base module — full-tower only |
| `cad/legacy/parts/rpi_ssd_module.py` | `cad/parts/rpi_ssd_module.py` ← stub | mk0.9 RPi/SSD device-specific module |
| `cad/legacy/parts/mini_pc_placeholder_module.py` | `cad/parts/mini_pc_placeholder_module.py` ← stub | mk0.9 Mini PC device-specific module |
| `cad/legacy/parts/roof_module.py` | `cad/parts/roof_module.py` ← stub | mk0.9 roof module — full-tower only |
| `cad/legacy/parts/modules.py` | `cad/parts/modules.py` ← stub | Device-specific tray factories (UPS, SSD, RPi, MikroTik, Mini PC) |
| `cad/legacy/parts/side_panels.py` | `cad/parts/side_panels.py` ← stub | Full-tower side panel system |
| `cad/legacy/parts/service_spine.py` | `cad/parts/service_spine.py` ← stub | Full-tower rear service spine and power bus |
| `cad/legacy/parts/airflow.py` | `cad/parts/airflow.py` ← stub | Airflow review placeholders — full-tower only |
| `cad/legacy/parts/cooling.py` | `cad/parts/cooling.py` ← stub | Fan panels, filter, grille — full-tower cooling |
| `cad/legacy/parts/review.py` | `cad/parts/review.py` ← stub | Full-tower review/analysis overlay models |
| `cad/legacy/parts/corner_blocks.py` | `cad/parts/corner_blocks.py` ← stub | Full-tower corner blocks |
| `cad/legacy/parts/frame.py` | `cad/parts/frame.py` ← stub | Full-tower structural frame rings |

### Legacy full-tower assembly (moved to cad/legacy/assembly/)

| Legacy location | Original location (now stub) | Reason |
|---|---|---|
| `cad/legacy/assembly/tower_assembly.py` | `cad/assembly/tower_assembly.py` ← stub | Full mk0.9.2 tower assembly — frozen in mk0.11 per D-006 |

Per decision D-006 (`revisions/mk0.11/DECISIONS.md`): the tower assembly
will not be modified until the single module bay is physically validated.

### Legacy compatibility shims (cad/*.py root files, NOT moved)

These files delegate to `cad/parts/` stubs which in turn delegate to `cad/legacy/parts/`.
They are kept as-is for backward compatibility with the export pipeline.

| File | Note |
|---|---|
| `cad/frame.py` | Shim → `cad/parts/frame.py` stub → `cad/legacy/parts/frame.py` |
| `cad/panels.py` | Shim → `cad/parts/cooling.py` + `cad/parts/side_panels.py` stubs |
| `cad/airflow.py` | Shim → `cad/parts/cooling.py` stub |
| `cad/trays.py` | Shim → `cad/parts/modules.py` stub |
| `cad/power_bus.py` | Shim → `cad/parts/service_spine.py` stub |
| `cad/export.py` | Export entry point — still used by export pipeline |

### Cancelled drawing-first workflow (moved to cad/legacy/)

| Legacy location | Original location | Reason |
|---|---|---|
| `cad/legacy/scripts/generate_architecture_drawings.py` | `scripts/generate_architecture_drawings.py` | mk0.10 SVG generator — cancelled (D-001) |
| `cad/legacy/drawings/mk0.10/*.svg` | `drawings/mk0.10/*.svg` | mk0.10 planning drawings — cancelled (D-001) |

The original `scripts/generate_architecture_drawings.py` and `drawings/mk0.10/*.svg`
are preserved in place (not deleted) with CANCELLED headers.
The canonical legacy copy lives here in `cad/legacy/`.

Historical document: `revisions/mk0.10/DRAWING_PLAN.md` — superseded by mk0.11.

**Reason for cancellation (Decision D-001):**
The mk0.10 SVG iteration did not unlock any design decision that could not be
read directly from `cad/config.py`. Physical prototyping produces faster and
more reliable validation.

### Uncertain — not classified, not moved

| File | Why uncertain |
|---|---|
| `cad/parts/coupons.py` | Fit coupon test pieces — may be useful for mk0.11 print validation |
| `cad/parts/module_interface.py` | Module interface geometry — dependency chain unclear |
| `cad/parts/placeholders.py` | Device placeholders — partially used by mk0.11 via rail_profile / pom_shoe |
| `cad/parts/rods.py` | M5 threaded rods — used in tower_assembly; not needed for mk0.11 single-bay |
| `cad/parts/feet.py` | TPU feet — not needed for single-bay validation but not harmful |

---

## Active mk0.11 files (NOT legacy)

These files are the active implementation targets for mk0.11:

| File | Role |
|---|---|
| `cad/config.py` | All parametric dimensions — shared source of truth |
| `cad/parts/generic_module.py` | Generic removable module shell (mk0.11 primary target) |
| `cad/parts/module_carriage.py` | Generic module carriage with POM-C shoe mounts |
| `cad/parts/pom_shoe.py` | Standalone POM-C shoe reference geometry |
| `cad/parts/rail_profile.py` | Standalone U-channel rail reference geometry |
| `cad/parts/carriages.py` | Open-frame carriage builder (used by module_carriage.py) |
| `cad/parts/rails.py` | Rail geometry (used in assemblies) |
| `cad/jigs/rail_carriage_fit_test.py` | Rail/carriage/shoe interface fit test jig |
| `cad/assembly/generic_module_assembly.py` | Module + carriage combined assembly |
| `cad/assembly/single_module_bay_assembly.py` | Full single-bay: module + rails + shoes (primary validation assembly) |
| `cad/exporters/` | Reusable STEP/STL export infrastructure |
| `cad/utils/` | Reusable geometry utilities |
| `scripts/export_revision.py` | Export pipeline (still used for mk0.11) |
| `scripts/analyze_revision.py` | Analysis pipeline (still used) |

---

## Where to start new mk0.11 work

New mk0.11 files go in `cad/current/mk0.11/`:

```
cad/current/mk0.11/
  parts/       ← new device-specific variants of the generic module
  assemblies/  ← future tower integration assemblies
  jigs/        ← additional fit test jigs as needed
```

See `cad/current/mk0.11/*/README.md` for what belongs in each directory.
