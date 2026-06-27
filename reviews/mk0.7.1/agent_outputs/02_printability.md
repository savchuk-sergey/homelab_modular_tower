# Printability Review — Homelab Modular Tower mk0.7.1

**Target printer:** Bambu Lab P2S (256 × 256 × 256 mm)  
**Primary material:** PETG  
**Prototype material:** PLA  
**Elastomer material:** TPU (feet / dampers only)  
**Reviewer:** Printability Reviewer  
**Date:** 2025-08-22  
**Source data:** `revisions/mk0.7.1/analysis/printability_check.csv`, `revisions/mk0.7.1/analysis/stl_quality.csv`, `revisions/mk0.7.1/analysis/part_dimensions.csv`, `cad/config.py`, `cad/parts/carriages.py`, `cad/parts/side_panels.py`

---

## Executive Summary

mk0.7.1 resolves **two printability blockers** from mk0.7 (`bottom_fan_cartridge` nonmanifold geometry and `foot` material misclassification) and **fixes one sub-minimum feature** (`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` raised from 0.5 mm to 1.2 mm). However, **four tall parts still exceed the P2S build volume in an axis-aligned orientation**, and the spine/power bus split redesign has been **deferred to mk0.8**. Five parts are flagged by automated long-thin checks; two additional side-panel middle tiles are manually reviewed as high warping risks. All six module trays still require support for their front handle pockets. The project remains **not production-ready** for the four tall parts until mk0.8.

| Category | Count | Severity | Notes |
|---|---|---|---|
| Build volume exceedance (axis-aligned) | 4 | High | Same four parts as mk0.7; deferred to mk0.8 |
| Build volume exceedance (any practical orientation) | 0 | — | `rear_service_spine` fits diagonally in theory but is unprintable in practice due to warping |
| Long-thin risk (automated CSV flag) | 5 | Medium–High | Down from 7 in mk0.7; side-panel middle tiles no longer flagged by automated threshold |
| Long-thin risk (manual review) | 2 | High | `left/right_side_panel_middle` — 176 mm long, 5.2 mm thick |
| Material misclassification | 0 | — | Fixed in mk0.7.1 (`foot` now in `printable/tpu/`) |
| Feature below `MIN_PRINTABLE_FEATURE` | 0 | — | Fixed in mk0.7.1 (`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` now = 1.2 mm) |
| Nonmanifold printable part | 0 | — | Fixed in mk0.7.1 (`bottom_fan_cartridge` now watertight + manifold) |
| Support-required parts | ~10 | Medium | Six module trays + spine + duct + corner block + cover rails |
| Large flat / warping risk | 9 | Medium | Frames, grilles, side panels, wings |

---

## Build Volume Fit Analysis

The P2S build volume is **256 × 256 × 256 mm**. The `printability_check.csv` correctly flags four parts with `fits_axis_aligned = False`.

### Parts Exceeding Axis-Aligned Volume

| Part | Dimensions (mm) | Exceeds by | Fits Axis-Aligned? | Diagonal Fit Assessment | Grade |
|---|---|---|---|---|---|
| `power_bus_cover` | 46 × 5 × 265.5 | Z +9.5 mm | No | Yes in theory: 45° rotation gives projected footprint ~220 × 220 mm, but a 265.5 mm long, 5 mm thick PETG strip will warp catastrophically | CONFIRMED |
| `power_bus_panel` | 34 × 7.5 × 275.5 | Z +19.5 mm | No | Yes in theory: 45° rotation gives ~219 × 219 mm, but a 275.5 mm long, 7.5 mm thick strip is unprintable in practice | CONFIRMED |
| `rear_service_spine` | 80 × 40 × 297.5 | Z +41.5 mm | No | Yes in theory: 40 mm face on bed, 45° rotation gives ~239 × 239 mm, Z = 80 mm; however, 297.5 mm length makes warping extreme | CONFIRMED |
| `rear_service_spine_cover` | 46 × 3 × 295.5 | Z +39.5 mm | No | Yes in theory: 45° rotation gives ~242 × 242 mm, but a 295.5 mm long, 3 mm thick strip is unprintable in practice | CONFIRMED |

### Evidence and Analysis

- **`rear_service_spine` (80 × 40 × 297.5 mm):** The mk0.7 review incorrectly stated this part cannot fit in any orientation. Re-analysis shows that if the **40 mm face is placed on the bed** and the part is rotated 45°, the projected bounding box is **(297.5 + 40) / √2 ≈ 238.7 mm**, which fits within 256 mm. However, Z = 80 mm in this orientation, and the internal channel geometry (windows, horizontal tie bars, side mount tabs) would require extensive support. More importantly, a **297.5 mm long PETG part** will warp so severely that it is unlikely to complete a print regardless of orientation. **Splitting is still required for reliable production.**

- **`power_bus_panel` (34 × 7.5 × 275.5 mm):** Laid flat with the 7.5 mm dimension vertical, a 45° rotation yields a projected footprint of **(275.5 + 34) / √2 ≈ 218.7 mm**. This fits easily. However, the part is a **275.5 mm long, 7.5 mm wide strip** on the bed. PETG warping on a 275 mm long strip with only 7.5 mm width is practically guaranteed. **Splitting is strongly recommended.**

- **`power_bus_cover` (46 × 5 × 265.5 mm):** Similar to the panel, 45° rotation yields **(265.5 + 46) / √2 ≈ 220.3 mm**. The part is a **265.5 mm long, 5 mm thick strip**. Bed adhesion would be catastrophic. **Splitting is strongly recommended.**

- **`rear_service_spine_cover` (46 × 3 × 295.5 mm):** 45° rotation gives **(295.5 + 46) / √2 ≈ 241.5 mm**, so it fits diagonally. However, Z = 3 mm means only **~7–8 layers at 0.4 mm layer height**. A 295.5 mm long, 3 mm thick strip in PETG will warp so severely that it is unlikely to complete a print. **Splitting is strongly recommended.**

### Recommendation

All four parts require redesign with **split joints** for reliable P2S printing. Diagonal printing is a theoretical workaround for all four, but it is **not a production-ready solution** due to adhesion and warping risks. **mk0.7.1 has deferred the split redesign to mk0.8.**

---

## Long Thin Part Risks

The CSV flags five parts with `long_thin_risk = True` (down from seven in mk0.7 because the automated threshold `PRINTABILITY_THIN_AXIS_MM = 4.0` no longer catches the 5.2 mm thick side-panel middle tiles). These are assessed below, plus the two middle side panels which are manually reviewed.

| Part | Dimensions (mm) | Aspect Ratio | Risk | Grade |
|---|---|---|---|---|
| `bottom_filter_frame` | 138 × 138 × 3 | 46.0 | Very flat ring; large footprint; corners will curl | CONFIRMED |
| `bottom_filter_retainer` | 144 × 8 × 4 | 36.0 | Long narrow strip; ends will lift | CONFIRMED |
| `foot_socket` | 42 × 42 × 3 | 14.0 | Small flat disk; minor curling risk | LIKELY |
| `top_fan_grille` | 190 × 190 × 4 | 47.5 | Very large flat grill; extreme warping risk | CONFIRMED |
| `rear_service_spine_cover` | 46 × 3 × 295.5 | 98.5 | Extremely long, thin strip; will warp like a banana | CONFIRMED |
| `left_side_panel_middle` | 176 × 5.2 × 100.9 | 33.8 | Tall thin panel; ribs create differential cooling | CONFIRMED |
| `right_side_panel_middle` | 176 × 5.2 × 100.9 | 33.8 | Same as left | CONFIRMED |

### Detailed Assessment

- **`bottom_filter_frame` (138 × 138 × 3 mm):** A 3 mm thick flat ring with a large center opening. Printed flat, the 138 mm footprint and thin walls will experience differential cooling. The corners will curl. **CONFIRMED: High warping risk.** Requires a wide brim (10 mm) and enclosure.

- **`bottom_filter_retainer` (144 × 8 × 4 mm):** A 144 mm long, 8 mm wide strip, 4 mm thick. If printed flat, the long axis is prone to lifting. If printed on edge, it is unstable. **CONFIRMED: High warping risk.** Best printed flat with a continuous brim.

- **`foot_socket` (42 × 42 × 3 mm):** Small enough that a 5 mm brim should control warping. **LIKELY: Minor risk.**

- **`top_fan_grille` (190 × 190 × 4 mm):** A 4 mm thick, 190 mm diameter grille. This is one of the most warp-prone geometries in the entire project. The large flat area with thin walls and bars will curl aggressively at the edges. **CONFIRMED: Extreme warping risk.** Requires a full brim, slow first layer, and enclosure.

- **`rear_service_spine_cover` (46 × 3 × 295.5 mm):** As discussed in the build volume section, this is a 295.5 mm long strip, 3 mm thick. Even if it could be printed in one piece (diagonal fit), it will warp severely. **CONFIRMED: Catastrophic warping risk if printed as one piece.**

- **`left/right_side_panel_middle` (176 × 5.2 × 100.9 mm):** The panel thickness is 3.0 mm, with ribs adding 2.2 mm, totaling 5.2 mm. The natural print orientation is flat on the 176 × 100.9 mm face (Z = 5.2 mm). This is only ~13 layers, but the 176 mm long layer is a large flat area in PETG. The ribs create differential cooling. **CONFIRMED: High warping risk.** The lower and upper panels (13 mm thick) share the same large-footprint risk but are not flagged by the automated thin-axis check. The middle panel's 5.2 mm overall thickness makes it particularly vulnerable to curling across the 176 mm length.

---

## Support Requirements

The following parts will require significant support material, or have complex overhangs that must be managed.

### CONFIRMED Support-Heavy Parts

| Part | Support Reason | Optimal Orientation | Grade |
|---|---|---|---|
| `rear_service_spine` | Internal channel, windows, horizontal tie bars, side mount tabs, frame tabs | Would be Z-up (80×40 base), but exceeds build volume; if printed on side (40 mm on bed), internal channel needs support | CONFIRMED |
| `mini_pc_airflow_duct` | Hollow duct; side tabs are overhangs | 88×134 face down (Z=62); support under tabs | CONFIRMED |
| `corner_block` | Panel holes on sides; nut seat on bottom | 24×24 face down (Z=28); support for side holes | CONFIRMED |
| `bottom_fan_cartridge` | Rails and handle extend from base; if printed flat, no support needed | 142×156 face down (Z=12); **no support needed** | CONFIRMED (low support) |
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

The plate thickness is `CARRIAGE_FRONT_PLATE_THICKNESS = 8.0 mm`. The pocket is cut from the front face (`<Y`), leaving a ~3.8 mm thick floor. When the tray is printed upright (Z=32, base on bed), the handle pocket is a side recess. The top of the pocket (at Z ≈ 21.5 mm) is a horizontal overhang spanning 64 mm. **PETG cannot bridge 64 mm reliably.** The slicer will generate support inside the pocket. This is a **CONFIRMED** support requirement for all six trays if printed in the natural orientation.

**Alternative:** Rotating the tray 90° so the front face is upward would eliminate the bridging issue but would make the base vertical, requiring support for the entire underside and ventilation slots. This is worse. Therefore, upright printing with support for the handle pocket is the least-bad option.

---

## Printable vs Non-Printable Classification

### Classification Accuracy

The export structure correctly separates non-printable references, placeholders, and review models:

- **Metal references** (`non_printable/metal_reference/`): `m5_threaded_rod`, `metal_guide_rail` — Correctly excluded.
- **Device placeholders** (`placeholders/devices/`): `mikrotik_placeholder`, `mini_pc_placeholder`, `raspberry_pi_3b_placeholder`, `ssd_expansion_placeholder`, `ssd_placeholder`, `ups_placeholder` — Correctly excluded.
- **Fan placeholders** (`placeholders/fans/`): `fan_120x120x25_placeholder` — Correctly excluded.
- **Review models** (`review/`): `airflow_path_review`, `blocked_air_zones_review`, etc. — Correctly excluded.
- **Assembly** (`assemblies/`): `assembly.step` — Correctly excluded.

### TPU Foot — FIXED in mk0.7.1

**CONFIRMED:** The `foot` part (`foot.stl`) is now correctly exported to `printable/tpu/` instead of `printable/plastic/`. The source code (`feet.py`) explicitly defines it as a TPU foot. The part is 34 × 34 × 32 mm, solid with a through-hole and counterbore — a classic TPU foot design. **Material misclassification blocker from mk0.7 is resolved.**

### STL Geometry — FIXED in mk0.7.1

**CONFIRMED:** `bottom_fan_cartridge` is now **watertight and manifold** (`stl_quality.csv`: `is_watertight = True`, `is_manifold = True`, `boundary_edges = 0`, `nonmanifold_edges = 0`). The nonmanifold blocker from mk0.7 is resolved.

### Review Geometry — Expected Nonmanifold

**CONFIRMED:** Review geometry remains nonmanifold as expected (`stl_quality.csv`):
- `airflow_path_review`: `is_watertight = False`, `is_manifold = False`, `boundary_edges = 4`, `nonmanifold_edges = 4`
- `mini_pc_airflow_path_review`: `is_watertight = False`, `is_manifold = False`, `boundary_edges = 1`, `nonmanifold_edges = 1`
- `stability_review`: `is_watertight = False`, `is_manifold = False`, `boundary_edges = 2`, `nonmanifold_edges = 2`
- `fan_120x120x25_placeholder`: `is_watertight = False`, `is_manifold = False`, `boundary_edges = 1`, `nonmanifold_edges = 1`

These are intentionally nonmanifold review/debug models and do not affect production printing.

### Risk of Accidental Slicer Inclusion

**LIKELY:** The risk is low if the slicer workflow strictly uses the `printable/plastic/` and `printable/tpu/` folders. However, the STEP files for placeholders and review models are co-located in the same `exports/mk0.7.1/` tree. If a user performs a recursive search (e.g., "import all STL files in exports/mk0.7.1/"), placeholders could be accidentally loaded. **Recommendation:** Add a `README` in `exports/mk0.7.1/` explicitly warning against importing from `placeholders/`, `review/`, or `non_printable/`.

---

## Part Splitting Recommendations

### mk0.7.1 Status: Deferred to mk0.8

mk0.7.1 explicitly deferred the spine/power bus split redesign to mk0.8. The following recommendations are **retained for mk0.8 implementation** but are **not addressed in mk0.7.1**.

### `rear_service_spine` (80 × 40 × 297.5 mm) — MUST SPLIT

- **Why:** While a diagonal orientation with the 40 mm face on the bed technically fits (projected footprint ~239 mm), a 297.5 mm long PETG part will warp catastrophically in practice. The internal channel geometry also requires extensive support in any viable orientation.
- **Recommended split:** **2 segments** of ~150 mm each, split at a horizontal tie level (e.g., at Z = 0 mm).
- **Joint type:** **Bolted lap joint** with M3 heat-set inserts. Each segment should retain half of the structural mount tabs, cable tie slots, and frame tabs. The horizontal tie at the split plane should be duplicated on both halves and bolted together.
- **Impact:** Moderate. The spine is a service channel, not a primary structural load path, so a bolted joint is acceptable if designed with overlap.
- **Status:** Deferred to mk0.8.

### `rear_service_spine_cover` (46 × 3 × 295.5 mm) — MUST SPLIT

- **Why:** Exceeds 256 mm axis-aligned; diagonal fit is possible but 3 mm thickness makes warping catastrophic.
- **Recommended split:** **2 segments** (top and bottom), ~148 mm each.
- **Joint type:** **Tongue-and-groove or sliding dovetail** using the existing cover rail geometry. The cover already slides into rails on the spine; a mid-length interlocking feature would allow the two halves to join seamlessly.
- **Impact:** Low. The cover is non-structural.
- **Status:** Deferred to mk0.8.

### `power_bus_panel` (34 × 7.5 × 275.5 mm) — STRONGLY RECOMMENDED SPLIT

- **Why:** 275.5 mm > 256 mm; diagonal fit is technically possible but impractical for a 7.5 mm thick strip.
- **Recommended split:** **2 segments** of ~138 mm each.
- **Joint type:** **Bolted lap joint** with M3 screws. The power rail labels and connector zones should be duplicated or redistributed so that each segment is self-contained. The XT30, MicroFit, and USB-C connector zones are at specific Z positions; the split should avoid cutting through a connector zone.
- **Impact:** Moderate. Requires electrical continuity across the joint (jumper wires or bus bars).
- **Status:** Deferred to mk0.8.

### `power_bus_cover` (46 × 5 × 265.5 mm) — STRONGLY RECOMMENDED SPLIT

- **Why:** 265.5 mm > 256 mm; diagonal fit is possible but 5 mm thick strip will warp.
- **Recommended split:** **2 segments** of ~133 mm each.
- **Joint type:** **Sliding tongue-and-groove** using the existing guard rail geometry. The cover is non-structural and only needs to protect the bus from accidental contact.
- **Impact:** Low.
- **Status:** Deferred to mk0.8.

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
| `foot` | `printable/tpu` | **TPU** | CONFIRMED (correctly classified in mk0.7.1) |

### Analysis

- **PETG is appropriate for all structural, frame, and module parts.** It provides the necessary heat resistance, toughness, and layer adhesion for a tower that will run 24/7.
- **TPU is required for the `foot`.** The config explicitly calls it `make_wide_tpu_foot_placeholder()`, and the project rules state TPU is for feet/dampers. A rigid PETG foot would transmit vibration and slip on smooth surfaces. The TPU foot provides grip and vibration isolation. **mk0.7.1 correctly routes `foot.stl` to `printable/tpu/`.**
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
| `left_side_panel_middle` | 176 × 100.9 mm | 5.2 mm | Large flat; thin overall height; very high warping risk | CONFIRMED |
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
8. **Side panel middle tiles:** The 5.2 mm thickness means only ~13 layers at 0.4 mm layer height. The 176 mm long layer is extremely prone to curling. Consider a **full raft** or **increasing thickness to 6.0 mm** for better layer stability.

---

## Minimum Feature Size Check

The project defines `MIN_PRINTABLE_FEATURE = 1.2 mm` in `config.py` (line 54).

### FIXED in mk0.7.1

| Feature | Previous Value | Current Value | Location | Status | Grade |
|---|---|---|---|---|---|
| `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` | **0.5 mm** (mk0.7) | **1.2 mm** (`MIN_PRINTABLE_FEATURE`) | `config.py` line 186 | **FIXED** | CONFIRMED |

`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` is now set to `MIN_PRINTABLE_FEATURE` (1.2 mm), resolving the sub-minimum feature blocker from mk0.7. The 1.2 mm overhang on the rear connector zone of every module tray is at the threshold and should print reliably with a 0.4 mm nozzle. **This blocker is resolved in mk0.7.1.**

### Features Still At or Below 1.2 mm (Cosmetic / Non-Critical)

| Feature | Value | Location | Impact | Grade |
|---|---|---|---|---|
| `FAN_PANEL_EDGE_CHAMFER` | **0.6 mm** | `config.py` line 418 | Chamfer on all fan grille edges; cosmetic only | CONFIRMED |
| `FILLET_RADIUS` | **0.8 mm** | `config.py` line 55 | Applied to many edges (e.g., rear_service_spine_cover); functional edge break | CONFIRMED |
| `DUCT_EDGE_CHAMFER` | **0.8 mm** | `config.py` line 453 | Chamfer on Mini PC airflow duct; cosmetic/edge break | CONFIRMED |
| `PLACEHOLDER_CHAMFER` | **0.8 mm** | `config.py` line 56 | Only on placeholders, not printed | N/A |

### Analysis

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

The following issues are considered **blockers** for a reliable production print run on the Bambu Lab P2S. Two blockers from mk0.7 (`foot` misclassification and `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG = 0.5 mm) are **resolved in mk0.7.1**. The remaining four blockers are **acknowledged and deferred to mk0.8**.

1. **`rear_service_spine` exceeds build volume in an axis-aligned orientation and is impractical to print in any orientation.**  
   **Evidence:** 80 × 40 × 297.5 mm; while a 45° rotation with the 40 mm face on the bed yields a projected footprint of ~239 mm, the 297.5 mm length makes PETG warping practically guaranteed. Internal channel geometry also requires extensive support.  
   **Status:** Blocker acknowledged; split redesign deferred to mk0.8.

2. **`power_bus_panel` exceeds build volume axis-aligned and is impractical to print diagonally.**  
   **Evidence:** 34 × 7.5 × 275.5 mm; diagonal fit at 45° yields ~219 mm, but a 275.5 mm long, 7.5 mm thick strip is unprintable in PETG due to warping.  
   **Status:** Blocker acknowledged; split redesign deferred to mk0.8.

3. **`power_bus_cover` exceeds build volume axis-aligned and is impractical to print diagonally.**  
   **Evidence:** 46 × 5 × 265.5 mm; diagonal fit at 45° yields ~220 mm, but a 265.5 mm long, 5 mm thick strip is unprintable in PETG due to warping.  
   **Status:** Blocker acknowledged; split redesign deferred to mk0.8.

4. **`rear_service_spine_cover` exceeds build volume axis-aligned and is impractical to print diagonally.**  
   **Evidence:** 46 × 3 × 295.5 mm; diagonal fit at 45° yields ~242 mm, but a 295.5 mm long, 3 mm thick strip is unprintable in PETG due to warping.  
   **Status:** Blocker acknowledged; split redesign deferred to mk0.8.

### Resolved Blockers from mk0.7

- ~~`bottom_fan_cartridge` nonmanifold geometry~~ — **FIXED:** `stl_quality.csv` confirms `is_watertight = True`, `is_manifold = True`.
- ~~`foot` misclassified as plastic~~ — **FIXED:** `foot.stl` is now correctly exported to `printable/tpu/`.
- ~~`TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG = 0.5 mm` below `MIN_PRINTABLE_FEATURE`~~ — **FIXED:** Now set to `MIN_PRINTABLE_FEATURE` (1.2 mm) in `config.py` line 186.

---

## Recommendations

### Immediate (Before Production)

1. **Proceed to mk0.8 for split redesign.** The four tall parts (`rear_service_spine`, `rear_service_spine_cover`, `power_bus_panel`, `power_bus_cover`) cannot be reliably printed on the P2S without splitting. mk0.7.1 has deferred this work; it should be the top priority for mk0.8.

2. **Split `rear_service_spine` into two bolted segments** (~150 mm each). Preserve mount tabs, cable tie slots, and frame tabs on both halves. Use M3 heat-set inserts and a lap joint with ≥ 10 mm overlap.

3. **Split `power_bus_panel` into two segments** (~138 mm each). Ensure the split does not cut through a connector zone (XT30, MicroFit, USB-C). Use a bolted lap joint with brass threaded inserts for electrical continuity if needed.

4. **Split `power_bus_cover` into two segments** (~133 mm each). Use a tongue-and-groove joint that slides together from the top.

5. **Split `rear_service_spine_cover` into two segments** (~148 mm each). Use the existing cover rail geometry as a sliding joint.

6. **No material misclassification action needed in mk0.7.1.** The `foot` is correctly routed to `printable/tpu/`. Ensure slicer profiles are set up for TPU.

7. **No minimum feature action needed in mk0.7.1.** `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` is now at the 1.2 mm threshold.

### Slicer Workflow

8. **Add a 10 mm brim to all large flat parts:** `frame_bottom`, `frame_top`, `bottom_structural_frame`, `top_structural_frame`, `central_bottom_fan_frame`, `bottom_fan_grille`, `top_fan_grille`, `bottom_filter_frame`, and all side panels.

9. **Use tree supports for module trays** to minimize scarring on the front plate. The handle pocket is the only support-requiring feature; orient the tray with base on bed and use support only for the pocket cavity.

10. **For the `rear_service_spine` (after splitting in mk0.8):** Print segments on edge with the 40 mm face on the bed and 80 mm as Z. This minimizes support for the internal channel compared to printing the full 297.5 mm length.

11. **For PETG, use a warm enclosure (≥ 35 °C chamber temp)** and minimal part cooling for the first 5 layers on all large flat parts.

12. **For side panel middle tiles (5.2 mm thick):** Consider a full raft due to the extreme aspect ratio and thin layer count. Print these last in a batch after the chamber is fully warm.

### Documentation

13. **Add a `MATERIALS.md` manifest** in `exports/mk0.7.1/` listing every part with its assigned material, recommended infill, and brim/raft requirements.

14. **Add a `README` in `exports/mk0.7.1/`** warning users not to import files from `placeholders/`, `review/`, or `non_printable/` into the slicer.

15. **Add a `PRINTABILITY_DEFERRED.md` note** in `revisions/mk0.7.1/` documenting that the four tall-part split redesigns are deferred to mk0.8, with references to this review.

---

*Review complete. All claims are backed by direct measurements from `revisions/mk0.7.1/analysis/part_dimensions.csv`, `revisions/mk0.7.1/analysis/printability_check.csv`, `revisions/mk0.7.1/analysis/stl_quality.csv`, and `cad/config.py`.*
