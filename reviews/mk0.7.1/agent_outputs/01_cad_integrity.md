# CAD Integrity Review — Homelab Modular Tower mk0.7.1

**Reviewer:** CAD Integrity Reviewer  
**Revision:** mk0.7.1  
**Date:** 2026-06-27  
**Source of Truth:** `cad/` (Python / CadQuery)  
**Derived Artifacts:** STEP/STL from `exports/mk0.7.1/`

---

## Executive Summary

mk0.7.1 is a **patch revision** that successfully fixes five of the six confirmed mk0.7 geometry defects that were scoped for correction. The bottom-fan cartridge handle is now properly fused, the duplicate-geometry check runs correctly, the power-bus cover holes align with the panel, the fan grilles are flush with the structural frames, and the top exhaust fan placeholder is present in the assembly. TPU foot export is now properly categorized.

However, the revision **does not resolve** the deeper structural issues that were deferred (base-plate rail slots, UPS tray width, base stability plate vs. sectional base inconsistency, and a number of registry/config hygiene problems). One mk0.7 config bug — the double-thickness definition for the rear spine cover — is still present in a slightly altered form.

**Overall verdict:** The scoped fixes are verified and correct. The model is cleaner than mk0.7 but still carries forward several unaddressed mk0.7 blockers. No new geometry defects were introduced. The revision is acceptable as a patch, but the remaining deferred issues must be tackled before any manufacturing export.

---

## Parametric Integrity

### Overall assessment
The mk0.7.1 scoped fixes all moved hardcoded literals into `config.py`. The remaining mk0.7 magic numbers and unexplained literals are unchanged.

### Findings — mk0.7.1 fixes (verified)

| ID | Finding | Location | Evidence | Grade |
|---|---|---|---|---|
| F-01 | `BOTTOM_FAN_PANEL_Z` now computed from frame and grille thickness | `cad/config.py:616` | `-(FRAME_THICKNESS / 2 + FAN_GRILLE_THICKNESS / 2 + FILTER_RAIL_HEIGHT)` | **CONFIRMED FIXED** |
| F-02 | `TOP_FAN_PANEL_Z_OFFSET` now computed from frame and grille thickness | `cad/config.py:619` | `FRAME_THICKNESS / 2 + FAN_GRILLE_THICKNESS / 2` | **CONFIRMED FIXED** |
| F-03 | `POWER_BUS_PAD_SCREW_OFFSET_X` now drives both panel and cover holes | `cad/config.py:538` | Used in `service_spine.py` panel (line 17) and cover (line 59) | **CONFIRMED FIXED** |
| F-04 | `AIRFLOW_ARROW_HEAD_HEIGHT_RATIO` now config-driven | `cad/config.py:594` | `1.6` in config; consumed in `review.py:14` as `cfg.AIRFLOW_ARROW_HEAD_HEIGHT_RATIO` | **CONFIRMED FIXED** |
| F-05 | `AIRFLOW_ARROW_SIDE_ROTATION_DEG` now config-driven | `cad/config.py:595` | `90.0` in config; consumed in `review.py:45` as `cfg.AIRFLOW_ARROW_SIDE_ROTATION_DEG` | **CONFIRMED FIXED** |

### Findings — remaining mk0.7 issues

| ID | Finding | Location | Evidence | Grade |
|---|---|---|---|---|
| R-01 | Unexplained literal `+24.0` in `TOWER_HEIGHT` | `cad/config.py:17` | `TOTAL_UNITS * UNIT_HEIGHT + 24.0` | **CONFIRMED** — not fixed in mk0.7.1 |
| R-02 | `SPINE_COVER_THICKNESS` dead definition | `cad/config.py:486` | `SPINE_COVER_THICKNESS = 2.0` | **CONFIRMED** — overwritten at line 513 |
| R-03 | `REAR_SPINE_COVER_THICKNESS` only defined once | `cad/config.py:488` | `REAR_SPINE_COVER_THICKNESS = 3.0` | **CONFIRMED** — but line 486 creates confusion |
| R-04 | Unexplained literal `-34.0` in `METAL_RAIL_HEIGHT` | `cad/config.py:106` | `TOWER_HEIGHT - 34.0` | **CONFIRMED** — unchanged |
| R-05 | Unexplained literal `* 6.5` in `MINIPC_DUCT_ZONE_OFFSET_Z` | `cad/config.py:392` | `STACK_START_Z + UNIT_HEIGHT * 6.5` | **CONFIRMED** — unchanged |
| R-06 | Unexplained literal `* 2.2` in `TRAY_STRUCTURAL_CLEARANCE_HEIGHT` | `cad/config.py:179` | `UNIT_HEIGHT * 2.2` | **CONFIRMED** — unchanged |
| R-07 | Unexplained literal `* 0.52` in `STABILITY_COM_Z` | `cad/config.py:609` | `TOWER_HEIGHT * 0.52` | **CONFIRMED** — unchanged |
| R-08 | Unexplained literal `+22.0` in `BOTTOM_FAN_CARTRIDGE_WIDTH` | `cad/config.py:430` | `FAN_120_SIZE + 22.0` | **CONFIRMED** — unchanged |

### Notes
The mk0.7.1 fixes correctly eliminate the hardcoded `1.6` and `90` in `review.py`, and the fan-panel / power-bus offsets are now parametric. The `SPINE_COVER_THICKNESS = 2.0` at line 486 is dead code because line 513 reassigns it to `REAR_SPINE_COVER_THICKNESS` (3.0). The `+24.0` in `TOWER_HEIGHT` remains undocumented and should be replaced by a named expression (e.g., `2 * FRAME_THICKNESS + BASE_CLEARANCE`).

---

## Function Separation

### Overall assessment
No regression. The separation of parts, assembly, and export remains clean. The mk0.7.1 changes did not alter file-level separation.

### Findings

| Finding | Evidence | Grade |
|---|---|---|
| `cooling.py` still contains redundant `create_*` aliases unused by registry | `create_fan_panel`, `create_bottom_fan_panel`, `create_top_fan_panel`, `create_bottom_fan_cartridge`, `create_bottom_filter_frame`, `create_bottom_filter_retainer`, `create_mini_pc_airflow_duct` | **LIKELY** (unchanged from mk0.7) |
| `frame.py` still contains redundant `create_frame_top` / `create_frame_bottom` | Same as above | **LIKELY** (unchanged) |
| `feet.py` still contains `create_foot()` unused alias | `create_foot()` calls `make_foot()` | **LIKELY** (unchanged) |
| `make_mini_pc_airflow_duct_placeholder()` still lacks `.tag()` | `cad/parts/cooling.py:146` returns raw geometry | **CONFIRMED** — not fixed |
| `create_power_bus_panel()` still lacks `.tag()` | `cad/parts/service_spine.py:41` returns raw geometry | **CONFIRMED** — not fixed |

---

## Export Organization

### Overall assessment
The `EXPORT_CATEGORIES` structure is cleaner than mk0.7 due to the addition of `power_bus_zone_placeholder` and the TPU foot category. However, duplicate aliases in `PARTS` and missing entries remain.

### Findings — mk0.7.1 fixes (verified)

| ID | Finding | Evidence | Grade |
|---|---|---|---|
| EF-01 | `foot` is now in `printable/tpu` | `cad/exporters/part_registry.py:107` | **CONFIRMED FIXED** |
| EF-02 | `power_bus_zone_placeholder` is now in `PARTS` and `EXPORT_CATEGORIES` | `PARTS:59`, `EXPORT_CATEGORIES:120` | **CONFIRMED FIXED** |

### Findings — remaining mk0.7 issues

| ID | Finding | Evidence | Grade |
|---|---|---|---|
| ER-01 | `base_stability_plate` is in `PARTS` but missing from `EXPORT_CATEGORIES` | `part_registry.py:16` vs `EXPORT_CATEGORIES` | **CONFIRMED** — unchanged |
| ER-02 | `bottom_fan_panel` / `top_fan_panel` duplicate grilles in `PARTS` | `part_registry.py:46-47` | **CONFIRMED** — unchanged |
| ER-03 | `frame_top` / `frame_bottom` duplicate frames in `PARTS` | `part_registry.py:11-12` | **CONFIRMED** — unchanged |
| ER-04 | `mini_pc_airflow_duct` / `mini_pc_airflow_duct_placeholder` duplicate in `PARTS` | `part_registry.py:60-61` | **CONFIRMED** — unchanged |
| ER-05 | `ssd_placeholder` name does not match factory `make_external_ssd_placeholder` | `part_registry.py:56` | **LIKELY** — unchanged |
| ER-06 | `fan_120x120x25_placeholder` name does not match factory `make_fan_120_placeholder` | `part_registry.py:51` | **LIKELY** — unchanged |

### Notes
The duplicate aliases in `PARTS` do not pollute exports because they are excluded from `EXPORT_CATEGORIES`, but they clutter the namespace and invite future misuse. The `base_stability_plate` remains silently skipped during export.

---

## STL Quality Issues

### Overall assessment
**The confirmed mk0.7 nonmanifold defect is fixed.** All printable plastic and TPU parts now produce watertight, manifold meshes.

### Findings from `revisions/mk0.7.1/analysis/stl_quality.csv`

| Part | Category | Watertight | Manifold | Nonmanifold Edges | Grade |
|---|---|---|---|---|---|
| `bottom_fan_cartridge` | `printable/plastic` | **True** | **True** | 0 | **CONFIRMED FIXED** — was nonmanifold in mk0.7 |
| `airflow_path_review` | `review` | False | False | 4 | Expected (open review geometry) |
| `mini_pc_airflow_path_review` | `review` | False | False | 1 | Expected |
| `stability_review` | `review` | False | False | 2 | Expected |
| All other `printable/plastic` and `printable/tpu` parts | — | True | True | 0 | OK |

### Root cause verification (mk0.7.1 fix)
In `cooling.py:82-95`, the service handle is now translated to `(-rail_y, rail_z)` where `rail_y = DEPTH/2 + RAIL_WIDTH/2 - FEATURE_OVERLAP`. With `DEPTH = 142.0`, `RAIL_WIDTH = 8.0`, `FEATURE_OVERLAP = 1.2`:
- `rail_y = 71.0 + 4.0 - 1.2 = 73.8`
- Handle center is at `y = -73.8`. Handle extends from `y = -77.8` to `y = -69.8`.
- Cartridge body extends from `y = -71.0` to `y = +71.0`.
- **Overlap is `1.2 mm`** (exactly `FEATURE_OVERLAP`), confirming the handle is now fused to the body. The STL exporter produces a manifold mesh.

---

## Duplicate Geometry Check

### Overall assessment
**CONFIRMED FIXED.** The `duplicate_geometry_check.csv` now contains valid data for all 50 parts. The script correctly uses `DUPLICATE_VOLUME_TOLERANCE_MM3`.

### Findings from `revisions/mk0.7.1/analysis/duplicate_geometry_check.csv`

| Status | Count | Notes |
|---|---|---|
| Parts with no duplicate | 44 | Normal |
| Exact duplicate groups | 6 | Expected: mirrored / symmetric parts |

### Duplicate groups (expected engineering duplicates)

| Group | Parts | Reason |
|---|---|---|
| `exact_001` | `bottom_structural_frame`, `top_structural_frame` | Same geometry function |
| `exact_002` | `front_stability_wing`, `rear_stability_wing` | Symmetric wings |
| `exact_003` | `left_foot_extension`, `right_foot_extension` | Mirrored extensions |
| `exact_004` | `left_side_panel_lower`, `right_side_panel_lower` | Mirrored panels |
| `exact_005` | `left_side_panel_middle`, `right_side_panel_middle` | Mirrored panels |
| `exact_006` | `left_side_panel_upper`, `right_side_panel_upper` | Mirrored panels |

### Fix verification
`scripts/analysis/detect_duplicate_geometry.py:56` now reads:
```python
volume_key = round(stats.volume_mm3 / cfg.DUPLICATE_VOLUME_TOLERANCE_MM3) * cfg.DUPLICATE_VOLUME_TOLERANCE_MM3
```
This matches the config key at `cad/config.py:640`. The mk0.7 tool failure (`AttributeError: module 'cad.config' has no attribute 'DUPLICATE_VOLUME_TOLERANCE_MM'`) is resolved.

---

## Config Consistency

### Overall assessment
The mk0.7.1 fixes improved parametric correctness but did not clean up the config file itself. The dead `SPINE_COVER_THICKNESS = 2.0` and many unused parameters remain.

### Critical finding

| Finding | Evidence | Grade |
|---|---|---|
| `SPINE_COVER_THICKNESS` defined as `2.0` then overwritten by `3.0` | Line 486: `SPINE_COVER_THICKNESS = 2.0`<br>Line 513: `SPINE_COVER_THICKNESS = REAR_SPINE_COVER_THICKNESS` (3.0) | **CONFIRMED** — the 2.0 mm value is dead code |
| `REAR_SPINE_COVER_THICKNESS` is defined once | Line 488: `REAR_SPINE_COVER_THICKNESS = 3.0` | **CONFIRMED** — but line 486 creates confusion |

### Notes
The exported `rear_service_spine_cover` has a bounding-box thickness of **3.0 mm** (per `duplicate_geometry_check.csv`: size_z = 3.000), confirming the 3.0 mm value is active. The `SPINE_COVER_THICKNESS = 2.0` at line 486 should be deleted or renamed to a legacy alias with a comment. The mk0.7 review said `REAR_SPINE_COVER_THICKNESS` was double-defined; in mk0.7.1 the names were split but the dead value remains.

---

## Assembly Realism

### Overall assessment
The five scoped placement fixes are verified. The assembly is more physically consistent than mk0.7. However, deferred mk0.7 placement issues remain.

### Confirmed mk0.7.1 fixes (verified)

| ID | Part | Fix | Evidence | Grade |
|---|---|---|---|---|
| AF-01 | Corner blocks | Now placed at frame corners (`FRAME_THICKNESS/2` and `TOWER_HEIGHT - FRAME_THICKNESS/2`) | `tower_assembly.py:16-18` | **CONFIRMED FIXED** |
| AF-02 | Top fan placeholder | Added to assembly | `tower_assembly.py:237-241` | **CONFIRMED FIXED** |
| AF-03 | Bottom fan grille | No longer overlaps bottom frame; sits flush below it | `BOTTOM_FAN_PANEL_Z = -8.5`; frame spans `[-3.5, 3.5]`; grille spans `[-10.5, -6.5]` | **CONFIRMED FIXED** |
| AF-04 | Top fan grille | No longer overlaps top frame; sits flush above it | `TOP_FAN_PANEL_Z_OFFSET = 5.5`; frame spans `[318.0, 325.0]`; grille spans `[325.0, 329.0]` | **CONFIRMED FIXED** |
| AF-05 | Power bus cover | Holes now aligned with panel holes at `±POWER_BUS_PAD_SCREW_OFFSET_X` | `service_spine.py:17-18` and `service_spine.py:59-60` | **CONFIRMED FIXED** |
| AF-06 | Bottom fan cartridge handle | Now fused to body with `FEATURE_OVERLAP` overlap | `cooling.py:82-95` | **CONFIRMED FIXED** |

### Remaining mk0.7 placement issues (not in scope)

| ID | Part | Issue | Evidence | Grade |
|---|---|---|---|---|
| AR-01 | Bottom fan cartridge rails | Rails and handle still overlap base plate by ~3.8 mm without slots | Rails top at `z = -10.2`; base spans `[-14.0, -4.0]` | **CONFIRMED** — deferred |
| AR-02 | Sectional base feet | Feet are placed but sectional base has no screw holes or sockets | `tower_assembly.py:50-57` vs `feet.py` sectional parts | **CONFIRMED** — deferred |
| AR-03 | UPS power tray | Battery marker still extends beyond tray width (186.5 mm vs 170 mm module) | `part_dimensions.csv` (implied by `duplicate_geometry_check.csv`: 186.500 mm) | **CONFIRMED** — deferred |
| AR-04 | Bottom filter frame / retainer | Still not placed in assembly | In `EXPORT_CATEGORIES` but not in `tower_assembly.py` | **LIKELY** — deferred |
| AR-05 | Base stability plate | Still in `PARTS` but not used in assembly | `part_registry.py:16` vs `tower_assembly.py` using sectional base | **LIKELY** — deferred |
| AR-06 | Rods placement | Rod starts at `z = 0` (center of bottom frame), not below it | `tower_assembly.py:36` | **LIKELY** (visualization only) — unchanged |

---

## Naming Consistency

### Findings

| Finding | Evidence | Grade |
|---|---|---|
| `ssd_placeholder` in registry, but factory is `make_external_ssd_placeholder` | `part_registry.py:56` | **LIKELY** — unchanged |
| `fan_120x120x25_placeholder` in registry, but factory is `make_fan_120_placeholder` | `part_registry.py:51` | **LIKELY** — unchanged |
| `mini_pc_airflow_duct` in registry, but factory is `make_mini_pc_airflow_duct_placeholder` | `part_registry.py:60` | **LIKELY** — unchanged |
| `mini_pc_airflow_duct_placeholder` also in registry, same factory | `part_registry.py:61` | **CONFIRMED** (redundant key) — unchanged |
| `bottom_fan_panel` / `top_fan_panel` duplicate `bottom_fan_grille` / `top_fan_grille` | `part_registry.py:46-47` | **CONFIRMED** — unchanged |
| `frame_top` / `frame_bottom` duplicate `top_structural_frame` / `bottom_structural_frame` | `part_registry.py:11-12, 13-14` | **CONFIRMED** — unchanged |
| `make_foot` → `make_wide_tpu_foot_placeholder` → `create_foot` alias chain | `feet.py` | **LIKELY** — unchanged |

---

## Blockers

mk0.7.1 **does not introduce any new blockers**. All the confirmed mk0.7 printable-part defects that were in scope are fixed. The following **deferred mk0.7 issues remain pre-blocking for any manufacturing export** and should be resolved before mk0.8:

1. **UPS tray exceeds module width (186.5 mm vs 170 mm slot)** — The battery marker geometry still protrudes beyond the module standard. The tray cannot be inserted.
2. **Cartridge rails overlap base plate without slots (~3.8 mm)** — The bottom fan cartridge rails and handle extend into the sectional base volume. No corresponding cutouts exist.
3. **Sectional base lacks foot attachment** — Feet are placed in the assembly but the sectional base pieces have no screw holes or sockets.
4. **Dead `SPINE_COVER_THICKNESS = 2.0`** — Dead code that will confuse future editors.

---

## Recommendations

### Immediate (before next export)
1. **Delete dead `SPINE_COVER_THICKNESS = 2.0`** at `config.py:486`. If 2.0 mm is a future design intent, document it as a commented-out alternative.
2. **Prune `PARTS` duplicate aliases**: Remove `bottom_fan_panel`, `top_fan_panel`, `frame_top`, `frame_bottom`, `mini_pc_airflow_duct`, `mini_pc_airflow_duct_placeholder` from `PARTS`.
3. **Add `.tag()` to `make_mini_pc_airflow_duct_placeholder()`** and `create_power_bus_panel()` for consistency.
4. **Remove or export `base_stability_plate`**: Either add it to `EXPORT_CATEGORIES` or remove it from `PARTS` if the sectional base is the intended design.

### Short-term (before mk0.8)
5. **Fix UPS tray width**: Reduce the battery marker width or shift it so the tray stays within `MODULE_WIDTH = 170.0` mm.
6. **Add base plate slots for cartridge rails**: Cut matching slots in `make_central_bottom_fan_frame` for the cartridge rails and handle, or redesign the cartridge to sit clear of the base.
7. **Add foot sockets to sectional base**: Replicate the `screw_cut` and `socket_cut` logic from `make_base_stability_plate` into the sectional base pieces.
8. **Name unexplained config literals**: Replace `+24.0`, `-34.0`, `*6.5`, `*2.2`, `*0.52`, `+22.0` with named parameters and comments.
9. **Audit unused parameters**: Delete or mark as "future use" the ~20 unused parameters in `config.py`.
10. **Add `bottom_filter_frame` and `bottom_filter_retainer` to the assembly** or remove them from export if they are not yet designed for the sectional base.
11. **Synchronize placeholder names**: Update registry names (`ssd_placeholder`, `fan_120x120x25_placeholder`, `mini_pc_airflow_duct`) to match their factory function names, or rename the factories.

### Process
12. **Re-run review package after mk0.8 changes**: Re-export STL, re-run STL quality, duplicate geometry, and part dimension checks. The mk0.7.1 package is now functional and should be used as a baseline.
13. **Require `.tag()` enforcement**: Add a lint check that every part function returning `cq.Workplane` must end with `.tag()`.
14. **Require registry audit**: Before any export, run a script that verifies `PARTS` keys are unique and `EXPORT_CATEGORIES` is a strict subset of `PARTS`.

---

## Appendix: Evidence Summary Table

| File | Lines | Key Issue | Status |
|---|---|---|---|
| `cad/parts/cooling.py` | 82–95 | Cartridge handle fused with `FEATURE_OVERLAP` | **Fixed in mk0.7.1** |
| `cad/parts/cooling.py` | 61–80 | Cartridge rails still overlap base plate | **Deferred** |
| `cad/parts/cooling.py` | 146 | `make_mini_pc_airflow_duct_placeholder()` lacks `.tag()` | **Deferred** |
| `cad/parts/service_spine.py` | 17–18 | Panel holes at `±POWER_BUS_PAD_SCREW_OFFSET_X` | **Fixed in mk0.7.1** |
| `cad/parts/service_spine.py` | 59–60 | Cover holes at `±POWER_BUS_PAD_SCREW_OFFSET_X` | **Fixed in mk0.7.1** |
| `cad/parts/service_spine.py` | 41 | `create_power_bus_panel()` lacks `.tag()` | **Deferred** |
| `cad/parts/review.py` | 14 | `cfg.AIRFLOW_ARROW_HEAD_HEIGHT_RATIO` used | **Fixed in mk0.7.1** |
| `cad/parts/review.py` | 45 | `cfg.AIRFLOW_ARROW_SIDE_ROTATION_DEG` used | **Fixed in mk0.7.1** |
| `cad/config.py` | 17 | `TOWER_HEIGHT = TOTAL_UNITS * UNIT_HEIGHT + 24.0` | **Deferred** |
| `cad/config.py` | 486, 488, 513 | `SPINE_COVER_THICKNESS` / `REAR_SPINE_COVER_THICKNESS` confusion | **Partially fixed; dead code remains** |
| `cad/config.py` | 616 | `BOTTOM_FAN_PANEL_Z` parametric | **Fixed in mk0.7.1** |
| `cad/config.py` | 619 | `TOP_FAN_PANEL_Z_OFFSET` parametric | **Fixed in mk0.7.1** |
| `cad/config.py` | 538 | `POWER_BUS_PAD_SCREW_OFFSET_X` drives both holes | **Fixed in mk0.7.1** |
| `cad/assembly/tower_assembly.py` | 16–18 | Corner blocks at `FRAME_THICKNESS/2` and `TOWER_HEIGHT - FRAME_THICKNESS/2` | **Fixed in mk0.7.1** |
| `cad/assembly/tower_assembly.py` | 237–241 | Top fan placeholder added | **Fixed in mk0.7.1** |
| `cad/assembly/tower_assembly.py` | 242–247 | Fan grilles placed flush with frames | **Fixed in mk0.7.1** |
| `cad/exporters/part_registry.py` | 107 | `foot` in `printable/tpu` | **Fixed in mk0.7.1** |
| `cad/exporters/part_registry.py` | 59, 120 | `power_bus_zone_placeholder` in registry and export | **Fixed in mk0.7.1** |
| `cad/exporters/part_registry.py` | 46–47 | `bottom_fan_panel` / `top_fan_panel` duplicate aliases | **Deferred** |
| `cad/exporters/part_registry.py` | 11–12 | `frame_top` / `frame_bottom` duplicate aliases | **Deferred** |
| `scripts/analysis/detect_duplicate_geometry.py` | 56 | Uses `DUPLICATE_VOLUME_TOLERANCE_MM3` | **Fixed in mk0.7.1** |
| `revisions/mk0.7.1/analysis/stl_quality.csv` | Line 12 | `bottom_fan_cartridge`: watertight, manifold | **Fixed in mk0.7.1** |
| `revisions/mk0.7.1/analysis/stl_quality.csv` | All printable/plastic | All watertight and manifold | **Verified** |
| `revisions/mk0.7.1/analysis/duplicate_geometry_check.csv` | All rows | No tool errors; 6 expected duplicate groups | **Verified** |

---

*End of review.*
