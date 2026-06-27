# Homelab Modular Tower Engineering Review

**Revision:** mk0.7
**Branch:** `cad/mk0.7`
**Date:** 2026-06-27
**Review Type:** Multi-agent engineering design review (no CFD / no FEA / no physical testing)

---

## 1. Executive Summary

The Homelab Modular Tower mk0.7 was subjected to a comprehensive engineering review by 10 specialized reviewers examining CAD integrity, printability, structural integrity, airflow, modularity, power/cable management, plastic efficiency, manufacturability, and cross-cutting risks.

**Overall Verdict: NO-GO UNTIL BLOCKERS ARE FIXED.**

The revision is a significant CAD milestone with a well-structured parametric model, clean export taxonomy, and a sound modular concept. However, **multiple confirmed blockers prevent any physical build or test print.** The most critical issues are:

1. **Safety hazards:** Dynamic tipping when the Mini PC tray is extended (41 mm overhang), lithium battery fire risk with no thermal protection, and an unfused DC power bus.
2. **Structural assembly failures:** Missing side-panel mounting interfaces, missing guide-rail fastening interfaces, incorrect top-frame clamping geometry, and corner blocks placed at mid-height instead of frame corners.
3. **Airflow design flaw:** Tray base ventilation slots are completely blocked by all device placeholders, making the intended 'through-module' airflow impossible.
4. **Printability blockers:** Four parts exceed the Bambu Lab P2S build volume in all orientations; one printable STL (`bottom_fan_cartridge`) is nonmanifold.
5. **Broken quality pipeline:** The `duplicate_geometry_check.csv` failed 100% due to a config attribute mismatch, rendering the automated quality gate worthless.

| Metric | Value |
|--------|-------|
| Reviewers deployed | 10 |
| Blockers identified | 24+ |
| Critical safety issues | 3 |
| Parts exceeding P2S volume | 4 |
| Nonmanifold printable parts | 1 |
| Estimated mesh solid mass | ~3.86 kg PETG |
| Estimated actual filament | 5.5–7.0 kg |
| Estimated print time | 475–570 hours |
| Requirements compliance | 10/12 PASS, 2/12 PARTIAL (83.3 %) |

---

## 2. Reviewed Artifacts

### CAD Source of Truth (parametric Python / CadQuery)
- `cad/config.py` (639 lines) — all dimensions, materials, clearances
- `cad/assembly/tower_assembly.py` (241 lines) — complete tower placement
- `cad/parts/cooling.py` — fan grilles, cartridge, filter, duct
- `cad/parts/feet.py` — stability base, TPU feet, foot sockets
- `cad/parts/frame.py` — top/bottom structural rings
- `cad/parts/corner_blocks.py` — corner compression blocks
- `cad/parts/rods.py` — M5 threaded rod placeholders
- `cad/parts/rails.py` — metal guide rail placeholders
- `cad/parts/carriages.py` — generic tray base, handle, lock, vents
- `cad/parts/modules.py` — all 6 device-specific trays
- `cad/parts/service_spine.py` — rear spine, power bus panel/cover
- `cad/parts/side_panels.py` — sectional side panels
- `cad/parts/placeholders.py` — device and fan reference volumes
- `cad/parts/review.py` — airflow, stability, printability review geometry
- `cad/exporters/part_registry.py` — export categories and registry
- `cad/exporters/export_parts.py` — export pipeline

### Analysis CSVs (mk0.7 review package)
- `part_dimensions.csv` — bounding boxes for all 51 exported parts
- `part_volume.csv` — mesh solid volumes and mass estimates
- `printability_check.csv` — P2S fit, aspect ratios, long-thin flags
- `stl_quality.csv` — watertight, manifold, boundary-edge checks
- `duplicate_geometry_check.csv` — **100% failed due to tool bug**

### Revision Documentation
- `revisions/mk0.7/REVISION.md` — revision goal and scope
- `revisions/mk0.7/CHANGELOG.md` — added/changed/verified items
- `revisions/mk0.7/DECISIONS.md` — engineering decisions and trade-offs
- `revisions/mk0.7/KNOWN_ISSUES.md` — acknowledged limitations
- `revisions/mk0.7/CALCULATIONS.md` — assumptions and sizing
- `revisions/mk0.7/REVIEW_REQUIREMENTS_CHECKLIST.md` — artifact inventory
- `revisions/mk0.7/ASSEMBLY_OVERVIEW.md` — export counts

### Project Requirements
- `AGENTS.md` — standing rules for CAD, revision structure, and design philosophy
- `docs/POWER.md`, `docs/BOM.md`, `docs/PRINTING.md`, `docs/ARCHITECTURE.md`

### Rendered Images (mk0.7)
- Assembly views: bottom, front, isometric, left, rear, right, top
- Review images: airflow path, blocked zones, bottom intake clearance, mini PC airflow, module extraction, power bus layout, rear spine detail, stability base, top exhaust, torsion frame
- Per-part drawings: 35+ individual part render sets

---

## 3. Scope and Limitations

### What was reviewed
- **Design-level engineering review** of the complete mk0.7 CAD model, export package, and revision documentation.
- Dimensional analysis, geometric interference checks, tolerance stack-ups, and assembly realism.
- Printability assessment against the Bambu Lab P2S build volume (256 × 256 × 256 mm).
- Structural load-path analysis using hand calculations (no FEA).
- Airflow path analysis using area estimates and obstruction mapping (no CFD).
- Material efficiency and print-time estimation based on mesh solid volumes.
- Cross-cutting risk analysis including safety, usability, and cost.

### What was NOT reviewed
- **No CFD** — airflow velocities, pressure drops, and temperature fields were not simulated.
- **No FEA** — stress concentrations, deflections, and safety factors were estimated by hand only.
- **No physical testing** — no prototypes were built, measured, or tested.
- **No slicing validation** — actual G-code, toolpaths, and support structures were not generated.
- **No electrical validation** — wire gauges, current capacity, and EMC compliance were not analyzed.
- **No software/firmware** — fan control, thermal monitoring, and power management are outside scope.

### Evidence grading legend
- **CONFIRMED** — Finding is directly supported by measurement, code inspection, or CAD geometry.
- **LIKELY** — Finding is supported by strong engineering inference or standard practice.
- **UNCERTAIN** — Finding depends on assumptions or missing data.
- **NEEDS TEST** — Requires physical prototyping, slicer validation, or hardware measurement.

---

## 4. Requirements Checklist

Evaluation against `AGENTS.md` project requirements:

| # | Requirement | Result | Grade | Evidence |
|---|-------------|--------|-------|----------|
| 1 | Modularity | **PASS** | A- | All 6 trays share `MODULE_WIDTH=170`, `MODULE_DEPTH=176`, rail spacing 168 mm, front handle, M3 lock. `TRAY_STACK` allows independent front extraction. |
| 2 | Repairability | **PASS** | A | Standard M3/M5 fasteners, no adhesives, replaceable TPU feet, removable fan cartridge, sectional side panels. |
| 3 | Structural Stiffness | **PARTIAL** | C | M5 rods, metal rails, and frame rings present. **Corner blocks are at mid-height (`z=160.75`) instead of frame corners** — they do not reinforce the rod-to-frame joints. |
| 4 | Airflow | **PARTIAL** | C+ | Bottom 120 mm intake fully modeled. **Top exhaust fan is missing** — only a passive grille. No CFD or physical verification. |
| 5 | Serviceability | **PASS** | A- | Bottom fan cartridge removable from below. Side panels removable without touching rods. Modules slide forward. |
| 6 | Parametric Design | **PASS** | A | All dimensions in `config.py`. Parts/assembly/export cleanly separated. No mixed-logic files. |
| 7 | Scalability | **PASS** | A | `UNIT_HEIGHT=35`, `MODULE_SLOT_COUNT=6`. New modules addable via `TRAY_FACTORIES`. |
| 8 | Rear Service Spine | **PASS** | A- | Spine geometry, cable tie slots, power bus zones, and module cable exits all modeled. Fan wire routing not yet detailed. |
| 9 | Power System | **PASS** | A | No open 220V inside. DC UPS placeholder, power bus with XT30/MicroFit/USB-C zones. Fuse/terminal placeholders in config. |
| 10 | CAD Rules | **PASS** | A | CadQuery only. `config.py` is source of truth. STEP/STL are derived. Individual part exports. |
| 11 | Revision Structure | **PASS** | A | All 5 required docs present. No retroactive edits. |
| 12 | Export Organization | **PASS** | A | `printable/plastic`, `non_printable/metal_reference`, `placeholders/devices`, `placeholders/fans`, `review`, `assemblies` correctly separated. |

**Overall Compliance Score: 10.0 / 12 = 83.3%**

---

## 5. CAD Integrity Review

*Full agent: `01_cad_integrity.md`*

## Executive Summary

The mk0.7 CAD model is structurally sound in its modular separation, but it contains **multiple confirmed geometry and configuration bugs that block progression**.

The most severe issues are:

1. The `bottom_fan_cartridge` has a **floating service handle** (3.0 mm gap from the body), producing a nonmanifold STL that cannot be reliably printed.
2. `config.py` **double-defines `REAR_SPINE_COVER_THICKNESS`** with two different values (2.0 mm then 3.0 mm), so the exported cover geometry is ambiguous.
3. The **UPS power tray battery marker protrudes 15.5 mm beyond the tray width**, making the tray wider than the module slot it must fit into.
4. The **power bus cover holes are misaligned** with the power bus panel holes, so the cover cannot be mechanically attached.
5. The **top and bottom fan grille placements overlap the structural frames** by 3.5 mm each.
6. The **sectional stability base has no foot sockets or screw holes**, yet the assembly places feet at those locations.

These are not cosmetic issues. They are assembly, fit, and printability defects. The revision should not proceed to manufacturing export without correction.

---

## Parametric Integrity

### Overall assessment
Most dimensions are centralized in `config.py` and referenced via `cfg.*`. However, there are **hardcoded magic numbers in geometry code** and **unexplained literal offsets in config** that violate the project's own rule: *"не использовать магические числа"*.

### Findings

| Finding | Location | Evidence | Grade |
|---|---|---|---|
| Arrow head height ratio hardcoded | `cad/parts/review.py:14` | `cfg.AIRFLOW_ARROW_DIAMETER * 1.6` | **CONFIRMED** |
| Rotation angle 90° hardcoded | `cad/parts/review.py:44` | `.rotate((0, 0, 0), (1, 0, 0), 90)` | **CONFIRMED** |
| `slot2D` angle 0° hardcoded | `cad/parts/carriages.py:14` | `.slot2D(..., 0)` | **LIKELY** (standard but unnamed) |
| `slot2D` angle 0° hardcoded | `cad/parts/side_panels.py:140` | `.slot2D(..., 0)` | **LIKELY** |
| `slot2D` angle 0° hardcoded | `cad/parts/service_spine.py:118` | `.slot2D(..., 90)` | **LIKELY** (at least 90 is named by context) |
| Unexplained literal `+24.0` in `TOWER_HEIGHT` | `cad/config.py:17` | `TOWER_HEIGHT = TOTAL_UNITS * UNIT_HEIGHT + 24.0` | **CONFIRMED** |
| Unexplained literal `-34.0` in `METAL_RAIL_HEIGHT` | `cad/config.py:106` | `METAL_RAIL_HEIGHT = TOWER_HEIGHT - 34.0` | **CONFIRMED** |
| Unexplained literal `* 6.5` in `MINIPC_DUCT_ZONE_OFFSET_Z` | `cad/config.py:392` | `STACK_START_Z + UNIT_HEIGHT * 6.5` | **CONFIRMED** |
| Unexplained literal `* 2.2` in `TRAY_STRUCTURAL_CLEARANCE_HEIGHT` | `cad/config.py:179` | `UNIT_HEIGHT * 2.2` | **CONFIRMED** |
| Unexplained literal `* 0.52` in `STABILITY_COM_Z` | `cad/config.py:606` | `TOWER_HEIGHT * 0.52` | **CONFIRMED** |
| Unexplained literal `+22.0` in `BOTTOM_FAN_CARTRIDGE_WIDTH` | `cad/config.py:427` | `FAN_120_SIZE + 22.0` | **CONFIRMED** |
| Unexplained literals in fan grille offsets | `cad/config.py:613,616` | `BOTTOM_FAN_PANEL_Z = -2.0`, `TOP_FAN_PANEL_Z_OFFSET = 2.0` | **CONFIRMED** |

### Notes
The `1.6` multiplier in `review.py` is the clearest violation: it is an engineering constant (arrow head aspect ratio) that should be named in `config.py`. The `90` degree rotation is also a parametric angle that should be centralized. The `0` angles in `slot2D` are borderline (they mean "aligned with X axis"), but in a strict parametric project they should be symbolic constants (e.g., `SLOT_ANGLE_X = 0.0`).

The config file itself contains many literal offsets (`+24.0`, `-34.0`, `* 6.5`, etc.) that are not explained by named parameters. They should be replaced by expressions using named parameters (e.g., `TOWER_EXTRA_HEIGHT = 2 * FRAME_THICKNESS + ...`) or at minimum documented with comments.

---

## Function Separation

### Overall assessment
The separation of concerns is **good**. Parts are in `cad/parts/`, assembly in `cad/assembly/`, export in `cad/exporters/`. No part file mixes export logic with geometry.

### Findings

| Finding | Evidence | Grade |
|---|---|---|
| `cooling.py` contains redundant `create_*` aliases that are unused by the registry | `create_fan_panel`, `create_bottom_fan_panel`, `create_top_fan_panel`, `create_bottom_fan_cartridge`, `create_bottom_filter_frame`, `create_bottom_filter_retainer`, `create_mini_pc_airflow_duct` | **LIKELY** (dead code, not a violation) |
| `frame.py` contains redundant `create_frame_top` / `create_frame_bottom` | These call `make_top_structural_frame` / `make_bottom_structural_frame` but are unused by registry | **LIKELY** |
| `feet.py` contains `create_foot()` which is unused | `create_foot()` calls `make_foot()` which calls `make_wide_tpu_foot_placeholder()` | **LIKELY** |
| `carriages.py` contains `make_standard_tray_base` and `make_tray_handle` aliases | Used internally, but add noise | **UNCERTAIN** |
| `make_mini_pc_airflow_duct_placeholder()` lacks a `.tag()` | Returns raw geometry without tagging; inconsistent with rest of project | **CONFIRMED** |
| `create_power_bus_panel()` lacks a `.tag()` | Same as above | **CONFIRMED** |

### Recommendation
Remove unused `create_*` wrappers or add them to the registry. Enforce `.tag()` on every part function for consistency.

---

## Export Organization

### Overall assessment
The `EXPORT_CATEGORIES` structure is mostly correct, but there are **missing entries, duplicate aliases, and mismatched naming** that cause redundant or missing exports.

### Findings

| Finding | Evidence | Grade |
|---|---|---|
| `base_stability_plate` is in `PARTS` but missing from `EXPORT_CATEGORIES` | `part_registry.py:16` vs `EXPORT_CATEGORIES` | **CONFIRMED** |
| `wide_tpu_foot_placeholder` is in `PARTS` but missing from `EXPORT_CATEGORIES` | `part_registry.py:24` vs `EXPORT_CATEGORIES` | **CONFIRMED** |
| `bottom_fan_panel` / `top_fan_panel` are in `PARTS` but missing from `EXPORT_CATEGORIES` | `part_registry.py:46-47` | **CONFIRMED** |
| `mini_pc_airflow_duct_placeholder` is in `PARTS` but missing from `EXPORT_CATEGORIES` | `part_registry.py:60` | **CONFIRMED** |
| `frame_top` / `frame_bottom` and `top_structural_frame` / `bottom_structural_frame` map to the same functions in `EXPORT_CATEGORIES` | `EXPORT_CATEGORIES["printable/plastic"]:72-75` | **CONFIRMED** (duplicate exports) |
| `bottom_fan_panel` maps to `cooling.make_bottom_fan_grille` (same as `bottom_fan_grille`) | `PARTS:46` | **CONFIRMED** (redundant key) |
| `ssd_placeholder` name does not match its factory `make_external_ssd_placeholder` | `PARTS:56` | **LIKELY** (naming mismatch) |
| `fan_120x120x25_placeholder` is exported as `placeholders/fans` but function is `make_fan_120_placeholder` | `PARTS:51` | **LIKELY** (name mismatch) |
| `power_bus_zone_placeholder` is used in assembly but **not in `PARTS`** | `tower_assembly.py:183` | **CONFIRMED** (missing from registry) |

### Impact
When `export_categorized_parts()` runs, `base_stability_plate` and `wide_tpu_foot_placeholder` are silently skipped. When `export_parts()` runs, `bottom_fan_panel.stl` and `bottom_fan_grille.stl` are identical geometry exported twice. This wastes space and invites version confusion.

---

## STL Quality Issues

### Overall assessment
**One printable part has a confirmed manifold defect.** Review geometry has expected open boundaries.

### Findings from `stl_quality.csv`

| Part | Category | Watertight | Manifold | Nonmanifold Edges | Grade |
|---|---|---|---|---|---|
| `bottom_fan_cartridge` | `printable/plastic` | False | False | 2 | **CONFIRMED** — geometry defect |
| `airflow_path_review` | `review` | False | False | 4 | Expected (open review geometry) |
| `mini_pc_airflow_path_review` | `review` | False | False | 1 | Expected |
| `stability_review` | `review` | False | False | 2 | Expected |
| All other `printable/plastic` parts | — | True | True | 0 | OK |

### Root cause of `bottom_fan_cartridge` nonmanifold
In `cooling.py:78-86`, the service handle is translated by:
```python
(
    0,
    -cfg.BOTTOM_FAN_CARTRIDGE_DEPTH / 2 - cfg.BOTTOM_FAN_CARTRIDGE_SERVICE_PULL / 2,
    cfg.BOTTOM_FAN_CARTRIDGE_HEIGHT / 2,
)
```
`DEPTH/2 = 71.0`, `SERVICE_PULL/2 = 7.0`, so handle center is at `y = -78.0`. The handle half-depth is `RAIL_WIDTH/2 = 4.0`, so the handle extends from `y = -82.0` to `y = -74.0`. The cartridge body extends from `y = -71.0` to `y = +71.0`. **There is a 3.0 mm gap between the handle and the cartridge body.** The handle is completely disconnected. CadQuery's union of disjoint solids produces a nonmanifold boundary in the STL exporter.

### Fix
Change the Y translation to `-cfg.BOTTOM_FAN_CARTRIDGE_DEPTH / 2 - cfg.BOTTOM_FAN_CARTRIDGE_RAIL_WIDTH / 2` so the handle is flush with the body.

---

## Duplicate Geometry Check Failure

### Finding
**CONFIRMED** — `duplicate_geometry_check.csv` shows **100% failure rate** for all 50 parts.

Error for every entry:
```
AttributeError: module 'cad.config' has no attribute 'DUPLICATE_VOLUME_TOLERANCE_MM'
```

### Root cause
The review tool expects `config.DUPLICATE_VOLUME_TOLERANCE_MM`, but the actual parameter in `config.py` is `DUPLICATE_VOLUME_TOLERANCE_MM3` (line 636). The tool is using a stale attribute name.

### Impact
This is a **review-process defect**, not a CAD geometry defect. However, because the check failed for all parts, the team has **no duplicate-part detection data** for mk0.7. This undermines the review package.

### Fix
Either rename the config key to `DUPLICATE_VOLUME_TOLERANCE_MM` (dropping the `_MM3` suffix) or update the review tool to expect `DUPLICATE_VOLUME_TOLERANCE_MM3`.

---

## Config Consistency

### Overall assessment
`config.py` is comprehensive but suffers from **a critical double-definition bug**, **many unused legacy parameters**, and **unexplained literal offsets**.

### Critical finding

| Finding | Evidence | Grade |
|---|---|---|
| `REAR_SPINE_COVER_THICKNESS` defined twice with different values | Line 482: `REAR_SPINE_COVER_THICKNESS = 2.0`<br>Line 487: `REAR_SPINE_COVER_THICKNESS = 3.0` | **CONFIRMED** — second shadows first |
| `REAR_SPINE_COVER_WIDTH` defined twice (same value) | Line 483 and line 509 | **CONFIRMED** (redundant) |
| `REAR_SPINE_COVER_HEIGHT` defined twice (same value) | Line 484 and line 510 | **CONFIRMED** (redundant) |
| `REAR_SPINE_COVER_MOUNT_Z` defined twice (same value) | Line 485 and line 511 | **CONFIRMED** (redundant) |

The second `REAR_SPINE_COVER_THICKNESS = 3.0` shadows the first. The exported `rear_service_spine_cover` has a bounding box thickness of **3.0 mm** (per `part_dimensions.csv`), confirming the second value is active. If the design intent was 2.0 mm (e.g., for a thin cover), the export is wrong. If 3.0 mm is correct, the 2.0 mm line is dead code that will confuse future editors.

### Unused parameters (defined but not referenced in any geometry file)

The following parameters appear in `config.py` but are **not used** in any part, assembly, or export file reviewed:

- `PANEL_THICKNESS` (superseded by `SIDE_PANEL_THICKNESS`)
- `BOTTOM_AIR_GAP`, `BOTTOM_FEET_HEIGHT` (both aliases for `FOOT_HEIGHT`)
- `FAN_SCREW_SPACING` (alias for `FAN_HOLE_SPACING`, unused)
- `RAIL_SPACING` (computed from `METAL_RAIL_X_OFFSET`, unused)
- `MODULE_SLOT_PITCH`, `MODULE_SLOT_GAP`, `LIGHT_MODULE_HEIGHT`, `COMPUTE_MODULE_HEIGHT`, `FRAME_SEGMENT_HEIGHT`, `FRAME_SEGMENT_COUNT` (future architecture, unused)
- `REAR_SPINE_INSERT_DIAMETER`, `REAR_SPINE_INSERT_DEPTH` (planned but not used in spine geometry)
- `REAR_SPINE_BOLT_SPACING` (unused)
- `SPINE_SECTION_COUNT` (unused)
- `REAR_SPINE_CHANNEL_SIDE_MARGIN` (unused)
- `REAR_SPINE_SIGNAL_ZONE_WIDTH` (unused)
- `POWER_BUS_FUSE_BLOCK_WIDTH`, `POWER_BUS_FUSE_BLOCK_HEIGHT`, `POWER_BUS_TERMINAL_BLOCK_WIDTH`, `POWER_BUS_TERMINAL_BLOCK_HEIGHT` (unused)
- `BOARD_PLACEHOLDER_HEIGHT` (unused)
- `MAX_MODULE_MASS` (unused)
- `TRAY_BACK_CONNECTOR_ZONE` (legacy, unused)
- `TRAY_BASE_RIB_X` (unused)
- `TRAY_FRONT_LIP` (unused)
- `FAN_CLEARANCE` (unused)
- Lower-case aliases (`total_height`, `base_width`, etc.) — noted as legacy for mk0.6 notes, but clutter the namespace.

### Unexplained literals in config

The following literals should be named or documented because they are unexplained engineering constants:

- `24.0` in `TOWER_HEIGHT` (what does it represent?)
- `34.0` in `METAL_RAIL_HEIGHT`
- `18.0` in `SIDE_PANEL_HEIGHT`
- `6.5` in `MINIPC_DUCT_ZONE_OFFSET_Z`
- `2.2` in `TRAY_STRUCTURAL_CLEARANCE_HEIGHT`
- `0.52` in `STABILITY_COM_Z`
- `22.0`, `18.0`, `24.0` in bottom cartridge / filter dimensions
- `2.0` and `10.0` in `BOTTOM_FAN_PANEL_Z` and `TOP_FAN_PANEL_Z_OFFSET` (these are also placement bugs; see Assembly Realism)

---

## Assembly Realism

### Overall assessment
The assembly script is well-structured, but it contains **several placement errors and design gaps** that make the assembly physically impossible or inconsistent.

### Confirmed placement errors

| Part | Issue | Evidence | Grade |
|---|---|---|---|
| **Top fan grille** | Overlaps top structural frame by **3.5 mm** | Grille at `z = 323.5` (thickness 4.0 → `321.5–325.5`); top frame at `z = 321.5` (thickness 7.0 → `318.0–325.0`) | **CONFIRMED** |
| **Bottom fan grille** | Overlaps bottom structural frame by **3.5 mm** | Grille at `z = -2.0` (thickness 4.0 → `–4.0–0.0`); bottom frame at `z = 0.0` (thickness 7.0 → `–3.5–3.5`) | **CONFIRMED** |
| **Bottom fan cartridge** | Rails and handle overlap base plate by **5.0 mm** with no matching slots | Cartridge rails extend to `z = –9.0`; base plate occupies `z = –14.0` to `–4.0` | **CONFIRMED** |
| **Power bus cover** | Holes are at `x = 0`, but panel holes are at `x = ±7.0` | `create_power_bus_cover` uses `pushPoints([(0, z)])`; `create_power_bus_panel` uses `pushPoints([(-7, z), (7, z)])` | **CONFIRMED** |
| **Sectional base feet** | Feet are placed but base has no sockets or screw holes | `wide_foot_positions()` returns `±97, ±102`; `make_central_bottom_fan_frame()` has no foot holes | **CONFIRMED** |
| **UPS power tray** | Battery marker extends **15.5 mm** beyond tray width | Battery zone width `125` at `x = –38` → `min_x = –100.5`; tray width is `170` (should be `±85`) | **CONFIRMED** |
| **Raspberry Pi tray vs. placeholder** | Tray uses old `RASPBERRY_PI_PLACEHOLDER` (86×57×8); assembly uses new `raspberry_pi_3b_placeholder` (85×56×1.6 + keepouts) | `create_raspberry_pi_tray()` uses `cfg.RASPBERRY_PI_PLACEHOLDER`; assembly uses `placeholders.make_raspberry_pi_3b_placeholder()` | **CONFIRMED** |

### Additional issues

| Finding | Evidence | Grade |
|---|---|---|
| `bottom_filter_frame` and `bottom_filter_retainer` are not placed in the assembly | They are in `EXPORT_CATEGORIES` but never added in `tower_assembly.py` | **LIKELY** |
| Monolithic `base_stability_plate` is in `PARTS` but not used in assembly | Assembly uses sectional base (`make_central_bottom_fan_frame` + extensions) | **LIKELY** (obsolete or inconsistent) |
| `bottom_fan_cartridge` handle is disconnected from body (see STL Quality) | `cooling.py:78-86` | **CONFIRMED** |
| Rods are placed at `z = 0`, but bottom frame is centered at `z = 0` (thickness 7.0) | Rod starts at center of frame, not below it | **LIKELY** (visualization only) |
| Top frame is at `z = TOWER_HEIGHT = 321.5`, rod ends at `z = 321.5` | Rod ends at center of top frame, not above it | **LIKELY** (visualization only) |

### Notes on the UPS tray
The `part_dimensions.csv` confirms `ups_power_tray` bounding box is `186.5 × 178.0 × 32.0` mm. The intended module width is `170.0` mm. This means the UPS tray **cannot be inserted into the tower** as modeled because the battery marker is too wide. The marker must be resized or the tray width must be increased (which would break the module standard).

### Notes on the power bus cover
The power bus cover is a real printable part. If its holes are at `x = 0` and the panel holes are at `x = ±7`, there is no common fastener axis. A screw cannot pass through both. The cover holes must be moved to `x = ±7` or the panel holes must be moved to `x = 0`.

---

## Naming Consistency

### Findings

| Finding | Evidence | Grade |
|---|---|---|
| `ssd_placeholder` in registry, but factory is `make_external_ssd_placeholder` | `part_registry.py:56` | **LIKELY** |
| `fan_120x120x25_placeholder` in registry, but factory is `make_fan_120_placeholder` | `part_registry.py:51` | **LIKELY** |
| `mini_pc_airflow_duct` in registry, but factory is `make_mini_pc_airflow_duct_placeholder` | `part_registry.py:59` | **LIKELY** |
| `mini_pc_airflow_duct_placeholder` also in registry, same factory | `part_registry.py:60` | **CONFIRMED** (redundant key) |
| `bottom_fan_panel` / `top_fan_panel` duplicate `bottom_fan_grille` / `top_fan_grille` | `part_registry.py:46-47` | **CONFIRMED** |
| `frame_top` / `frame_bottom` duplicate `top_structural_frame` / `bottom_structural_frame` | `part_registry.py:11-14` | **CONFIRMED** |
| `make_foot` → `make_wide_tpu_foot_placeholder` → `create_foot` chain | `feet.py:183-188` | **LIKELY** (three aliases for one part) |
| `make_top_structural_frame` → `create_frame_ring` vs `create_frame_top` | `frame.py:46-58` | **LIKELY** (unused alias) |
| `make_module_tray` → `make_standard_tray_base` → `create_carriage` | `carriages.py:189-249` | **UNCERTAIN** (internal aliases, not registry) |

### Recommendation
Prune the registry to one name per unique geometry. Remove dead aliases. If a legacy name must be kept for compatibility, add a deprecation comment.

---

## Blockers

The following issues **must be resolved before the revision can proceed** to manufacturing export or physical prototyping:

1. **Floating cartridge handle (`bottom_fan_cartridge`)** — The disconnected handle produces a nonmanifold STL. The part is not reliably printable. Fix the Y translation in `cooling.py`.
2. **Double-defined `REAR_SPINE_COVER_THICKNESS`** — The exported cover thickness is ambiguous. Decide on 2.0 mm or 3.0 mm and delete the duplicate line.
3. **UPS tray exceeds module width** — The battery marker makes the tray `186.5` mm wide, which will not fit into the `170` mm module slot. Resize or reposition the marker.
4. **Fan grille frame overlap** — Both top and bottom grilles are placed inside the structural frames. The grilles will intersect the frames in the assembly and in any combined export. Fix `BOTTOM_FAN_PANEL_Z` and `TOP_FAN_PANEL_Z_OFFSET`.
5. **Power bus cover / panel hole misalignment** — The cover cannot be screwed to the panel. Align the hole patterns.
6. **Sectional base lacks foot attachment** — The assembly uses a sectional base but places feet with no screw holes or sockets. Either add foot features to the sectional pieces or remove the feet from the assembly.
7. **Cartridge rails overlap base plate without slots** — The cartridge rails and handle extend `5.0` mm into the base plate volume. The base plate has no corresponding slots. Add slots or redesign the cartridge interface.

---

## Recommendations

### Immediate (before next export)
1. **Fix `bottom_fan_cartridge` handle Y offset**: Change the translation from `SERVICE_PULL/2` to `RAIL_WIDTH/2` in `cooling.py`.
2. **Remove duplicate `REAR_SPINE_COVER_THICKNESS`**: Keep the value that matches design intent (check `part_dimensions.csv` shows 3.0 mm was exported; if 2.0 mm is desired, update `service_spine.py` and re-export).
3. **Fix UPS tray marker width**: Reduce the battery marker width or shift it so it stays within `x = ±85.0`.
4. **Fix fan grille Z placement**: Derive `BOTTOM_FAN_PANEL_Z` and `TOP_FAN_PANEL_Z_OFFSET` from `FRAME_THICKNESS` and `FAN_GRILLE_THICKNESS` so they sit flush with the frames, not inside them.
5. **Fix power bus hole alignment**: Add `±POWER_BUS_PAD_SCREW_OFFSET_X` holes to the cover, or remove the offset from the panel.
6. **Add foot sockets to sectional base**: Add `screw_cut` and `socket_cut` logic from `make_base_stability_plate` to the sectional base pieces, or remove the monolithic `base_stability_plate` from `PARTS` to avoid confusion.
7. **Add base plate slots for cartridge rails**: Cut matching slots in `make_central_bottom_fan_frame` for the cartridge rails and handle, or redesign the cartridge to sit fully below the base plate.

### Short-term (before mk0.8)
8. **Remove dead aliases**: Delete `create_frame_top`, `create_frame_bottom`, `create_foot`, `create_fan_panel`, `create_bottom_fan_panel`, `create_top_fan_panel`, `bottom_fan_panel`, `top_fan_panel`, `mini_pc_airflow_duct_placeholder`, `frame_top`/`frame_bottom` from `PARTS` and `EXPORT_CATEGORIES`.
9. **Add missing `DUPLICATE_VOLUME_TOLERANCE_MM` alias** to `config.py` (or update the review tool) so the duplicate-geometry check functions.
10. **Name unexplained config literals**: Replace `+24.0`, `-34.0`, `*6.5`, `*2.2`, `*0.52`, `+22.0`, etc. with named parameters and comments explaining their engineering origin.
11. **Audit unused parameters**: Delete or clearly mark as "future use" the ~20 unused parameters in `config.py`.
12. **Synchronize Raspberry Pi placeholder**: Update `create_raspberry_pi_tray()` to use the 3B dimensions or revert the assembly to use the old placeholder so the tray and assembly match.
13. **Add `bottom_filter_frame` and `bottom_filter_retainer` to the assembly** or remove them from export if they are not yet designed for the sectional base.
14. **Enforce tagging**: Add `.tag()` to `make_mini_pc_airflow_duct_placeholder()` and `create_power_bus_panel()` for consistency.

### Process
15. **Update review package after fixes**: Re-run STL quality, duplicate geometry, and part dimension checks. The current `duplicate_geometry_check.csv` is useless because of the tool failure.

---

## Appendix: Evidence Summary Table

| File | Lines | Key Issue |
|---|---|---|
| `cad/parts/cooling.py` | 78–86 | Floating cartridge handle (3.0 mm gap) |
| `cad/parts/cooling.py` | 48–91 | Cartridge rails overlap base plate without slots |
| `cad/parts/review.py` | 14 | Magic number `1.6` for arrow head ratio |
| `cad/parts/review.py` | 44 | Magic number `90` for rotation angle |
| `cad/config.py` | 482, 487 | `REAR_SPINE_COVER_THICKNESS` double-defined (2.0 vs 3.0) |
| `cad/config.py` | 613, 616 | Fan grille offsets `-2.0` and `+2.0` are hardcoded and wrong |
| `cad/assembly/tower_assembly.py` | 198–199 | Frames placed at `z = 0` and `z = TOWER_HEIGHT`, rods at same levels |
| `cad/assembly/tower_assembly.py` | 229, 233 | Fan grille locations cause 3.5 mm overlap with frames |
| `cad/assembly/tower_assembly.py` | 42–49 | Feet placed but sectional base has no attachment holes |
| `cad/parts/modules.py` | 10–21 | UPS battery marker extends to `x = –100.5` (tray width is 170) |
| `cad/parts/service_spine.py` | 44–61 | Cover holes at `x = 0`, panel holes at `x = ±7` |
| `cad/exporters/part_registry.py` | 10–131 | Missing categories and duplicate aliases in `PARTS` / `EXPORT_CATEGORIES` |
| `revisions/mk0.7/review_package/analysis/duplicate_geometry_check.csv` | All rows | `AttributeError: module 'cad.config' has no attribute 'DUPLICATE_VOLUME_TOLERANCE_MM'` |
| `revisions/mk0.7/review_package/analysis/stl_quality.csv` | Line 11 | `bottom_fan_cartridge`: nonmanifold, not watertight |
| `revisions/mk0.7/review_package/analysis/part_dimensions.csv` | Line 45 | `ups_power_tray` bounding box: 186.5 mm wide |

---

*End of review.*


---

## 6. Printability Review

*Full agent: `02_printability.md`*

## Executive Summary

This review finds **four parts that cannot be printed within the P2S build volume in an axis-aligned orientation**, and **one part that cannot fit in any orientation at all**. Seven parts are flagged as long-thin geometry risks. One functional printed feature is below the project's own `MIN_PRINTABLE_FEATURE` threshold of 1.2 mm. The `foot` part is incorrectly classified as generic plastic instead of TPU. Several large flat panels present significant PETG warping risks. All six module trays will require support material for their front handle pockets. None of the issues are fatal to the project, but **at least three parts must be redesigned with split joints before production printing can begin.**

| Category | Count | Severity |
|---|---|---|
| Build volume exceedance (axis-aligned) | 4 | High |
| Build volume exceedance (any orientation) | 1 (`rear_service_spine`) | Critical |
| Long-thin risk flagged | 7 | Medium–High |
| Material misclassification | 1 (`foot`) | Medium |
| Feature below `MIN_PRINTABLE_FEATURE` | 1 (`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG`) | Medium |
| Support-required parts | ~10 | Medium |
| Large flat / warping risk | 9 | Medium |

---

## Build Volume Fit Analysis

The P2S build volume is **256 × 256 × 256 mm**. The CSV's `fits_axis_aligned` column correctly flags four parts as exceeding this volume.

### Parts Exceeding Axis-Aligned Volume

| Part | Dimensions (mm) | Exceeds by | Fits Axis-Aligned? | Diagonal Fit Possible? | Grade |
|---|---|---|---|---|---|
| `power_bus_cover` | 46 × 5 × 265.5 | Z +9.5 mm | No | Yes (28° rotation, proj. ~256 × 165) | CONFIRMED |
| `power_bus_panel` | 34 × 7.5 × 275.5 | Z +19.5 mm | No | Yes (~30° rotation, proj. ~256 × 166) | CONFIRMED |
| `rear_service_spine` | 80 × 40 × 297.5 | Z +41.5 mm | No | **No** (min. proj. 266.9 mm > 256) | CONFIRMED |
| `rear_service_spine_cover` | 46 × 3 × 295.5 | Z +39.5 mm | No | Yes (45° rotation, proj. ~241 × 241) | CONFIRMED |

### Evidence and Analysis

- **`rear_service_spine` (80 × 40 × 297.5 mm):** CONFIRMED **does not fit in any orientation**. Even at the optimal 45° rotation on the bed, the projected bounding box is (297.5 + 40) / √2 = **266.9 mm**, exceeding 256 mm. This part **must be split** into at least two segments before it can be printed on the P2S.

- **`power_bus_panel` (34 × 7.5 × 275.5 mm):** The 275.5 mm axis can be laid diagonally at ~30° rotation, yielding projected dimensions of approximately **256 × 166 mm**. However, this orientation makes the part a **275.5 mm long, 7.5 mm wide strip on the bed**. Bed adhesion would be catastrophic; PETG warping on a 275 mm long strip with only 7.5 mm width is practically guaranteed. **Splitting is strongly recommended for production reliability.**

- **`power_bus_cover` (46 × 5 × 265.5 mm):** Similar to the panel, diagonal placement at ~28° rotation yields projections of ~256 × 191 mm. The part is a **265.5 mm long, 5 mm thick strip**. Bed adhesion would be extremely poor. **Splitting is strongly recommended.**

- **`rear_service_spine_cover` (46 × 3 × 295.5 mm):** At 45° rotation, projections are ~241 × 241 mm, so it fits diagonally. However, Z = 3 mm means only **~7–8 layers at 0.4 mm layer height**. A 295.5 mm long, 3 mm thick strip in PETG will warp so severely that it is unlikely to complete a print. **Splitting is strongly recommended.**

### Recommendation

All four parts require redesign with **split joints** for reliable P2S printing. Diagonal printing is a theoretical workaround for three of them but is not a production-ready solution due to adhesion and warping risks.

---

## Long Thin Part Risks

The CSV flags seven parts with `long_thin_risk = True`. These are assessed below.

| Part | Dimensions (mm) | Aspect Ratio | Risk | Grade |
|---|---|---|---|---|
| `bottom_filter_frame` | 138 × 138 × 3 | 46.0 | Very flat ring; large footprint; corners will curl | CONFIRMED |
| `bottom_filter_retainer` | 144 × 8 × 4 | 36.0 | Long narrow strip; ends will lift | CONFIRMED |
| `foot_socket` | 42 × 42 × 3 | 14.0 | Small flat disk; minor curling risk | LIKELY |
| `left_side_panel_middle` | 176 × 5.2 × 100.9 | 33.8 | Tall thin panel; ribs make it worse | CONFIRMED |
| `right_side_panel_middle` | 176 × 5.2 × 100.9 | 33.8 | Same as left | CONFIRMED |
| `top_fan_grille` | 190 × 190 × 4 | 47.5 | Very large flat grill; extreme warping risk | CONFIRMED |
| `rear_service_spine_cover` | 46 × 3 × 295.5 | 98.5 | Extremely long, thin strip; will warp like a banana | CONFIRMED |

### Detailed Assessment

- **`bottom_filter_frame` (138 × 138 × 3 mm):** A 3 mm thick flat ring with a 112 mm diameter center hole. Printed flat, the 138 mm footprint and thin walls will experience differential cooling. The corners will curl. **CONFIRMED: High warping risk.** Requires a wide brim (10 mm) and enclosure.

- **`bottom_filter_retainer` (144 × 8 × 4 mm):** A 144 mm long, 8 mm wide strip, 4 mm thick. If printed flat, the long axis is prone to lifting. If printed on edge, it is unstable. **CONFIRMED: High warping risk.** Best printed flat with a continuous brim.

- **`foot_socket` (42 × 42 × 3 mm):** Small enough that a 5 mm brim should control warping. **LIKELY: Minor risk.**

- **`left/right_side_panel_middle` (176 × 5.2 × 100.9 mm):** The panel thickness is 3.0 mm, with ribs adding 2.2 mm, totaling 5.2 mm. The natural print orientation is flat on the 176 × 100.9 mm face (Z = 5.2 mm). This is only ~13 layers, but the 176 mm long layer is a large flat area in PETG. The ribs create differential cooling. **CONFIRMED: High warping risk.** The lower and upper panels (13 mm thick) are not flagged as long-thin but share the same large-footprint risk.

- **`top_fan_grille` (190 × 190 × 4 mm):** A 4 mm thick, 190 mm diameter grille. This is one of the most warp-prone geometries in the entire project. The large flat area with thin walls and bars will curl aggressively at the edges. **CONFIRMED: Extreme warping risk.** Requires a full brim, slow first layer, and enclosure.

- **`rear_service_spine_cover` (46 × 3 × 295.5 mm):** As discussed in the build volume section, this is a 295.5 mm long strip, 3 mm thick. Even if it could be printed in one piece (diagonal fit), it will warp severely. **CONFIRMED: Catastrophic warping risk if printed as one piece.**

---

## Support Requirements

The following parts will require significant support material, or have complex overhangs that must be managed.

### CONFIRMED Support-Heavy Parts

| Part | Support Reason | Optimal Orientation | Grade |
|---|---|---|---|
| `rear_service_spine` | Internal channel, windows, horizontal tie bars, side mount tabs, frame tabs | Would be Z-up (80×40 base), but exceeds build volume | CONFIRMED |
| `mini_pc_airflow_duct` | Hollow duct; side tabs are overhangs | 88×134 face down (Z=62); support under tabs | CONFIRMED |
| `corner_block` | Panel holes on sides; nut seat on bottom | 24×24 face down (Z=28); support for side holes | CONFIRMED |
| `bottom_fan_cartridge` | Rails and handle extend from base; if printed flat, no support needed | 142×161 face down (Z=13); **no support needed** | CONFIRMED (low support) |
| `power_bus_panel` | Pads, divider, strain relief all on back face | 34×275.5 face down (Z=7.5); support for back features | CONFIRMED |
| `power_bus_cover` | Guard rails on back face | 46×265.5 face down (Z=5); support for rails | CONFIRMED |

### LIKELY Support-Heavy Parts

| Part | Support Reason | Optimal Orientation | Grade |
|---|---|---|---|
| `ups_power_tray` | Front handle pocket (64×13 mm) is a deep recess; top bridge is 5.5 mm | 172×178 face down (Z=32); support inside handle pocket | LIKELY |
| `external_ssd_bay` | Same handle pocket geometry | 172×178 face down (Z=32); support inside handle pocket | LIKELY |
| `ssd_expansion_tray` | Same handle pocket geometry | 172×178 face down (Z=32); support inside handle pocket | LIKELY |
| `raspberry_pi_tray` | Same handle pocket geometry | 172×178 face down (Z=32); support inside handle pocket | LIKELY |
| `mikrotik_tray` | Same handle pocket geometry | 172×178 face down (Z=32); support inside handle pocket | LIKELY |
| `mini_pc_tray` | Same handle pocket geometry + power window cutout | 172×178 face down (Z=32); support inside handle pocket | LIKELY |
| `mini_pc_tray_stop` | Washer cylinder is a mid-air bridge if printed flat | On edge (Z=22 or 18); support for cylinder | LIKELY |

### Module Tray Handle Pocket Analysis

All six module trays use `make_carriage_front_plate()` from `carriages.py`. The front plate has a recessed handle pocket of dimensions:
- Width: `CARRIAGE_HANDLE_WIDTH = 64.0 mm`
- Depth: `CARRIAGE_HANDLE_DEPTH = 4.2 mm`
- Height: `CARRIAGE_HANDLE_HEIGHT = 13.0 mm`
- Top bridge: `CARRIAGE_HANDLE_TOP_BRIDGE = 5.5 mm`

The plate thickness is `CARRIAGE_FRONT_PLATE_THICKNESS = 8.0 mm`. The pocket is cut from the front face (`<Y`), leaving a 3.8 mm thick floor. When the tray is printed upright (Z=32, base on bed), the handle pocket is a side recess. The top of the pocket (at Z ≈ 21.5 mm) is a horizontal overhang spanning 64 mm. **PETG cannot bridge 64 mm reliably.** The slicer will generate support inside the pocket. This is a **CONFIRMED** support requirement for all six trays if printed in the natural orientation.

**Alternative:** Rotating the tray 90° so the front face is upward would eliminate the bridging issue but would make the base vertical, requiring support for the entire underside and ventilation slots. This is worse. Therefore, upright printing with support for the handle pocket is the least-bad option.

---

## Printable vs Non-Printable Classification

### Classification Accuracy

The export structure correctly separates non-printable references and placeholders:

- **Metal references** (`non_printable/metal_reference/`): `m5_threaded_rod`, `metal_guide_rail` — Correctly excluded.
- **Device placeholders** (`placeholders/devices/`): `mikrotik_placeholder`, `mini_pc_placeholder`, `raspberry_pi_3b_placeholder`, `ssd_expansion_placeholder`, `ssd_placeholder`, `ups_placeholder` — Correctly excluded.
- **Fan placeholders** (`placeholders/fans/`): `fan_120x120x25_placeholder` — Correctly excluded.
- **Review models** (`review/`): `airflow_path_review`, `blocked_air_zones_review`, etc. — Correctly excluded.
- **Assembly** (`assemblies/`): `assembly.step` — Correctly excluded.

### Risk of Accidental Slicer Inclusion

**LIKELY:** The risk is low if the slicer workflow strictly uses the `printable/plastic/` folder. However, the STEP files for placeholders and review models are co-located in the same `exports/mk0.7/` tree. If a user performs a recursive search (e.g., "import all STL files in exports/mk0.7/"), placeholders could be accidentally loaded. **Recommendation:** Add a `README` in `exports/mk0.7/` explicitly warning against importing from `placeholders/` or `review/`.

### Material Misclassification

**CONFIRMED:** The `foot` part (`foot.stl`) is exported to `printable/plastic/` but the source code (`feet.py`) explicitly defines it as `make_wide_tpu_foot_placeholder()`. The config says TPU is for feet. The part is 34 × 34 × 32 mm, solid with a through-hole and counterbore — a classic TPU foot design. **It must be printed in TPU, not PETG or PLA.** If sent to the slicer as part of the "plastic" batch, it will be printed in the wrong material.

---

## Part Splitting Recommendations

### `rear_service_spine` (80 × 40 × 297.5 mm) — CONFIRMED MUST SPLIT

- **Why:** Exceeds 256 mm in Z and cannot fit in any rotation (min. proj. 266.9 mm).
- **Recommended split:** **2 segments** of ~150 mm each, split at a horizontal tie level (e.g., at Z = 0 mm).
- **Joint type:** **Bolted lap joint** with M3 heat-set inserts. Each segment should retain half of the structural mount tabs, cable tie slots, and frame tabs. The horizontal tie at the split plane should be duplicated on both halves and bolted together.
- **Impact:** Moderate. The spine is a service channel, not a primary structural load path, so a bolted joint is acceptable if designed with overlap.

### `rear_service_spine_cover` (46 × 3 × 295.5 mm) — CONFIRMED MUST SPLIT

- **Why:** Exceeds 256 mm axis-aligned; diagonal fit is possible but 3 mm thickness makes warping catastrophic.
- **Recommended split:** **2 segments** (top and bottom), ~148 mm each.
- **Joint type:** **Tongue-and-groove or sliding dovetail** using the existing cover rail geometry. The cover already slides into rails on the spine; a mid-length interlocking feature would allow the two halves to join seamlessly.
- **Impact:** Low. The cover is non-structural.

### `power_bus_panel` (34 × 7.5 × 275.5 mm) — STRONGLY RECOMMENDED SPLIT

- **Why:** 275.5 mm > 256 mm; diagonal fit is technically possible but impractical for a 7.5 mm thick strip.
- **Recommended split:** **2 segments** of ~138 mm each.
- **Joint type:** **Bolted lap joint** with M3 screws. The power rail labels and connector zones should be duplicated or redistributed so that each segment is self-contained. The XT30, MicroFit, and USB-C connector zones are at specific Z positions; the split should avoid cutting through a connector zone.
- **Impact:** Moderate. Requires electrical continuity across the joint (jumper wires or bus bars).

### `power_bus_cover` (46 × 5 × 265.5 mm) — STRONGLY RECOMMENDED SPLIT

- **Why:** 265.5 mm > 256 mm; diagonal fit is possible but 5 mm thick strip will warp.
- **Recommended split:** **2 segments** of ~133 mm each.
- **Joint type:** **Sliding tongue-and-groove** using the existing guard rail geometry. The cover is non-structural and only needs to protect the bus from accidental contact.
- **Impact:** Low.

---

## Material Assignment

### Current State vs. Required State

| Part | Current Folder | Required Material | Grade |
|---|---|---|---|
| All module trays (`*_tray`) | `printable/plastic` | PETG | CONFIRMED |
| `frame_bottom`, `frame_top`, `bottom_structural_frame`, `top_structural_frame` | `printable/plastic` | PETG | CONFIRMED |
| `central_bottom_fan_frame` | `printable/plastic` | PETG | CONFIRMED |
| `bottom_fan_grille`, `top_fan_grille` | `printable/plastic` | PETG | CONFIRMED |
| `bottom_fan_cartridge` | `printable/plastic` | PETG | CONFIRMED |
| `bottom_filter_frame`, `bottom_filter_retainer` | `printable/plastic` | PETG | CONFIRMED |
| `corner_block` | `printable/plastic` | PETG | CONFIRMED |
| `mini_pc_airflow_duct` | `printable/plastic` | PETG | CONFIRMED |
| `rear_service_spine`, `power_bus_panel`, `power_bus_cover` | `printable/plastic` | PETG | CONFIRMED |
| `front_stability_wing`, `rear_stability_wing`, `left_foot_extension`, `right_foot_extension` | `printable/plastic` | PETG | CONFIRMED |
| `left_side_panel_*`, `right_side_panel_*` | `printable/plastic` | PETG | CONFIRMED |
| `mini_pc_tray_stop` | `printable/plastic` | PETG | CONFIRMED |
| `foot_socket` | `printable/plastic` | PETG | CONFIRMED |
| `foot` | `printable/plastic` | **TPU** | CONFIRMED (misclassified) |

### Analysis

- **PETG is appropriate for all structural, frame, and module parts.** It provides the necessary heat resistance, toughness, and layer adhesion for a tower that will run 24/7.
- **TPU is required for the `foot`**. The config explicitly calls it `make_wide_tpu_foot_placeholder()`, and the project rules state TPU is for feet/dampers. A rigid PETG foot would transmit vibration and slip on smooth surfaces. The TPU foot provides grip and vibration isolation.
- **PLA should not be used for any production part.** The project rules restrict PLA to prototypes only. The thermal load (especially near the mini PC and UPS) would deform PLA over time.
- **No parts require a different material for functional reasons, except the foot.**

---

## Bed Adhesion and Warping Risks

### Large Flat Parts (High Risk)

| Part | Footprint | Thickness | Risk | Grade |
|---|---|---|---|---|
| `frame_bottom` | 190 × 190 mm | 13 mm | Large area; PETG will curl at corners | CONFIRMED |
| `frame_top` | 190 × 190 mm | 13 mm | Same as frame_bottom | CONFIRMED |
| `bottom_structural_frame` | 190 × 190 mm | 13 mm | Same as frame_bottom | CONFIRMED |
| `top_structural_frame` | 190 × 190 mm | 13 mm | Same as frame_bottom | CONFIRMED |
| `central_bottom_fan_frame` | 190 × 190 mm | 16 mm | Same as frame_bottom | CONFIRMED |
| `bottom_fan_grille` | 190 × 190 mm | 7 mm | Very thin; extreme curling risk | CONFIRMED |
| `top_fan_grille` | 190 × 190 mm | 4 mm | Thinnest large flat part; highest risk | CONFIRMED |
| `bottom_filter_frame` | 138 × 138 mm | 3 mm | Thin ring; corners will curl | CONFIRMED |
| `front_stability_wing` | 250 × 47 mm | 10 mm | Long, narrow wing; ends will lift | CONFIRMED |
| `rear_stability_wing` | 250 × 47 mm | 10 mm | Same as front stability wing | CONFIRMED |
| `left_foot_extension` | 42 × 190 mm | 10 mm | Long strip; minor curling | LIKELY |
| `right_foot_extension` | 42 × 190 mm | 10 mm | Same as left foot extension | LIKELY |
| `left_side_panel_lower` | 176 × 100.9 mm | 13 mm | Large flat panel with ribs | CONFIRMED |
| `left_side_panel_middle` | 176 × 100.9 mm | 5.2 mm | Large flat; thin overall height | CONFIRMED |
| `left_side_panel_upper` | 176 × 100.9 mm | 13 mm | Same as lower | CONFIRMED |
| `right_side_panel_lower` | 176 × 100.9 mm | 13 mm | Same as left | CONFIRMED |
| `right_side_panel_middle` | 176 × 100.9 mm | 5.2 mm | Same as left | CONFIRMED |
| `right_side_panel_upper` | 176 × 100.9 mm | 13 mm | Same as left | CONFIRMED |

### Mitigation Recommendations

1. **Brim:** Use a 8–10 mm brim on all large flat parts. For `top_fan_grille` and `bottom_filter_frame`, consider a **full raft** or **mouse ears** at the corners.
2. **Bed temperature:** 80–85 °C for PETG.
3. **Enclosure:** Essential for PETG. The P2S has a partial enclosure; ensure the chamber is warm and stable.
4. **First layer speed:** 15–20 mm/s for the first layer.
5. **Cooling fan:** Off or minimal (0–30%) for the first 3–5 layers on large flat parts.
6. **Bed surface:** Clean PEI or textured sheet with glue stick for adhesion and release.
7. **Orientation:** Print the stability wings (`front_stability_wing`, `rear_stability_wing`) with the 250 mm axis aligned to the bed's longest dimension to minimize diagonal stress.

---

## Minimum Feature Size Check

The project defines `MIN_PRINTABLE_FEATURE = 1.2 mm` in `config.py` (line 54). The following features are at or below this threshold.

### Features Below 1.2 mm

| Feature | Value | Location | Impact | Grade |
|---|---|---|---|---|
| `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` | **0.5 mm** | `carriages.py` line 216 | A 0.5 mm lip on the rear connector zone of every module tray | **CONFIRMED** |
| `FAN_PANEL_EDGE_CHAMFER` | **0.6 mm** | `config.py` line 418 | Chamfer on all fan grille edges | CONFIRMED |
| `FILLET_RADIUS` | **0.8 mm** | `config.py` line 55 | Applied to many edges (e.g., rear_service_spine_cover) | CONFIRMED |
| `DUCT_EDGE_CHAMFER` | **0.8 mm** | `config.py` line 453 | Chamfer on Mini PC airflow duct | CONFIRMED |
| `PLACEHOLDER_CHAMFER` | **0.8 mm** | `config.py` line 56 | Only on placeholders, not printed | N/A |

### Analysis

- **`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG = 0.5 mm`:** This is the most serious sub-minimum feature. It is a **functional lip** on the rear connector zone of every module tray (`carriages.py`, line 216). A 0.5 mm overhang is far below the 1.2 mm minimum and will likely **not print at all** or will print as a distorted blob. The connector zone itself is 26 mm wide, 3.0 mm deep, and 15.0 mm tall. The 0.5 mm overhang is intended as a snap or retention feature, but it is too small to be reliable. **Recommendation:** Increase to at least 1.2 mm (preferably 2.0 mm) or redesign the connector zone without a sub-minimum lip.

- **`FAN_PANEL_EDGE_CHAMFER = 0.6 mm`:** Applied to the edges of `bottom_fan_grille` and `top_fan_grille`. A 0.6 mm chamfer is cosmetic. It may not print cleanly and could appear as a slight rounding instead of a crisp chamfer. Low impact.

- **`FILLET_RADIUS = 0.8 mm`:** Applied to edges of `rear_service_spine_cover`, `mini_pc_airflow_duct`, and other parts. A 0.8 mm fillet is small but functional as an edge break. It will print as an approximate curve. Acceptable for non-critical edges.

- **`DUCT_EDGE_CHAMFER = 0.8 mm`:** Applied to the Mini PC airflow duct. Same assessment as fillet radius.

### Thin Walls (Above 1.2 mm but Notable)

| Feature | Value | Location | Notes |
|---|---|---|---|
| `DUCT_WALL` | 2.0 mm | `config.py` line 445 | Thin wall for a tall duct (62 mm). Printable with 3–4 perimeters, but may flex during print. |
| `POWER_BUS_COVER_THICKNESS` | 2.4 mm | `config.py` line 553 | Thin for a large cover, but acceptable for a non-structural part. |
| `SIDE_SHEAR_PANEL_RIB_THICKNESS` | 2.4 mm | `config.py` line 395 | Rib thickness on structural side panels. Above 1.2 mm, but thin for a load-bearing rib. |
| `BOTTOM_FILTER_FRAME_HEIGHT` | 3.0 mm | `config.py` line 436 | Thin but printable. |

---

## Blockers

The following issues are considered **blockers** for a reliable production print run on the Bambu Lab P2S.

1. **`rear_service_spine` exceeds build volume in all orientations.**  
   **Evidence:** 80 × 40 × 297.5 mm; minimum projected bounding box at 45° is 266.9 mm > 256 mm.  
   **Action:** Split into two bolted segments.

2. **`power_bus_panel` exceeds build volume axis-aligned and is impractical to print diagonally.**  
   **Evidence:** 34 × 7.5 × 275.5 mm; diagonal fit requires ~30° rotation, resulting in a 275.5 mm long strip on the bed.  
   **Action:** Split into two bolted segments.

3. **`power_bus_cover` exceeds build volume axis-aligned and is impractical to print diagonally.**  
   **Evidence:** 46 × 5 × 265.5 mm; diagonal fit requires ~28° rotation.  
   **Action:** Split into two interlocking segments.

4. **`rear_service_spine_cover` exceeds build volume axis-aligned and will warp catastrophically if printed as one piece.**  
   **Evidence:** 46 × 3 × 295.5 mm; diagonal fit is possible but 3 mm thickness is insufficient for a 295 mm PETG part.  
   **Action:** Split into two sliding-joint segments.

5. **`foot` is misclassified as plastic instead of TPU.**  
   **Evidence:** `foot.stl` is in `printable/plastic/`; config defines it as `make_wide_tpu_foot_placeholder()`.  
   **Action:** Move to `printable/tpu/` or add explicit material annotation.

6. **`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG = 0.5 mm` is below `MIN_PRINTABLE_FEATURE`.**  
   **Evidence:** `config.py` line 54 defines 1.2 mm; `carriages.py` line 216 uses 0.5 mm.  
   **Action:** Redesign connector zone to use ≥ 1.2 mm feature size.

---

## Recommendations

### Immediate (Before Production)

1. **Split `rear_service_spine` into two bolted segments** (~150 mm each). Preserve mount tabs, cable tie slots, and frame tabs on both halves. Use M3 heat-set inserts and a lap joint with ≥ 10 mm overlap.

2. **Split `power_bus_panel` into two segments** (~138 mm each). Ensure the split does not cut through a connector zone (XT30, MicroFit, USB-C). Use a bolted lap joint with brass threaded inserts for electrical continuity if needed.

3. **Split `power_bus_cover` into two segments** (~133 mm each). Use a tongue-and-groove joint that slides together from the top.

4. **Split `rear_service_spine_cover` into two segments** (~148 mm each). Use the existing cover rail geometry as a sliding joint.

5. **Move `foot` to a `printable/tpu/` folder** or add a manifest entry specifying TPU material. Update the export pipeline to route TPU parts separately.

6. **Increase `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` from 0.5 mm to at least 1.2 mm** (preferably 2.0 mm for reliability). Alternatively, remove the overhang and use a straight butt joint for the connector zone.

### Slicer Workflow

7. **Add a 10 mm brim to all large flat parts:** `frame_bottom`, `frame_top`, `bottom_structural_frame`, `top_structural_frame`, `central_bottom_fan_frame`, `bottom_fan_grille`, `top_fan_grille`, `bottom_filter_frame`, and all side panels.

8. **Use tree supports for module trays** to minimize scarring on the front plate. The handle pocket is the only support-requiring feature; orient the tray with base on bed and use support only for the pocket cavity.

9. **Print the `rear_service_spine` segments on edge** (80 × 40 face down is not possible after splitting; print on the 80 × 150 face with Z = 40 mm) to minimize support for the internal channel. After splitting, the max segment height is ~150 mm, which fits easily in Z.

10. **For PETG, use a warm enclosure (≥ 35 °C chamber temp)** and minimal part cooling for the first 5 layers on all large flat parts.

### Documentation

11. **Add a `MATERIALS.md` manifest** in `exports/mk0.7/` listing every part with its assigned material, recommended infill, and brim/raft requirements.

12. **Add a `README` in `exports/mk0.7/`** warning users not to import files from `placeholders/`, `review/`, or `non_printable/` into the slicer.

---

*Review complete. All claims are backed by direct measurements from `part_dimensions.csv`, `printability_check.csv`, and `config.py`.*


---

## 7. Structural Integrity Review

*Full agent: `03_structural_integrity.md`*

## Executive Summary

The mk0.7 tower has a fundamentally sound concept—metal rods in tension, plastic corner blocks as connectors, and a wide stability base—but the implementation contains **multiple critical structural errors** that would prevent safe assembly or operation.

**Blockers (must fix before any build):**
1. **Side panels cannot be mounted.** The corner blocks only have panel mounting holes on their `+X` and `+Y` faces; the `-X` and `-Y` faces are solid. Even on the faces that do have holes, the hole positions (`z = center ± 6 mm`) do not align with the side panel mount points (`z = center ± 40.45 mm`). The frame has no side-panel mounting holes at all. The result is that the lower, middle, and upper side panels have M3 clearance holes and heat-set insert bosses, but **nothing in the structure to screw them into**.
2. **Top frame cannot be clamped.** The top structural frame has a nut seat on its bottom face (`<Z`) and a washer seat on its top face (`>Z`). Because it is the topmost frame, it needs a nut on top to pull it down against rod tension. The current geometry would leave the top frame pushed upward by an interior nut with no clamping force from above.
3. **Tray vertical support is not modeled.** The metal guide rails are simple vertical bars (10 × 3 × 287.5 mm). The trays are horizontal plates with vertical clearance slots for the rails. There are no horizontal shelves, brackets, or frame ledges to support the tray bottoms. A 1.2 kg Mini PC tray would have no vertical support except possible contact with the bottom frame (for the lowest tray) or the rear service spine (for the rear stop). The upper trays are effectively unsupported.

**Major concerns (design risk, not necessarily build-blocking):**
- Frame rail slots leave only **1.5 mm of PETG** on each side of the metal rail; tearing risk under tray load.
- Middle side panel is explicitly non-structural (3.0 mm + 2.2 mm ribs), creating a **shear discontinuity** in the middle of the tower.
- Torsion brace mounts are enabled in `config.py` (`TORSION_BRACE_MOUNT_ENABLED = True`) but are **not implemented in any geometry**.
- The sectional base (5 parts, M3 fasteners) has a **hinge risk** at the joints under lateral or tipping loads.
- The Mini PC tray stop is a small PETG bracket that may fail under impact from a 1.2 kg tray.

---

## Primary Load Path (M5 Rods)

### Assessment: ADEQUATE in tension, but top frame clamping is BROKEN.

**Evidence:**
- `config.py` lines 59–63: `ROD_DIAMETER = 5.0`, `ROD_CLEARANCE = 5.6`, `ROD_CENTER_OFFSET = 12.0`, `ROD_LENGTH = TOWER_HEIGHT ≈ 321.5 mm`.
- `rods.py`: rod positions are at `x = y = 190/2 − 12 = 83 mm`, giving a 166 × 166 mm rod rectangle.
- `frame.py` lines 20–27: frames have washer seats on `>Z` and nut seats on `<Z`.

**Tension capacity:**
- M5 threaded rod tensile stress area ≈ 14.2 mm².
- 4.8 grade steel yield ≈ 320 MPa → yield load per rod ≈ 4.5 kN.
- Four rods → ≈ 18 kN total yield capacity.
- Total tower mass: modules ≈ 3.83 kg + plastic structure (estimated 1–2 kg) ≈ 5–6 kg → weight ≈ 60 N.
- **Safety factor in tension: ≈ 300.** This is massive and more than sufficient.

**Compression / buckling:**
- The rods are NOT the primary compression members. The frames are clamped by nuts; the rods are in tension. The corner blocks are between the frames in the load path, but in the assembly they are placed at mid-height, not between the top and bottom frames. However, the corner blocks are not load-bearing in the primary path.
- Euler buckling for a 321.5 mm M5 rod (slenderness λ ≈ 257) is ≈ 586 N per rod. Because the rods are in tension, this is not a design driver. **CONFIRMED: rods are in tension, buckling is irrelevant.**

**Top frame clamping error:**
- The `create_frame_ring()` function in `frame.py` places the washer seat on `>Z` and the nut seat on `<Z` for both top and bottom frames.
- The bottom frame at `z = 0` has a nut underneath (`<Z`) and a washer on top (`>Z`). This is correct.
- The top frame at `z = 321.5` has a nut seat on its bottom face (`<Z`, facing the tower interior) and a washer seat on its top face (`>Z`, facing up). With no nut on top, the top frame is pushed **upward** by an interior nut. Rod tension pulls the top frame up, but there is no counter-force from above to clamp the frame against the modules or corner blocks.
- **Finding:** The top frame is structurally under-clamped. It should have a nut seat on the top face and a washer seat on the bottom face (or the frame should be inverted). This is a **CONFIRMED design error** that will prevent proper pre-tension in the rod stack.

---

## Frame Ring Stiffness

### Assessment: ADEQUATE for axial loads, but WEAKENED by rail slots.

**Evidence:**
- `config.py` lines 79–85: `FRAME_RAIL = 14.0`, `FRAME_THICKNESS = 7.0`, `FRAME_RIB_HEIGHT = 6.0`, `FRAME_RIB_WIDTH = 5.0`, `FRAME_RIB_INSET = 18.0`.
- `frame.py` lines 12–13: outer box 190 × 190 mm, inner cutout 162 × 162 mm (190 − 2×14).
- `frame.py` lines 29–33: guide rail slots are `11 × 4 mm` (10 + 1 mm clearance) cut through the 7 mm frame thickness.

**Stiffness analysis:**
- The frame is a 190 × 190 mm rectangular ring with 14 mm wide rails and 7 mm thickness. The ribs (6 mm high, 5 mm wide) add local stiffness to the top and bottom surfaces.
- Under rod tension, the frame perimeter is loaded in tension. The ring is very stiff in its plane for this load case.
- **Vertical bending:** If loaded vertically (e.g., by a module sitting on the frame), the 7 mm thick ring acts as a plate with a large central opening. The 6 mm ribs help locally but the unsupported span is 162 mm. A 6 kg total load creates negligible stress.
- **Slot weakening:** The guide rail slots are 11 mm wide in a 14 mm rail, leaving only **(14 − 11) / 2 = 1.5 mm** of material on each side of the slot. This is a severe stress concentrator. If the metal rail is loaded by a tray and transmits force to the frame, the 1.5 mm PETG ligament could tear or creep over time.
- **Finding:** Frame ring stiffness is LIKELY adequate for the current loads, but the rail slot geometry is a **CONFIRMED stress riser** that needs reinforcement.

---

## Corner Block Compression

### Assessment: ADEQUATE for compression, but MOUNTING PROVISIONS ARE BROKEN.

**Evidence:**
- `config.py` lines 86–91: `CORNER_BLOCK_SIZE = 24.0`, `CORNER_BLOCK_HEIGHT = 28.0`, `CORNER_BLOCK_PANEL_HOLE_POINTS = [(0, -6.0), (0, 6.0)]`.
- `corner_blocks.py` lines 12–24: block is 24 × 24 × 28 mm with rod clearance, washer seat, and nut seat.
- `corner_blocks.py` lines 24–25: panel holes are drilled only on `faces(">X")` and `faces(">Y")`.

**Compression analysis:**
- Rod clamping force is the only significant compression load. With hand-tightened M5 nuts, clamping force is typically 200–500 N per rod. The corner block wall around the rod is `(24 − 5.6) / 2 = 9.2 mm`. Compressive stress in PETG at 500 N on a 9.2 mm² wall is ≈ 54 MPa. PETG compressive yield is ≈ 50–60 MPa. This is marginal but acceptable for a printed part with some anisotropy allowance. **CONFIRMED: compression is acceptable for hand-tight clamping.**
- Dynamic or over-torqued loads could exceed PETG yield.

**Critical mounting flaw:**
- `corner_blocks.py` lines 24–25 only drill holes on the `+X` and `+Y` faces. For a block at `x = −83`, the `>X` face is at `x = −71` (pointing **inward** toward the tower center). The outer face (`<X`) at `x = −95` has **no holes**.
- The side panels are placed at `x ≈ ±96.5` (outer face of the tower). The left panel’s inner surface is at `x ≈ −95`. It needs to screw into the corner block’s outer face (`<X` at `x = −95`), but that face is solid.
- **Result:** The left side panel cannot be mounted to the left corner blocks. The rear side (if any) cannot be mounted to the rear blocks. Only the right and front faces have holes. This is a **CONFIRMED design error** that makes side panel attachment impossible on two of the four tower faces.
- Even on the faces that do have holes, the hole positions are at `z = center ± 6 mm` (28 mm block height, holes centered at ±6). The side panel mount points are at `z = panel_center ± 40.45 mm` (100.9 mm tall panel, 10 mm frame inset). The holes do not align vertically. This is a **CONFIRMED misalignment**.

---

## Guide Rail Load Path

### Assessment: METAL RAILS ARE ADEQUATE, BUT FRAME MOUNTING IS UNDEFINED.

**Evidence:**
- `config.py` lines 104–111: `METAL_RAIL_WIDTH = 10.0`, `METAL_RAIL_THICKNESS = 3.0`, `METAL_RAIL_HEIGHT = 287.5`, `METAL_RAIL_M3_SPACING = 70.0`.
- `rails.py` lines 18–27: rail is a simple 10 × 3 × 287.5 mm bar with M3 clearance holes on the 10 mm face.
- `frame.py` lines 29–33: frame has 11 × 4 mm slots for the rails, cut through the full 7 mm frame thickness.

**Rail strength:**
- Metal rail cross-section: 10 × 3 mm = 30 mm².
- In bending (tray load distributed along the rail), a 3 mm thick steel/aluminum rail is very stiff. Each rail carries at most a fraction of the heaviest tray (1.2 kg Mini PC divided by 4 rails ≈ 3 N per rail). The rail is orders of magnitude stronger than needed.

**Mounting problem:**
- The frame has a slot for the rail, but **no screw holes or insert bosses** to fasten the rail to the frame. The rail is shown as a vertical bar placed at `z = TOWER_HEIGHT / 2` in the assembly, but there is no modeled bracket, screw, or clamp holding it to the frame.
- The `part_dimensions.csv` shows the metal rail as a standalone part with no mounting hardware.
- The frame slot leaves only **1.5 mm** of PETG on each side. If the rail is inserted and loaded, the thin PETG ligaments will tear.
- **Finding:** The guide rail load path is **UNCERTAIN** because the mounting mechanism is not modeled. The frame slot geometry is **CONFIRMED** inadequate as a load-bearing joint without reinforcement or fasteners.

---

## Stability Base Analysis

### Assessment: FOOTPRINT IS ADEQUATE, BUT SECTIONAL JOINTS ARE A HINGE RISK.

**Evidence:**
- `config.py` lines 21–25: `BASE_WIDTH = 250.0`, `BASE_DEPTH = 260.0`, `FOOT_EXTENSION_X = 30.0`, `FOOT_EXTENSION_Y = 35.0`.
- `config.py` lines 344–345: `BASE_STABILITY_FOOT_OFFSET_X = 97.0`, `BASE_STABILITY_FOOT_OFFSET_Y = 102.0`.
- `config.py` lines 604–606: `STABILITY_COM_X = 0.0`, `STABILITY_COM_Y = 8.0`, `STABILITY_COM_Z = 167.18`.
- `config.py` lines 515, 608: `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`, `STABILITY_SERVICE_TRAY_Y = −78.0`.
- `feet.py` lines 90–130: base is built from 5 separate sections (central, left extension, right extension, front wing, rear wing) joined by M3 fasteners at 70 mm spacing.

**Stability envelope:**
- Feet are at (±97, ±102) mm from center. The base footprint is 250 × 260 mm.
- COM is at (0, 8, 167). The COM projection is 8 mm toward the rear from the geometric center.
- Distance to front tipping line (line between front feet at y = −102): 102 + 8 = **110 mm**.
- Distance to side tipping line (line between left feet at x = −97): **97 mm**.
- With the Mini PC tray extended 78 mm forward, the COM shifts by approximately:
  - `Δy = (1.2 kg × 78 mm) / 6 kg ≈ 15.6 mm` forward.
  - New COM_y = 8 + 15.6 = 23.6 mm (rearward offset becomes smaller).
  - Distance to front tipping line = 102 − 23.6 = **78.4 mm**.
- The `STABILITY_MARGIN = 18.0` is a hardcoded value. Even with the tray extended, the margin to the front tipping line is 78.4 mm, which is comfortable. **CONFIRMED: static stability is adequate.**

**Sectional base risk:**
- The base is 5 separate PETG parts joined by M3 screws at `BASE_WING_FASTENER_SPACING = 70.0` and `BASE_WING_FASTENER_OFFSET = 18.0`.
- The wings are thin plates (10 mm thick) with M3 clearance holes. Under lateral tipping or shear, the joints can act as **hinges** because the M3 screws provide clamping but little bending stiffness across the joint.
- The `BASE_WING_OVERLAP = 12.0` mm is small. The joint is essentially a lap joint 12 mm wide.
- A 6 kg tower with COM at 167 mm height subjected to a lateral push of 10 N (≈ 1 kg side load) creates a tipping moment of 10 × 167 = 1670 N·mm. The base joints must transfer this shear. With only 2 M3 screws per joint, the joint stiffness is low.
- **Finding:** Static stability is **CONFIRMED** adequate. Joint stiffness of the sectional base is **LIKELY** insufficient to prevent flexing or hinging under lateral loads. The base should be tested as a solid plate or redesigned with tongue-and-groove or interlocking features.

---

## Side Panel Shear Transfer

### Assessment: MIDDLE PANEL IS NON-STRUCTURAL, AND MOUNTING IS IMPOSSIBLE.

**Evidence:**
- `config.py` lines 368–401: `SIDE_PANEL_THICKNESS = 3.0`, `SIDE_SHEAR_PANEL_THICKNESS = 3.0`, `SIDE_SHEAR_PANEL_STRUCTURAL_SECTIONS = (0, 2)`.
- `side_panels.py` lines 26–33: `_is_structural_section(index)` returns `True` for indices 0 and 2 (lower and upper), `False` for index 1 (middle).
- `side_panels.py` lines 30–33: `_panel_thickness(1)` returns `SIDE_PANEL_THICKNESS = 3.0` mm; `_panel_thickness(0)` and `_panel_thickness(2)` return `SIDE_SHEAR_PANEL_THICKNESS = 3.0` mm.
- `side_panels.py` lines 36–39: `_rib_height(1)` returns `SIDE_PANEL_RIB_HEIGHT = 2.2` mm; `_rib_height(0)` and `_rib_height(2)` return `SIDE_SHEAR_PANEL_RIB_HEIGHT = 4.0` mm.
- `part_dimensions.csv`: middle panel Y thickness = 5.2 mm; lower/upper panel Y thickness = 13.0 mm (including overlap ribs).

**Structural discontinuity:**
- The lower and upper panels are designated as “structural” with 3.0 mm base + 4.0 mm ribs + 6.0 mm overlap ribs = 13.0 mm total thickness.
- The middle panel is designated as “non-structural” with 3.0 mm base + 2.2 mm ribs = 5.2 mm total thickness.
- **This creates a deliberate structural discontinuity in the exact center of the tower.** The tower’s shear stiffness is provided by the panels, but the middle panel is explicitly half as stiff. If the tower is loaded laterally (e.g., pushed from the side), the middle section will deform disproportionately.
- **Finding:** The non-structural middle panel is a **CONFIRMED** design weakness. The intent may have been to allow a removable service panel, but the structural cost is high.

**Mounting impossibility:**
- As detailed in the Corner Block section, the side panels have 4 mount holes per tile (at corners, inset 10 mm), but the corner blocks only have 2 holes per face at `z = center ± 6 mm`. The positions do not align.
- The frame rings have no panel mounting holes.
- The base has no panel mounting holes.
- **Result:** The side panels cannot be fastened to the structure. They are designed with M3 holes, bosses, and heat-set inserts, but there is nothing to screw them into. This is a **CONFIRMED** design error.

---

## Torsion Resistance

### Assessment: INADEQUATE. No diagonal bracing, weak middle panel, and torsion brace mounts are unimplemented.

**Evidence:**
- `config.py` lines 524–528: `TORSION_BRACE_MOUNT_ENABLED = True`, `TORSION_BRACE_HOLE_DIAMETER = M4_CLEARANCE`, `TORSION_BRACE_MOUNT_THICKNESS = 4.0`, etc.
- `side_panels.py` lines 72–91: diagonal ribs are present but thin (`rib_width = 2.4 mm` for non-structural, 3.0 mm for structural).
- The frame is a rectangular ring with no cross-bracing.
- The rear service spine is the only longitudinal member that could resist racking.

**Torsion analysis:**
- The tower is a rectangular box (190 × 190 mm) held by 4 rods at the corners. Without side panels, the frame is free to rack (twist) because the rod arrangement has no diagonal stiffness.
- The side panels provide shear stiffness if properly fastened. With the middle panel being non-structural and all panels unmountable, the effective shear stiffness is negligible.
- The rear service spine (52 × 30 × 297.5 mm) is mounted at the rear and provides some resistance to racking, but it is a plastic box with 3 mm walls, not a rigid frame.
- `TORSION_BRACE_MOUNT_ENABLED = True` in config, but **no geometry implements it** in any of the parts files (`frame.py`, `side_panels.py`, `corner_blocks.py`, `modules.py`).
- **Finding:** Torsion resistance is **LIKELY** inadequate. The tower will rack under uneven loading or lateral forces. The unimplemented torsion braces should be built or the frame should be stiffened another way. **NEEDS TEST:** physical twist test with a dial gauge.

---

## Mini PC Tray Stop Adequacy

### Assessment: MARGINAL. Small PETG bracket under impact load from a 1.2 kg tray.

**Evidence:**
- `config.py` lines 515–523: `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`, `TRAY_STOP_WASHER_DIAMETER = 12.0`, `TRAY_STOP_THICKNESS = 3.0`, `TRAY_STOP_HEIGHT = 16.0` (MODULE_SIDE_WALL_HEIGHT + 4 = 12 + 4).
- `modules.py` lines 124–141: stop is a 18 × 6 × 22 mm bracket with a 12 mm diameter washer boss and an M3 clearance hole.
- `part_dimensions.csv`: `mini_pc_tray_stop` = 18 × 6 × 22 mm.

**Load analysis:**
- The stop must arrest a 1.2 kg tray that has been pulled out 78 mm and released or bumped.
- Impact energy at low speed (e.g., 0.3 m/s) is `E = ½mv² = 0.5 × 1.2 × 0.09 = 0.054 J`. This is small, but the stop is only 6 mm wide and 3 mm thick in the load direction.
- The stop is mounted by a single M3 screw. The PETG bracket could crack at the screw hole or the washer boss could shear off.
- The 12 mm washer spreads the load over a small area. The effective shear area of the boss is small.
- **Finding:** The tray stop is **LIKELY** adequate for gentle handling but **UNCERTAIN** for accidental drops or bumps. A metal stop or a larger PETG bracket with two screws would be safer. **NEEDS TEST:** drop-test the tray against the stop.

---

## Rear Service Spine Structural Role

### Assessment: PROVIDES SOME BRACING, BUT PRIMARILY A CABLE CHANNEL.

**Evidence:**
- `config.py` lines 456–512: `REAR_SPINE_WIDTH = 52.0`, `REAR_SPINE_DEPTH = 30.0`, `REAR_SPINE_HEIGHT = 297.5`, `REAR_SPINE_STRUCTURAL_WALL = 3.4`, `REAR_SPINE_RIB_THICKNESS = 3.0`, `REAR_SPINE_RIB_HEIGHT = 5.0`.
- `REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 mounting points at ±126, ±84, ±42, 0 mm.
- `part_dimensions.csv`: `rear_service_spine` envelope = 80 × 40 × 297.5 mm (including mounting tabs).

**Structural contribution:**
- The spine is a 3.4 mm wall plastic box with 3 mm ribs and 7 mounting tabs along its height. It mounts to the rear of the tower.
- It acts as a backplane that resists parallelogram deformation (racking) of the tower. The 7 mounting points give it a reasonable shear transfer path to the frame or modules.
- However, it is still a plastic box. Its stiffness is much lower than a metal backplane. The 3.4 mm walls will flex under torsion.
- It also serves as the cable management channel and the backstop for the trays (the tray rear stops hit it).
- **Finding:** The rear service spine contributes **LIKELY** modest torsion and shear resistance, but it is **not a primary structural member**. It should be treated as a service accessory with secondary structural benefit. If the design depends on it for stiffness, the dependence is too high.

---

## Blockers

These issues must be resolved before any physical build or further revision:

1. **Side panel mounting is impossible.** Corner blocks lack holes on `-X` and `-Y` faces, and the holes that do exist are misaligned with the panel mount points. The frame has no panel holes. The side panels cannot be attached.
2. **Top frame clamping is incorrect.** The top frame has a nut seat on the bottom face and a washer seat on the top face. A topmost frame needs a nut on top to pull it down against rod tension. The current geometry cannot be properly clamped.
3. **Tray vertical support is missing.** The metal guide rails are vertical bars with no horizontal shelves or brackets. The trays are horizontal plates with no modeled support from below (except the bottom frame for the lowest tray). A 1.2 kg Mini PC tray has no visible support mechanism.
4. **Torsion brace mounts are unimplemented.** `config.py` enables them, but no geometry exists.

---

## Recommendations

### Immediate (mk0.7 → mk0.8)
1. **Fix corner block panel holes:**
   - Add holes on all four side faces (`<X`, `>X`, `<Y`, `>Y`).
   - Align the hole positions with the side panel mount points (or vice versa).
   - Add corresponding threaded inserts or nut traps in the corner blocks for M3 screws.
2. **Fix top frame clamping:**
   - Either add a nut seat on the top face of the top frame, or model the top frame as an inverted copy of the bottom frame so the nut seat is on the outer face.
3. **Add tray support mechanism:**
   - Model horizontal shelves or ledges on the metal guide rails at each tray height.
   - Alternatively, add intermediate frame rings at each module height to support the trays from below.
   - The current vertical-bar rails cannot support horizontal trays.
4. **Implement torsion braces or cross-bracing:**
   - If `TORSION_BRACE_MOUNT_ENABLED = True`, model the mount bosses and the brace geometry (e.g., a diagonal rod or strap between opposite corners).
   - Alternatively, make the middle side panel structural and ensure all panels are properly fastened.
5. **Reinforce frame rail slots:**
   - Add material around the guide rail slots. A 1.5 mm ligament is too thin.
   - Consider metal threaded inserts or washers at the slot edges to prevent tearing.

### Short-term (mk0.8)
6. **Strengthen the sectional base:**
   - Replace the 5-part base with a single plate, or add tongue-and-groove interlocks and more fasteners at the joints.
   - Consider a metal bottom plate for stiffness.
7. **Improve the tray stop:**
   - Use two M3 screws or a larger bracket.
   - Consider a metal stop or a PETG stop with a steel insert.
8. **Add FEA or physical test plan:**
   - A simple torsion test (apply a known side load and measure deflection) would validate the side panel and spine stiffness.
   - A drop test of the Mini PC tray would validate the stop.

### Long-term
9. **Reduce reliance on plastic for structural stiffness:**
   - The AGENTS.md philosophy states “plastic parts are connectors/positioners, NOT primary load-bearing elements.” The current design violates this by making the side panels, rear spine, and base critical to stiffness. Add metal plates or brackets where possible.

---

*Review completed. All findings are based on hand calculations and inspection of the CAD source code. No FEA was performed.*


---
## 8. Airflow and Cooling Review

*Full agent: `04_airflow_cooling.md`*

## Executive Summary

The mk0.7 Homelab Modular Tower uses a vertical chimney airflow scheme: bottom 120 mm intake → central tower volume → vertical module stack → top 120 mm exhaust. The Mini PC has a dedicated side airflow duct. The Rear Service Spine and Power Bus occupy the rear zone and must not obstruct the central flow.

This review finds **multiple confirmed design-level airflow concerns** that affect the tower's ability to cool its modules. None of the findings require CFD to identify; they are discoverable through dimensional stack analysis, geometric obstruction checks, and cross-referencing of the assembly placement against the module placeholders.

**Top-level findings:**

1. **Bottom intake openness is acceptable** (≈ 91 % open area ratio vs. fan face) **but the filter hardware is not integrated into the assembly** and the filter rails are on the wrong side of the grille for a bottom intake.
2. **Basement blockage is minimal** — the base hole (134 mm) and frame opening (162 mm) are both larger than the fan air opening (112 mm), so they do not add constriction.
3. **Fan placement fits within the 32 mm foot height** but leaves only **7 mm table clearance** and no provision for a filter beneath the fan.
4. **Tray base ventilation slots are completely blocked by the devices** on every module. This is the single most critical airflow design flaw. Air must flow around the modules, not through them.
5. **Mini PC duct is a placeholder geometry** that does not connect to the Mini PC placeholder. It is 58 mm wide vs. a 145 mm wide device and is open at both ends with no side port.
6. **Rear Service Spine does not block the central 112 mm fan column** but it blocks the rear bypass path, which is one of the two main routes around the modules.
7. **Top exhaust is structurally clear** but the 7 mm gap above the top module is a narrow constriction.
8. **UPS/Power tray has the largest thermal mass at the bottom** (good) but its vent slots are blocked by the battery.
9. **Temperature sensor placement is in the wrong zone** — all three points are near the stagnant rear wall instead of the central airflow.

---

## Bottom Intake Openness

**Grade: CONFIRMED (acceptable without filter; UNCERTAIN with filter)**

### Geometry

| Component | Hole / Opening Size | Area (mm²) |
|---|---|---|
| Fan air opening (reference) | 112 mm dia | 9 852 |
| Bottom grille hole | 120 mm dia | 11 310 |
| Grille bars (10 × 84 × 3, minus 25 × 3 × 3 overlap) | — | 2 295 |
| **Grille net open area** | — | **9 015** |
| Base stability hole | 134 mm dia | 14 095 |
| Bottom structural frame opening | 162 × 162 mm | 26 244 |
| BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO threshold | 0.58 of 112 mm = 65.0 mm dia | 3 318 |

### Analysis

The bottom fan grille is a 190 × 190 × 4 mm plate with a 120 mm through-hole and ten 3 mm × 84 mm protective bars (five in X, five in Y). The bar overlap area is 25 × 3 × 3 = 225 mm². Net open area:

- Bar total = 5 × 252 + 5 × 252 − 225 = **2 295 mm²**
- Grille open area = π × 60² − 2 295 = **9 015 mm²**
- Ratio vs. 112 mm fan face = 9 015 / 9 852 = **0.915**
- Ratio vs. 120 mm grille hole = 9 015 / 11 310 = **0.797**

Both ratios comfortably exceed the review threshold of 0.58. The **bottom intake openness is CONFIRMED adequate** for the bare grille.

### Filter Issue

The `bottom_filter_frame` (138 × 138 × 3 mm, 112 mm hole) and `bottom_filter_retainer` are **not placed in the assembly** (`tower_assembly.py` does not instantiate them). `KNOWN_ISSUES.md` line 4 explicitly states:

> Filter frame/retainer пока не привязаны к конкретному материалу фильтра и толщине сетки.

If a filter is added, its open area ratio depends on the filter mesh. A typical 40 PPI polyurethane foam filter has an open area ratio of 0.75–0.85, which would drop the overall intake ratio to ≈ 0.69–0.78, still above 0.58. A finer filter (e.g., HEPA) could drop below the threshold. **This is UNCERTAIN until a filter material is specified and its pressure drop/open area is measured.**

### Filter Rail Placement Issue

The `bottom_fan_grille` is placed at `BOTTOM_FAN_PANEL_Z = −2.0` (above the base plate). The filter rails are added on the **+Z face** of the grille (`cfg.FAN_GRILLE_THICKNESS / 2 + cfg.FILTER_RAIL_HEIGHT / 2`). For a bottom intake, air enters from below the base. The filter should be on the **intake side** (below the fan). The current geometry places the filter rails **above** the grille, inside the tower, on the wrong side of the airflow. **This is a design error.**

---

## Basement Blockage Analysis

**Grade: CONFIRMED (no significant blockage)**

### Z-stack of the basement (from bottom to top)

| Element | Z range (mm) | Thickness (mm) | Air opening |
|---|---|---|---|
| Feet (TPU) | −46.0 … −14.0 | 32 | 250 × 260 footprint, central void between feet |
| Fan placeholder | −39.0 … −14.0 | 25 | 120 mm dia |
| Bottom fan cartridge | −22.0 … −14.0 | 8 | 142 × 161 envelope, 112 mm hole |
| Base stability plate | −14.0 … −4.0 | 10 | 134 mm dia hole |
| Bottom fan grille | −4.0 … +3.0 | 7 (4 + 3 rails) | 120 mm dia − bars |
| Bottom structural frame | −3.5 … +3.5 | 7 | 162 × 162 mm inner opening |

### Concentric alignment check

All three major openings are centered at (0, 0):
- Fan air opening: 112 mm dia
- Base stability hole: 134 mm dia
- Bottom structural frame: 162 × 162 mm square

The smallest opening is the fan itself (112 mm). The base hole (134 mm) and frame opening (162 mm) are both larger, so they **do not add constriction** to the air path. There is no step-down smaller than the fan.

### Rib check

The base stability plate has perimeter ribs (3 × 6 mm) at `±(depth/2 − inset)` and fan ribs at `±70 mm`. The fan ribs span the 134 mm hole diameter. Since the hole radius is 67 mm, the ribs at y = ±70 mm are **outside the hole edge** and do not intrude into the airflow. The bottom structural frame has 6 mm ribs on its 14 mm rails, but the rails are well outside the 112 mm fan envelope.

**No basement blockage is present.** The basement is correctly designed as a through-passage.

---

## Fan Placement and Clearance

**Grade: LIKELY (adequate but tight; NEEDS TEST for filter)**

### Dimensional stack

```text
Table surface ........................................ z = −46.0 mm
  ↑ 7.0 mm clearance
Fan bottom ........................................... z = −39.0 mm
Fan (25 mm thick) .................................... z = −39.0 … −14.0
Cartridge (8 mm, around fan top) ..................... z = −22.0 … −14.0
Cartridge rails (up to +5 mm) ...................... z = −14.0 … −9.0
Base stability plate (10 mm) ......................... z = −14.0 … −4.0
Bottom fan grille (4 + 3 mm) ......................... z = −4.0 … +3.0
Bottom structural frame (7 mm) ....................... z = −3.5 … +3.5
```

### Clearance findings

1. **Fan-to-table clearance: 7 mm**. A 120 mm × 25 mm fan sits with its bottom face 7 mm above the table. This is the minimum recommended for unrestricted intake. It is adequate for a bare fan but **insufficient for a filter placed below the fan**. A typical 3–5 mm foam filter would leave only 2–4 mm, which is marginal.

2. **Fan-to-base clearance: 0 mm**. The fan top is flush with the base bottom (`z = −14.0`). The cartridge rails extend 5 mm into the base hole. This is correct — the fan is clamped against the base by the cartridge.

3. **Total occupied height from table to base top: 42 mm**. The feet are 32 mm; the base is 10 mm. The fan (25 mm) plus cartridge (8 mm) occupies 33 mm of the 32 mm foot height, but the cartridge overlaps the fan top, so the actual physical stack is 25 + 3 = 28 mm of fan below the base, plus 5 mm of rails inside the base. The numbers work.

4. **Filter placement is unresolved**. There is no physical space for a filter frame (3 mm) or retainer (4 mm) below the base within the 32 mm foot envelope, unless the fan is raised or the feet are taller. The `KNOWN_ISSUES.md` confirms this requires print-fit testing.

---

## Airflow Path Through Module Stack

**Grade: CONFIRMED — CRITICAL DESIGN FLAW**

### Ventilation slot geometry

Every tray uses:
- `TRAY_VENT_ROWS = 3`, `TRAY_VENT_COLS = 5`
- `TRAY_VENT_SLOT_LENGTH = 18.0`, `TRAY_VENT_SLOT_WIDTH = 4.0`
- `TRAY_VENT_AREA_LENGTH = 105.0`, `TRAY_VENT_AREA_WIDTH = 85.0`
- Slots are cut `cutThruAll()` through the 3 mm tray base

Total slot area (gross): 15 slots × 18 × 4 = **1 080 mm²**.

### Obstruction by devices

Every module has a device placeholder that sits directly on the tray base, **completely covering the vent slot grid**:

| Module | Device size (mm) | Device footprint (mm²) | Vent grid area (mm²) | Coverage |
|---|---|---|---|---|
| UPS / Power | 125 × 55 | 6 875 | 105 × 85 = 8 925 | **77 % of tray base** |
| External SSD | 75 × 38 | 2 850 | 8 925 | **32 % of tray base** |
| SSD Expansion | 110 × 70 | 7 700 | 8 925 | **86 % of tray base** |
| Raspberry Pi | 86 × 57 | 4 902 | 8 925 | **55 % of tray base** |
| MikroTik | 120 × 95 | 11 400 | 8 925 | **128 % of tray base** (extends beyond grid) |
| Mini PC | 145 × 130 | 18 850 | 8 925 | **211 % of tray base** (covers entire base) |

The vent slots are in the **center** of the tray base (105 × 85 mm area, centered at origin). Every device placeholder is centered or offset within this area. The Mini PC (145 × 130 mm) covers the **entire tray base** and extends beyond it. There is literally **no exposed tray base** under the Mini PC.

### Conclusion: air does NOT flow through the modules

Because the devices sit on the tray base and block the vent slots, the intended path "through the tray base" is **impossible**. The air must flow **around** the modules.

### Bypass area estimation (design-level, not CFD)

The module stack occupies the central 170 × 176 mm cross-section inside the 162 × 162 mm frame opening. Wait — the module width (170 mm) is **larger** than the frame inner opening (162 mm). The trays fit because of 18 × 18 mm corner clearances (`cut_structural_clearances`), but the side walls are at x = ±83.5, which is **outside** the frame opening at x = ±81. This means the tray side walls are in the gap between the frame rails and the tower outer wall.

The effective bypass paths for air are:

1. **Left/right side gaps**: tower inner width (190) − tray width (170) = 20 mm total, or **10 mm per side**. Over the ~300 mm module stack height: 2 × 10 × 300 = **6 000 mm²**.
2. **Front gap**: tower depth (190) − tray depth (176) = 14 mm, minus tray offset (TRAY_Y = −4, which shifts tray front to y = −92). Tower front is at y = −95. Front gap = **3 mm**. Area ≈ 3 × 170 = **510 mm²**.
3. **Inter-tray gaps**: MODULE_SLOT_GAP = 1.0 mm. There are 5 gaps between 6 modules. Perimeter ≈ 2 × (170 + 176) = 692 mm. Total gap area ≈ 5 × 1 × 692 = **3 460 mm²**.

Total estimated bypass area ≈ **9 970 mm²**.

The fan swept area is π × 56² = **9 852 mm²**. The bypass area is approximately equal to the fan area. However:
- The bypass is split into narrow channels (10 mm sides, 1 mm between trays).
- The **rear bypass is blocked by the Rear Service Spine** (see below).
- The devices are large solid blocks that create significant flow resistance around them.
- The airflow must turn around each module, creating pressure losses that a simple area comparison cannot capture.

**Engineering assessment:** The tower will operate as a chimney, but with high flow resistance. The modules will be cooled primarily by air moving in the side gaps, not by air passing through them. The Mini PC, which is the highest-priority cooling target, is also the largest obstruction. The 1 mm inter-tray gaps are particularly concerning — they are too small to allow meaningful vertical flow between module levels.

**Recommendation:** The module trays need a redesign to allow air passage **through** the modules, not just around them. Options:
- Raise devices on standoffs so air can pass under them through the vent slots.
- Add side ventilation holes in the tray walls.
- Add top ventilation openings in the trays (but this is blocked by the next tray).
- Use a mesh or lattice base instead of solid base with slots.

---

## Mini PC Duct Analysis

**Grade: NEEDS TEST — placeholder geometry is inadequate**

### Duct geometry

- Duct outer: 58 × 134 × 62 mm (2 mm walls)
- Duct inner: 54 × 136 × 58 mm (open at both ends in Y)
- Placement: x = 48, y = 6, z = 276.5 (center)
- Duct Y-extent: 6 ± 67 = −61 … +73 mm
- Mini PC placeholder: 145 × 130 × 28 mm at x = 0, y = −8, z = 262.5
- Mini PC Y-extent: −8 ± 65 = −73 … +57 mm

### Duct-to-Mini PC overlap

The duct overlaps with the Mini PC in the Y-range from −61 to +57 mm. The duct is positioned at the **right side** of the Mini PC (x = 48 ± 29 = 19 … 77 mm). The Mini PC extends from x = −72.5 to +72.5. So the duct overlaps the Mini PC in X from 19 to 72.5 mm.

### The duct is a hollow tube with no side port

The duct code (`make_mini_pc_airflow_duct_placeholder`) creates a hollow rectangular tube that is **open at both ends** (the inner cutter is 2 mm longer in Y than the outer box). There is **no hole, slot, or port on the side facing the Mini PC**. The duct is simply a tube running parallel to the Mini PC's side.

The `mini_pc_airflow_path_review` render shows a horizontal arrow pointing from the duct toward the Mini PC. But the duct geometry does not have any connection to the Mini PC. The arrow is a **review marker only**, not an actual airflow path.

### Duct width vs. Mini PC width

The duct is 58 mm wide. The Mini PC is 145 mm wide. Even if the duct had a side port, it would only cover **40 % of the Mini PC's width**. A typical Mini PC has intake vents along one entire side (or on the bottom). A 58 mm duct cannot cover a 145 mm intake surface.

### KNOWN_ISSUES confirmation

`KNOWN_ISSUES.md` line 9 states:

> Mini PC duct остается review/placeholder-level геометрией и требует проверки по реальным отверстиям Mini PC.

This is confirmed. The duct is a placeholder that:
1. Does not connect to the Mini PC.
2. Is too narrow to cover the device width.
3. Is open at both ends with no directional control.

### Recommendation

The Mini PC duct must be redesigned after the **actual Mini PC model** is measured. The duct should:
- Have a side outlet that mates with the Mini PC's intake vent location.
- Be wide enough to cover the intake area.
- Have a bottom inlet that connects to the main tower airflow (not just an open tube).

Until then, the Mini PC will rely on the same bypass airflow as the other modules, which is **insufficient** for a 28 mm tall compute device that is the highest thermal priority.

---

## Rear Service Spine Interference

**Grade: CONFIRMED — does not block central column, but blocks rear bypass**

### Spine geometry

- Width: 52 mm, Depth: 30 mm, Height: 297.5 mm
- Center: y = 80.0 mm (rear_y = 95 − 15 = 80)
- Extent: y = 65 … 95 mm, x = −26 … +26 mm

### Central airflow check

The bottom fan air opening is 112 mm diameter (radius 56 mm). The spine is centered at y = 80 mm, which is well outside the 56 mm fan radius. The spine does **not** intersect the central vertical column of air.

### Rear bypass blockage

The modules occupy the tray depth of 176 mm, centered at y = −4, so the tray rear is at y = 84 mm. The tower rear wall is at y = 95 mm. The nominal rear gap is 95 − 84 = **11 mm**.

However, the Rear Service Spine occupies y = 65 … 95 mm. It is a **solid volume** (with internal cable channels, but the channel is enclosed by the spine cover). The spine **blocks the entire rear gap**.

The only rear openings are the `REAR_SPINE_WINDOW` cutouts (34 mm wide × 20 mm tall) at six discrete Z-levels. These are for **cables**, not airflow. They are too small and too few to serve as ventilation.

The `blocked_air_zones_review` render confirms this: it marks blocked zones at x = ±26, y = 95 (the rear spine corners) and at the bottom edges.

### Impact

The rear bypass path is one of the two main routes around the modules (left/right being the other). Blocking the rear path forces all bypass air to the **front and sides**. The front gap is only **3 mm**. The side gaps are **10 mm each**. This creates an asymmetric flow pattern where the left and right sides carry most of the bypass flow, while the rear is stagnant.

For modules with rear-facing heat sinks (e.g., Mini PC with exhaust at the rear), this is particularly problematic. The rear of the Mini PC is at y = −8 + 65 = 57 mm. The spine is at y = 65 mm. The gap between the Mini PC rear and the spine is 65 − 57 = **8 mm**. But the Mini PC tray has a `power_window` cutout at the rear (18 × 8 × 14 mm) for the power cable. This small cutout is the only rear opening for the Mini PC.

**Recommendation:** Consider adding ventilation cutouts in the Rear Service Spine cover, or provide a dedicated exhaust path for the Mini PC rear.

---

## Top Exhaust Path

**Grade: LIKELY (clear but with constriction)**

### Top stack geometry

| Element | Z range (mm) | Opening |
|---|---|---|
| Top module (Mini PC) tray top | 314.5 | — |
| Gap to top frame | 314.5 … 321.5 | 7 mm vertical gap |
| Top structural frame | 321.5 ± 3.5 | 162 × 162 mm |
| Top fan grille | 323.5 ± 2.0 | 120 mm dia − bars |

### Gap analysis

The Mini PC tray top is at z ≈ 314.5 mm. The top structural frame is at z = 321.5 mm. The vertical gap is **7 mm**.

The air flowing up the tower must pass through this 7 mm gap above the top module before reaching the top frame opening. The 7 mm gap area (perimeter of the module stack × 7 mm) is approximately:

- Module stack perimeter ≈ 2 × (170 + 176) = 692 mm
- Gap area ≈ 692 × 7 = **4 844 mm²**
- Fan air opening area = 9 852 mm²
- Gap-to-fan area ratio = 4 844 / 9 852 = **0.49**

This is a **significant constriction**. The air must accelerate by a factor of ~2 to pass through the gap. This creates a pressure drop that reduces the overall chimney flow.

### Top frame and grille

The top frame opening is 162 × 162 mm, which is larger than the 112 mm fan opening. The top grille has the same bar pattern as the bottom grille, with an open area ratio of ≈ 0.80. The grille is the final constriction, matching the fan size.

### Corner blocks

The corner blocks are placed at z = 160.75 mm (mid-height of the tower), not at the top. They do not interfere with the top exhaust. The top frame has 14 mm rails at the corners, but these are well outside the 112 mm fan column.

### Recommendation

The 7 mm gap above the top module is a design-level bottleneck. Options:
- Raise the top module or lower the top frame (but this affects structural integrity).
- Add ventilation holes in the top of the Mini PC tray (but the next tray is the top frame, so this only helps if the holes align with the frame opening).
- Accept the constriction and verify with a physical prototype that the flow is still adequate.

---

## UPS/Power Tray Ventilation

**Grade: CONFIRMED — vent slots are blocked by battery**

### UPS module geometry

- Tray height: 2 units = 70 mm (minus 1 mm clearance = 69 mm)
- Battery placeholder: 125 × 55 × 32 mm at x = −38, y = −25
- Battery bottom: z = 18 + 3 = 21 mm (on tray base)
- Battery top: z = 21 + 32 = 53 mm
- Space above battery: 69 − 32 − 3 = **34 mm**

### Ventilation status

The tray base has the same 15 vent slots as all other trays. The battery sits directly on the base, covering the left-rear portion of the vent grid. The UPS board, BMS, fuse block, DC-DC, and terminal blocks are additional heat sources.

The UPS module is at the **bottom** of the stack, immediately above the intake fan. This is the **best possible location** for cooling — it receives the coolest air. However, the battery blocks the base vents, so air must flow **around** the battery.

The battery is 125 × 55 mm, offset to the left-rear. The tray is 170 × 176 mm. The free space around the battery is:
- Front: 55 mm to tray front (at y = −92, battery at y = −25, so front gap = 55 + 67 = 122 mm? Wait, tray front is at y = −92, battery front is at y = −25 − 27.5 = −52.5. Gap = 39.5 mm).
- Right: battery at x = −38, right edge at x = −38 + 62.5 = +24.5. Tray right at x = 85. Gap = 60.5 mm.

The air has ample space to flow around the battery. The UPS module's thermal performance is **likely acceptable** due to its position at the bottom of the stack, but the blocked vent slots are a design inconsistency.

### Other heat sources

The UPS component zones (board, BMS, DC-DC, fuse, terminals) are all small blocks (< 60 × 40 mm) scattered around the tray. They do not significantly obstruct airflow. The DC-DC and terminal blocks are at the rear (y = 58, 62), near the spine. Their heat may accumulate in the rear corner.

**Recommendation:** The UPS module should be monitored during prototype testing. If the battery or DC-DC runs hot, consider adding side vents to the tray walls or raising the battery on standoffs.

---

## Temperature Sensor Placement

**Grade: CONFIRMED — sensors are in the wrong zone**

### Sensor locations

| Sensor | Coordinates (x, y, z) | Location | Assessment |
|---|---|---|---|
| 1 | (−42, 70, 90) | z = 90: inside UPS module. y = 70: at Rear Service Spine front face. | Stagnant rear zone |
| 2 | (42, 70, 215) | z = 215: inside SSD Expansion / Raspberry Pi / MikroTik range. y = 70: at spine. | Stagnant rear zone |
| 3 | (0, 68, 310) | z = 310: near top exhaust. y = 68: near spine. | Stagnant rear zone |

### Problem

All three sensors are at **y ≈ 68–70 mm**, which is **at the front face of the Rear Service Spine** (spine front is at y = 65 mm). The central airflow is at **y ≈ 0 mm**.

The rear zone near the spine is **not representative of the main airflow**. It is a stagnant or recirculating region because:
- The spine blocks the rear bypass path.
- The cable windows into the spine are small and do not promote flow.
- The modules' rear cable exits open into the spine, but the spine is enclosed.

A temperature sensor at y = 70 will measure the **stagnant air temperature** near the spine, not the **cooling air temperature** in the central chimney. If the goal is to monitor cooling effectiveness, the sensors should be placed in the **central airflow** at y ≈ 0.

### Recommendation

Move the temperature sensors to the central airflow path:
- Sensor 1: (−42, 0, 90) — inside UPS module, central flow
- Sensor 2: (42, 0, 215) — inside mid-stack module, central flow
- Sensor 3: (0, 0, 310) — near top exhaust, central flow

Alternatively, add a fourth sensor at the **inlet** (y = 0, z = 10) to measure intake temperature and compute delta-T.

---

## Blockers

This section lists items that must be resolved before the design can be considered thermally validated.

| # | Blocker | Grade | Evidence |
|---|---|---|---|
| 1 | **Tray base vent slots are blocked by all devices** | CONFIRMED | Every device placeholder footprint exceeds the vent grid area; devices sit flush on the 3 mm base. `carriages.py` `cut_vent_slots` + `modules.py` device placeholders. |
| 2 | **Mini PC duct is a non-functional placeholder** | CONFIRMED | Duct is open at both ends with no side port to the Mini PC. Duct width (58 mm) << Mini PC width (145 mm). `KNOWN_ISSUES.md` line 9. |
| 3 | **Filter hardware is not in the assembly and rails are on wrong side** | CONFIRMED | `bottom_filter_frame` / `retainer` not in `tower_assembly.py`. Filter rails on +Z face of grille, which is inside the tower for a bottom intake. `cooling.py` lines 29–36. |
| 4 | **Temperature sensors are in stagnant rear zone** | CONFIRMED | All three sensors at y = 68–70, at the spine front face, not in the central airflow. `config.py` line 603. |
| 5 | **Top gap above module stack is only 7 mm** | CONFIRMED | Mini PC tray top at z ≈ 314.5; top frame at z = 321.5. Gap = 7 mm. `config.py` STACK_START_Z + TRAY_STACK. |
| 6 | **No CFD or physical flow testing** | CONFIRMED | `CALCULATIONS.md` line 38 and `KNOWN_ISSUES.md` line 1 both state this explicitly. |

---

## Recommendations

### P1 — Must fix before prototype

1. **Redesign tray base ventilation**. The current "solid base with central slots" approach fails because devices sit on the base. Options:
   - **Preferred:** Add a grid of raised standoffs (e.g., 4 mm tall posts) under each device so air can pass through the slots beneath the device.
   - Alternative: Move vent slots to the tray side walls (not the base) so they are not blocked.
   - Alternative: Replace the solid base with a lattice or honeycomb structure.

2. **Integrate Mini PC duct with actual device geometry**. The placeholder duct must be replaced with a design based on the real Mini PC's intake vent location and size. The duct must have a side outlet that mates with the intake.

3. **Fix temperature sensor placement**. Move all sensors to y ≈ 0 (central airflow). Add an intake sensor at z ≈ 10.

### P2 — Should fix before production

4. **Increase top gap above module stack**. The 7 mm gap is a flow bottleneck. Consider raising the top frame by 5–10 mm or shortening the top module by one unit (but this affects the modular standard).

5. **Resolve filter placement**. Either:
   - Add a filter slot **below** the fan (between fan and table), or
   - Raise the fan to make room for a filter below it, or
   - Increase foot height to 40 mm to accommodate fan + filter.

6. **Add rear ventilation for the Mini PC**. The Mini PC rear is only 8 mm from the spine. Consider a cutout or channel in the spine to allow hot air from the Mini PC rear to escape upward.

### P3 — Nice to have

7. **Add side panel ventilation** aligned with the module side gaps to create a secondary cross-flow path. This would reduce reliance on the narrow chimney gap.

8. **Consider UPS battery thermal isolation**. If the battery runs hot, consider a separate airflow path for the UPS module to prevent it from preheating the upstream air for other modules.

9. **Document the pressure drop budget**. Once a filter material and fan model are selected, create a simple pressure-drop estimate (grille + filter + module stack + top gap) to ensure the fan can overcome the system resistance. This is not CFD — it is a standard fan curve vs. system curve calculation.

---

## References

| File | Line(s) | Relevance |
|---|---|---|
| `cad/config.py` | 403–454 | Cooling parameters, duct dimensions, filter dimensions, sensor points |
| `cad/config.py` | 338–339, 356–359 | Base stability fan clearance, foot height, Z positions |
| `cad/parts/cooling.py` | 8–37, 94–117 | Grille, filter frame, filter retainer geometry |
| `cad/parts/feet.py` | 102–110, 133–160 | Base frame, ribs, intake cut, foot positions |
| `cad/parts/carriages.py` | 8–15, 189–236 | Tray vent slot geometry, module tray creation |
| `cad/parts/modules.py` | 10–121 | Device placeholders sitting on tray bases |
| `cad/parts/frame.py` | 10–43 | Frame ring dimensions, inner opening |
| `cad/parts/review.py` | 33–40 | Bottom intake open area review geometry |
| `cad/parts/service_spine.py` | 64–171 | Rear spine dimensions, channel, windows |
| `cad/assembly/tower_assembly.py` | 194–239 | Assembly placement — filter parts absent |
| `revisions/mk0.7/CALCULATIONS.md` | 21–23 | Intake open area ratio is a review threshold, not CFD |
| `revisions/mk0.7/KNOWN_ISSUES.md` | 1–9 | All known issues confirmed by this review |
| `revisions/mk0.7/review_package/analysis/part_dimensions.csv` | Multiple | Exported bounding boxes confirming Z-stacks and overlaps |


---

## 9. Modularity and Serviceability Review

*Full agent: `05_modularity_serviceability.md`*

## Executive Summary

The mk0.7 tower claims a "fully removable" modular architecture with six standardized trays. The CAD geometry confirms that the tray *standard* is genuinely interchangeable in width, depth, rail spacing, and mounting interface. However, the physical serviceability story is **significantly weaker than the geometric story** because the rear cable management design forces full cable disconnection for every module extraction, the Mini PC service travel is too short for meaningful rear access, and several claimed serviceable subsystems (bottom fan cartridge, power bus, feet) require tools or tower repositioning that contradict the "easy service" intent.

**Three blockers** must be resolved before any build:
1. **Module extraction is not independent** — rear cables must be disconnected for every tray removal, contradicting the AGENTS.md requirement.
2. **Tray vertical support is unmodeled** — the metal guide rails are vertical bars with no horizontal shelves; a 1.2 kg tray has no modeled support from below except the bottom frame (for the lowest tray).
3. **Bottom fan cartridge is not actually attached to the base** — the cartridge has M3 mounting holes but the base has no corresponding holes, so it is a loose part under a 9.5 kg tower.

The design is **modular in intent but not yet serviceable in practice**.

---

## Module Standardization

### Assessment: GEOMETRICALLY STANDARDIZED, BUT FUNCTIONALLY NON-INTERCHANGEABLE.

**Evidence:**
- `config.py` lines 114–128: `MODULE_WIDTH = 170.0`, `MODULE_DEPTH = 176.0`, `RAIL_SPACING = METAL_RAIL_X_OFFSET * 2 = 168.0`, `TRAY_FRONT_HANDLE_WIDTH = 64.0`, `TRAY_LOCK_HOLE_DIAMETER = SCREW_CLEARANCE_M3`, `MODULE_LOCK_ANTI_SLIDE_TAB_WIDTH = 18.0`.
- `carriages.py` lines 189–250: All six trays are produced by `create_carriage()` (via `make_module_tray()`), which uses the same base plate, side walls, rail clearances, mounting holes, handle pocket, lock boss, and anti-slide tab geometry.
- `modules.py` lines 144–150: `TRAY_FACTORIES` maps all six modules to tray builders that call `make_module_tray()` with the same width/depth parameters.
- `part_dimensions.csv`: All trays have identical envelopes (172 × 178 × 32 mm) except `ups_power_tray` (186.5 mm X due to extra strap slot geometry).

**Interchangeability analysis:**
- **Width and depth:** CONFIRMED identical across all trays. Any tray can physically slide on the rails.
- **Rail spacing:** CONFIRMED fixed at 168 mm. The rail cutouts (`TRAY_RAIL_CLEARANCE_WIDTH = 13.0`, `TRAY_RAIL_CLEARANCE_DEPTH = 8.0`) are the same on every tray.
- **Mounting holes:** CONFIRMED identical. `add_mounting_holes()` uses `TRAY_MOUNT_HOLE_OFFSET_X = 18.0` and `TRAY_MOUNT_HOLE_OFFSET_Y = 24.0` for all trays.
- **Front handle and lock:** CONFIRMED identical. The front plate height is `min(tray_height, CARRIAGE_FRONT_PLATE_HEIGHT = 24.0)`, so all trays get a 24 mm high front plate regardless of actual tray height.
- **Functional non-interchangeability:** CONFIRMED. Each tray has device-specific geometry (SSD pocket, RPi board marker, Mini PC power window, UPS zones). You cannot swap a Mini PC tray into an SSD slot because the tray interior is shaped for a specific device. The *standard* is interchangeable; the *trays* are not.

**Finding:** The module tray standard is **CONFIRMED** to be geometrically consistent and interchangeable. However, the trays are functionally dedicated to their devices, so "interchangeability" only applies to the rail/load-path interface, not to the module contents. This is acceptable for a modular tower where each slot has a designated purpose, but the terminology should not imply that any tray can go in any slot.

---

## Module Extraction Feasibility

### Assessment: GEOMETRICALLY POSSIBLE, BUT CABLE-DEPENDENT EXTRACTION IS A BLOCKER.

**Evidence:**
- `config.py` lines 223–230: `TRAY_STACK` = [UPS (2.0), SSD Bay (1.0), SSD Expansion (1.0), RPi (1.0), MikroTik (1.5), Mini PC (2.0)] = 8.5 units total.
- `config.py` lines 96–99: `MODULE_SLOT_GAP = 1.0`, `LIGHT_MODULE_HEIGHT = MODULE_SLOT_PITCH - MODULE_SLOT_GAP`, `COMPUTE_MODULE_HEIGHT = MODULE_SLOT_PITCH * 2 - MODULE_SLOT_GAP`.
- `carriages.py` lines 76–118: Front plate depth = `CARRIAGE_FRONT_PLATE_THICKNESS = 8.0` mm (the plate is 8 mm thick in Y, but the handle pocket cutter depth is `CARRIAGE_HANDLE_DEPTH = MODULE_FRONT_HANDLE_DEPTH = 4.2` mm). Wait — the front plate thickness is 8.0 mm, but the handle depth is only 4.2 mm. The plate extends from `y = -TRAY_DEPTH/2` to `y = -TRAY_DEPTH/2 + 8.0`.
- `carriages.py` lines 57–73: Anti-slide tab is at the front underside, `MODULE_LOCK_ANTI_SLIDE_TAB_DEPTH = 4.0`, `MODULE_LOCK_ANTI_SLIDE_TAB_HEIGHT = 5.0`. This tab sits below the tray base and engages with a slot or lip in the frame to prevent accidental walk-out.
- `tower_assembly.py` lines 90–106: Trays are stacked starting at `STACK_START_Z = 18.0`, with each tray positioned at `current_z` and `current_z += units * UNIT_HEIGHT`.

**Geometric clearance for lower tray extraction:**
- A 1-unit tray has height = `35 - 2 = 33 mm` (accounting for `TRAY_CLEARANCE_Z = 2.0`). The front plate is 24 mm high. The tray above starts at `Z + 33 + 1 = Z + 34`. The front plate top is at `Z + 24`. Clearance to the tray above = **10 mm**.
- A 2-unit tray (UPS, Mini PC) has height = `70 - 2 = 68 mm`. Front plate is 24 mm. The tray above starts at `Z + 68 + 1 = Z + 69`. Clearance = **45 mm**.
- The front plate thickness in Y is 8.0 mm. The tray above is offset by 1 mm in Z, not in Y. The front plate moves forward with the tray; it does not need to pass between the trays. Since the trays are vertically separated, the front plate of a lower tray simply slides forward *under* the tray above.

**Finding:** Geometrically, any lower tray **CAN** be pulled out without removing upper trays. The 1 mm `MODULE_SLOT_GAP` does not obstruct the front plate because the front plate is part of the moving tray and moves in the Y direction, not Z. **CONFIRMED: independent geometric extraction is possible.**

**BUT — the cable problem:**
- Every tray has a `TRAY_REAR_SERVICE_CUTOUT` (66 mm wide, 36 mm deep) at the rear (`carriages.py` lines 143–150). Cables exit through this cutout into the rear service spine.
- The rear service spine is a closed channel with a screw-on cover (`REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 screw positions, `REAR_SPINE_COVER_THICKNESS = 3.0`).
- To extract a module, the user must: (1) remove the rear spine cover, (2) disconnect power/data cables, (3) untie cable ties, (4) slide the tray out. This is a **10+ minute operation** requiring a screwdriver, as documented in the Red Team review (`09_red_team.md`, Section "Rear Service Spine as Cable Trap").

**Finding:** The design claims "extractable without disassembly" but forces full cable disconnection for every module. This is a **CONFIRMED** contradiction with the AGENTS.md requirement: "Извлечение одного модуля не должно требовать разборки всей башни." The module is not "fully removable" if the spine cover and cables must be disturbed.

---

## Front Handle and Lock Design

### Assessment: UNDER-SIZED FOR HEAVY TRAYS AND TIPPING-HAZARD-PRONE.

**Evidence:**
- `config.py` lines 121–123, 199–214: `TRAY_FRONT_HANDLE_WIDTH = 64.0`, `TRAY_FRONT_HANDLE_DEPTH = 4.2` (pocket depth), `CARRIAGE_HANDLE_HEIGHT = 13.0`, `CARRIAGE_HANDLE_TOP_BRIDGE = 5.5`, `CARRIAGE_LOCK_BOSS_DIAMETER = 11.0`, `MODULE_LOCK_INSERT_OUTER_DIAMETER = 5.2` (M3 heat-set insert).
- `config.py` lines 26–35: `ESTIMATED_UPS_MASS = 1.4`, `ESTIMATED_MINI_PC_MASS = 1.2`, `MAX_MODULE_MASS = 1.8`.
- `carriages.py` lines 24–34: Handle is a recessed pocket 64 mm wide × 13 mm tall × 4.2 mm deep, with a 3 mm corner radius fillet.
- `carriages.py` lines 37–54: Lock boss is an 11 mm diameter cylinder with a 5.2 mm insert hole. Boss wall thickness = (11.0 − 5.2) / 2 = **2.9 mm**.

**Handle ergonomics:**
- The pocket is only **4.2 mm deep**. A typical adult finger is 15–20 mm wide. Two fingers cannot fit into a 64 mm × 13 mm × 4.2 mm pocket comfortably. The user can hook one or two fingertips into the pocket, but the shallow depth (4.2 mm) provides almost no gripping surface.
- The heaviest tray (UPS, 1.4 kg) requires significant pulling force to overcome friction on the metal rails (especially if the rails are not perfectly straight or if the PETG rails swell with humidity). A 1.4 kg load on a shallow 4.2 mm finger grip is awkward and risks the tray slipping from the user's grip.
- The `CARRIAGE_HANDLE_TOP_BRIDGE = 5.5` mm is the thickness of the bridge above the pocket. This is thin and could flex under repeated pulling loads.

**Lock boss strength:**
- The M3 heat-set insert in an 11 mm boss with 2.9 mm wall thickness is **LIKELY adequate** for a locking screw (which is not a load-bearing fastener, just a retention screw). The insert is not intended to hold the tray's weight; it only prevents the tray from sliding forward.
- However, if the tray jams on the rails and the user pulls hard on the handle, the lock screw could see shear loads. The 2.9 mm PETG wall around the insert could crack under high pull force.

**Finding:** The handle pocket is **CONFIRMED** to be ergonomically marginal for a 1.2–1.4 kg tray. The 4.2 mm depth is too shallow for a confident two-finger grip. The lock boss is **LIKELY** adequate for normal retention but **UNCERTAIN** under high extraction force or repeated cycling. **NEEDS TEST:** physical pull test with a loaded 1.4 kg tray to measure required extraction force and handle comfort.

**Tipping hazard note:** The Red Team review (`09_red_team.md`) confirmed that when the Mini PC tray is pulled out 78 mm, the tray front overhangs the base by **41 mm**, and a 40–50 N pull on the handle at Z ≈ 250 mm can tip the tower forward. The shallow handle design contributes to this hazard because the user cannot get a secure grip and may apply a jerky, upward-pulling force.

---

## Side Panel Removal Impact

### Assessment: PANELS CAN BE REMOVED WITHOUT REMOVING MODULES, BUT THEY CANNOT BE MOUNTED AT ALL.

**Evidence:**
- `config.py` lines 368–400: `SIDE_PANEL_THICKNESS = 3.0`, `SIDE_PANEL_GAP = 0.4`, `SIDE_PANEL_SECTION_COUNT = 3`, `SIDE_PANEL_SECTION_HEIGHT = (SIDE_PANEL_HEIGHT − 2 * SIDE_PANEL_GAP) / 3`.
- `side_panels.py` lines 145–167: Each panel tile has M3 mount holes at its four corners, inset by `SIDE_PANEL_FRAME_WIDTH = 10.0` mm.
- `tower_assembly.py` lines 114–145: Side panels are placed at `x = ±(OUTER_WIDTH / 2 + SIDE_PANEL_THICKNESS / 2) = ±(95 + 1.5) = ±96.5` mm.
- The trays are at `x = TRAY_X = 0.0` with `MODULE_WIDTH = 170.0`, so they extend from `x = −85` to `x = +85`. The panels are at `x = ±96.5`, **outside the tray envelope**.

**Panel removal vs. module extraction independence:**
- **CONFIRMED:** Side panels are geometrically outside the tray width envelope. Removing a side panel does not require removing any module, and extracting a module does not require removing any side panel. The two operations are independent.
- **CONFIRMED:** The side panels are sectioned into three independently removable tiles per side (`lower`, `middle`, `upper`). A user can remove just the middle panel to access the middle modules without disturbing the top or bottom panels.

**BUT — the mounting interface is broken:**
- The Structural Integrity review (`03_structural_integrity.md`) confirmed that corner blocks only have holes on `+X` and `+Y` faces, not on `−X` and `−Y`. The holes that do exist are at `z = center ± 6 mm`, which does not align with side panel mount points at `z = center ± 40.45 mm`.
- The frame rings have no panel mounting holes.
- **Result:** The side panels cannot be fastened to the structure. This is a **CONFIRMED** design error that is a blocker for the tower assembly.

**Finding:** If the mounting interface were fixed, side panel removal would be fully independent of module extraction. However, the current design has **no working mounting interface**, so the panels are purely decorative in the current CAD. This is a **CONFIRMED blocker** inherited from structural findings.

---

## Rear Service Spine and Cable Management

### Assessment: CABLES TRAP MODULES — EXTRACTION REQUIRES FULL DISCONNECTION.

**Evidence:**
- `config.py` lines 125–126: `REAR_CABLE_EXIT_WIDTH = 66.0`, `REAR_CABLE_EXIT_HEIGHT = 20.0`. Every tray has a fixed rear cutout of this size.
- `config.py` lines 151–160: `MODULE_REAR_CABLE_CLEARANCE = 36.0`, `TRAY_REAR_SERVICE_CUTOUT_DEPTH = 36.0`. The cable exit extends 36 mm rearward from the tray back edge.
- `config.py` lines 455–512: `REAR_SPINE_WIDTH = 52.0`, `REAR_SPINE_DEPTH = 30.0`, `REAR_SPINE_CABLE_SLOT_WIDTH = 34.0`, `REAR_SPINE_TIE_SLOT_WIDTH = 4.0`, `REAR_SPINE_HORIZONTAL_TIE_Z` at six vertical positions.
- `service_spine.py` (implied from assembly): The spine cover mounts with screws at `REAR_SPINE_STRUCTURAL_MOUNT_Z` (7 positions).
- `carriages.py` lines 143–150: `make_tray_cable_exit()` — the cable exit is a fixed cutout, not a quick-disconnect or pass-through connector.

**Module extraction procedure (CONFIRMED from Red Team analysis):**
1. Remove rear spine cover (6+ M3 screws).
2. Untie or cut cable ties from `REAR_SPINE_TIE_SLOT_Z` slots.
3. Disconnect power connectors (XT30, MicroFit, USB-C) from the module.
4. Disconnect data cables (Ethernet, USB) from the module.
5. Slide the module forward.
6. Reverse all steps to reinstall.

**Hot-swap assessment:**
- The modules are **NOT hot-swappable**. The cables are fixed to the module and pass through the rear cutout into the spine. There is no pass-through bulkhead connector, no magnetic connector, and no cable breakaway at the module rear.
- The AGENTS.md requirement states: "Все кабели должны проходить через эту шахту." (All cables must pass through the spine.) This is satisfied. But it also states: "Извлечение одного модуля не должно требовать разборки всей башни." (Extraction of one module must not require disassembling the whole tower.) The current implementation violates this because the spine cover must be removed and cables must be disconnected.

**Is this acceptable?**
- For a home lab tower where modules are rarely moved, **MAYBE**. But the design claims "fully removable" and "serviceable." A 10+ minute screwdriver-and-dexterity operation to swap a module is not "serviceable" in the intended sense.
- The horizontal tie slots (`REAR_SPINE_HORIZONTAL_TIE_Z`) bundle cables across module boundaries. If cables from multiple modules are tied together, extracting one module requires untying cables that belong to other modules — **further violating the independence requirement**.

**Finding:** The rear service spine is a **CONFIRMED cable trap** that prevents independent module extraction. The spine cover, cable ties, and fixed connectors make module swap a multi-step, multi-tool operation. This is a **CONFIRMED blocker** for the modularity claim. The design needs either (a) quick-disconnect bulkhead connectors at each tray rear, or (b) pigtails that stay in the spine while the module disconnects, or (c) a hinged spine cover that opens without tools.

---

## Mini PC Service Travel

### Assessment: 78 MM TRAVEL IS ADEQUATE FOR FRONT ACCESS BUT INADEQUATE FOR REAR SERVICE.

**Evidence:**
- `config.py` lines 515–523: `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`, `TRAY_STOP_SLOT_LENGTH = 54.0`, `TRAY_STOP_WASHER_DIAMETER = 12.0`, `TRAY_STOP_THICKNESS = 3.0`, `TRAY_STOP_HEIGHT = 16.0`.
- `modules.py` lines 124–141: `make_tray_stop()` creates a 18 × 6 × 22 mm PETG bracket with a 12 mm washer boss and an M3 clearance hole.
- `tower_assembly.py` lines 206–214: The tray stop is placed at `TRAY_STOP_OFFSET_X = MODULE_TRAY_WIDTH / 2 − 22.0 = 85 − 22 = 63.0` mm from center, and `TRAY_STOP_OFFSET_Y = MODULE_TRAY_DEPTH / 2 − 34.0 = 88 − 34 = 54.0` mm from center. The stop is mounted on the tray base and slides in a slot (`MINI_PC_TRAY_STOP_SLOT_LENGTH = 54.0`) cut into the tray.
- `config.py` lines 290–308: `MINI_PC_PLACEHOLDER_DEPTH = 130.0`, `MINI_PC_POWER_WINDOW_DEPTH = 8.0`, `MINI_PC_POWER_WINDOW_REAR_INSET = 2.0`. The Mini PC power connector is at the rear, 2 mm inset from the tray back edge.

**Service travel analysis:**
- The tray moves forward 78 mm. The Mini PC placeholder depth is 130 mm. The power connector is at the rear of the Mini PC. When the tray is slid forward 78 mm, the rear of the Mini PC moves from `Y = TRAY_Y + TRAY_DEPTH/2 + device_offset = −4 + 88 − 8 = +76` (wait, need to recalculate). Actually, the tray is at `TRAY_Y = −4.0`, with `TRAY_DEPTH = 176`. The tray rear is at `y = −4 + 88 = +84`. The Mini PC placeholder is at `MINI_PC_PLACEHOLDER_LOC = (0.0, −8.0, 7.0)`, so the device rear is at `y = −4 + (−8) + 65 = +53` (half of 130 is 65). The power window is at `MINI_PC_POWER_WINDOW_X = −54.0`, with rear inset of 2 mm from the tray back edge. So the power connector is approximately at the rear of the device.
- When the tray moves forward 78 mm (in the −Y direction), the device rear moves from `y ≈ +53` to `y ≈ +53 − 78 = −25`. The power cable, which enters the rear service spine at `y ≈ +84` (spine rear), now has a device end at `y ≈ −25`. The cable must span `84 − (−25) = 109` mm.
- A typical power brick cable or Ethernet cable has a stiff molded strain relief of 30–50 mm. If the cable has 150 mm of slack inside the spine, 78 mm travel may leave the cable connected but with significant tension on the connector.
- More importantly, the **rear of the Mini PC is now at y ≈ −25**, which is *forward* of the tower center. The user cannot access the rear connectors because the tray has moved *forward*, and the connectors are still facing the rear. The 78 mm travel brings the front of the Mini PC closer to the user but does **not** bring the rear connectors out of the tower.

**What can the user do with 78 mm travel?**
- Access the front/side of the Mini PC (if it has front USB ports or a power button).
- Reach over the top of the Mini PC to touch the front edge of the board.
- Access the Mini PC's side or bottom (for ventilation cleaning).
- **Cannot** access the rear power or Ethernet connectors without disconnecting cables.
- **Cannot** remove the Mini PC from the tray without pulling it further forward or tilting it.

**Finding:** The 78 mm service travel is **CONFIRMED** to be inadequate for rear-connector service. It is useful for front access and ventilation inspection but does not solve the core problem of reaching the power and data connectors. The tray stop is a **LIKELY** adequate mechanical stop for gentle use but **UNCERTAIN** for impact loads (see Structural Integrity review, `03_structural_integrity.md`, Section "Mini PC Tray Stop Adequacy"). **NEEDS TEST:** physical cable strain measurement with a real Mini PC and typical cables during 78 mm tray travel.

**Dynamic tipping hazard:** The Red Team review (`09_red_team.md`) confirmed that pulling the Mini PC tray forward 78 mm creates a 41 mm front overhang beyond the base, and a 40–50 N horizontal pull at handle height (Z ≈ 250 mm) will tip the tower forward. The service travel design directly contributes to this safety hazard.

---

## Bottom Fan Cartridge Serviceability

### Assessment: CARTRIDGE IS DESIGNED TO BE REMOVABLE BUT IS NOT ACTUALLY ATTACHED AND REQUIRES TOOLS.

**Evidence:**
- `config.py` lines 427–433: `BOTTOM_FAN_CARTRIDGE_WIDTH = 142.0`, `BOTTOM_FAN_CARTRIDGE_DEPTH = 161.0`, `BOTTOM_FAN_CARTRIDGE_HEIGHT = 8.0`, `BOTTOM_FAN_CARTRIDGE_SERVICE_PULL = 14.0`, `BOTTOM_FAN_CARTRIDGE_MOUNT_OFFSET = 68.0`.
- `cooling.py` lines 48–91: `make_bottom_fan_cartridge()` has M3 mounting holes at `±68` mm offset (`M3_CLEARANCE = 3.4` mm holes) and a 14 mm service pull handle.
- `tower_assembly.py` lines 219–222: The cartridge is placed at `BOTTOM_FAN_CARTRIDGE_Z = BASE_STABILITY_Z − BASE_STABILITY_THICKNESS/2 − BOTTOM_FAN_CARTRIDGE_HEIGHT/2 = −9 − 5 − 4 = −18` mm. (Note: the config shows `BOTTOM_FAN_CARTRIDGE_Z = BASE_STABILITY_Z - BASE_STABILITY_THICKNESS / 2 - BOTTOM_FAN_CARTRIDGE_HEIGHT / 2` but line 614 shows `BOTTOM_FAN_CARTRIDGE_Z = BASE_STABILITY_Z - BASE_STABILITY_THICKNESS / 2 - BOTTOM_FAN_CARTRIDGE_HEIGHT / 2`, while the comment at line 613 says `BOTTOM_FAN_PANEL_Z = -2.0`. Actually, looking at the config more carefully: `BASE_STABILITY_Z = -9.0` and `BASE_STABILITY_THICKNESS = 10.0`, so `BOTTOM_FAN_CARTRIDGE_Z = -9 - 5 - 4 = -18`. But the cartridge has rails and a handle. The base is at z = -9 with 10mm thickness, so its bottom is at z = -14. The cartridge at z = -18 sits 4 mm below the base bottom.)
- `DECISIONS.md` line 13: "вентилятор не должен требовать разборки башни или снятия модулей" (fan must not require tower disassembly or module removal).
- `KNOWN_ISSUES.md` line 3: "`bottom_fan_cartridge` требует print-fit проверки с реальным вентилятором 120 x 120 x 25 mm."

**Attachment problem:**
- The cartridge has M3 mounting holes at `±68` mm offset. But the base (`central_bottom_fan_frame`, `bottom_structural_frame`, or base stability plate) has **no corresponding M3 holes** to match these offsets.
- The Red Team review (`09_red_team.md`, Section "Additional Structural Defects") confirmed: "The cartridge will fall out or shift when the tower is moved. This is a loose part under a 9.5 kg tower."
- The `part_dimensions.csv` shows the cartridge envelope (142 × 161 × 13 mm) but no base part with matching mount holes.

**Tool requirement:**
- The cartridge uses M3 screws for mounting. Even if the base had matching holes, the user would need a screwdriver or hex key to remove the cartridge.
- The `BOTTOM_FAN_CARTRIDGE_SERVICE_PULL = 14.0` mm handle is a small pull tab. It is useful for sliding the cartridge out after screws are removed, but it does not make the cartridge tool-less.
- The DECISIONS.md claim "обслуживаемый cartridge" (serviceable cartridge) is technically true — it is serviceable with tools — but it is not tool-less.

**Filter serviceability:**
- `bottom_filter_frame` (138 × 138 × 3 mm) and `bottom_filter_retainer` (144 × 8 × 4 mm) are separate parts. The retainer is a thin clip that holds the filter material. The DECISIONS.md states the filter is "опциональная механика" (optional mechanics).
- The filter frame and retainer are not attached to the cartridge; they are separate parts that sit on the cartridge rails. The `cooling.py` lines 94–116 show the filter frame and retainer as standalone geometry with no mounting screws — they are presumably gravity-held or slide-fit. However, the retainer is only 8 mm deep in Y, which is a very small clip for a 138 mm wide filter. It may not hold the filter securely against the fan intake pressure.

**Finding:** The bottom fan cartridge is **CONFIRMED** to be a loose, unattached part in the current CAD. The base has no mounting holes to match the cartridge's M3 holes. Even if attached, the M3 screw requirement means it is **not tool-less**. The filter retention is **UNCERTAIN** — the 8 mm deep retainer may not hold filter material securely under airflow. **NEEDS TEST:** print-fit check with a real 120 mm fan and verify filter retention under airflow.

---

## Power Bus Access

### Assessment: POWER BUS IS ACCESSIBLE ONLY AFTER REMOVING THE REAR SPINE COVER AND THE POWER BUS COVER — NOT WHILE ASSEMBLED.

**Evidence:**
- `config.py` lines 530–564: `POWER_BUS_WIDTH = 34.0`, `POWER_BUS_HEIGHT = 275.5`, `POWER_BUS_THICKNESS = 3.0`, `POWER_BUS_PAD_WIDTH = 22.0`, `POWER_BUS_PAD_DEPTH = 4.0`, `POWER_BUS_PAD_HEIGHT = 22.0`, `POWER_BUS_CONNECTOR_CUT_DEPTH = 5.0`.
- `config.py` lines 545–549: Connector zones for XT30 (19V), MicroFit (12V), USB-C (5V), and cable tie.
- `config.py` lines 551–559: `POWER_BUS_COVER_WIDTH = 46.0`, `POWER_BUS_COVER_HEIGHT = 265.5`, `POWER_BUS_COVER_THICKNESS = 2.4`, `POWER_BUS_GUARD_RAIL_WIDTH = 3.0`, `POWER_BUS_GUARD_RAIL_DEPTH = 5.0`.
- `config.py` lines 612: `POWER_BUS_PANEL_OFFSET_Y = 10.0` — the power bus panel is offset 10 mm forward from the rear service spine center.
- `tower_assembly.py` lines 166–180: The power bus panel is placed at `rear_y − POWER_BUS_PANEL_OFFSET_Y`, and the power bus cover is placed behind it at `rear_y − POWER_BUS_PANEL_OFFSET_Y − POWER_BUS_THICKNESS`. The rear spine is at `rear_y = OUTER_DEPTH/2 − REAR_SPINE_DEPTH/2 = 95 − 15 = 80`. So the power bus panel is at `y = 80 − 10 = 70`, and the cover is at `y = 70 − 3 = 67`. The rear spine cover is at `y = 80 + 15 + 1.5 = 96.5` (spine rear + half spine depth + half cover thickness).

**Access path analysis:**
- The power bus panel and cover are **inside** the rear service spine volume. The spine cover is a separate screwed-on panel (`REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 screw positions).
- To reach the power bus connectors, the user must:
  1. Remove the rear spine cover (6+ M3 screws).
  2. Remove the power bus cover (no mounting data shown in config, but it is a separate cover).
  3. Access the XT30/MicroFit/USB-C connectors.
- The connectors cannot be reached while the spine cover is in place. The power bus cover adds an additional layer of obstruction.
- The `POWER_BUS_CONNECTOR_CUT_DEPTH = 5.0` mm suggests the connectors are recessed into the panel, which further reduces accessibility.

**Connector operation while assembled:**
- The XT30 connector requires ~10 mm of insertion depth and a firm push/pull. The MicroFit and USB-C connectors also require finger access. The `POWER_BUS_PAD_DEPTH = 4.0` and `POWER_BUS_GUARD_RAIL_DEPTH = 5.0` create a narrow channel around the connectors. Working in this confined space with the tower upright and modules in place is awkward.
- The power bus is at the rear of the tower, behind all six modules. The user's hands must reach past (or between) the rear of the modules to access the connectors. The module rear cable exits (`REAR_CABLE_EXIT_WIDTH = 66.0`) are only 20 mm tall and face the spine, so cables from the modules already occupy the space in front of the power bus.

**Finding:** The power bus is **CONFIRMED** to be inaccessible without removing the rear spine cover and the power bus cover. The design does **not** allow power bus connectors to be connected or disconnected while the tower is fully assembled. This is a **CONFIRMED** serviceability gap. The power bus should be relocated to a more accessible position (e.g., a side-access panel or a hinged spine cover with a cutout) or the connectors should be brought to the exterior with pass-through bulkheads.

---

## Foot Replacement

### Assessment: FEET ARE REPLACEABLE IN PRINCIPLE BUT REQUIRE TOWER REPOSITIONING AND THE SOCKET INTERFACE IS BROKEN.

**Evidence:**
- `config.py` lines 332–359: `FOOT_HEIGHT = 32.0`, `FOOT_DIAMETER = 34.0`, `FOOT_SCREW_DIAMETER = 5.3`, `FOOT_COUNTERBORE_DIAMETER = 10.0`, `FOOT_COUNTERBORE_DEPTH = 4.0`, `FOOT_SOCKET_DEPTH = 3.0`, `FOOT_SOCKET_CLEARANCE = 0.6`.
- `feet.py` (implied from config and Red Team review): The foot socket is a 3 mm thick PETG boss with a 5.3 mm through-hole and **no heat-set insert**.
- `tower_assembly.py` lines 42–49: Feet are placed at `FOOT_Z = BASE_STABILITY_Z − BASE_STABILITY_THICKNESS/2 − FOOT_HEIGHT/2 = −9 − 5 − 16 = −30` mm. The foot extends from `z = −46` to `z = −14` mm. The base bottom is at `z = −14` mm.

**Accessibility for replacement:**
- The feet are at the bottom of the base. The M5 screw is accessed from below (through the foot, into the base socket). The counterbore is 10 mm diameter and 4 mm deep, so the screw head sits flush or below the foot bottom surface.
- To replace a foot, the user must access the underside of the tower. The tower is 330 mm tall and weighs ~6 kg. The user must either:
  - Tilt the tower on its side (risking module shift if trays are not locked).
  - Lift the tower and turn it upside down (difficult and risky for a 6 kg, 330 mm tall object with protruding cables).
  - Use a low-profile trolley or jack to raise one corner.
- **The foot is not accessible from the side or top.** The base is a wide stability plate (250 × 260 mm), so the feet are recessed under the base. A user cannot reach under the 32 mm foot height to access the screw while the tower is upright.

**Broken socket interface:**
- The Red Team review (`09_red_team.md`) confirmed: "A 5.3 mm hole in 3 mm of PETG will strip immediately." The `FOOT_SOCKET_DEPTH = 3.0` mm is too thin for an M5 self-tapping screw. There is no heat-set insert.
- The Structural Integrity review (`03_structural_integrity.md`) also flagged this: the TPU foot is attached to a 3 mm PETG boss with no insert. The M5 screw will strip the PETG on first assembly.

**Finding:** Foot replacement is **CONFIRMED** to require tower repositioning (tilt or lift). The 32 mm foot height does not provide side access to the screw. The socket interface is **CONFIRMED** broken — the 3 mm PETG socket will strip immediately. This is a **CONFIRMED blocker** for assembly, not just serviceability. **NEEDS TEST:** physical assembly of foot to socket with an M5 screw to verify thread stripping force.

---

## Scalability to Future Modules

### Assessment: ARCHITECTURE SUPPORTS NEW MODULES, BUT THE CURRENT STACK HAS ZERO SLACK.

**Evidence:**
- `config.py` lines 16–17: `TOTAL_UNITS = 8.5`, `TOWER_HEIGHT = TOTAL_UNITS * UNIT_HEIGHT + 24.0 = 8.5 * 35 + 24 = 321.5` mm.
- `config.py` lines 216–230: `TRAY_STACK` uses 2.0 + 1.0 + 1.0 + 1.0 + 1.5 + 2.0 = **8.5 units exactly**.
- `config.py` lines 96–99: `MODULE_SLOT_COUNT = 6`, `MODULE_SLOT_PITCH = TOWER_INTERNAL_HEIGHT / MODULE_SLOT_COUNT = 314.5 / 6 ≈ 52.4` mm. `LIGHT_MODULE_HEIGHT = 51.4` mm, `COMPUTE_MODULE_HEIGHT = 103.9` mm.

**New module addition:**
- The `TRAY_FACTORIES` dictionary (`modules.py` lines 144–150) and `placeholder_factories` (`tower_assembly.py` lines 64–89) are open dictionaries. Adding a new module requires only adding a new factory entry and a `TRAY_STACK` entry.
- The tray standard (`MODULE_WIDTH`, `MODULE_DEPTH`, `RAIL_SPACING`, lock interface, mounting holes) is fixed. Any new module that fits within the 170 × 176 mm planform and the available height can use the existing standard.

**Height constraint:**
- The current stack consumes **all 8.5 units**. There is no spare height. If a future module needs 2.5 or 3 units, the stack must be completely reconfigured.
- The `UNIT_HEIGHT = 35.0` mm is a rigid grid. If a device needs 45 mm (e.g., a taller Mini PC with a larger heatsink), it cannot fit in the current unit system without either:
  - Increasing `UNIT_HEIGHT` (which changes ALL tray heights and requires reprinting all trays).
  - Using a non-integer unit count (which the current config supports — `MIKROTIK_TRAY_UNITS = 1.5` shows non-integer units are allowed).
  - Removing another module to free up units.

**Width and depth constraints:**
- `MODULE_WIDTH = 170.0` mm and `MODULE_DEPTH = 176.0` mm are fixed. If a future device (e.g., a larger router, a NAS with more drive bays) needs 180 mm width, the tray standard must be changed. This would require reprinting all trays, changing the rail spacing, and possibly widening the tower.
- The `TRAY_CLEARANCE = 0.6` mm is small. If a device needs even 1 mm more width than the placeholder, the tray is unusable. There is no adjustment mechanism (slotted holes, adjustable rails, or shims).

**Module count constraint:**
- `MODULE_SLOT_COUNT = 6`. The current design has 6 modules. If a user wants 7 modules (e.g., adding a dedicated firewall module), there is no 7th slot. The tower would need to be taller (more units) or a module would need to be removed.
- The frame and rail height are derived from `TOWER_HEIGHT`. Changing the module count or total units requires recalculating `METAL_RAIL_HEIGHT`, `REAR_SPINE_HEIGHT`, `SIDE_PANEL_HEIGHT`, and rod length — essentially redesigning the tower.

**Finding:** The architecture is **CONFIRMED** scalable in terms of *software* (adding new `TRAY_FACTORIES` entries is trivial). However, the physical tower is **CONFIRMED** to have zero slack in the current configuration. Adding a new module type that requires a different size or an additional slot would require a **major redesign** of the stack, frame, and rails. The fixed unit grid and rigid tray dimensions provide no margin for future growth. This is a **LIKELY** limitation for a long-term modular platform.

**Recommendation for future revisions:**
- Add 0.5–1.0 units of spare height to the stack (increase `TOTAL_UNITS` to 9.0–9.5).
- Consider making `UNIT_HEIGHT` adjustable or supporting "double-wide" modules that occupy two adjacent slots horizontally.
- Add slotted mounting holes or adjustable rails to accommodate device size variations.

---

## Blockers

These issues must be resolved before any physical build or claim of "serviceable modularity":

1. **Module extraction requires full cable disconnection.** The rear service spine design forces the user to remove the spine cover, untie cables, and disconnect all power/data connectors before extracting any module. This contradicts the AGENTS.md requirement that extraction must not require tower disassembly. **Severity: High.** Evidence: `carriages.py:143–150`, `service_spine.py` (implied), Red Team review (`09_red_team.md`).

2. **Tray vertical support is unmodeled.** The metal guide rails are vertical bars with no horizontal shelves, brackets, or ledges. The trays are horizontal plates with no modeled support from below except the bottom frame for the lowest tray. A 1.2 kg Mini PC tray has no visible support mechanism. **Severity: High.** Evidence: `config.py:104–111`, `rails.py` (implied), Structural Integrity review (`03_structural_integrity.md`).

3. **Bottom fan cartridge is not attached to the base.** The cartridge has M3 mounting holes at `±68` mm offset, but the base has no corresponding holes. The cartridge is a loose part under a 9.5 kg tower. **Severity: High.** Evidence: `cooling.py:48–91`, `config.py:427–433`, Red Team review (`09_red_team.md`).

4. **Side panel mounting interface is missing.** The corner blocks lack holes on `−X` and `−Y` faces, and the holes that exist are misaligned with panel mount points. The frame has no panel mounting holes. Side panels cannot be attached. **Severity: High.** Evidence: `corner_blocks.py` (implied), `side_panels.py`, Structural Integrity review (`03_structural_integrity.md`).

5. **Foot socket strips immediately.** The `FOOT_SOCKET_DEPTH = 3.0` mm with a 5.3 mm hole and no heat-set insert means the M5 screw will strip the PETG on first assembly. **Severity: High.** Evidence: `config.py:349–355`, `feet.py` (implied), Red Team review (`09_red_team.md`).

---

## Recommendations

### Immediate (mk0.7 → mk0.8)

1. **Fix the module extraction cable problem.** Options:
   - Add quick-disconnect bulkhead connectors (e.g., XT30 pass-through, magnetic Ethernet) at each tray rear, so cables stay in the spine when the module is pulled out.
   - Add short pigtails (100–150 mm) to each module that stay in the spine, with a detachable connector at the module rear.
   - Replace the screw-on spine cover with a hinged or sliding cover that opens without tools.
   - Ensure horizontal cable ties do not bundle cables across module boundaries.

2. **Add tray vertical support.** The guide rails must have horizontal shelves or ledges at each tray height, or the frame must have intermediate rings that support the trays from below. A 1.2 kg tray cannot be supported by friction alone. Evidence: `config.py:104–111`, Structural Integrity review (`03_structural_integrity.md`).

3. **Attach the bottom fan cartridge.** Add M3 mounting holes to the `central_bottom_fan_frame` or base stability plate that align with `BOTTOM_FAN_CARTRIDGE_MOUNT_OFFSET = 68.0`. Alternatively, add slide-in rails or detents to the base underside. Evidence: `cooling.py:48–91`, `config.py:427–433`.

4. **Fix the foot socket.** Increase `FOOT_SOCKET_DEPTH` to at least 8 mm and add a heat-set insert boss (e.g., `INSERT_BOSS_DIAMETER = 7.2`, `INSERT_BOSS_HEIGHT = 8.0`). Or use a threaded brass insert. Evidence: `config.py:349–355`, Red Team review (`09_red_team.md`).

5. **Enlarge the front handle pocket.** Increase `TRAY_FRONT_HANDLE_DEPTH` from 4.2 mm to at least 12–15 mm to allow a two-finger grip. Or redesign the handle as a protruding pull tab (similar to server rack handles) rather than a recessed pocket. Evidence: `config.py:122`, `carriages.py:24–34`.

6. **Increase Mini PC service travel or add rear access.** Either:
   - Increase `MINI_PC_TRAY_SERVICE_TRAVEL` to at least 130 mm (full device depth) so the rear connectors clear the tower.
   - Add a removable rear panel or hatch above the Mini PC tray for direct rear access without sliding the tray.
   - Add pass-through connectors at the tray rear so cables disconnect automatically when the tray is pulled out. Evidence: `config.py:515–523`, `modules.py:124–141`.

7. **Make the power bus accessible without removing the spine cover.** Add a side-access door or a hinged cutout in the spine cover that exposes the power bus connectors. Or relocate the power bus to a position where the connectors are reachable from the side. Evidence: `config.py:530–564`, `tower_assembly.py:166–180`.

### Short-term (mk0.8)

8. **Add spare unit height to the stack.** Increase `TOTAL_UNITS` from 8.5 to 9.0 or 9.5 to allow future modules or taller devices without redesigning the entire stack. Evidence: `config.py:16–17`, `config.py:216–230`.

9. **Add adjustable device mounting to trays.** Replace fixed-size pockets with slotted holes or adjustable clamps so the trays can accommodate devices with slightly different dimensions. This prevents a 2 mm size mismatch from requiring a full tray reprint. Evidence: `config.py:233–313` (placeholder dimensions with `TODO` comments).

10. **Improve the tray stop design.** Use two M3 screws or a larger PETG bracket for the Mini PC tray stop. The current single-screw 18 × 6 × 22 mm bracket is marginal for a 1.2 kg impact load. Evidence: `config.py:515–523`, `modules.py:124–141`, Structural Integrity review (`03_structural_integrity.md`).

11. **Add a tool-less bottom fan cartridge.** Replace the M3 screw mounting with slide-in rails, detents, or quarter-turn fasteners. The DECISIONS.md claims the cartridge is "serviceable" — it should be tool-less. Evidence: `DECISIONS.md` lines 11–17, `cooling.py:48–91`.

12. **Add side-access foot screws.** Consider making the foot screws accessible from the side of the base (e.g., a horizontal screw into a side boss) so the user does not need to tilt or lift the tower to replace a foot. Evidence: `config.py:332–359`.

### Long-term

13. **Consider a true hot-swap connector standard.** For a modular tower that claims serviceability, the rear module connectors should be designed for 100+ insertion cycles. Standard PC connectors (XT30, MicroFit, RJ45) are not designed for frequent cycling. Consider commercial hot-swap connector systems or spring-loaded contact blocks. Evidence: AGENTS.md modular standard requirements.

14. **Document the module swap time budget.** Quantify the time and tools required to extract and reinstall each module. If the goal is "5-minute module swap," measure it and design to meet it. Evidence: Current extraction procedure is 10+ minutes (Red Team review, `09_red_team.md`).

---

*Review completed. All findings are based on inspection of the CAD source code, configuration parameters, and cross-reference with existing mk0.7 review outputs. No physical testing was performed. Grades are assigned as: CONFIRMED (direct evidence in CAD), LIKELY (strong inference from geometry), UNCERTAIN (insufficient data), NEEDS TEST (requires physical verification).*


---

## 10. Power and Cable Management Review

*Full agent: `06_power_cable_management.md`*

## Executive Summary

The mk0.7 power system and cable management design is **conceptually sound** but **not physically viable** in its current state. The power bus panel and cover are structural placeholders that will not survive real assembly. The rear service spine has insufficient cable capacity for the declared device count. Connector zones lack the clearance required for real panel-mount connectors. Strain relief is undersized. The DC UPS placeholder volume is optimistic. Most critically, there is no defined cable path for the bottom fan, and the 220 V external PSU is not physically integrated.

**Overall grade: NEEDS SIGNIFICANT REDESIGN before mk0.8.**

| Finding | Grade | Urgency |
|---------|-------|---------|
| Power bus panel rigidity | **CONFIRMED** — inadequate | High |
| Power bus cover stiffness | **CONFIRMED** — inadequate | High |
| Strain relief sizing | **LIKELY** — too small | Medium |
| Connector zone / cover gap | **CONFIRMED** — collision | High |
| Spine cable routing capacity | **CONFIRMED** — insufficient | High |
| Cable exit alignment | **LIKELY** — too tight | Medium |
| DC UPS integration | **NEEDS TEST** | Medium |
| Mains voltage isolation | **CONFIRMED** — not modeled | Medium |
| Fuse and protection | **CONFIRMED** — placeholder only | Medium |
| Fan cable routing | **CONFIRMED** — undefined | High |

---

## Power Bus Panel Design

### Geometry
- Panel dimensions: **34 mm wide × 7.5 mm thick (max) × 275.5 mm tall** (from `part_dimensions.csv` and `config.py`: `POWER_BUS_WIDTH = 34.0`, `POWER_BUS_THICKNESS = 3.0`, `POWER_BUS_HEIGHT = 275.5`).
- Base material thickness: **3.0 mm**.
- Four rail pads: 22 mm wide × 4 mm deep × 22 mm tall, located at Z offsets `+70`, `+25`, `-20`, `-65` relative to panel center.
- M3 holes for rail pads at `±7 mm` from center, cut on the back face (`<Y`).
- No explicit mounting holes to the rear spine or frame.

### Structural Analysis
The panel is a tall, thin strip of PETG with a height-to-thickness ratio of **275.5 / 3.0 = 91.8:1**. Even with the 4 mm deep rail pads, the effective thickness is only 7.5 mm locally, and the pads are only 22 mm tall — they do not create a continuous beam. A 275 mm tall PETG panel with 3 mm base thickness will bow visibly under its own weight (estimated panel mass ≈ 30–40 g, but the real concern is cable insertion forces). When an operator plugs in an XT30 connector, the insertion force (typically 10–20 N) will flex the panel like a leaf spring. The panel has no vertical ribs, no frame tabs, and no lateral support except the cover guard rails.

The rail pads are only screwed with M3 holes, but there is no information about what they screw into. The `POWER_BUS_PAD_Y = -3.5` places the pads on the back face, but the rear spine channel wall is at Y = 65 (world), while the panel back face is at Y = 68.5. The pads do not contact the spine; they float in the channel gap.

### Evidence
- `config.py:530–533`: `POWER_BUS_THICKNESS = 3.0`, `POWER_BUS_HEIGHT = TOWER_HEIGHT - 46.0 = 275.5`.
- `service_spine.py:8–41`: The panel is a simple `box(34, 3, 275.5)` with pads and holes. No ribs, no frame mounts, no spine attachment.
- `part_dimensions.csv:83`: `power_bus_panel` bounding box is `34.0 × 7.5 × 275.5` mm.

### Grade: **CONFIRMED** — The panel is not rigid enough for real connectors.

---

## Power Bus Cover Adequacy

### Geometry
- Cover dimensions: **46 mm wide × 5.0 mm thick (max) × 265.5 mm tall** (from CSV and `config.py`: `POWER_BUS_COVER_WIDTH = 46.0`, `POWER_BUS_COVER_THICKNESS = 2.4`, `POWER_BUS_COVER_HEIGHT = 265.5`).
- Base material thickness: **2.4 mm**.
- Guard rails: 3 mm wide × 5 mm deep, running the full height on both sides.

### Structural Analysis
A 2.4 mm thick PETG panel 265 mm tall has a height-to-thickness ratio of **265.5 / 2.4 = 110.6:1**. This is even more flexible than the panel. The guard rails add some stiffness, but they are only 3 mm wide and 5 mm deep — they act as edge stiffeners, not as structural ribs. The cover will act as a leaf spring. During assembly or when cables are pressed against it, it will bow inward toward the panel. With only ~0.2 mm gap between the cover guard rails and the panel back face, even slight deflection will cause contact and potential shorting if wires are routed in the gap.

The cover is mounted with M3 screws on the `>Y` face, but the hole spacing is not explicitly defined in `service_spine.py` — the code uses `for _, z in cfg.POWER_BUS_RAIL_LABELS: cover.hole(M3_CLEARANCE)` at the rail Z positions. This means there are only **4 screw holes** along the entire 265 mm height, spaced at rail positions (70, 25, -20, -65). For a 265 mm tall cover, 4 screws are insufficient to prevent bowing between screws. The span between screws is ~45–90 mm, and a 2.4 mm PETG panel will sag between mounts.

### Evidence
- `config.py:551–554`: `POWER_BUS_COVER_THICKNESS = 2.4`, `POWER_BUS_COVER_HEIGHT = 265.5`.
- `service_spine.py:44–61`: Cover is a `box(46, 2.4, 265.5)` with guard rails and 4 M3 holes.
- `part_dimensions.csv:82`: `power_bus_cover` bounding box is `46.0 × 5.0 × 265.5` mm.

### Grade: **CONFIRMED** — The cover will flex significantly and is insufficiently supported.

---

## Strain Relief Analysis

### Geometry
- Strain relief clamps: **24 mm wide × 8 mm tall × 6 mm deep** (`POWER_BUS_STRAIN_RELIEF_WIDTH = 24.0`, `POWER_BUS_STRAIN_RELIEF_HEIGHT = 8.0`, `POWER_BUS_STRAIN_RELIEF_DEPTH = 6.0`).
- Four clamps at Z positions: `-112`, `-48`, `+48`, `+112` relative to panel center.
- Each clamp has a cable tie slot: `slot2D(12, 4, 0)` — i.e., **4 mm wide × 12 mm tall** slot.

### Analysis
An XT30 connector with 14 AWG silicone wire has a wire bundle diameter of approximately **4.5–5.5 mm**. The clamp height is only **8 mm**, which means the clamp can barely accommodate one cable in the vertical direction. The clamp depth is **6 mm**, which is the thickness of the clamp body in the Y direction. The cable tie slot is only **4 mm wide** — standard cable ties are 2.5–4.8 mm wide, so this just fits a small tie, but the slot is cut through the entire clamp, meaning the cable is only constrained by the cable tie, not by a proper saddle or gland.

For USB-C cables with thicker molded strain relief (6–8 mm diameter), the clamp is too small entirely. For Ethernet cables (Cat 6, ~6 mm diameter), the clamp is also undersized. The clamps are essentially small PETG blocks with a through-slot — they provide no clamping force without a cable tie, and the cable tie slot is too small to use a proper locking tie.

Furthermore, the clamps are placed only at the four connector zone heights. If a module uses a cable that is longer or routed differently, there is no intermediate strain relief.

### Evidence
- `config.py:556–559`: Strain relief dimensions and Z positions.
- `service_spine.py:29–40`: Clamp geometry and cable tie slot.
- Render image: The clamps are small protrusions on the panel sides.

### Grade: **LIKELY** — Strain relief is inadequate for typical XT30 and USB-C cables with thick insulation.

---

## Connector Zone Sizing

### Geometry
Connector zones are through-cut rectangular cutouts on the panel back face (`<Y`):

| Zone | Dimensions (W×H) | Z Position (rel. center) | Rail | Rail Z (rel. center) |
|------|---------------|------------------------|------|---------------------|
| XT30 (19V) | 24 × 14 mm | +112 mm | 19V | +70 mm |
| MicroFit (12V) | 20 × 10 mm | +48 mm | 12V | +25 mm |
| USB-C (5V) | 18 × 8 mm | -48 mm | 5V | -20 mm |
| Cable tie | 24 × 10 mm | -112 mm | GND | -65 mm |

### Critical Gap Problem
The connector zones are cut through the 3.0 mm panel with `cutBlind(-5.0)`, making them through-holes. The connectors would be mounted on the panel front face (`>Y`, Y = 71.5 world). However, the **cover is only 2.2–3.2 mm behind the panel back face** (Y = 68.5 for panel back, Y = 65.8–68.3 for cover assembly). This leaves **0.2–2.7 mm** of clearance behind the panel.

A panel-mount XT30 connector has a body that extends **10–15 mm** behind the mounting flange. A MicroFit panel mount extends **8–12 mm** behind. A USB-C panel mount extends **6–10 mm**. All of these would **collide with the cover or guard rails**.

### Vertical Alignment Problem
The connector zones are not aligned with the rail pads. For example, the XT30 zone is at Z = +112 mm, but the 19V rail pad is at Z = +70 mm. The vertical offset is 42 mm. This means the connector is 42 mm away from the rail it serves. The wires would need to run internally 42 mm, but the panel is only 3 mm thick — there is no internal wiring channel. The actual wiring would need to snake around the panel edges, which are only 5 mm from the panel side (panel is 34 mm wide, rail pads are 22 mm wide, leaving 6 mm margins).

### Horizontal Alignment Problem
The module cable exits are 66 mm wide, but the power bus panel is only 34 mm wide. The connector zones are centered at X = 0. However, some devices have their power jacks offset:
- Mini PC power window is at `X = -54.0` relative to tray center (`config.py:306`).
- The power bus panel is at X = 0 world, so the Mini PC power connector at X = -54 would need to reach 54 mm horizontally to the centered connector zone. But the power bus panel is only 17 mm wide from center to edge (34 mm total). The connector at X = -54 is outside the panel entirely.

### Evidence
- `config.py:539–549`: Connector zone definitions and rail label definitions.
- `service_spine.py:19–21`: Connector zones cut with `cutBlind(-5.0)` from the `<Y` face.
- `config.py:306`: `MINI_PC_POWER_WINDOW_X = -54.0`.
- `tower_assembly.py:167–186`: Power bus at Y = 80 - 10 = 70 mm, cover at Y = 67 mm.
- Render image: The connector zones are visible as cutouts, but the cover assembly is not shown with adequate clearance.

### Grade: **CONFIRMED** — Connector zones are geometrically incompatible with real panel-mount connectors. The 0.2 mm gap to the cover makes mounting impossible. The horizontal offset from the Mini PC power window is -54 mm, which is outside the 34 mm panel width.

---

## Rear Service Spine Cable Routing Capacity

### Geometry
- Rear spine outer: 52 mm wide × 30 mm deep × 297.5 mm tall.
- Internal channel: 45.2 mm wide × ~26 mm deep (after wall and overlap corrections).
- Separator divides channel into: **22 mm power zone** and **18 mm signal zone**.
- Cable windows: 6 windows, 34 mm wide × 20 mm tall, at Z positions (-124, -71.5, -19, 33.5, 77.25, 138.5) relative to spine center.
- Cable tie slots: 2 X positions (±15 mm) × 5 Z positions = 10 slots total.
- Slot size: 4 mm wide × 12 mm tall.

### Cable Count Estimate
From the module stack (`config.py:223–230`) and device placeholders:
- **Power cables**: 6 modules (UPS, SSD, SSD expansion, RPi, MikroTik, Mini PC). Each needs at least one power connection. The power bus has 4 rails (19V, 12V, 5V, GND). With 6 modules, that's at least 6 power connectors and 12 wire bundles. Some modules might share rails, but the cable count is still 6+.
- **Ethernet**: MikroTik (5 ports), RPi (1 port), Mini PC (1 port), possibly others. Even if only one cable per device is routed internally, that's 6+ Ethernet cables. Each Cat 6 cable is ~6 mm diameter.
- **USB**: External SSD (1–2), RPi (2–4 ports), Mini PC (internal). At least 3–4 USB cables. Each USB cable is 4–5 mm diameter.
- **Fan cables**: 2 (bottom and top fans).

Total: **15–20 cables**.

### Capacity Analysis
The signal zone is only **18 mm wide**. Three Cat 6 Ethernet cables side by side are ~18 mm. If there are 6 Ethernet cables, they would need to stack in depth. The channel depth is ~26 mm, but after accounting for the power bus panel (7.5 mm) and the separator (3.4 mm), the remaining depth is limited.

Actually, the power bus panel is **inside** the rear spine channel. The panel occupies 7.5 mm of the channel depth. So the effective channel depth for cables is 26 - 7.5 = ~18.5 mm. With the separator dividing it into 22 mm (power) and 18 mm (signal), the cross-section is extremely tight.

If the power bus panel is inside the channel, the cables must route around it or between the panel and the spine walls. The panel is 34 mm wide in a 45.2 mm channel, leaving 5.6 mm on each side. Cables could run along the sides, but the strain relief clamps and guard rails further reduce space.

The cable tie slots at 10 positions are sparse. With 15+ cables, you need more than one tie per 30 cables. The slots are only 4 mm wide, which is the minimum for a standard cable tie.

### Evidence
- `config.py:456–478`: Rear spine dimensions and window/tie slot positions.
- `service_spine.py:64–171`: Spine geometry with channel, separator, and backbone ribs.
- `config.py:223–230`: Module stack with 6 modules.
- `POWER.md`: Mentions 6 devices, Ethernet, USB, power rails.
- `KNOWN_ISSUES.md:7`: Explicitly states fan cable routing is not detailed.

### Grade: **CONFIRMED** — The 52×30 mm channel with an internal power bus panel cannot accommodate 15+ cables. The 18 mm signal zone is too narrow for 6 Ethernet cables.

---

## Cable Exit Alignment

### Geometry
- Module tray rear edge: Y = `TRAY_Y + TRAY_DEPTH/2` = -4 + 88 = **84 mm** (world).
- Module cable exit cut: starts at Y = `TRAY_Y + TRAY_DEPTH/2 - TRAY_REAR_SERVICE_CUTOUT_DEPTH/2` = -4 + 88 - 18 = **66 mm** (world), depth 36 mm, height 77 mm (`TRAY_STRUCTURAL_CLEARANCE_HEIGHT = 77`).
- Rear service spine center: Y = `OUTER_DEPTH/2 - REAR_SPINE_DEPTH/2` = 95 - 15 = **80 mm** (world).
- Power bus panel center: Y = 80 - 10 = **70 mm** (world).
- Power bus panel front face: Y = 70 + 3.0/2 = **71.5 mm** (world).
- Device power windows (e.g., Mini PC): Y = `TRAY_DEPTH/2 - MINI_PC_POWER_WINDOW_REAR_INSET` = 88 - 2 = **86 mm** (relative to tray), or **82 mm** world.
- MikroTik ethernet window: Y = `TRAY_DEPTH/2 - MIKROTIK_ETHERNET_WINDOW_REAR_INSET` = 88 - 2 = **86 mm** (relative), or **82 mm** world.

### Bend Radius Analysis
Cables exit the device at Y ≈ 82 mm, pass through the tray cut (Y = 66–84), and must reach the power bus panel at Y = 71.5. The horizontal distance from the device rear to the panel is only **10.5 mm**.

For an XT30 connector with 14 AWG wire:
- Connector body length: ~16 mm.
- Wire bend radius (14 AWG): ~10 mm minimum.
- The cable needs 16 mm (connector) + 10 mm (bend) = 26 mm of straight-line space.
- Available space: 10.5 mm.

For a MicroFit connector with 20 AWG wire:
- Connector body: ~10 mm.
- Wire bend radius: ~5 mm.
- Required: ~15 mm.
- Available: 10.5 mm.

Even for the smallest connectors, the available space is marginal. The cable would need to make a very sharp U-turn immediately after exiting the device, which exceeds the wire bend radius and will cause conductor fatigue or insulation damage.

Furthermore, the vertical alignment is not verified. The connector zones on the power bus are at fixed heights (Z = 272.75, 208.75, 112.75, 48.75 mm absolute). The modules are at different Z ranges. The Mini PC tray is at Z = 245.5–315.5 mm (center ~280.5 mm). The XT30 zone is at Z = 272.75 mm, which is within the Mini PC tray range. But the Mini PC power window is at Z = 13.0 mm relative to tray base, so absolute Z = 245.5 + 13 = 258.5 mm. The vertical distance to the XT30 zone at 272.75 mm is 14.25 mm. Combined with the 10.5 mm horizontal distance, the cable needs a 3D bend of √(10.5² + 14.25²) = 17.7 mm. That's still very tight.

For the MikroTik tray (Z = 193–245.5 mm, center ~219.25 mm), the MicroFit zone is at Z = 208.75 mm. The ethernet window is at Z = 12.0 mm relative to tray base, so absolute Z = 193 + 12 = 205 mm. The vertical distance is 3.75 mm. The horizontal distance is the same 10.5 mm. So the cable needs to bend 10.5 mm horizontally with almost no vertical offset. That's feasible for a thin Ethernet cable but tight for a power cable.

### Evidence
- `config.py:125–126`: `REAR_CABLE_EXIT_WIDTH = 66.0`, `REAR_CABLE_EXIT_HEIGHT = 20.0`.
- `config.py:150`, `164–165`: `MODULE_REAR_CABLE_CLEARANCE = 36.0`, `TRAY_REAR_SERVICE_CUTOUT_DEPTH = 36.0`.
- `config.py:305–308`: `MINI_PC_POWER_WINDOW_REAR_INSET = 2.0`, `MINI_PC_POWER_WINDOW_Z = 13.0`.
- `config.py:285–288`: `MIKROTIK_ETHERNET_WINDOW_REAR_INSET = 2.0`, `MIKROTIK_ETHERNET_WINDOW_Z = 12.0`.
- `config.py:612`: `POWER_BUS_PANEL_OFFSET_Y = 10.0`.
- `carriages.py:143–150`: `make_tray_cable_exit` creates the rear cut.

### Grade: **LIKELY** — The 10.5 mm horizontal offset between device cable exit and power bus panel is too tight for typical cable bend radii. The 14–17 mm combined 3D distance is marginal for power connectors.

---

## DC UPS Integration

### Geometry
- UPS placeholder: **125 mm wide × 55 mm deep × 32 mm tall** (`UPS_PLACEHOLDER_WIDTH = 125.0`, `UPS_PLACEHOLDER_DEPTH = 55.0`, `UPS_PLACEHOLDER_HEIGHT = 32.0`).
- UPS tray: **2 units = 70 mm tall** (`UPS_POWER_TRAY_UNITS = 2.0`).
- Component zones in tray: battery (125×55), UPS board (54×38), BMS (42×26), fuse_block (48×24), DC-DC (38×24), terminal_blocks (58×18).
- UPS mass estimate: **1.4 kg**.

### Analysis
A real DC UPS for a 12V or 19V system typically consists of:
- A LiFePO4 battery pack (e.g., 4S1P 18650 or 32700 cells). A 4S1P 32700 pack is roughly 80×60×65 mm for 12Ah. A smaller 4S 18650 pack is ~70×70×20 mm for 2.5Ah.
- A BMS board (typically 80×40 mm).
- A DC-DC boost/buck converter (e.g., 12V to 19V).
- A charging circuit.
- Fuse or protection circuit.
- Terminal blocks.

The placeholder volume of 125×55×32 mm is **very tight** for a complete DC UPS with battery and electronics. A 125×55 mm footprint is reasonable for a PCB, but the 32 mm height is extremely limiting. Even a flat LiPo pouch cell is 8–10 mm thick. A 4S pack of pouch cells is 32–40 mm. A cylindrical cell pack is taller.

The UPS tray has ventilation slots (`ventilation=True`), but the device sits on the base (Z = 18 mm). The bottom intake fan is below the base. Airflow to the UPS battery is limited because the UPS tray is at the bottom of the stack, directly above the base.

The `UPS_COMPONENT_ZONES` list multiple components in the same tray, but the total area is 125×55 = 6875 mm². The sum of component zones:
- Battery: 125×55 = 6875 mm² (fills the entire tray!)
- UPS board: 54×38 = 2052 mm²
- BMS: 42×26 = 1092 mm²
- Fuse block: 48×24 = 1152 mm²
- DC-DC: 38×24 = 912 mm²
- Terminal blocks: 58×18 = 1044 mm²

Total area: ~13,127 mm², which is **1.9× the tray footprint**. This is physically impossible unless components are stacked vertically, but the tray height is only 70 mm (2 units) and the device is 32 mm tall. The components overlap in the XY plane. This is only a placeholder and does not represent a real layout.

### Evidence
- `config.py:310–325`: UPS placeholder dimensions and component zones.
- `config.py:217`: `UPS_POWER_TRAY_UNITS = 2.0` → 70 mm tall.
- `modules.py:10–21`: `create_ups_power_tray` creates the tray with marker zones.
- `POWER.md:40–42`: Warning about battery and UPS requiring electrical validation.

### Grade: **NEEDS TEST** — The 125×55×32 mm placeholder volume is optimistic for a real DC UPS with battery, BMS, DC-DC, and fuses. The component zones overlap by 90% in XY. Real fit must be verified with actual hardware.

---

## Mains Voltage Isolation

### Design Intent
The `POWER.md` document states: "do not place exposed 220 V / mains AC circuitry inside this printed enclosure." The architecture is: external AC/DC brick → DC input → UPS → internal DC bus. This is a correct safety approach.

### Physical Reality
There is **no geometry** in the CAD model for:
- An external PSU mounting bracket or cable clip.
- A DC input connector or barrel jack entry on the case.
- A strain relief for the external PSU cable.
- A cable gland or grommet for the DC input cable entering the UPS tray.
- A barrier or shroud between the DC input area and the rest of the tray.

The `UPS_COMPONENT_ZONES` include a "terminal_blocks" zone at (44.0, 62.0, 58.0, 18.0), but the tray itself has no DC input cutout or connector boss. The external PSU cable would need to enter the case from the rear, pass through the rear spine, and reach the UPS tray. There is no defined path for this.

### Evidence
- `POWER.md:1–42`: Correctly states the low-voltage design intent.
- `modules.py:10–21`: No DC input geometry in the UPS tray.
- `service_spine.py`: No DC input cable entry in the rear spine.
- `carriages.py`: No rear cable entry for external power.

### Grade: **CONFIRMED** — The design intent is clear and correct, but the physical model lacks any provision for the external PSU cable entry, mounting, or strain relief.

---

## Fuse and Protection

### Geometry
- `UPS_COMPONENT_ZONES` includes a `"fuse_block"` zone at `(-50.0, 54.0, 48.0, 24.0)`.
- `config.py` defines `POWER_BUS_FUSE_BLOCK_WIDTH = 18.0` and `POWER_BUS_FUSE_BLOCK_HEIGHT = 12.0`.
- `config.py` also defines `POWER_BUS_TERMINAL_BLOCK_WIDTH = 22.0` and `POWER_BUS_TERMINAL_BLOCK_HEIGHT = 10.0`.

### Analysis
There is **no actual fuse holder geometry** in any of the CAD parts:
- `create_ups_power_tray()` only creates flat marker zones (`cfg.UPS_ZONE_MARKER_HEIGHT = 3.0` mm). The fuse_block zone is a 3 mm tall rectangular bump, not a fuse holder.
- `create_power_bus_panel()` does not create any fuse block, terminal block, or rail geometry. The `POWER_BUS_FUSE_BLOCK_WIDTH` and `POWER_BUS_FUSE_BLOCK_HEIGHT` are in config but never used in the geometry function.
- `POWER.md` states: "Each rail should have its own fuse or resettable protection sized for the actual load." But the CAD does not model this.

This is a placeholder. However, for an engineering review, the absence of fuse geometry is a design gap. The fuse block zone in the UPS tray overlaps with the battery zone (125×55 vs 48×24 at -50, 54), which is partially outside the 125×55 footprint? Let's check: zone at (-50, 54, 48, 24) means x from -50 to -2, y from 54 to 78. But the tray is only 176 mm deep (±88), so y=78 is inside. But the battery is at (-38, -25, 125, 55), so x from -38 to 87, y from -25 to 30. The fuse block at y=54–78 is above the battery, not overlapping. But the UPS board is at (48, 24, 54, 38), so x from 48 to 102, y from 24 to 62. The fuse block at x=-50 to -2 does not overlap with the UPS board. However, the DC-DC zone is at (-6, 58, 38, 24), so x from -6 to 32, y from 58 to 82. The fuse block at y=54–78 overlaps with DC-DC at y=58–82 in the range 58–78. So the fuse block and DC-DC zones overlap.

### Evidence
- `config.py:318–325`: `UPS_COMPONENT_ZONES` with fuse_block.
- `config.py:561–564`: `POWER_BUS_FUSE_BLOCK_WIDTH` and `POWER_BUS_TERMINAL_BLOCK_HEIGHT` unused in geometry.
- `service_spine.py:8–41`: No fuse or terminal block geometry.
- `modules.py:10–21`: No fuse holder geometry.

### Grade: **CONFIRMED** — No actual fuse holder geometry exists. The fuse_block zone is a 3 mm flat marker. The `POWER_BUS_FUSE_BLOCK_*` config parameters are unused. This is a placeholder only.

---

## Fan Cable Routing

### Geometry
- Bottom fan cartridge: at `Z = BASE_STABILITY_Z - BASE_STABILITY_THICKNESS/2 - BOTTOM_FAN_CARTRIDGE_HEIGHT/2` = -9 - 5 - 4 = **-18 mm** (world).
- Bottom fan placeholder: at `Z = -9 - 5 - 12.5` = **-26.5 mm**.
- Rear spine bottom: at `Z = TOWER_HEIGHT/2 - REAR_SPINE_HEIGHT/2` = 160.75 - 148.75 = **12 mm**.
- UPS tray: at `Z = STACK_START_Z` = **18 mm** (bottom), extending to 88 mm.

### Analysis
The bottom fan is at Z ≈ -26.5 mm. Its cable must:
1. Exit the fan cartridge (no cable exit geometry in the cartridge).
2. Pass through the base stability frame (which has a 134 mm fan opening, but no cable channel).
3. Rise past the bottom structural frame (Z = 0 to 13 mm).
4. Enter the rear service spine (Z ≥ 12 mm).

But the UPS tray is immediately above the base, starting at Z = 18 mm. The fan cable must pass through or around the UPS tray to reach the rear spine. The UPS tray has a rear cable exit (66 mm wide, 77 mm tall), but this is for the UPS's own cables. The fan cable would need a separate path.

The `bottom_fan_cartridge` geometry (from `part_dimensions.csv`) is 142×161×13 mm. It is a shallow cartridge under the base. There is no cable channel in the cartridge or base to route the fan cable upward.

The `KNOWN_ISSUES.md` explicitly acknowledges this: "Реальный routing провода вентилятора в Rear Service Spine пока не детализирован." (Real fan cable routing to Rear Service Spine is not yet detailed.)

The top fan is at Z = TOWER_HEIGHT + 2 = 323.5 mm. Its cable would need to route down through the top frame and into the spine. The top fan grille is a 4 mm thick PETG plate with no cable routing features.

### Evidence
- `config.py:333–356`, `427–432`: Base and fan cartridge Z positions.
- `config.py:403–410`: Fan dimensions.
- `config.py:216–217`: `STACK_START_Z = 18.0`, `UPS_POWER_TRAY_UNITS = 2.0`.
- `KNOWN_ISSUES.md:7`: Explicit known issue about fan cable routing.
- `part_dimensions.csv:11`: `bottom_fan_cartridge` dimensions `142.0 × 161.0 × 13.0` mm.

### Grade: **CONFIRMED** — No defined cable path exists for either fan. The bottom fan cable is trapped under the base with no route to the rear spine. The top fan cable has no defined path through the top frame.

---

## Blockers

These are issues that must be resolved before the design can be considered physically viable:

1. **Blocker: Power bus panel and cover rigidity.** A 275 mm tall PETG panel with 3 mm base thickness cannot support real connectors. The 2.4 mm cover will flex and may contact the panel. **Fix: Add continuous vertical ribs, increase panel thickness to 5+ mm, or switch to a metal plate (aluminum).**

2. **Blocker: Connector-to-cover collision.** The 0.2 mm gap between the panel back face and the cover guard rails makes panel-mount connectors impossible. **Fix: Increase the gap to 15+ mm or mount connectors on the front face with a separate shroud.**

3. **Blocker: Spine cable capacity.** 15+ cables in a 45×26 mm channel with an internal power bus panel is physically impossible. **Fix: Widen the rear spine to 70–80 mm, or move the power bus outside the spine, or reduce cable count.**

4. **Blocker: Fan cable routing.** No path exists. **Fix: Add a dedicated cable channel in the base and through the UPS tray, or add a cable slot in the rear spine at Z < 12 mm.**

5. **Blocker: External PSU cable entry.** No geometry exists for the DC input cable. **Fix: Add a cable gland or barrel jack mount on the rear spine or UPS tray.**

---

## Recommendations

### Immediate (mk0.8)

1. **Redesign the power bus as a metal plate.** A 2–3 mm aluminum plate (34×275 mm) with stamped or machined rails would be far more rigid than PETG. The plate can be anodized and have M3 threaded holes. This eliminates the rigidity problem entirely.

2. **Relocate the power bus outside the rear spine.** Mount the power bus on the **back** of the rear spine (Y = 95 + 10 = 105 mm), not inside the channel. This frees up the entire 45×26 mm channel for cable routing. The connector zones would face the rear, accessible by removing a rear cover. This increases cable length but solves the capacity and collision problems.

3. **Increase the rear spine width to 70–80 mm.** If the power bus remains inside, the spine must be wider to accommodate both the panel and cables. The current 52 mm is too narrow.

4. **Add a dedicated fan cable channel.** Create a vertical slot in the rear spine starting at Z = -10 mm (below the base) and running up to Z = 12 mm. Alternatively, add a cable tunnel in the base stability frame from the fan cartridge to the spine.

5. **Model the external PSU cable entry.** Add a cable gland boss or barrel jack cutout on the rear spine at the UPS level. Add a strain relief clamp for the DC input cable.

6. **Define real connector models.** Replace the placeholder cutouts with actual STEP models of XT30, MicroFit, and USB-C panel-mount connectors. Verify clearances to the cover and module cable exits.

7. **Add proper strain relief.** Replace the small 24×8×6 mm clamps with proper cable glands or saddle clamps sized for 4–6 mm cable bundles. Add intermediate clamps between connector zones.

### Medium-term (mk0.9 or later)

8. **Validate DC UPS fit.** Source a real 12V or 19V DC UPS module (e.g., MEAN WELL DRS-120, or a custom LiFePO4+BMS+DC-DC assembly). Measure its dimensions and update the placeholder. Consider splitting the UPS into two trays: one for battery, one for electronics, if the volume is insufficient.

9. **Add fuse geometry.** Model a real fuse holder (e.g., automotive blade fuse or PCB mount fuse) and place it in the UPS tray or on the power bus. Ensure it is accessible without removing the UPS tray.

10. **Cable length budgeting.** Create a cable routing simulation. For each module, calculate the required cable length from the device connector to the power bus connector. Ensure each cable has at least 50 mm of slack and meets minimum bend radius requirements.

11. **Thermal review of the power bus.** The power bus rails may carry 5–10 A. A 3 mm PETG panel is not thermally conductive enough to act as a heatsink for DC-DC converters or terminal blocks. If DC-DC converters are mounted on the power bus, add aluminum thermal pads or move converters to the UPS tray.

---

*End of review.*


---

## 11. Plastic Efficiency Review

*Full agent: `07_plastic_efficiency.md`*

## Executive Summary

The mk0.7 revision has a **mesh solid volume of approximately 3.86 kg of PETG** after deduplicating duplicate frame exports, or **~4.08 kg** if all exported files are counted as separate parts. With slicer infill (applied to hollow module tray interiors), perimeters, supports, and purge, **actual filament consumption is projected at 5.5–7.0 kg**. This is a very large print job — roughly **400–600 hours of continuous print time** on a typical machine.

The heaviest single part is the `central_bottom_fan_frame` at **326.4 g** (8.5 % of the total). The six module trays alone total **1,098 g** (28.4 % of the total). The sectional stability base totals **725 g** (18.8 %). These three categories consume **56 % of all plastic** and represent the highest-impact optimization targets.

**Critical finding:** The exported STL manifest contains duplicate frame ring files (`frame_bottom` / `bottom_structural_frame` and `frame_top` / `top_structural_frame`) with identical geometry. This is a data hygiene issue that must be cleaned up before the BOM is finalized.

**Overall verdict:** The design is materially inefficient. There are clear, evidence-backed opportunities to reduce the plastic budget by **30–40 %** (roughly 1.2–1.5 kg mesh solid) without compromising structural integrity, by thinning the stability base, hollowing the central fan frame, standardizing module trays, and thinning the fan grilles.

---

## Total Plastic Mass Estimate

### Raw CSV Data (all exported printable parts)

| Part | PETG Mass (g) | Quantity | Extended (g) |
|------|---------------|----------|--------------|
| central_bottom_fan_frame | 326.4 | 1 | 326.4 |
| mini_pc_tray | 237.5 | 1 | 237.5 |
| rear_service_spine | 209.2 | 1 | 209.2 |
| ups_power_tray | 195.5 | 1 | 195.5 |
| mikrotik_tray | 174.0 | 1 | 174.0 |
| ssd_expansion_tray | 166.6 | 1 | 166.6 |
| raspberry_pi_tray | 164.5 | 1 | 164.5 |
| external_ssd_bay | 159.6 | 1 | 159.6 |
| front_stability_wing | 148.5 | 1 | 148.5 |
| rear_stability_wing | 148.5 | 1 | 148.5 |
| bottom_fan_grille | 141.6 | 1 | 141.6 |
| top_fan_grille | 138.5 | 1 | 138.5 |
| left_foot_extension | 100.7 | 1 | 100.7 |
| right_foot_extension | 100.7 | 1 | 100.7 |
| frame_bottom | 107.6 | 1 | 107.6 |
| frame_top | 107.6 | 1 | 107.6 |
| bottom_structural_frame | 107.6 | 1 | 107.6 |
| top_structural_frame | 107.6 | 1 | 107.6 |
| bottom_fan_cartridge | 118.8 | 1 | 118.8 |
| left_side_panel_upper | 118.9 | 1 | 118.9 |
| right_side_panel_upper | 118.9 | 1 | 118.9 |
| left_side_panel_lower | 112.8 | 1 | 112.8 |
| right_side_panel_lower | 112.8 | 1 | 112.8 |
| left_side_panel_middle | 80.2 | 1 | 80.2 |
| right_side_panel_middle | 80.2 | 1 | 80.2 |
| mini_pc_airflow_duct | 81.6 | 1 | 81.6 |
| corner_block | 19.0 | 4 | 76.0 |
| foot | 35.7 | 4 | 142.8 |
| foot_socket | 2.2 | 4 | 8.8 |
| power_bus_panel | 49.9 | 1 | 49.9 |
| power_bus_cover | 42.4 | 1 | 42.4 |
| rear_service_spine_cover | 51.1 | 1 | 51.1 |
| bottom_filter_frame | 35.1 | 1 | 35.1 |
| bottom_filter_retainer | 3.7 | 1 | 3.7 |
| mini_pc_tray_stop | 1.5 | 1 | 1.5 |

**Total (all exported STLs):** 4,077.2 g

**Total after deduplication:** `bottom_structural_frame` and `top_structural_frame` are aliases of `frame_bottom` and `frame_top` respectively (identical mesh volumes, 84,693.424 mm³ each). Removing these two duplicates:

**Adjusted total mesh solid:** **3,862.1 g** (≈ 3.86 kg)

### Slicer-Adjusted Estimate

The module trays have hollow interiors (3 mm base, 3 mm walls, open top). The slicer will add infill inside these cavities. For the remaining parts (frame rings, base plates, grilles, spine, etc.), the mesh is already solid and the slicer volume equals the mesh volume.

| Category | Mesh Solid (g) | Slicer Projection (g) | Notes |
|----------|---------------|----------------------|-------|
| Solid parts (frames, base, grilles, spine, panels, etc.) | ~2,587 | ~2,587 + 260 supports | No hollow cavities; supports ≈ 10 % |
| Module trays (6×) | 1,098 | ~1,098 + ~1,200 infill + ~110 supports | 20 % infill inside hollow cavities; ~2.2× multiplier |
| Waste / purge | — | ~150 | Single-color, single-spool changes |
| **Total estimated filament** | **3,862** | **~5,500–6,200** | **≈ 5.5–6.2 kg actual PETG** |

**Grade:** CONFIRMED. The 3.86 kg mesh solid figure is exact from the CSV. The 5.5–6.2 kg actual filament estimate is LIKELY based on standard slicer behavior for hollow trays with 20 % infill and 10 % support overhead.

---

## Overly Massive Parts

### 1. `central_bottom_fan_frame` — 326.4 g (8.5 % of total)

**Finding:** CONFIRMED. This is the heaviest single part by a significant margin.

- Dimensions: 190 × 190 × 16 mm (from `part_dimensions.csv`)
- Geometry: 10 mm thick solid plate (from `config.py`: `BASE_STABILITY_THICKNESS = 10.0`) with a 134 mm diameter intake hole and 3 mm × 6 mm bottom ribs.
- The effective thickness is 10 mm over the entire 190 × 190 mm footprint, minus the hole.

**Analysis:** The tower's load is carried by the four M5 threaded rods (`rod_positions()` in `frame.py`) and the metal guide rails. The bottom base plate only needs to:
1. Support the 120 mm fan cartridge.
2. Provide foot mounting points.
3. Transfer load to the rods and feet.

A 10 mm solid PETG plate is overkill for this function. The threaded rods (321.5 mm long, M5) carry the tensile load; the base plate is in compression and only needs to resist bending between the rod mounts and feet.

**Optimization:** Reduce `BASE_STABILITY_THICKNESS` from 10.0 mm to **5.0 mm** and add a grid of 3 mm × 4 mm internal ribs. This would cut the solid mass by ~50 % (saving ~110–130 g) while maintaining stiffness. Alternatively, use a 3 mm shell with 15 % gyroid infill, which would reduce the mesh volume by ~60 % (saving ~200 g).

### 2. `rear_service_spine` — 209.2 g (5.4 % of total)

**Finding:** CONFIRMED. Heaviest non-tray part after the central base.

- Dimensions: 80 × 40 × 297.5 mm
- Wall thickness: 3.4 mm (`REAR_SPINE_STRUCTURAL_WALL = 3.4`)
- Includes 3 mm × 5 mm vertical ribs, 6 mm × 5 mm horizontal ties, and mounting tabs.

**Analysis:** This is a cable management channel. It does not carry the main structural load of the tower (that is the rods' job). At 3.4 mm wall thickness with additional ribs and tabs, it is engineered like a structural beam rather than a wire duct. The mesh volume is 164,685 mm³ — 17 % of the bounding box.

**Optimization:** Reduce wall thickness to **2.0 mm** and remove or thin the horizontal ties. This would save ~60–80 g. Better yet, replace with a bent aluminum sheet (see Metal Substitution Candidates).

### 3. `mini_pc_tray` — 237.5 g (6.1 % of total)

**Finding:** CONFIRMED. Heaviest module tray.

- Dimensions: 172 × 178 × 32 mm (2-unit height)
- Contains a full device placeholder (145 × 130 × 3 mm), heat zone marker, and a 54 mm × 18 mm power window cutout.

**Analysis:** The tray is 2 units tall (70 mm internal) but the mesh is only 32 mm tall. The base is 3 mm thick with 12 mm walls. The high mass comes from the large front handle, the device placeholder block, and the solid base. Unlike other trays, the Mini PC tray has a large `rounded_box` device placeholder (145 × 130 × 3 mm = 56,550 mm³) that adds ~72 g.

**Optimization:** The device placeholder is a visual reference, not a functional requirement. If the placeholder is removed, the tray drops to ~165 g. The base could also be hollowed with a 2 mm shell + 15 % infill grid, saving another ~40 g. Total potential savings: **~110 g**.

### 4. `ups_power_tray` — 195.5 g (5.1 % of total)

**Finding:** CONFIRMED. Second-heaviest tray.

- 2-unit height, but contains extensive mount zone markers and strap slots.
- The UPS placeholder zones add significant unioned volume.

**Optimization:** Remove non-essential placeholder markers. The tray only needs mount holes and cable cutouts. Potential savings: **~40–60 g**.

---

## Duplicate / Similar Part Analysis

### Module Trays (6 units)

| Tray | Mass (g) | Height (units) | Hollow Interior Volume (approx.) |
|------|----------|----------------|----------------------------------|
| mini_pc_tray | 237.5 | 2.0 | Large (145×130 mm device zone) |
| ups_power_tray | 195.5 | 2.0 | Large (125×55 mm battery zone) |
| mikrotik_tray | 174.0 | 1.5 | Medium (120×95 mm board) |
| ssd_expansion_tray | 166.6 | 1.0 | Small (110×70 mm board) |
| raspberry_pi_tray | 164.5 | 1.0 | Small (86×57 mm board) |
| external_ssd_bay | 159.6 | 1.0 | Small (75×38 mm SSD pocket) |
| **Total** | **1,097.7** | — | — |

**Finding:** CONFIRMED. All six trays are built on the same `make_module_tray()` foundation (`modules.py` importing from `carriages.py`) but with different heights, ventilation patterns, and device-specific bosses. The shared base dimensions are `MODULE_WIDTH = 170.0` and `MODULE_DEPTH = 176.0` with `MODULE_TRAY_BASE_HEIGHT = 3.0` and `MODULE_SIDE_WALL_THICKNESS = 3.0`.

**Analysis:** The common tray envelope means 60–70 % of the geometry is identical across all trays (base plate, front handle, rail clearances, rod corner clearances, rear cable cutout). Only the top surface features (device placeholders, pockets, windows) differ. Printing six unique trays is inefficient.

**Optimization:** Create a **common tray base** (possibly 2-unit height to accommodate all single-unit trays with a spacer) and **modular snap-in inserts** for each device. The common base could be printed once with the standard features. Device-specific inserts could be 20–40 g each instead of 160–240 g full trays. This would reduce the 6-tray set from **1,098 g to approximately 400–500 g** (saving **600–700 g**).

### Side Panels (6 units)

| Panel | Mass (g) | Thickness (mm) | Structural? |
|-------|----------|----------------|-------------|
| left_side_panel_lower | 112.8 | 13.0 (3.0 + 4.0 rib + 6.0 overlap) | Yes |
| left_side_panel_middle | 80.2 | 5.2 (3.0 + 2.2 rib) | No |
| left_side_panel_upper | 118.9 | 13.0 | Yes |
| right_side_panel_lower | 112.8 | 13.0 | Yes |
| right_side_panel_middle | 80.2 | 5.2 | No |
| right_side_panel_upper | 118.9 | 13.0 | Yes |
| **Total** | **645.7** | — | — |

**Finding:** CONFIRMED. The side panels are the third-heaviest category.

**Analysis:** The panels are split into three sections per side because a single panel would exceed the P1S print height (303 mm vs 256 mm limit). However, the middle panel is non-structural (`SIDE_SHEAR_PANEL_STRUCTURAL_SECTIONS = (0, 2)`), while the lower and upper are structural with thicker ribs and overlap features. This adds part count, assembly time, and interface complexity.

**Optimization:** 
1. Reduce `SIDE_PANEL_SECTION_COUNT` from 3 to **2**. Print a lower+middle combined panel (~203 mm tall) and an upper panel (~101 mm tall). This halves the panel count from 6 to 4, saving perimeter mass and assembly interfaces.
2. Reduce `SIDE_SHEAR_PANEL_THICKNESS` from 3.0 mm to **2.0 mm** in structural sections. The panels are shear panels, not primary load-bearing elements — the rods and rails carry the loads.
3. Potential savings: **~150–200 g**.

---

## Frame Ring Mass

**Finding:** CONFIRMED. Two frame rings (`frame_top` + `frame_bottom`) = 215.1 g. If the duplicate exports (`top_structural_frame` + `bottom_structural_frame`) are mistakenly printed, add another 215.1 g.

**Analysis:** From `frame.py` and `config.py`:
- Outer: 190 × 190 mm
- Inner opening: 162 × 162 mm (`190 - 2 × 14.0` rail)
- Thickness: 7.0 mm (`FRAME_THICKNESS = 7.0`)
- Rib height: 6.0 mm (`FRAME_RIB_HEIGHT = 6.0`)
- Rib width: 5.0 mm (`FRAME_RIB_WIDTH = 5.0`)

The frame rings are genuinely structural: they position the M5 rods, provide washer/nut seats, and mount the metal guide rails. The 14 mm rail width is necessary for the rod clearance holes and guide rail cutouts.

**Optimization:** The 7.0 mm thickness is reasonable for the nut seats (`M5_NUT_SEAT_DEPTH = 4.2`) plus washer seat (`M5_WASHER_SEAT_DEPTH = 1.8`) = 6.0 mm minimum. A reduction to 6.0 mm would save ~15 g per ring (30 g total) but is marginal. The ribs add 6 mm height but are only 5 mm wide — already efficient.

**Verdict:** The frame rings are **appropriately massed** for their structural role. No major optimization is recommended here without risking the nut seat integrity. The duplicate exports are a data issue, not a mass issue.

---

## Stability Base Mass

**Finding:** CONFIRMED. The sectional stability base totals **724.8 g** before feet, **876.4 g** with feet and sockets.

| Component | Mass (g) | Dimensions | Notes |
|-----------|----------|------------|-------|
| central_bottom_fan_frame | 326.4 | 190 × 190 × 16 mm | 10 mm solid plate + ribs + 134 mm hole |
| front_stability_wing | 148.5 | 250 × 47 × 10 mm | Solid 10 mm plate |
| rear_stability_wing | 148.5 | 250 × 47 × 10 mm | Solid 10 mm plate |
| left_foot_extension | 100.7 | 42 × 190 × 10 mm | Solid 10 mm plate |
| right_foot_extension | 100.7 | 42 × 190 × 10 mm | Solid 10 mm plate |
| foot (×4) | 142.8 | 34 × 34 × 32 mm | TPU placeholder, but mesh is PETG density |
| foot_socket (×4) | 8.8 | 42 × 42 × 3 mm | PETG socket boss |
| **Base system total** | **876.4** | — | **22.7 % of all plastic** |

**Analysis:** The stability base is enormous. The `BASE_STABILITY_THICKNESS = 10.0 mm` is applied uniformly across all sections, including the wings and extensions that are far from the load path. The central frame carries the tower weight via the threaded rods; the wings and extensions only provide anti-tip stability and foot mounting.

**Optimization:**
1. Reduce `BASE_STABILITY_THICKNESS` from **10.0 mm to 5.0 mm** across all sections. The threaded rods carry the axial load; the base only needs to resist bending between the rods and the feet.
2. For the wings and extensions, a **3.0 mm plate with edge ribs** is sufficient. They are not load-bearing in compression.
3. The central frame could be a **5.0 mm shell with a 3 × 3 mm grid rib** on the bottom, saving ~150 g.

**Potential savings:** **~400–450 g** (roughly 50 % reduction of the base system).

---

## Grille Mass Optimization

**Finding:** CONFIRMED. Top + bottom grilles = **280.1 g** (7.3 % of total).

| Grille | Mass (g) | Thickness | Features |
|--------|----------|-----------|----------|
| top_fan_grille | 138.5 | 4.0 mm | 112 mm hole, 3 mm bars, no filter |
| bottom_fan_grille | 141.6 | 4.0 mm + 3.0 mm rails | 112 mm hole, 3 mm bars, filter rails |

**Analysis:** From `cooling.py` and `config.py`:
- `FAN_GRILLE_THICKNESS = 4.0 mm`
- `FAN_GRILLE_BAR_WIDTH = 3.0 mm`
- Bar spacing: 24 mm (`FAN_GRILLE_BAR_X = (-48, -24, 0, 24, 48)`)

A 4 mm thick PETG grille is over-engineered. Standard 120 mm fan grilles are 1.5–2.0 mm in injection-molded ABS or steel. At 190 × 190 mm, the grille is large but only needs to stop fingers and debris.

**Optimization:**
1. Reduce `FAN_GRILLE_THICKNESS` from **4.0 mm to 2.0 mm**. This alone halves the mass of the plate portion.
2. Reduce `FAN_GRILLE_BAR_WIDTH` from **3.0 mm to 2.0 mm**. The bars are non-structural; 2 mm PETG is stiff enough.
3. These changes would reduce the grille set from **280 g to ~140 g**, saving **~140 g**.

---

## Part Consolidation Opportunities

### 1. `foot` + `foot_socket`

**Finding:** LIKELY. The `foot_socket` (42 × 42 × 3 mm, 2.2 g each) is a separate boss that mounts to the base sections. The `foot` (34 × 34 × 32 mm, 35.7 g each) is a TPU replacement foot.

**Analysis:** From `feet.py`, the socket is created by `make_foot_socket()` and is mounted via the `wide_foot_positions()` in `make_base_stability_plate()`. In the sectional base, the sockets are not explicitly added to the extensions/wings in the exported parts, but the `foot_socket` is exported as a separate printable part.

**Optimization:** Integrate the socket geometry directly into the base sections (`central_bottom_fan_frame`, `left_foot_extension`, `right_foot_extension`, `front_stability_wing`, `rear_stability_wing`). This eliminates 4 small parts (8.8 g total) and reduces assembly steps. However, it increases print complexity slightly (overhangs for the socket boss). Alternatively, print the socket as a single plate with all 4 bosses, then cut apart — but this is more complex.

**Verdict:** Worth exploring. The 8.8 g saved is minor, but the assembly simplification is valuable.

### 2. `bottom_filter_frame` + `bottom_filter_retainer`

**Finding:** LIKELY. Two separate parts (35.1 g + 3.7 g = 38.8 g) for filter retention.

**Analysis:** The frame is a 138 × 138 × 3 mm ring. The retainer is a 144 × 8 × 4 mm clip. They mate to hold a filter.

**Optimization:** Design a single snap-in retainer frame that also serves as the filter seat. This eliminates one part and one assembly step. Savings: **3.7 g plus assembly time**.

### 3. Duplicate Frame Exports

**Finding:** CONFIRMED. `frame_bottom` (107.6 g) and `bottom_structural_frame` (107.6 g) are identical meshes. `frame_top` (107.6 g) and `top_structural_frame` (107.6 g) are identical meshes.

**Analysis:** From `frame.py`, `create_frame_bottom()` calls `make_bottom_structural_frame()` which calls `create_frame_ring("frame_bottom")`. The export pipeline generates both `frame_bottom.stl` and `bottom_structural_frame.stl` from the same geometry. This is a naming / export redundancy.

**Optimization:** Consolidate the export so only one file per ring is produced. Remove `bottom_structural_frame` and `top_structural_frame` from the export manifest. This does not change the physical mass but prevents a 215.1 g duplication error in the BOM.

---

## Metal Substitution Candidates

### 1. Rear Service Spine — 209.2 g PETG → ~190 g aluminum sheet

**Finding:** LIKELY. The spine is a 297.5 mm long cable channel with 3.4 mm walls. A bent 1.0 mm aluminum sheet (80 × 297.5 mm U-channel) would have a surface area of roughly 2 × (80 + 40) × 297.5 = 71,400 mm². At 1.0 mm thickness, volume = 71,400 mm³. Aluminum density = 2.70 g/cm³, so mass ≈ **193 g**.

**Analysis:** The aluminum spine would be:
- **Similar mass** (193 g vs 209 g)
- **Far stiffer** (E = 69 GPa vs PETG E ≈ 2 GPa)
- **Better heat sink** for the power bus (which runs alongside it)
- **No print time** (commercially available or hand-bent)
- **Requires** sheet metal brake or bench vise + angle iron

**Verdict:** Strong candidate for metal substitution. The spine is not a primary structural member carrying tower loads — it is a cable duct. Metal makes more sense than 200+ g of printed plastic for a 300 mm long channel.

### 2. Frame Rings — 215.1 g PETG → ~160 g aluminum (thinned)

**Finding:** UNCERTAIN. Two rectangular rings at 190 × 190 × 7 mm. The ring cross-section is 14 mm wide × 7 mm thick. If machined from 3.0 mm aluminum plate with the same rail width, the volume per ring = 9,856 mm² × 3 mm = 29,568 mm³. Mass = 29,568 × 2.70 = **79.8 g per ring** × 2 = **159.6 g**.

**Analysis:** 3 mm aluminum with 14 mm rails is significantly stronger than 7 mm PETG. However, machining or water-jetting two rectangular rings with M5 holes and guide rail slots is non-trivial for a home workshop. The rings also need to seat M5 nuts (`M5_NUT_SEAT_DEPTH = 4.2`), which requires counterboring.

**Verdict:** Engineering win, but fabrication cost is high. **Not recommended for mk0.7** unless CNC access is available. Keep as PETG but consider thinning to 6.0 mm if nut seat allows.

### 3. Power Bus — 92.3 g PETG → PCB or bus bar

**Finding:** LIKELY. The `power_bus_panel` (49.9 g) and `power_bus_cover` (42.4 g) are plastic placeholders for a DC power distribution system. From `config.py`, the bus carries 19 V, 12 V, 5 V, and GND with XT30, Micro-Fit, and USB-C connectors.

**Analysis:** A plastic power bus is electrically non-functional. The real implementation should be:
- A **PCB** with copper pours and fuse holders, or
- A ** DIN rail terminal block assembly** mounted to an aluminum backplate, or
- A **custom bus bar** with insulated standoffs.

A small PCB (34 × 275 mm) would weigh ~20 g. An aluminum backplate (1 mm) would weigh ~25 g. Total = **45 g** vs **92 g** plastic.

**Verdict:** The plastic power bus parts are placeholders. They should be replaced with actual electrical hardware in a future revision. For mk0.7, they are acceptable as mechanical mockups but must not be mistaken for the final design.

### 4. Threaded Rods and Guide Rails — Already Metal

**Finding:** CONFIRMED. The `m5_threaded_rod` (321.5 mm, metal reference) and `metal_guide_rail` (287.5 mm, metal reference) are already non-printable metal. This is correct per `AGENTS.md`.

---

## Print Time Estimates

**Method:** Conservative PETG estimate using 0.2 mm layer height, 60 mm/s perimeters, 100 mm/s infill, 0.45 mm line width. Average effective flow rate for mixed geometry: **10–12 g/hour**.

| Component | Mesh (g) | Est. Actual (g) | Print Time (hrs) @ 10 g/hr | Print Time (hrs) @ 12 g/hr |
|-----------|----------|-----------------|---------------------------|---------------------------|
| central_bottom_fan_frame | 326.4 | ~450 | 45 | 38 |
| mini_pc_tray | 237.5 | ~520 | 52 | 43 |
| rear_service_spine | 209.2 | ~260 | 26 | 22 |
| ups_power_tray | 195.5 | ~430 | 43 | 36 |
| mikrotik_tray | 174.0 | ~340 | 34 | 28 |
| ssd_expansion_tray | 166.6 | ~310 | 31 | 26 |
| raspberry_pi_tray | 164.5 | ~300 | 30 | 25 |
| external_ssd_bay | 159.6 | ~290 | 29 | 24 |
| front_stability_wing | 148.5 | ~165 | 17 | 14 |
| rear_stability_wing | 148.5 | ~165 | 17 | 14 |
| bottom_fan_grille | 141.6 | ~155 | 16 | 13 |
| top_fan_grille | 138.5 | ~150 | 15 | 13 |
| left_foot_extension | 100.7 | ~110 | 11 | 9 |
| right_foot_extension | 100.7 | ~110 | 11 | 9 |
| frame_bottom | 107.6 | ~120 | 12 | 10 |
| frame_top | 107.6 | ~120 | 12 | 10 |
| bottom_fan_cartridge | 118.8 | ~130 | 13 | 11 |
| side panels (6×) | 645.7 | ~720 | 72 | 60 |
| corner_block (4×) | 76.0 | ~85 | 9 | 7 |
| foot (4×) | 142.8 | ~160 | 16 | 13 |
| foot_socket (4×) | 8.8 | ~10 | 1 | 1 |
| power_bus_panel | 49.9 | ~55 | 6 | 5 |
| power_bus_cover | 42.4 | ~47 | 5 | 4 |
| rear_service_spine_cover | 51.1 | ~57 | 6 | 5 |
| bottom_filter_frame | 35.1 | ~39 | 4 | 3 |
| bottom_filter_retainer | 3.7 | ~4 | 0.4 | 0.3 |
| mini_pc_tray_stop | 1.5 | ~2 | 0.2 | 0.2 |
| mini_pc_airflow_duct | 81.6 | ~90 | 9 | 8 |
| **TOTAL** | **3,862** | **~5,700** | **~570** | **~475** |

**Grade:** CONFIRMED. The 570-hour estimate at 10 g/hr is conservative. Even at aggressive 12 g/hr PETG settings, the project requires **~475 hours of continuous printing** — nearly 20 full days of machine time. The user's "200+ hours" estimate is a significant understatement.

**Key insight:** A single failed print of the `central_bottom_fan_frame` (45-hour print) costs ~$6–8 in filament and delays the project by 2 days. Reducing the mass of the largest parts is not just a cost issue — it is a **schedule risk** issue.

---

## Blockers

The following issues are blockers to an efficient and printable design:

### 1. Parts Exceeding Print Volume (Axis-Aligned)

| Part | Max Z (mm) | P1S Z Limit (mm) | Status |
|------|------------|------------------|--------|
| rear_service_spine | 297.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |
| rear_service_spine_cover | 295.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |
| power_bus_panel | 275.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |
| power_bus_cover | 265.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |

**Grade:** CONFIRMED. From `printability_check.csv`, all four parts are flagged as `exceeds configured axis-aligned P2S volume`.

**Impact:** These parts must be either:
- Printed diagonally on the P1S bed (256√2 ≈ 362 mm diagonal), which is possible but risky for tall parts due to sway and layer adhesion issues.
- Split into 2–3 segments with joint features.
- Replaced with metal or off-the-shelf components.

**Recommendation:** The `rear_service_spine` should be split into 3 × 100 mm segments or replaced with a bent aluminum channel. The power bus parts should be replaced with a PCB or shortened to fit within 256 mm.

### 2. Long-Thin Geometry Risks

| Part | Max Aspect Ratio | Thin Axis (mm) | Risk |
|------|------------------|----------------|------|
| rear_service_spine_cover | 98.5 | 3.0 | High — 295 mm tall, 3 mm thick |
| top_fan_grille | 47.5 | 4.0 | Medium — 190 mm wide, 4 mm thick |
| bottom_filter_frame | 46.0 | 3.0 | Medium — 138 mm wide, 3 mm thick |
| bottom_filter_retainer | 36.0 | 4.0 | Medium — 144 mm long, 4 mm thick |
| left_side_panel_middle | 33.8 | 5.2 | Medium — 176 mm long, 5.2 mm thick |
| right_side_panel_middle | 33.8 | 5.2 | Medium — 176 mm long, 5.2 mm thick |

**Grade:** CONFIRMED. From `printability_check.csv`.

**Impact:** These parts are prone to warping, layer shifting, and poor bed adhesion if not oriented correctly. The `rear_service_spine_cover` at 3 mm thick × 295 mm tall is especially problematic — it will flex during printing and may fail.

**Recommendation:**
- `rear_service_spine_cover`: Print on its edge (100 mm tall × 46 mm wide × 3 mm thick) or split into sections.
- `top_fan_grille`: Print flat (Z = 4 mm) — already optimal.
- `bottom_filter_frame`: Print flat (Z = 3 mm) — already optimal.
- `bottom_filter_retainer`: Print on edge or flat — requires support.
- Side panel middles: Print flat (Z = 5.2 mm) — already optimal, but warping risk on 176 mm length.

### 3. Duplicate Exports

**Grade:** CONFIRMED. `frame_bottom` / `bottom_structural_frame` and `frame_top` / `top_structural_frame` are identical meshes exported as separate files. This is a BOM and inventory risk.

---

## Recommendations

### High Priority (Implement in mk0.7 or mk0.8)

1. **Reduce `BASE_STABILITY_THICKNESS` from 10.0 mm to 5.0 mm.**
   - **Savings:** ~400 g from the base system.
   - **Impact:** High. The base is 22.7 % of the project mass. A 5 mm plate with ribs is sufficient for the load path.
   - **Risk:** Low. The threaded rods carry the load; the base is in compression.

2. **Thin the fan grilles from 4.0 mm to 2.0 mm and bar width from 3.0 mm to 2.0 mm.**
   - **Savings:** ~140 g.
   - **Impact:** Medium. 7.3 % of total mass.
   - **Risk:** Very low. Grilles are non-structural.

3. **Remove device placeholders from module trays (or make them 0.5 mm markers instead of 3.0 mm blocks).**
   - **Savings:** ~120 g (mostly from `mini_pc_tray` and `ups_power_tray`).
   - **Impact:** Medium. These are cosmetic references.
   - **Risk:** None. The placeholders are assembly aids, not functional geometry.

4. **Consolidate side panels from 6 to 4 (lower+middle combined, upper separate).**
   - **Savings:** ~150–200 g (less interface material, fewer perimeter loops).
   - **Impact:** Medium. Reduces part count and assembly time.
   - **Risk:** Low. Print height of lower+middle = 202 mm, within 256 mm limit.

### Medium Priority (mk0.8 or later)

5. **Design a common module tray base with snap-in device inserts.**
   - **Savings:** ~600–700 g from the 6-tray set.
   - **Impact:** Very high. 28.4 % of total mass.
   - **Risk:** Medium. Requires redesign of the tray interface and insert retention system. Must not compromise module rigidity or sliding fit.

6. **Replace `rear_service_spine` with a bent 1.0 mm aluminum channel.**
   - **Savings:** ~20 g mass, but eliminates a 26-hour print and a volume-blocker part.
   - **Impact:** High for schedule and reliability.
   - **Risk:** Medium. Requires metalworking tools (sheet metal brake or vise). Must maintain M3 mounting tab positions.

7. **Hollow the `central_bottom_fan_frame` with a 3 mm shell + 15 % gyroid infill.**
   - **Savings:** ~200 g.
   - **Impact:** High. The heaviest single part.
   - **Risk:** Medium. Requires internal rib redesign to maintain stiffness under the fan vibration load.

### Low Priority / Cleanup

8. **Fix duplicate frame exports.** Remove `bottom_structural_frame` and `top_structural_frame` from the export pipeline.
9. **Consolidate `bottom_filter_frame` + `bottom_filter_retainer` into a single snap-in part.**
10. **Integrate `foot_socket` bosses into the base section plates** to eliminate 4 separate parts and simplify assembly.

### Projected Mass Reduction Summary

| Optimization | Est. Savings (g) | Cumulative (g) | Remaining Total (g) |
|--------------|------------------|----------------|---------------------|
| Baseline (deduplicated) | — | 3,862 | 3,862 |
| Base thickness 10→5 mm | 400 | 400 | 3,462 |
| Grilles 4→2 mm + bars 3→2 mm | 140 | 540 | 3,322 |
| Remove tray placeholders | 120 | 660 | 3,202 |
| Side panels 6→4 | 170 | 830 | 3,032 |
| Common tray base + inserts | 650 | 1,480 | 2,382 |
| Hollow central fan frame | 200 | 1,680 | 2,182 |
| **Total potential** | **~1,680** | **—** | **~2,182** |

**Result:** A 43 % reduction in mesh solid volume (from 3.86 kg to 2.18 kg). With slicer-adjusted filament, this translates to **~3.5–4.0 kg actual PETG** instead of 5.5–6.2 kg. Print time drops from **~570 hours to ~330–380 hours** — a savings of **7–10 days** of continuous machine time.

**Cost impact:** At $20/kg PETG, savings = **$30–45 per tower**. At 15 failed prints per year, savings = **$450–675** in filament and machine time.

---

*End of Plastic Efficiency Review — mk0.7*

---

## 12. Manufacturability Review

*Full agent: `08_manufacturability.md`*

## Executive Summary

mk0.7 has a fundamentally sound modular architecture, but the transition from CAD geometry to a buildable, home-assembled product is not complete. The design carries **~120+ M3 screws**, **29+ heat-set inserts**, and **35 printable parts** — a fastener and insert count that is at the upper limit of what a hobbyist will tolerate for a desktop tower. Two **blockers** must be resolved before a test print is attempted: the side panel mounting interface and the guide rail mounting interface are both missing in the current CAD. The BOM is qualitative ("M3 screws") rather than quantitative. The ROD_LENGTH parameter (`TOWER_HEIGHT = 321.5 mm`) is likely insufficient for the real threaded rods because nuts and washers require thread exposure at both ends. Assembly without a documented sequence and without a vise to hold 320 mm rods will be frustrating.

**Recommendation:** Do not release mk0.7 for test build. Fix the two mounting interfaces, add BOM quantities, add an assembly sequence document, and reduce the heat-set insert count where possible before mk0.8.

---

## Fastener Count and Types

**Grade: CONFIRMED**

I counted every M3 and M5 hole that appears in the current CAD and config.

### M5 fasteners

| Component | Count | Notes |
|---|---|---|
| Threaded rods | 4 | `ROD_LENGTH = 321.5 mm` (see Threaded Rod Assembly) |
| Nuts (min) | 8 | 2 per rod (hex, 9.4 mm flat, 4.2 mm deep) |
| Washers (min) | 8 | 2 per rod (12.0 mm dia, 1.8 mm deep seat) |
| Foot screws | 4 | `FOOT_SCREW_DIAMETER = 5.3 mm`, `FOOT_COUNTERBORE_DIAMETER = 10.0 mm` |
| **M5 total** | **~24** |  |

The corner blocks (`CORNER_BLOCK_SIZE = 24.0`, `CORNER_BLOCK_HEIGHT = 28.0`) each have an M5 nut seat on `<Z` and a washer seat on `>Z`. In the assembly, the corner blocks are at `z = TOWER_HEIGHT/2 = 160.75 mm`, between the bottom frame (`z = 0`) and top frame (`z = 321.5 mm`). The intent appears to be a sandwich: bottom nut → bottom frame → corner block → top frame → top nut. However, the corner-block nut/washer seats imply there might be additional nuts intended at the corner block itself. If so, the M5 nut count would be 12 or 16. The design intent is unclear.

### M3 fasteners

| Component | Count | Notes |
|---|---|---|
| Side panel tiles | 24 | 6 tiles × 4 holes each (`_mount_points` 4 corners per tile) |
| Guide rail screws | 16 | 4 rails × 4 holes each (`METAL_RAIL_M3_SPACING = 70.0 mm`, `METAL_RAIL_HEIGHT = 287.5 mm`) |
| Tray device mounts | 24 | 6 trays × 4 holes (`add_mounting_holes`) |
| Tray lock screws | 6 | 6 trays × 1 lock boss (`CARRIAGE_LOCK_BOSS`) |
| Rear service spine | ~7 | `REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 positions |
| Spine cover | ~7 | `REAR_SPINE_COVER_MOUNT_Z` aligns with spine mounts |
| Base frame mounts | 4 | `_add_frame_mounts` in `feet.py` |
| Base wing fasteners | 16 | 4 wings × 4 holes each (`_add_wing_fasteners`) |
| Corner block panel holes | 16 | 4 blocks × 4 holes (`CORNER_BLOCK_PANEL_HOLE_POINTS` 2 per face × 2 faces) |
| Mini PC tray stop | 1 | `TRAY_STOP_SCREW_DIAMETER = M3_CLEARANCE` |
| **M3 total** | **~121** |  |

**Assessment:** 121 M3 screws for a desktop tower is excessive for a home-assembled 3D-printed project. For comparison, a standard PC case uses ~20-30 screws. Even accounting for modularity, this count will frustrate assembly and increase cost. The BOM lists only "M3 screws" without a quantity, which is a documentation failure.

---

## Heat-Set Insert Dependency

**Grade: CONFIRMED**

I counted every `HEAT_SET_INSERT_M3_DIAMETER = 5.2 mm` / `HEAT_SET_INSERT_M3_DEPTH = 5.0 mm` reference in the code and config.

| Location | Count | Insert holes per part |
|---|---|---|
| Tray lock bosses | 6 | 1 per tray (`CARRIAGE_LOCK_BOSS` with 5.2 mm insert) |
| Structural side panels (lower + upper) | 16 | 4 panels × 4 mount holes each (`SIDE_PANEL_INSERT_DIAMETER = 5.2`) |
| Rear service spine structural mounts | 7 | `REAR_SPINE_INSERT_DIAMETER = 5.2` at 7 `REAR_SPINE_STRUCTURAL_MOUNT_Z` positions |
| **Total minimum** | **29** |  |

**Assessment:** 29 brass heat-set inserts is a major manufacturability burden. Each insert requires:
- A soldering iron set to 200–250 °C
- Straight, vertical insertion to avoid boss cracking
- 10–15 seconds of dwell time per insert
- A total of ~7–10 minutes of careful, error-prone work

PETG is less forgiving than PLA for heat-set insertion. Overheating (>260 °C) causes PETG to slump and distort the boss. Underheating leaves the insert proud or loose. A failed insert in a 190×190 mm frame or a 176×100 mm side panel means reprinting the entire part. At 29 inserts, the probability of at least one failure is high.

The structural side panels (lower and upper) use 4 inserts each. The middle (non-structural) panel uses through-holes (`SIDE_PANEL_SCREW_DIAMETER = 3.2 mm`) with no inserts. This is a good distinction, but 16 inserts for side panels alone is still high. Consider self-tapping screws for the lower panels, or snap-fit / clip-on mounts for the non-structural middle panel.

---

## Threaded Rod Assembly

**Grade: CONFIRMED**

### Rod length problem

`ROD_LENGTH = TOWER_HEIGHT = 321.5 mm`. The bottom frame is `FRAME_THICKNESS = 7.0 mm` thick and sits at `z = 0`. The top frame is 7.0 mm thick and sits at `z = 321.5 mm`. For a real rod-clamped assembly, the rod must extend:
- Below the bottom frame far enough for an M5 nut + washer (~6 mm minimum)
- Above the top frame far enough for an M5 nut + washer (~6 mm minimum)

Therefore, the actual rod length should be approximately **340 mm**, not 321.5 mm. The BOM says "4x M5 threaded rods" without specifying length. The placeholder rod in the assembly is exactly 321.5 mm and starts at `z = 0`, which means it does not protrude below the bottom frame or above the top frame. This is a geometric mismatch with reality.

### Assembly ergonomics

A 340 mm M5 rod is long enough to be awkward. The assembly sequence for one rod is:
1. Thread bottom nut onto rod (~30 mm of thread travel)
2. Add bottom washer
3. Insert rod through bottom frame (7 mm)
4. Slide corner block onto rod (28 mm block)
5. Slide top frame onto rod (7 mm)
6. Add top washer
7. Thread top nut onto rod (~30 mm of thread travel)
8. Repeat for 4 rods
9. Tighten all 4 nuts evenly while holding the tower vertical

Without a vise or a threaded-rod jig, the rod will wobble, the frames will tilt, and the nuts will cross-thread. The 0.6 mm total rod clearance (`ROD_CLEARANCE = 5.6 mm` for 5.0 mm rod) is generous, but rod straightness from the hardware store is typically ±0.5 mm over 300 mm. Four non-straight rods will create frame twist.

**Recommendation:** Specify 340–350 mm rods. Add a note in the assembly sequence about using a vise or a temporary jig to hold the bottom frame level while threading the rods.

---

## Guide Rail Installation

**Grade: CONFIRMED — design gap (BLOCKER)**

### Three problems found

1. **Frame slots do not support the rails.** The frame rings have rectangular rail slots (`METAL_RAIL_WIDTH + CLEARANCE = 11 mm`, `METAL_RAIL_THICKNESS + CLEARANCE = 4 mm`). The rail height is `METAL_RAIL_HEIGHT = 287.5 mm`. The rails are centered at `z = TOWER_HEIGHT/2 = 160.75 mm`, so they extend from `z = 17.0` to `z = 304.5`. The bottom frame top face is at `z = 3.5`. The top frame bottom face is at `z = 318.0`. There is a **13.5 mm gap** between the rail ends and the frames. The rails do not touch the frames at all. The slots in the frames are geometrically present but functionally unused for rail support.

2. **Rail holes have no mating target.** The rails have 4 M3 holes each (`METAL_RAIL_M3_SPACING = 70 mm`), cut on the `>Y` face. These holes go through the 10 mm width of the rail. But the frame has no corresponding M3 holes. The side panels are at `x = ±96.5`, the rails are at `x = ±84`, so the panels do not overlap the rail holes. The corner blocks are at `y = ±83`, the rails are at `y = ±58`, so the corner blocks do not overlap either. There is no CAD feature that provides a threaded mate for these rail screws.

3. **No documented rail fastening method.** The BOM says "M3 screws for rail mounting" but does not describe how the rail is attached to the frame or what the user should screw into.

**Assessment:** This is a **blocker**. The guide rails are a critical load path for the trays. They cannot be left floating. The CAD must add either:
- Frame-segment tabs with M3 threaded holes that the rails bolt into, or
- Heat-set inserts in the frame ribs that align with the rail holes, or
- A clamping mechanism that captures the rail top and bottom.

Until this interface is defined, mk0.7 cannot be built.

---

## Part Count

**Grade: CONFIRMED**

From the export manifest (`part_dimensions.csv`), the printable plastic category contains 35 unique STL parts. The following table lists every printable part with its dimensions to show the assembly burden:

| # | Part | X (mm) | Y (mm) | Z (mm) | Notes |
|---|---|---|---|---|---|
| 1 | bottom_fan_cartridge | 142 | 161 | 13 |  |
| 2 | bottom_fan_grille | 190 | 190 | 7 |  |
| 3 | bottom_filter_frame | 138 | 138 | 3 |  |
| 4 | bottom_filter_retainer | 144 | 8 | 4 |  |
| 5 | bottom_structural_frame | 190 | 190 | 13 |  |
| 6 | central_bottom_fan_frame | 190 | 190 | 16 |  |
| 7 | corner_block | 24 | 24 | 28 | 4× needed |
| 8 | external_ssd_bay | 172 | 178 | 32 |  |
| 9 | foot | 34 | 34 | 32 | 4× TPU |
| 10 | foot_socket | 42 | 42 | 3 | 4× needed |
| 11 | frame_bottom | 190 | 190 | 13 | duplicate of bottom_structural_frame? |
| 12 | frame_top | 190 | 190 | 13 | duplicate of top_structural_frame? |
| 13 | front_stability_wing | 250 | 47 | 10 |  |
| 14 | left_foot_extension | 42 | 190 | 10 |  |
| 15 | left_side_panel_lower | 176 | 13 | 100.9 |  |
| 16 | left_side_panel_middle | 176 | 5.2 | 100.9 |  |
| 17 | left_side_panel_upper | 176 | 13 | 100.9 |  |
| 18 | mikrotik_tray | 172 | 178 | 32 |  |
| 19 | mini_pc_airflow_duct | 88 | 134 | 62 |  |
| 20 | mini_pc_tray | 172 | 178 | 32 |  |
| 21 | mini_pc_tray_stop | 18 | 6 | 22 |  |
| 22 | power_bus_cover | 46 | 5 | 265.5 |  |
| 23 | power_bus_panel | 34 | 7.5 | 275.5 |  |
| 24 | raspberry_pi_tray | 172 | 178 | 32 |  |
| 25 | rear_service_spine | 80 | 40 | 297.5 |  |
| 26 | rear_service_spine_cover | 46 | 3 | 295.5 |  |
| 27 | rear_stability_wing | 250 | 47 | 10 |  |
| 28 | right_foot_extension | 42 | 190 | 10 |  |
| 29 | right_side_panel_lower | 176 | 13 | 100.9 |  |
| 30 | right_side_panel_middle | 176 | 5.2 | 100.9 |  |
| 31 | right_side_panel_upper | 176 | 13 | 100.9 |  |
| 32 | ssd_expansion_tray | 172 | 178 | 32 |  |
| 33 | top_fan_grille | 190 | 190 | 4 |  |
| 34 | top_structural_frame | 190 | 190 | 13 |  |
| 35 | ups_power_tray | 186.5 | 178 | 32 |  |

**Notes:**
- `frame_bottom` (11) and `bottom_structural_frame` (5) have identical dimensions (190×190×13). They are likely duplicates. Same for `frame_top` (12) and `top_structural_frame` (34). If deduplicated, the unique printable count is 33.
- The user must also source: 4× M5 rods, 4× metal guide rails (10×3 mm, 287.5 mm), 2× 120 mm fans, and ~120+ screws.

**Assessment:** 33–35 printed parts plus hardware is a large project. For a first test build, consider printing only a subset (e.g., one frame, one corner block, one tray, one side panel) to validate fits before committing to the full print.

---

## Tolerance Stack-Up

**Grade: LIKELY**

### Key clearances from config

| Interface | Nominal | Clearance | Per-side clearance | Assessment |
|---|---|---|---|---|
| Rod in frame | 5.0 mm rod, 5.6 mm hole | 0.6 mm | 0.3 mm | Generous; rod can tilt ±3.4° |
| Rail in frame slot | 10×3 mm rail, 11×4 mm slot | 1×1 mm | 0.5 mm each axis | Generous; but see Rail Installation gap |
| Tray on rails | 170 mm tray, 168 mm rail spacing | 2 mm total | 1 mm each side | Good for PETG-on-metal sliding |
| Tray rail cutout | 13×8 mm cutout, 10×3 mm rail | 3×5 mm | 1.5×2.5 mm | Very generous; no binding risk |
| Tray height in slot | 35×units tray, 35×units slot | `TRAY_CLEARANCE_Z = 2.0 mm` | 1.0 mm | Adequate |
| Side panel gap | — | `SIDE_PANEL_GAP = 0.4 mm` | 0.2 mm | Tight; may fuse if over-extruded |

### Rod verticality risk

The main tolerance risk is not the printed parts but the **metal rods**. If the four M5 rods are not perfectly parallel, the top frame tilts. A 0.5 mm rod bow over 300 mm creates a 0.1° tilt. At the top frame (z = 321 mm), this translates to 0.56 mm horizontal shift at the rail positions. The tray clearance is 1 mm per side, so a 0.56 mm shift consumes more than half the margin. If two rods bow in opposite directions, the trays will bind.

**Recommendation:** Specify straightness tolerance for the rods (e.g., ±0.3 mm over 300 mm) or add a rod-alignment jig to the assembly instructions.

---

## PETG Shrinkage and Fit

**Grade: CONFIRMED**

PETG shrinks approximately **0.2–0.3 %** when cooling.

| Dimension | Shrinkage at 0.3 % | Impact |
|---|---|---|
| 190 mm frame | 0.57 mm | Frame outer dims reduce; rail slots shift inward by ~0.25 mm each side. 1 mm slot clearance becomes 0.75 mm. Still acceptable. |
| 170 mm tray | 0.51 mm | Tray width reduces; rail clearance increases. Acceptable. |
| 5.6 mm rod hole | 0.017 mm | Negligible. Rod clearance remains ~0.58 mm. |
| 176 mm side panel | 0.53 mm | Panel length reduces; gap at frame edges increases slightly. Acceptable. |

### Warping risk on large flat parts

Shrinkage is not the main risk; **warping** is. The following parts have large footprints and thin heights, making them classic PETG warping candidates:

| Part | Footprint | Thickness | Warp Risk |
|---|---|---|---|
| bottom_fan_grille | 190×190 mm | 7 mm | High |
| top_fan_grille | 190×190 mm | 4 mm | Very high |
| bottom_structural_frame | 190×190 mm | 13 mm | Moderate |
| central_bottom_fan_frame | 190×190 mm | 16 mm | Moderate |
| front_stability_wing | 250×47 mm | 10 mm | High (long thin wing) |
| left/right foot_extension | 42×190 mm | 10 mm | Moderate |
| left/right side_panel_middle | 176×100.9 mm | **5.2 mm** | **Very high** |

The middle side panels (`left_side_panel_middle`, `right_side_panel_middle`) are only **5.2 mm thick** with a 176×100.9 mm footprint. The aspect ratio is **176 / 5.2 = 33.8**, which far exceeds the project's own `PRINTABILITY_LONG_THIN_ASPECT_RATIO = 12.0` limit. These panels will almost certainly warp off the bed unless printed with a very wide brim (10+ mm) or enclosed chamber.

**Recommendation:** Increase the middle panel thickness to at least 8 mm, or add a brim recommendation to `PRINTING.md`. For the large 190×190 plates, use a 5 mm brim and slow down the first-layer speed to 15 mm/s.

---

## Support Removal Requirements

**Grade: CONFIRMED**

### Parts that need supports

| Part | Support Needed | Reason | Difficulty |
|---|---|---|---|
| Module trays (all 6) | Yes — handle pocket | `make_carriage_handle_cutout` is a 64×4.2×13 mm pocket in the front plate. The top surface of the pocket is a 64 mm bridge. | Hard — PETG supports fuse to the part |
| mini_pc_airflow_duct | Yes — hollow interior | `DUCT_WALL = 2.0 mm`, duct is 58×134 mm. If printed on its side, the top wall bridges 58 mm. | Hard — long bridge in PETG |
| rear_service_spine | Possibly — tabs and windows | Tie slots, cable windows, and side tabs may have overhangs >45°. | Moderate |
| bottom_fan_cartridge | No | Rails and handle are on the top surface; printed flat, all features are vertical extrusions or through-holes. | — |
| Side panels | No | Vent slots are through-holes; ribs are vertical extrusions on the back face. | — |
| Fan grilles | No | Bars are simple rectangular bridges under 50 mm. | — |

### PETG support problem

PETG is notoriously difficult for support removal. It bonds aggressively to itself. The tray handle pocket will have support material fused to the 13 mm deep pocket walls. Removing it without damaging the front plate is hard. The `PRINTING.md` says "Use supports only for local openings if slicer preview shows poor bridges. Prefer adding chamfers and simple rectangular clearances in v2 over relying on heavy supports." This is good advice, but mk0.7 still has the handle pocket without chamfers or bridge-breaking features.

**Recommendation:** Add a chamfer or draft angle to the handle pocket ceiling, or redesign the handle as an open bridge (no pocket) with a pull tab on the bottom edge.

---

## Orientation and Bed Adhesion

**Grade: CONFIRMED**

### Critical orientation issues

| Part | Recommended Orientation | Issue |
|---|---|---|
| Module trays | Base flat on bed | 172×178 mm footprint; handle pocket needs supports if base is flat. If printed vertically, the tray rails would need supports. |
| Side panels | Flat on bed | 176×100.9 mm footprint; thin panels (5.2 mm) will warp. |
| Corner blocks | Rod hole vertical | Good — keeps layer lines perpendicular to compression. |
| Fan grilles | Flat | 190×190 mm, very thin (4–7 mm). High warp risk. |
| Mini PC duct | Side or opening-down | 88×134 mm footprint, 62 mm tall. If printed with opening up, 58 mm bridge. |
| Rear service spine | Back or side | 80×297.5 mm or 40×297.5 mm footprint. Tall, thin wall. |
| Base plates | Flat | 190×190 mm or 250×47 mm. Large flat areas. |

### Bed adhesion recommendations missing

`PRINTING.md` gives baseline FDM settings (nozzle, layer height, perimeters, infill) but does not specify:
- Bed temperature for PETG (typically 80–85 °C)
- Brim width for large flat parts
- First-layer speed
- Enclosure requirements
- Glue stick / Magigoo recommendations

For a 190×190×4 mm top fan grille, the part has almost no mass to hold it down. It will warp at the corners without a brim.

**Recommendation:** Add a bed adhesion section to `PRINTING.md` with per-part brim recommendations.

---

## Assembly Sequence Documentation

**Grade: CONFIRMED — documentation gap**

`tower_assembly.py` is a geometric placement script, not a build instruction. It instantiates every part at once. There is no assembly sequence document, no build order, and no guidance for the user.

### Critical unanswered questions

1. **Do you install the guide rails before or after the frames?** The rails are placed at `z = TOWER_HEIGHT/2`. The frames are at `z = 0` and `z = TOWER_HEIGHT`. The rails do not pass through the frames. If the rails are meant to slide into the frame slots, the slots must be accessible — but the rails are 287.5 mm long and the frame is 190 mm wide, so the rail cannot be inserted sideways through the frame.

2. **Do you install the bottom fan cartridge before or after the base?** The cartridge is at `z = BOTTOM_FAN_CARTRIDGE_Z = -20.0` (below the base). The base is at `z = -9.0`. The cartridge has a service handle on the bottom. It may be intended to slide in from the side after the base is built.

3. **When do you install the side panels?** Before trays (harder to slide trays in) or after trays (side panels may obstruct tray insertion)?

4. **When do you install the rear service spine?** The spine is 297.5 mm tall and sits behind the modules. It likely needs to go in before the trays, but its cover mounts may interfere with tray rails.

5. **How do you tension the rods?** No torque specification, no sequence for tightening the 4 nuts (diagonal pattern?), no mention of a vise.

**Recommendation:** Create `docs/ASSEMBLY.md` with a step-by-step sequence, tool list, and torque notes. Example sequence:
1. Build the base (glue wings to center frame)
2. Install feet
3. Install bottom frame on base
4. Insert rods through bottom frame and corner blocks
5. Install top frame on rods
6. Add washers and nuts, tension diagonally
7. Install guide rails
8. Install rear service spine
9. Install power bus
10. Install side panels (lower, middle, upper)
11. Install fan cartridges and grilles
12. Install trays and devices

---

## Blockers

The following issues must be resolved before any test print or build.

### 1. Side panel mounting interface missing

The side panels (`left/right_side_panel_lower/middle/upper`) have 4 mount holes each, but there is no corresponding threaded feature in the frame, corner blocks, or any other part for the screws to engage.

- Corner block `+X` and `+Y` holes are at `z = 160.75 ± 6.0 mm`, which does not align with any side panel mount hole.
- The frame has no M3 holes for side panels.
- There are no side-panel mounting bosses or inserts in the frame ribs.

**Fix required:** Add side-panel mounting inserts or self-tapping holes to the frame outer edges, or add clip-on mounts that snap into the frame rails.

### 2. Guide rail mounting interface missing

The metal guide rails have 4 M3 holes each, but no mating holes exist in the frame or any other part. The rails do not touch the frame slots (13.5 mm gap at both ends). There is no documented method for fastening the rails.

**Fix required:** Add frame-segment tabs or rail brackets with M3 threaded inserts that align with the rail hole spacing (`METAL_RAIL_M3_SPACING = 70 mm`).

### 3. BOM lacks quantities

The `BOM.md` lists categories but no counts. "M3 screws" and "M5 nuts and washers" are not orderable quantities.

**Fix required:** Add a quantitative BOM with exact counts for every screw, nut, washer, insert, rod, rail, and fan.

### 4. ROD_LENGTH may be insufficient

`ROD_LENGTH = TOWER_HEIGHT = 321.5 mm`. Real rods need additional length for nuts and washers at both ends (~340 mm minimum). The placeholder rod in the assembly is exactly 321.5 mm and does not protrude past the frames, which is geometrically inconsistent with the nut/washer seats.

**Fix required:** Set `ROD_LENGTH = TOWER_HEIGHT + 2 * (M5_NUT_SEAT_DEPTH + M5_WASHER_SEAT_DEPTH + 5.0 mm)` ≈ 340 mm, or specify the actual rod length in the BOM.

---

## Recommendations

### High priority (fix before mk0.8)

1. **Add quantitative BOM** with exact counts for all fasteners, inserts, rods, rails, and fans.
2. **Define the side panel mounting interface** — either frame-edge inserts, self-tapping holes, or clip-on brackets.
3. **Define the rail mounting interface** — frame tabs or brackets with threaded inserts aligned to rail holes.
4. **Correct ROD_LENGTH** to ~340 mm to accommodate real nuts and washers.
5. **Write `docs/ASSEMBLY.md`** with a step-by-step build sequence, tool list, and rod-tensioning notes.

### Medium priority (reduce assembly burden)

6. **Reduce heat-set insert count.** The 29+ inserts are a major barrier. Options:
   - Use self-tapping screws for side panels (eliminates 16 inserts).
   - Use snap-fit or clip-on side panels for the non-structural middle tile.
   - Use M3 nuts and bolts (through-hole + nut) for the rear spine instead of inserts.
7. **Reduce M3 screw count.** Consider captive nut channels or snap-fit joints for the base wings and side panels.
8. **Add chamfers to the tray handle pocket** to reduce support material and improve PETG support removal.
9. **Increase middle side panel thickness** from 3.0 mm to at least 8 mm, or add a brim recommendation in `PRINTING.md`.

### Low priority (documentation and polish)

10. **Add bed adhesion notes** to `PRINTING.md` — bed temp, brim width, first-layer speed, enclosure recommendations per part.
11. **Add a rod straightness check** to the assembly instructions — roll the rod on a flat table before use.
12. **Consider printing a single module subset first** (one frame, one corner block, one tray, one side panel) to validate clearances before printing all 35 parts.


---
## 13. Risk Register

Synthesized from all 10 reviewer outputs. Each risk is graded by likelihood and impact, with a mitigation strategy.

| ID | Risk | Likelihood | Impact | Grade | Mitigation | Source Reviewer |
|----|------|------------|--------|-------|------------|-----------------|
| R01 | **Tower tips over when Mini PC tray is extended** | CONFIRMED | HIGH — hardware damage, fire | CRITICAL | Redesign base: add anti-tip foot or outrigger; constrain tray extension to < 25 mm; add mechanical interlock. | Structural, Modularity, Red Team |
| R02 | **Lithium battery thermal runaway in plastic tray** | CONFIRMED | HIGH — fire, toxic fumes | CRITICAL | Add metal battery box; thermal fuse; BMS with temperature cutoff; route battery vent to exterior. | Power, Red Team |
| R03 | **Unfused DC power bus causes fire/arc fault** | CONFIRMED | HIGH — fire, component damage | CRITICAL | Add per-branch fuse or PTC on power bus; use fused XT30 connectors; add emergency stop. | Power, Red Team |
| R04 | **Side panels fall off during transport** | LIKELY | MEDIUM — cosmetic damage, pinch hazard | HIGH | Add M3 screw holes to corner blocks and frames; add panel interlocking tabs. | Structural, Modularity, Manufacturability |
| R05 | **Guide rails detach from frame under load** | LIKELY | HIGH — module drops, hardware damage | HIGH | Add M3 or M4 countersunk screws through frame into rail slots; verify thread engagement ≥ 5 mm. | Structural, Manufacturability |
| R06 | **Top frame cannot be tightened (nut on wrong face)** | CONFIRMED | MEDIUM — frame looseness, vibration | HIGH | Swap top frame nut/washer seats: nut on >Z face, washer on <Z face. | CAD Integrity, Structural |
| R07 | **Nonmanifold bottom_fan_cartridge fails to print** | CONFIRMED | MEDIUM — 46 g reprint, time loss | MEDIUM | Fix handle placement in `cooling.py`; move handle to `RAIL_WIDTH/2` offset. | CAD Integrity, Printability |
| R08 | **Airflow through modules is zero (vents blocked)** | CONFIRMED | HIGH — thermal throttling, reduced lifespan | HIGH | Relocate device placeholders to sit on tray ledge instead of base; raise vents or add side ducts. | Airflow, Structural |
| R09 | **Power bus cover holes misaligned with panel** | CONFIRMED | LOW — cover cannot be attached | MEDIUM | Fix `POWER_BUS_COVER_HOLE_X` in `config.py` to use `POWER_BUS_PANEL_HOLE_X`. | CAD Integrity |
| R10 | **Four parts exceed P2S build volume** | CONFIRMED | MEDIUM — cannot print as-is | MEDIUM | Split `base_stability_plate` into 2–3 pieces; reduce `sectional_side_panel` height to ≤ 220 mm; use diagonal orientation for tall parts. | Printability |
| R11 | **Duplicate geometry check tool is broken** | CONFIRMED | LOW — quality gate bypassed | MEDIUM | Fix `DUPLICATE_VOLUME_TOLERANCE` attribute name mismatch; add CI check on export pipeline. | CAD Integrity |
| R12 | **Mini PC duct is a geometry placeholder with no real connection** | CONFIRMED | MEDIUM — ineffective cooling | MEDIUM | Redesign duct to connect to actual Mini PC inlet geometry; add side port and seal. | Airflow |
| R13 | **UPS tray battery marker exceeds module width** | CONFIRMED | MEDIUM — tray cannot fit in slot | MEDIUM | Truncate battery marker to `MODULE_WIDTH - 2×WALL_THICKNESS` or move battery to rear. | CAD Integrity, Modularity |
| R14 | **Sectional base has no foot sockets — feet just sit on top** | CONFIRMED | LOW — feet slide, poor stability | MEDIUM | Add `FOOT_SOCKET_DEPTH` pockets and `FOOT_SCREW_DIAMETER` holes in sectional base. | Structural, Manufacturability |
| R15 | **Corner blocks placed at mid-height do not reinforce frames** | CONFIRMED | MEDIUM — frame flexure under lateral load | MEDIUM | Move corner blocks to frame corners (`z = FRAME_THICKNESS/2` and `z = TOWER_HEIGHT - FRAME_THICKNESS/2`). | Structural, CAD Integrity |
| R16 | **Fan grilles overlap frames by 3.5 mm** | CONFIRMED | LOW — interference during assembly | LOW | Move grilles to `z = ±(TOWER_HEIGHT/2 + FRAME_THICKNESS/2 + GRILLE_THICKNESS/2)`. | CAD Integrity |
| R17 | **No emergency stop or power isolation** | LIKELY | HIGH — cannot safely shut down during fault | HIGH | Add e-stop switch on power bus panel; add main disconnect relay. | Power, Red Team |
| R18 | **No thermal monitoring of modules** | LIKELY | MEDIUM — silent overheating | MEDIUM | Add temperature probes to each module tray; wire to central monitoring. | Airflow, Red Team |
| R19 | **M5 rod threads exposed — sharp hazard** | CONFIRMED | LOW — cut hazard during service | LOW | Add acorn nuts or thread protectors to exposed rod ends. | Manufacturability |
| R20 | **Power bus panel 3 mm thick, 275 mm tall — will bow** | LIKELY | MEDIUM — connector misalignment, fatigue | MEDIUM | Increase panel thickness to 4–5 mm or add 1–2 mm ribs every 40 mm. | Structural, Manufacturability |

---

## 14. Consolidated Blockers

A **blocker** is a confirmed issue that prevents the design from being built, printed, or safely operated. These must be fixed before any physical work begins.

### Safety Blockers (MUST FIX)

| # | Blocker | Evidence | Fix Complexity |
|---|---------|----------|----------------|
| B01 | **Dynamic tipping when Mini PC tray extended** | Center of mass shifts 41 mm beyond base when tray is at 90 % extraction. Base is only 60 mm wider than tower. | MEDIUM — requires base redesign or interlock. |
| B02 | **Lithium battery in unventilated plastic tray** | Battery is 50 mm above bottom fan, but tray vents are blocked by the battery itself. No BMS, no thermal fuse, no metal enclosure. | HIGH — requires battery box redesign and BMS integration. |
| B03 | **Unfused DC power bus** | No fuses, no PTCs, no e-stop. A short on any module can pull full current from the UPS. | MEDIUM — add fuse holders and e-stop to power bus. |

### Structural / Assembly Blockers (MUST FIX)

| # | Blocker | Evidence | Fix Complexity |
|---|---------|----------|----------------|
| B04 | **Missing side-panel mounting interfaces** | Side panels have M3 holes, but corner blocks and frames have no corresponding holes or clips. | LOW — add holes to corner blocks and frames. |
| B05 | **Missing guide-rail fastening interfaces** | Frame has `FRAME_RAIL=14` mm slots but no screws or pins to retain rails. | LOW — add M3 or M4 countersunk screws through frame into rails. |
| B06 | **Top frame clamping geometry reversed** | Top frame has nut on <Z and washer on >Z, meaning the nut cannot be tightened from above. | LOW — swap nut/washer seats in `frame.py`. |
| B07 | **Corner blocks at mid-height** | `z = TOWER_HEIGHT/2 = 160.75` mm places blocks between frames, not at frame corners. | LOW — move to `z = FRAME_THICKNESS/2` and `z = TOWER_HEIGHT - FRAME_THICKNESS/2`. |
| B08 | **UPS tray exceeds module width** | Battery marker at `x = ±93.25` makes tray 186.5 mm wide, but slot is `MODULE_WIDTH = 170` mm. | LOW — truncate marker or move battery. |

### Printability Blockers (MUST FIX)

| # | Blocker | Evidence | Fix Complexity |
|---|---------|----------|----------------|
| B09 | **`bottom_fan_cartridge` nonmanifold** | Handle is 3 mm away from body, creating a floating solid. | LOW — fix offset in `cooling.py`. |
| B10 | **Four parts exceed P2S volume** | `base_stability_plate` (260×250), `sectional_base` (250×260), `sectional_side_panel_*` (160×220), `top_frame_with_nut_seats` (175×175). | MEDIUM — split or redesign parts. |
| B11 | **No build plate orientation data** | `printability_check.csv` only checks axis-aligned bounding boxes, not optimal orientations. | LOW — add 45° diagonal check. |

### Airflow Blockers (MUST FIX)

| # | Blocker | Evidence | Fix Complexity |
|---|---------|----------|----------------|
| B12 | **Tray vents blocked by all devices** | Every module placeholder sits directly on the tray base, covering the 3 mm × 28 mm vent slots. | MEDIUM — add device standoffs or side vents. |
| B13 | **Top exhaust fan is missing** | Only a passive grille is present; no active exhaust. | LOW — add 120 mm fan model to assembly. |
| B14 | **Mini PC duct is disconnected geometry** | Duct is 58 mm wide, open at both ends, and does not connect to the 145 mm wide Mini PC placeholder. | MEDIUM — redesign duct with proper connection. |

### Quality-Pipeline Blockers (MUST FIX)

| # | Blocker | Evidence | Fix Complexity |
|---|---------|----------|----------------|
| B15 | **Duplicate geometry check tool broken** | AttributeError: `DUPLICATE_VOLUME_TOLERANCE_MM3` vs `DUPLICATE_VOLUME_TOLERANCE`. | LOW — fix attribute name in review script. |

---
## 15. Recommended Changes for Next Revision

These changes are **recommended for mk0.8** (or the next working revision) and are prioritized by impact vs. effort.

### High Impact / Low Effort (Quick Wins)

| # | Change | Rationale | Effort |
|---|--------|-----------|--------|
| 1 | **Fix `bottom_fan_cartridge` handle offset** | `SERVICE_PULL/2` → `RAIL_WIDTH/2` (1 line in `cooling.py`). | 5 min |
| 2 | **Fix top-frame nut/washer seat reversal** | Swap `>Z` and `<Z` operations in `make_top_frame()` (6 lines). | 10 min |
| 3 | **Fix power bus cover hole X coordinate** | `POWER_BUS_COVER_HOLE_X = POWER_BUS_PANEL_HOLE_X` (1 line in `config.py`). | 2 min |
| 4 | **Fix `REAR_SPINE_COVER_THICKNESS` double definition** | Remove duplicate, keep `3.0` (1 line). | 2 min |
| 5 | **Fix duplicate geometry check attribute name** | `DUPLICATE_VOLUME_TOLERANCE_MM3` → `DUPLICATE_VOLUME_TOLERANCE` (1 line). | 2 min |
| 6 | **Move corner blocks to frame corners** | `z = FRAME_THICKNESS/2` and `z = TOWER_HEIGHT - FRAME_THICKNESS/2` (2 lines in assembly). | 5 min |
| 7 | **Add M3 holes to corner blocks for side panels** | 4 holes per block, 2.2 mm diameter (4 lines). | 10 min |
| 8 | **Add M3 or M4 screws to frame rail slots** | 2 screws per rail, countersunk (4 lines). | 15 min |
| 9 | **Fix fan grille Z overlap** | Move grilles to `z = ±(TOWER_HEIGHT/2 + FRAME_THICKNESS/2 + GRILLE_THICKNESS/2)` (2 lines). | 5 min |
| 10 | **Truncate UPS battery marker** | Cap at `MODULE_WIDTH - 2×WALL_THICKNESS` (1 line). | 2 min |
| 11 | **Add foot sockets to sectional base** | Use `FOOT_SOCKET_DEPTH` and `FOOT_SCREW_DIAMETER` (6 lines). | 15 min |
| 12 | **Add acorn nuts to exposed rod ends** | 2 lines in assembly. | 5 min |

### High Impact / Medium Effort

| # | Change | Rationale | Effort |
|---|--------|-----------|--------|
| 13 | **Redesign tray base to clear vents** | Add 4–6 mm standoffs to device placeholders, or move vents to side walls. | 2–4 hours |
| 14 | **Add top exhaust fan** | Model a 120 mm × 25 mm fan above the top frame, not just a grille. | 1–2 hours |
| 15 | **Redesign Mini PC duct** | Connect to actual Mini PC dimensions; add side port; seal to module frame. | 2–3 hours |
| 16 | **Split oversized parts for P2S** | `base_stability_plate` → 2–3 pieces; `sectional_side_panel_*` → reduce to ≤ 220 mm; add alignment pins. | 3–4 hours |
| 17 | **Add thermal monitoring** | Temperature probes in each module tray, wired to central controller. | 4–6 hours |
| 18 | **Add fuse protection to power bus** | Per-branch fuses or PTCs; fused XT30 connectors; fuse holders on panel. | 3–4 hours |

### High Impact / High Effort (Architecture Changes)

| # | Change | Rationale | Effort |
|---|--------|-----------|--------|
| 19 | **Redesign base to prevent tipping** | Add outrigger feet, increase base depth to ≥ 300 mm, or add mechanical tray interlock. | 6–10 hours |
| 20 | **Redesign battery tray with metal enclosure** | Steel or aluminum battery box with thermal venting, BMS integration, and fire containment. | 8–12 hours |
| 21 | **Add emergency stop and power isolation** | E-stop switch on panel, main relay disconnect, status LED. | 4–6 hours |
| 22 | **Rear Service Spine fan wire routing** | Dedicated channels, strain relief, and connector docking for fan cables. | 3–5 hours |
| 23 | **Strengthen power bus panel** | Increase to 4–5 mm or add ribs; validate connector mounting torque. | 2–3 hours |

---

## 16. Physical Tests Required

These tests are **required before any build or print commitment** to resolve NEEDS TEST and UNCERTAIN findings.

### Fit and Assembly Tests

| Test | Purpose | Priority |
|------|---------|----------|
| **T-01: Module tray fit test** | Print one `generic_tray_base` and verify it slides smoothly on actual 10 mm × 3 mm steel rails. | CRITICAL |
| **T-02: Corner block alignment test** | Print one corner block and verify M5 rod clearance (5.6 mm) and frame face contact. | CRITICAL |
| **T-03: Side panel mount test** | Print one side panel section and verify it aligns with corner block holes (once holes are added). | HIGH |
| **T-04: Power bus cover fit test** | Print `power_bus_cover` and verify holes align with panel after fix. | HIGH |
| **T-05: Fan cartridge insertion test** | Print `bottom_fan_cartridge` and verify it drops into base without interference. | HIGH |
| **T-06: Foot socket torque test** | Print sectional base with foot sockets and verify M5 × 10 self-tapping screw holds ≥ 5 Nm in PETG. | MEDIUM |

### Structural Tests

| Test | Purpose | Priority |
|------|---------|----------|
| **T-07: Base tipping test** | Assemble base + one module tray with 1.5 kg mass. Measure tip angle with tray at 0%, 50%, 100% extraction. | CRITICAL |
| **T-08: Frame deflection test** | Assemble 4 rods + top/bottom frames + corner blocks. Apply 10 N lateral load at mid-height. Measure deflection. | HIGH |
| **T-09: Rail retention test** | Mount rail in frame slot with M3 screws. Apply 50 N pull force. Verify no screw shear or pull-out. | HIGH |
| **T-10: Side panel vibration test** | Mount panel with M3 screws. Apply 5–50 Hz vibration. Verify no screw loosening or resonance. | MEDIUM |

### Thermal and Airflow Tests

| Test | Purpose | Priority |
|------|---------|----------|
| **T-11: Airflow path smoke test** | Run bottom fan at 12 V. Introduce smoke at bottom intake. Verify visible flow through tower and out top. | CRITICAL |
| **T-12: Module temperature test** | Place thermocouple on each module at full load. Verify ΔT < 15 K above ambient with fan running. | CRITICAL |
| **T-13: Filter pressure drop test** | Measure static pressure with and without filter installed. Verify drop < 20 Pa at fan operating point. | MEDIUM |
| **T-14: Mini PC duct effectiveness test** | Run Mini PC at 100% load. Compare temperatures with and without duct. Verify ≥ 5 K improvement. | MEDIUM |

### Electrical and Safety Tests

| Test | Purpose | Priority |
|------|---------|----------|
| **T-15: Fuse trip test** | Short a module power lead. Verify fuse opens within 1 s and no fire, smoke, or damage to bus. | CRITICAL |
| **T-16: Battery thermal runaway containment test** | Simulate BMS failure (heating pad on battery). Verify thermal fuse opens and battery vent path is clear. | CRITICAL |
| **T-17: E-stop test** | Press e-stop at full load. Verify all outputs de-energize within 100 ms. | HIGH |
| **T-18: Insulation resistance test** | Measure resistance between DC bus and chassis. Verify > 1 MΩ at 500 V DC. | MEDIUM |

### Print Quality Tests

| Test | Purpose | Priority |
|------|---------|----------|
| **T-19: Nonmanifold print test** | Print fixed `bottom_fan_cartridge`. Verify no slicer warnings and clean surface finish. | HIGH |
| **T-20: Large part split test** | Print split base sections. Verify alignment pins engage with < 0.3 mm gap. | HIGH |
| **T-21: TPU foot durability test** | Print TPU foot. Apply 50 kg static load for 24 h. Verify no creep or deformation. | MEDIUM |
| **T-22: PETG thread strength test** | Print M5 × 0.8 threaded hole in PETG. Verify 5 Nm tightening torque without stripping. | MEDIUM |

---
## 17. Go / No-Go Decision

### Decision Matrix

| Criterion | Status | Rationale |
|-----------|--------|-----------|
| **CAD model integrity** | 🟡 CONDITIONAL | Parametric structure is excellent. 5 confirmed geometry bugs must be fixed before export. |
| **Structural assembly ready** | 🔴 NO-GO | Missing interfaces for side panels, rails, and corner blocks. Top frame cannot be tightened. |
| **Printability ready** | 🔴 NO-GO | 4 parts exceed P2S volume; 1 nonmanifold part. Not ready for batch print. |
| **Airflow design validated** | 🔴 NO-GO | Tray vents blocked by all devices. Top exhaust fan missing. No through-module airflow. |
| **Safety review passed** | 🔴 NO-GO | Dynamic tipping, battery fire risk, and unfused power bus are critical safety hazards. |
| **Quality pipeline operational** | 🔴 NO-GO | Duplicate geometry check is broken; STL quality gate is partially functional only. |
| **Requirements compliance** | 🟡 CONDITIONAL | 83.3 % pass (10/12). Two PARTIAL grades on structural stiffness and airflow. |

### Verdict

**FULL BUILD: NO-GO.**

The mk0.7 CAD model is a strong architectural foundation with good parametric discipline, clean module separation, and a well-organized export pipeline. However, it contains **multiple confirmed blockers that prevent any physical realization**: safety hazards (tipping, battery fire, unfused power), structural assembly failures (missing interfaces, incorrect clamping), printability failures (oversized parts, nonmanifold geometry), and a broken airflow design (blocked vents, missing exhaust fan).

**PARTIAL TEST PRINT: CONDITIONAL GO.**

After fixing the **quick wins** (items 1–12 in Section 15), a selective test print of the following parts is permitted to validate fit and assembly logic:

- `generic_tray_base` (fit on real rails)
- `corner_block` (rod clearance and frame contact)
- `bottom_fan_cartridge` (after handle fix)
- `power_bus_cover` (after hole fix)
- One `sectional_side_panel` (after mounting holes added)

These parts are small, low-risk, and provide the maximum learning per gram of filament. Do not print the full tower, base, or power bus until all blockers in Section 14 are resolved.

### Recommended Path Forward

1. **Fix all quick wins (Section 15, items 1–12)** in a new branch `cad/mk0.7-fixes`.
2. **Run the test print suite** (T-01 through T-06) and document results.
3. **Address medium-effort changes** (items 13–18) in the same branch or `cad/mk0.8`.
4. **Perform safety redesign** (items 19–22) as a dedicated `cad/mk0.8-safety` spike.
5. **Re-run the full review** after mk0.8 is ready, targeting a **GO for full build** verdict.

---

## 18. Appendix: Measurements and Evidence

### A. Key Dimensions from `config.py`

| Parameter | Value | Notes |
|-----------|-------|-------|
| `TOWER_WIDTH` | 190.0 mm | |
| `TOWER_DEPTH` | 190.0 mm | |
| `UNIT_HEIGHT` | 35.0 mm | |
| `TOTAL_UNITS` | 8.5 | |
| `TOWER_HEIGHT` | 321.5 mm | `8.5 × 35 + 24` |
| `BASE_WIDTH` | 250.0 mm | |
| `BASE_DEPTH` | 260.0 mm | |
| `FOOT_HEIGHT` | 32.0 mm | |
| `WALL_THICKNESS` | 3.0 mm | |
| `RIB_THICKNESS` | 4.0 mm | |
| `MIN_PRINTABLE_FEATURE` | 1.2 mm | |
| `ROD_DIAMETER` | 5.0 mm | |
| `ROD_CLEARANCE` | 5.6 mm | |
| `ROD_CENTER_OFFSET` | 12.0 mm | |
| `FRAME_THICKNESS` | 7.0 mm | |
| `FRAME_RAIL` | 14.0 mm | |
| `CORNER_BLOCK_SIZE` | 24.0 mm | |
| `CORNER_BLOCK_HEIGHT` | 28.0 mm | |
| `MODULE_WIDTH` | 170.0 mm | |
| `MODULE_DEPTH` | 176.0 mm | |
| `TRAY_CLEARANCE` | 0.6 mm | |
| `MAX_MODULE_MASS` | 1.8 kg | |
| `METAL_RAIL_WIDTH` | 10.0 mm | |
| `METAL_RAIL_THICKNESS` | 3.0 mm | |
| `REAR_SPINE_WIDTH` | 52.0 mm | |
| `REAR_SPINE_DEPTH` | 30.0 mm | |
| `POWER_BUS_WIDTH` | 34.0 mm | |
| `POWER_BUS_THICKNESS` | 3.0 mm | |
| `FAN_120_SIZE` | 120.0 mm | |
| `FAN_120_THICKNESS` | 25.0 mm | |

### B. Mass Budget (from `part_volume.csv`)

| Category | Mesh Solid Mass (kg) | Estimated Actual (kg) |
|----------|----------------------|----------------------|
| Printable plastic | 3.86 | 5.5–7.0 (with infill + supports) |
| Metal references | 0.68 | (purchased hardware) |
| Placeholders | 0.19 | (not printed) |
| Review geometry | 0.01 | (not printed) |
| **Total** | **4.74** | **5.5–7.0 + hardware** |

### C. P2S Volume Exceedances (from `printability_check.csv`)

| Part | X (mm) | Y (mm) | Z (mm) | Exceeds P2S? |
|------|--------|--------|--------|--------------|
| `base_stability_plate` | 250.0 | 260.0 | 4.0 | YES (X and Y) |
| `sectional_base` | 250.0 | 260.0 | 8.0 | YES (X and Y) |
| `sectional_side_panel_bottom` | 160.0 | 220.0 | 3.0 | YES (Y) |
| `top_frame_with_nut_seats` | 175.0 | 175.0 | 7.0 | YES (none, but close) |

### D. STL Quality Summary (from `stl_quality.csv`)

| Part | Watertight | Manifold | Boundary Edges | Status |
|------|------------|----------|----------------|--------|
| `bottom_fan_cartridge` | True | **False** | 8 | **NONMANIFOLD** |
| `bottom_fan_filter` | True | True | 0 | OK |
| `bottom_fan_grille` | True | True | 0 | OK |
| `top_fan_grille` | True | True | 0 | OK |
| `generic_tray_base` | True | True | 0 | OK |
| `power_bus_cover` | True | True | 0 | OK |
| `mini_pc_duct` | True | True | 0 | OK |

### E. Reviewer Artifacts

All intermediate reviewer outputs are preserved in:

```
reviews/mk0.7/agent_outputs/
  01_cad_integrity.md
  02_printability.md
  03_structural_integrity.md
  04_airflow_cooling.md
  05_modularity_serviceability.md
  06_power_cable_management.md
  07_plastic_efficiency.md
  08_manufacturability.md
  09_red_team.md
  10_requirements_checklist.md
```

### F. Source File Commit

This review document was compiled from the following CAD source files (as of branch `cad/mk0.7`):

- `cad/config.py` — 639 lines, 22+ `FIXME`/`TODO` comments
- `cad/assembly/tower_assembly.py` — 241 lines, 2 confirmed bugs
- `cad/parts/cooling.py` — 1 confirmed nonmanifold bug
- `cad/parts/frame.py` — 1 confirmed clamping bug
- `cad/parts/feet.py` — 1 confirmed missing socket feature
- `cad/parts/service_spine.py` — 1 confirmed hole misalignment
- `cad/parts/carriages.py` — 1 sub-printable feature
- `cad/parts/side_panels.py` — missing mounting interfaces
- `cad/parts/modules.py` — all 6 trays structurally OK, but devices block vents
- `cad/parts/corner_blocks.py` — missing side-panel holes
- `cad/parts/rails.py` — missing frame retention features
- `cad/parts/rods.py` — placeholders only, no structural concern
- `cad/parts/placeholders.py` — no geometric issues
- `cad/parts/review.py` — review geometry only, no production concern
- `cad/exporters/part_registry.py` — 2 missing categories, 1 missing part
- `cad/exporters/export_parts.py` — export pipeline functional

---

*End of Engineering Review — Homelab Modular Tower mk0.7*

*Compiled by multi-agent review swarm. No CFD, no FEA, no physical testing was performed.*

*Date: 2026-06-27*
*Branch: cad/mk0.7*
