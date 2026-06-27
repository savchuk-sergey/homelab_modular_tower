# CAD Integrity Review — Homelab Modular Tower mk0.7

**Reviewer:** CAD Integrity Reviewer  
**Revision:** mk0.7  
**Date:** 2026-04-28  
**Source of Truth:** `cad/` (Python / CadQuery)  
**Derived Artifacts:** STEP/STL from `exports/mk0.7/`

---

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
