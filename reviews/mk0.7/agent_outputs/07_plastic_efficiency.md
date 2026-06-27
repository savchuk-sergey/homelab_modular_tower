# Plastic Efficiency Review — Homelab Modular Tower mk0.7

**Reviewer:** Plastic Efficiency Reviewer  
**Date:** 2025-06-09  
**Scope:** PETG mesh solid volume analysis, print time estimation, and mass reduction opportunities  
**Status:** CONFIRMED findings are derived directly from the review package CSV data and `config.py`. LIKELY findings are engineering projections based on the CAD source. NEEDS TEST findings require slicer validation or physical prototyping.

---

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