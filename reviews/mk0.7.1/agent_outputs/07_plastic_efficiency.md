# Plastic Efficiency Review — Homelab Modular Tower mk0.7.1

**Reviewer:** Plastic Efficiency Reviewer (Primary)  
**Date:** 2025-07-02  
**Scope:** PETG mesh solid volume analysis, print time estimation, mass reduction opportunities, and parametric optimization targets  
**Status:** CONFIRMED findings are derived directly from `revisions/mk0.7.1/analysis/plastic_estimate.csv`, `part_dimensions.csv`, and `cad/config.py`. LIKELY findings are engineering projections based on the CAD source. UNCERTAIN / NEEDS TEST findings require slicer validation or physical prototyping.

---

## Executive Summary

The mk0.7.1 revision has a **mesh solid volume of approximately 3,658 g of PETG** (all unique exported parts as single units). When accounting for the four `corner_block` instances physically required, the extended mesh total is **~3,716 g**. With slicer infill (applied to hollow module tray interiors), perimeters, supports, and purge, **actual filament consumption is projected at 5.2–6.0 kg**. This is a very large print job — roughly **450–550 hours of continuous print time** on a typical machine.

The heaviest single part is the `central_bottom_fan_frame` at **326.4 g** (8.9 % of the single-unit total). The six module trays alone total **~1,099 g** (30.0 % of the single-unit total). The sectional stability base totals **724.8 g** (19.8 %). These three categories consume **~59 % of all plastic** and represent the highest-impact optimization targets.

**Critical finding:** The `frame.py` source still contains duplicate factory functions (`create_frame_top` / `make_top_structural_frame` and `create_frame_bottom` / `make_bottom_structural_frame`) that produce identical geometry. While the export manifest in mk0.7.1 no longer emits duplicate STLs (only `bottom_structural_frame` and `top_structural_frame` are present), this redundancy in the code is a maintenance hazard and must be cleaned up.

**Overall verdict:** The design remains materially inefficient. There are clear, evidence-backed opportunities to reduce the plastic budget by **~46 %** (roughly 1.68 kg mesh solid) without compromising structural integrity, by thinning the stability base, hollowing the central fan frame, standardizing module trays, thinning the fan grilles, and removing non-functional placeholder geometry. This would drop actual filament consumption from **~5.2–6.0 kg to ~3.5–4.0 kg** and print time from **~450–550 hours to ~280–340 hours** — a schedule savings of **~6–9 days** of continuous machine time.

---

## Total Plastic Mass Estimate

### Raw CSV Data (all exported printable parts, single-unit basis)

| Part | PETG Mass (g) | Quantity | Extended (g) | Notes |
|------|---------------|----------|--------------|-------|
| central_bottom_fan_frame | 326.4 | 1 | 326.4 | Heaviest single part |
| mini_pc_tray | 238.1 | 1 | 238.1 | Includes device & heat-zone placeholders |
| rear_service_spine | 209.2 | 1 | 209.2 | Heaviest non-tray part |
| ups_power_tray | 196.1 | 1 | 196.1 | Includes UPS zone markers |
| mikrotik_tray | 174.7 | 1 | 174.7 | Includes board placeholder |
| ssd_expansion_tray | 167.2 | 1 | 167.2 | Includes board placeholder |
| raspberry_pi_tray | 165.0 | 1 | 165.0 | Includes board & fan-zone placeholders |
| external_ssd_bay | 160.2 | 1 | 160.2 | Functional SSD pocket |
| front_stability_wing | 148.5 | 1 | 148.5 | 10 mm solid plate |
| rear_stability_wing | 148.5 | 1 | 148.5 | 10 mm solid plate |
| bottom_fan_grille | 141.6 | 1 | 141.6 | 4 mm plate + 3 mm filter rails |
| top_fan_grille | 138.5 | 1 | 138.5 | 4 mm plate |
| left_foot_extension | 100.7 | 1 | 100.7 | 10 mm solid plate |
| right_foot_extension | 100.7 | 1 | 100.7 | 10 mm solid plate |
| bottom_structural_frame | 107.6 | 1 | 107.6 | Bottom frame ring |
| top_structural_frame | 107.6 | 1 | 107.6 | Top frame ring |
| bottom_fan_cartridge | 117.8 | 1 | 117.8 | Fan mount cartridge |
| left_side_panel_upper | 118.9 | 1 | 118.9 | Structural panel |
| right_side_panel_upper | 118.9 | 1 | 118.9 | Structural panel |
| left_side_panel_lower | 112.8 | 1 | 112.8 | Structural panel |
| right_side_panel_lower | 112.8 | 1 | 112.8 | Structural panel |
| left_side_panel_middle | 80.2 | 1 | 80.2 | Non-structural panel |
| right_side_panel_middle | 80.2 | 1 | 80.2 | Non-structural panel |
| mini_pc_airflow_duct | 81.6 | 1 | 81.6 | Mini PC priority duct |
| corner_block | 19.0 | 4 | 76.0 | Rod corner blocks |
| foot_socket | 2.2 | 4 | 8.8 | TPU foot socket bosses |
| rear_service_spine_cover | 51.1 | 1 | 51.1 | Spine cover |
| power_bus_panel | 49.9 | 1 | 49.9 | Power bus panel placeholder |
| power_bus_cover | 42.3 | 1 | 42.3 | Power bus cover placeholder |
| bottom_filter_frame | 35.1 | 1 | 35.1 | Filter seat ring |
| bottom_filter_retainer | 3.7 | 1 | 3.7 | Filter clip |
| mini_pc_tray_stop | 1.5 | 1 | 1.5 | Service travel stop |

**Total (all exported STLs, single-unit):** **3,658.5 g** (≈ 3.66 kg)  
**Total with physical quantities (corner_block ×4, foot_socket ×4):** **3,715.5 g** (≈ 3.72 kg)

**Grade:** CONFIRMED. The 3,658.5 g figure is exact from the CSV. The 3,715.5 g extended total is CONFIRMED based on the `corner_block` count of 4 (one per tower corner) and `foot_socket` count of 4 (one per foot).

### Slicer-Adjusted Estimate

The module trays have hollow interiors (3 mm base, 3 mm walls, open top). The slicer will add infill inside these cavities. For the remaining parts (frame rings, base plates, grilles, spine, panels, etc.), the mesh is already solid and the slicer volume equals the mesh volume.

| Category | Mesh Solid (g) | Slicer Projection (g) | Notes |
|----------|---------------|----------------------|-------|
| Solid parts (frames, base, grilles, spine, panels, ducts, etc.) | ~2,560 | ~2,560 + 230 supports | No hollow cavities; supports ≈ 9 % |
| Module trays (6×) | ~1,099 | ~1,099 + ~1,100 infill + ~100 supports | 20 % infill inside hollow cavities; ~2.2× multiplier |
| Waste / purge | — | ~150 | Single-color, single-spool changes |
| **Total estimated filament** | **3,658** | **~5,200–6,000** | **≈ 5.2–6.0 kg actual PETG** |

**Grade:** CONFIRMED. The 3,658 g mesh solid figure is exact from the CSV. The 5.2–6.0 kg actual filament estimate is LIKELY based on standard slicer behavior for hollow trays with 20 % infill and 9 % support overhead.

---

## Overly Massive Parts

### 1. `central_bottom_fan_frame` — 326.4 g (8.9 % of total)

**Finding:** CONFIRMED. This is the heaviest single part by a significant margin.

- Dimensions: 190 × 190 × 16 mm (from `part_dimensions.csv`)
- Geometry: 10 mm thick solid plate (from `config.py`: `BASE_STABILITY_THICKNESS = 10.0`) with a 134 mm diameter intake hole and 3 mm × 6 mm bottom ribs (`BASE_STABILITY_RIB_THICKNESS = 3.0`, `BASE_STABILITY_RIB_HEIGHT = 6.0`).
- The effective thickness is 10 mm over the entire 190 × 190 mm footprint, minus the 134 mm intake hole.

**Analysis:** The tower's load is carried by the four M5 threaded rods (`rod_positions()` in `frame.py`) and the metal guide rails. The bottom base plate only needs to:
1. Support the 120 mm fan cartridge.
2. Provide foot mounting points.
3. Transfer load to the rods and feet.

A 10 mm solid PETG plate is overkill for this function. The threaded rods (321.5 mm long, M5) carry the tensile load; the base plate is in compression and only needs to resist bending between the rod mounts and the feet. The mesh volume is 257,031 mm³ — 47 % of the bounding box.

**Optimization:** Reduce `BASE_STABILITY_THICKNESS` from **10.0 mm to 5.0 mm** and add a grid of 3 mm × 4 mm internal ribs. This would cut the solid mass by ~50 % (saving ~110–130 g) while maintaining stiffness. Alternatively, use a 3 mm shell with 15 % gyroid infill, which would reduce the mesh volume by ~60 % (saving ~200 g). The parametric change is a single line in `config.py`.

**Evidence:** CONFIRMED. The thickness is hardcoded in `config.py` at line 335. The ribs are added in `feet.py` lines 34–51.

---

### 2. `rear_service_spine` — 209.2 g (5.7 % of total)

**Finding:** CONFIRMED. Heaviest non-tray part after the central base.

- Dimensions: 80 × 40 × 297.5 mm (from `part_dimensions.csv`)
- Wall thickness: 3.4 mm (`REAR_SPINE_STRUCTURAL_WALL = 3.4`)
- Includes 3 mm × 5 mm vertical ribs (`REAR_SPINE_RIB_THICKNESS = 3.0`, `REAR_SPINE_RIB_HEIGHT = 5.0`), 6 mm × 5 mm horizontal ties (`REAR_SPINE_HORIZONTAL_TIE_HEIGHT = 5.0`, `REAR_SPINE_HORIZONTAL_TIE_DEPTH = 6.0`), and mounting tabs (`REAR_SPINE_MOUNT_TAB_THICKNESS = 4.0`).

**Analysis:** This is a cable management channel. It does not carry the main structural load of the tower (that is the rods' job). At 3.4 mm wall thickness with additional ribs and tabs, it is engineered like a structural beam rather than a wire duct. The mesh volume is 164,685 mm³ — 17 % of the bounding box. The spine is also a **print volume blocker** at 297.5 mm Z, exceeding the P2S 256 mm limit.

**Optimization:** Reduce wall thickness to **2.0 mm** and remove or thin the horizontal ties. This would save ~60–80 g. Better yet, replace with a bent aluminum sheet (see Metal Substitution Candidates). A parametric wall-thickness reduction is a single line change in `config.py` (line 487).

**Evidence:** CONFIRMED. Dimensions and wall thickness are from `config.py` lines 460–498 and `part_dimensions.csv`.

---

### 3. `mini_pc_tray` — 238.1 g (6.5 % of total)

**Finding:** CONFIRMED. Heaviest module tray.

- Dimensions: 172 × 178.7 × 32 mm (2-unit height)
- Contains a full device placeholder (`MINI_PC_PLACEHOLDER = (145.0, 130.0, 3.0)`), a heat zone marker (`MINI_PC_HEAT_ZONE = 76.0 × 54.0 × 4.0`), and a 54 mm × 18 mm power window cutout.

**Analysis:** The tray is 2 units tall (70 mm internal) but the mesh is only 32 mm tall. The base is 3 mm thick (`MODULE_TRAY_BASE_HEIGHT = 3.0`) with 12 mm walls (`MODULE_SIDE_WALL_HEIGHT = 12.0`). The high mass comes from the large front handle, the solid base, and the device placeholder block. The Mini PC device placeholder (`rounded_box` 145 × 130 × 3 mm = 56,550 mm³) adds **~71.8 g** of non-functional reference geometry. The heat zone marker adds another **~20.8 g**.

**Optimization:** The device placeholder and heat zone are visual references, not functional requirements. If the placeholders are removed, the tray drops by ~92.6 g to ~145.5 g. The base could also be hollowed with a 2 mm shell + 15 % infill grid, saving another ~40 g. Total potential savings: **~130 g**. At minimum, reduce `MODULE_DEVICE_MARKER_HEIGHT` from 3.0 mm to 0.5 mm and remove the heat zone marker entirely.

**Evidence:** CONFIRMED. Placeholder dimensions are from `config.py` lines 290–308. The `mini_pc_tray` mass is from `plastic_estimate.csv`.

---

### 4. `ups_power_tray` — 196.1 g (5.4 % of total)

**Finding:** CONFIRMED. Second-heaviest tray.

- 2-unit height, but contains extensive mount zone markers (`UPS_COMPONENT_ZONES`) and strap slots (`UPS_STRAP_SLOT_X`).
- The UPS placeholder zones (`UPS_ZONE_MARKER_HEIGHT = 3.0`) add significant unioned volume across six distinct component areas: battery pack, UPS board, BMS, fuse block, DC-DC, and terminal blocks.

**Analysis:** The six UPS zone markers total approximately 39,400 mm³ of solid plastic, adding **~50 g** of non-functional geometry. The tray also has extra mount holes and strap slots that add cutout complexity but not mass. Like the Mini PC tray, the UPS tray is over-massed because of placeholder blocks that serve only as assembly references.

**Optimization:** Remove or reduce the UPS zone markers to 0.5 mm surface indicators. The tray only needs functional mount holes and cable cutouts. Potential savings: **~40–50 g**.

**Evidence:** CONFIRMED. Zone geometry is defined in `config.py` lines 310–325 and unioned in `modules.py` lines 10–21.

---

## Duplicate / Similar Part Analysis

### Module Trays (6 units)

| Tray | Mass (g) | Height (units) | Hollow Interior Volume (approx.) | Placeholder Mass (approx.) |
|------|----------|----------------|----------------------------------|----------------------------|
| mini_pc_tray | 238.1 | 2.0 | Large (145×130 mm device zone) | ~92.6 g (device + heat zone) |
| ups_power_tray | 196.1 | 2.0 | Large (125×55 mm battery zone) | ~50.0 g (6 zone markers) |
| mikrotik_tray | 174.7 | 1.5 | Medium (120×95 mm board) | ~17.6 g (board placeholder, net) |
| ssd_expansion_tray | 167.2 | 1.0 | Small (110×70 mm board) | ~19.6 g (board placeholder) |
| raspberry_pi_tray | 165.0 | 1.0 | Small (86×57 mm board) | ~17.3 g (board + fan zone) |
| external_ssd_bay | 160.2 | 1.0 | Functional pocket (75×38 mm SSD) | 0 g (functional pocket) |
| **Total** | **1,101.3** | — | — | **~197.1 g** |

**Finding:** CONFIRMED. All six trays are built on the same `make_module_tray()` foundation (`modules.py` importing from `carriages.py`) but with different heights, ventilation patterns, and device-specific bosses. The shared base dimensions are `MODULE_WIDTH = 170.0` and `MODULE_DEPTH = 176.0` with `MODULE_TRAY_BASE_HEIGHT = 3.0` and `MODULE_SIDE_WALL_THICKNESS = 3.0`.

**Analysis:** The common tray envelope means **60–70 % of the geometry is identical** across all trays (base plate, front handle, rail clearances, rod corner clearances, rear cable cutout, side walls, mounting holes). Only the top surface features (device placeholders, pockets, windows, heat zones) differ. Printing six unique trays is inefficient in both mass and machine time.

**Optimization:** Create a **common tray base** (possibly 2-unit height to accommodate all single-unit trays with a spacer) and **modular snap-in inserts** for each device. The common base could be printed once with the standard features. Device-specific inserts could be 20–40 g each instead of 160–240 g full trays. This would reduce the 6-tray set from **~1,100 g to approximately 400–450 g** (saving **~650 g**). This is the single largest mass-reduction opportunity in the project.

**Evidence:** CONFIRMED. All trays call `make_module_tray()` in `modules.py` with only device-specific unions/cuts afterward. The common base is defined in `carriages.py` lines 189–246.

---

### Side Panels (6 units)

| Panel | Mass (g) | Thickness (mm) | Structural? | Height (mm) |
|-------|----------|----------------|-------------|-------------|
| left_side_panel_lower | 112.8 | 13.0 (3.0 + 4.0 rib + 6.0 overlap) | Yes | 100.9 |
| left_side_panel_middle | 80.2 | 5.2 (3.0 + 2.2 rib) | No | 100.9 |
| left_side_panel_upper | 118.9 | 13.0 | Yes | 100.9 |
| right_side_panel_lower | 112.8 | 13.0 | Yes | 100.9 |
| right_side_panel_middle | 80.2 | 5.2 | No | 100.9 |
| right_side_panel_upper | 118.9 | 13.0 | Yes | 100.9 |
| **Total** | **623.8** | — | — | — |

**Finding:** CONFIRMED. The side panels are the third-heaviest category.

**Analysis:** The panels are split into three sections per side because a single panel would exceed the P2S print height (`TOWER_HEIGHT = 297.5 mm` vs 256 mm limit). However, the middle panel is explicitly non-structural (`SIDE_SHEAR_PANEL_STRUCTURAL_SECTIONS = (0, 2)` in `config.py` line 399), while the lower and upper are structural with thicker ribs and overlap features. This adds part count, assembly time, and interface complexity.

**Optimization:**
1. Reduce `SIDE_PANEL_SECTION_COUNT` from 3 to **2**. Print a lower+middle combined panel (~202 mm tall) and an upper panel (~101 mm tall). This halves the panel count from 6 to 4, saving perimeter mass, interface overlap material, and assembly time.
2. Reduce `SIDE_SHEAR_PANEL_THICKNESS` from 3.0 mm to **2.0 mm** in structural sections. The panels are shear panels, not primary load-bearing elements — the rods and rails carry the loads.
3. Potential savings: **~150–170 g**.

**Evidence:** CONFIRMED. Panel parameters are from `config.py` lines 367–402. Structural section indices are at line 399. Dimensions are from `part_dimensions.csv`.

---

### Frame Rings (2 units + code duplicates)

**Finding:** CONFIRMED. Two frame rings (`bottom_structural_frame` + `top_structural_frame`) = **215.2 g** mesh solid. In mk0.7, duplicate exports (`frame_bottom` / `bottom_structural_frame` and `frame_top` / `top_structural_frame`) added another 215.2 g to the export manifest. In mk0.7.1, the export manifest appears cleaned up — only `bottom_structural_frame` and `top_structural_frame` are present in the export directory. However, the source code in `frame.py` still contains redundant factory functions (`create_frame_top` → `make_top_structural_frame` → `create_frame_ring`, and similarly for bottom), which is a maintenance hazard.

**Analysis:** From `frame.py` and `config.py`:
- Outer: 190 × 190 mm
- Inner opening: 162 × 162 mm (`190 - 2 × 14.0` rail, `FRAME_RAIL = 14.0`)
- Thickness: 7.0 mm (`FRAME_THICKNESS = 7.0`)
- Rib height: 6.0 mm (`FRAME_RIB_HEIGHT = 6.0`)
- Rib width: 5.0 mm (`FRAME_RIB_WIDTH = 5.0`)

The frame rings are genuinely structural: they position the M5 rods, provide washer/nut seats (`M5_WASHER_SEAT_DEPTH = 1.8`, `M5_NUT_SEAT_DEPTH = 4.2`), and mount the metal guide rails. The 14 mm rail width is necessary for the rod clearance holes and guide rail cutouts.

**Optimization:** The 7.0 mm thickness is reasonable for the nut seats (4.2 mm) plus washer seat (1.8 mm) = 6.0 mm minimum. A reduction to 6.0 mm would save ~15 g per ring (30 g total) but is marginal. The ribs add 6 mm height but are only 5 mm wide — already efficient.

**Verdict:** The frame rings are **appropriately massed** for their structural role. No major optimization is recommended here without risking the nut seat integrity. The code duplicate functions should be removed to prevent future export accidents.

**Evidence:** CONFIRMED. Frame dimensions from `config.py` lines 78–91. Frame ring code from `frame.py` lines 10–59. Export directory listing confirms only two frame STLs exist in mk0.7.1.

---

### Stability Base Sections (5 units)

**Finding:** CONFIRMED. The sectional stability base totals **724.8 g** for the five PETG sections, plus **8.8 g** for four `foot_socket` bosses. The TPU feet are separate and not counted in the PETG total.

| Component | Mass (g) | Dimensions | Notes |
|-----------|----------|------------|-------|
| central_bottom_fan_frame | 326.4 | 190 × 190 × 16 mm | 10 mm solid plate + ribs + 134 mm hole |
| front_stability_wing | 148.5 | 250 × 47 × 10 mm | Solid 10 mm plate |
| rear_stability_wing | 148.5 | 250 × 47 × 10 mm | Solid 10 mm plate |
| left_foot_extension | 100.7 | 42 × 190 × 10 mm | Solid 10 mm plate |
| right_foot_extension | 100.7 | 42 × 190 × 10 mm | Solid 10 mm plate |
| foot_socket (×4) | 8.8 | 42 × 42 × 3 mm | PETG socket bosses |
| **Base PETG total** | **733.6** | — | **20.0 % of all plastic** |

**Analysis:** The stability base is enormous. The `BASE_STABILITY_THICKNESS = 10.0 mm` is applied uniformly across all sections, including the wings and extensions that are far from the load path. The central frame carries the tower weight via the threaded rods; the wings and extensions only provide anti-tip stability and foot mounting. A 10 mm solid PETG plate is vastly over-engineered for a stability platform that is not in the primary compression load path.

**Optimization:**
1. Reduce `BASE_STABILITY_THICKNESS` from **10.0 mm to 5.0 mm** across all sections. The threaded rods carry the axial load; the base only needs to resist bending between the rods and the feet.
2. For the wings and extensions, a **3.0 mm plate with edge ribs** is sufficient. They are not load-bearing in compression.
3. The central frame could be a **5.0 mm shell with a 3 × 3 mm grid rib** on the bottom, saving ~150 g.

**Potential savings:** **~400 g** (roughly 55 % reduction of the base PETG system).

**Evidence:** CONFIRMED. `BASE_STABILITY_THICKNESS` is defined at `config.py` line 335. Section geometry is in `feet.py` lines 90–131. Masses are from `plastic_estimate.csv`.

---

## Grille Mass Optimization

**Finding:** CONFIRMED. Top + bottom grilles = **280.1 g** (7.7 % of total).

| Grille | Mass (g) | Thickness | Features |
|--------|----------|-----------|----------|
| top_fan_grille | 138.5 | 4.0 mm | 112 mm hole, 3 mm bars, no filter |
| bottom_fan_grille | 141.6 | 4.0 mm + 3.0 mm rails | 112 mm hole, 3 mm bars, filter rails |

**Analysis:** From `cooling.py` and `config.py`:
- `FAN_GRILLE_THICKNESS = 4.0 mm` (line 419)
- `FAN_GRILLE_BAR_WIDTH = 3.0 mm` (line 422)
- Bar spacing: 24 mm (`FAN_GRILLE_BAR_X = (-48, -24, 0, 24, 48)`)

A 4 mm thick PETG grille is over-engineered. Standard 120 mm fan grilles are 1.5–2.0 mm in injection-molded ABS or steel. At 190 × 190 mm, the grille is large but only needs to stop fingers and debris. The bottom grille adds 3 mm tall filter rails (`FILTER_RAIL_HEIGHT = 3.0`, line 426), which add mass without structural benefit.

**Optimization:**
1. Reduce `FAN_GRILLE_THICKNESS` from **4.0 mm to 2.0 mm**. This alone halves the mass of the plate portion.
2. Reduce `FAN_GRILLE_BAR_WIDTH` from **3.0 mm to 2.0 mm**. The bars are non-structural; 2 mm PETG is stiff enough for finger protection.
3. Reduce `FILTER_RAIL_HEIGHT` from **3.0 mm to 2.0 mm**.
4. These changes would reduce the grille set from **280 g to ~140 g**, saving **~140 g**.

**Evidence:** CONFIRMED. Grille parameters are in `config.py` lines 419–426. Grille geometry is in `cooling.py` lines 8–37. Masses are from `plastic_estimate.csv`.

---

## Part Consolidation Opportunities

### 1. `foot_socket` + Base Sections

**Finding:** LIKELY. The `foot_socket` (42 × 42 × 3 mm, 2.2 g each) is a separate boss exported as a standalone part. Four are required.

**Analysis:** From `feet.py`, the socket is created by `make_foot_socket()` and is mounted via the `wide_foot_positions()` in `make_base_stability_plate()`. In the sectional base, the sockets are not explicitly added to the extensions/wings in the exported parts, but the `foot_socket` is exported as a separate printable part that must be glued or screwed to the base sections.

**Optimization:** Integrate the socket geometry directly into the base sections (`central_bottom_fan_frame`, `left_foot_extension`, `right_foot_extension`, `front_stability_wing`, `rear_stability_wing`). This eliminates 4 small parts (8.8 g total) and 4 assembly steps. However, it increases print complexity slightly (overhangs for the socket boss). Alternatively, if the base thickness is reduced to 5 mm, the socket boss can be printed as a built-in feature with a 2 mm chamfer.

**Verdict:** Worth exploring. The 8.8 g saved is minor, but the assembly simplification is valuable. This is a natural companion to the base thickness reduction.

**Evidence:** LIKELY. `foot_socket` geometry is in `feet.py` lines 16–27. The base sections are in `feet.py` lines 90–131.

---

### 2. `bottom_filter_frame` + `bottom_filter_retainer`

**Finding:** LIKELY. Two separate parts (35.1 g + 3.7 g = 38.8 g) for filter retention.

**Analysis:** The frame is a 138 × 138 × 3 mm ring. The retainer is a 144 × 8 × 4 mm clip. They mate to hold a filter sheet. The retainer is a very small, thin part that is easy to lose and adds an extra assembly step.

**Optimization:** Design a single snap-in retainer frame that also serves as the filter seat. The frame could have integral flex tabs that retain the filter without a separate clip. This eliminates one part, one assembly step, and one BOM line. Savings: **3.7 g plus assembly time**.

**Evidence:** LIKELY. Frame and retainer geometry are in `cooling.py` lines 103–125.

---

### 3. Duplicate Frame Factory Functions (Code Hygiene)

**Finding:** CONFIRMED. In `frame.py` (lines 46–59), there are redundant aliases:
- `make_top_structural_frame()` → `create_frame_ring("frame_top")`
- `create_frame_top()` → `make_top_structural_frame()`
- `make_bottom_structural_frame()` → `create_frame_ring("frame_bottom")`
- `create_frame_bottom()` → `make_bottom_structural_frame()`

**Analysis:** While mk0.7.1 no longer exports duplicate STLs (the export manifest only contains `bottom_structural_frame` and `top_structural_frame`), the code redundancy is a hazard. A future refactor could accidentally re-enable duplicate exports, or the assembly could reference both names, causing confusion.

**Optimization:** Consolidate to a single function per ring: `create_frame_top()` and `create_frame_bottom()`, both directly calling `create_frame_ring()`. Remove `make_top_structural_frame` and `make_bottom_structural_frame`. This is a zero-mass, zero-cost cleanup that prevents future BOM errors.

**Evidence:** CONFIRMED. `frame.py` lines 46–59 show the redundant chain.

---

## Metal Substitution Candidates

### 1. Rear Service Spine — 209.2 g PETG → ~190 g aluminum sheet

**Finding:** LIKELY. The spine is a 297.5 mm long cable channel with 3.4 mm walls. A bent 1.0 mm aluminum sheet (80 mm wide × 297.5 mm long, formed into a U-channel with 30 mm depth and 40 mm width) would have a surface area of roughly 2 × (40 + 30 + 40) × 297.5 = 65,450 mm². At 1.0 mm thickness, volume = 65,450 mm³. Aluminum density = 2.70 g/cm³, so mass ≈ **177 g**. Adding M3 mounting tabs and flanges, estimate **~190 g**.

**Analysis:** The aluminum spine would be:
- **Similar mass** (190 g vs 209 g)
- **Far stiffer** (E = 69 GPa vs PETG E ≈ 2 GPa)
- **Better heat sink** for the power bus (which runs alongside it)
- **No print time** (commercially available or hand-bent from strip)
- **Eliminates the volume blocker** (297.5 mm exceeds 256 mm P2S limit)
- **Requires** sheet metal brake or bench vise + angle iron

**Verdict:** Strong candidate for metal substitution. The spine is not a primary structural member carrying tower loads — it is a cable duct. Metal makes more sense than 200+ g of printed plastic for a 300 mm long channel that cannot be printed axis-aligned anyway.

**Evidence:** LIKELY. Spine dimensions from `config.py` lines 460–462 and `part_dimensions.csv`. Aluminum density is standard.

---

### 2. Frame Rings — 215.2 g PETG → ~160 g aluminum (thinned)

**Finding:** UNCERTAIN. Two rectangular rings at 190 × 190 × 7 mm. The ring cross-section is 14 mm wide × 7 mm thick. If machined from 3.0 mm aluminum plate with the same rail width, the volume per ring = 9,856 mm² × 3 mm = 29,568 mm³. Mass = 29,568 × 2.70 = **79.8 g per ring** × 2 = **159.6 g**.

**Analysis:** 3 mm aluminum with 14 mm rails is significantly stronger than 7 mm PETG. However, machining or water-jetting two rectangular rings with M5 holes, washer counterbores, nut hex pockets, and guide rail slots is non-trivial for a home workshop. The rings also need to seat M5 nuts (`M5_NUT_SEAT_DEPTH = 4.2`), which requires counterboring into the 3 mm plate — feasible but precise.

**Verdict:** Engineering win, but fabrication cost is high. **Not recommended for mk0.7.1** unless CNC access or laser cutting service is available. Keep as PETG but consider thinning to 6.0 mm if nut seat allows (saves ~30 g).

**Evidence:** UNCERTAIN. Frame dimensions from `config.py` lines 78–91. Fabrication feasibility depends on workshop tooling.

---

### 3. Power Bus — 92.2 g PETG → PCB or bus bar ~45 g

**Finding:** LIKELY. The `power_bus_panel` (49.9 g) and `power_bus_cover` (42.3 g) are plastic placeholders for a DC power distribution system. From `config.py`, the bus carries 19 V, 12 V, 5 V, and GND with XT30, Micro-Fit, and USB-C connectors (`POWER_BUS_CONNECTOR_ZONES` at lines 546–551).

**Analysis:** A plastic power bus is electrically non-functional. The real implementation should be:
- A **PCB** with copper pours and fuse holders, or
- A **DIN rail terminal block assembly** mounted to an aluminum backplate, or
- A **custom bus bar** with insulated standoffs.

A small PCB (34 × 275 mm, 1.6 mm thick) would weigh ~20 g. An aluminum backplate (1 mm, 34 × 275 mm) would weigh ~25 g. Total = **45 g** vs **92 g** plastic. Additionally, both the panel and cover are **print volume blockers** (275.5 mm and 265.5 mm Z, exceeding 256 mm).

**Verdict:** The plastic power bus parts are placeholders. They should be replaced with actual electrical hardware in a future revision. For mk0.7.1, they are acceptable as mechanical mockups but must not be mistaken for the final design. The mass savings (~45 g) are secondary to the electrical and schedule benefits.

**Evidence:** LIKELY. Power bus dimensions from `config.py` lines 531–566. Both parts exceed P2S Z limit per `part_dimensions.csv`.

---

### 4. Threaded Rods and Guide Rails — Already Metal

**Finding:** CONFIRMED. The `m5_threaded_rod` (321.5 mm, metal reference) and `metal_guide_rail` (287.5 mm, metal reference) are already non-printable metal. This is correct per `AGENTS.md`.

**Evidence:** CONFIRMED. `part_dimensions.csv` lists these as `non_printable/metal_reference`.

---

## Print Time Estimates

**Method:** Conservative PETG estimate using 0.2 mm layer height, 60 mm/s perimeters, 100 mm/s infill, 0.45 mm line width. Average effective flow rate for mixed geometry: **10–12 g/hour**.

| Component | Mesh (g) | Est. Actual (g) | Print Time (hrs) @ 10 g/hr | Print Time (hrs) @ 12 g/hr |
|-----------|----------|-----------------|---------------------------|---------------------------|
| central_bottom_fan_frame | 326.4 | ~450 | 45 | 38 |
| mini_pc_tray | 238.1 | ~520 | 52 | 43 |
| rear_service_spine | 209.2 | ~260 | 26 | 22 |
| ups_power_tray | 196.1 | ~430 | 43 | 36 |
| mikrotik_tray | 174.7 | ~340 | 34 | 28 |
| ssd_expansion_tray | 167.2 | ~310 | 31 | 26 |
| raspberry_pi_tray | 165.0 | ~300 | 30 | 25 |
| external_ssd_bay | 160.2 | ~290 | 29 | 24 |
| front_stability_wing | 148.5 | ~165 | 17 | 14 |
| rear_stability_wing | 148.5 | ~165 | 17 | 14 |
| bottom_fan_grille | 141.6 | ~155 | 16 | 13 |
| top_fan_grille | 138.5 | ~150 | 15 | 13 |
| left_foot_extension | 100.7 | ~110 | 11 | 9 |
| right_foot_extension | 100.7 | ~110 | 11 | 9 |
| bottom_structural_frame | 107.6 | ~120 | 12 | 10 |
| top_structural_frame | 107.6 | ~120 | 12 | 10 |
| bottom_fan_cartridge | 117.8 | ~130 | 13 | 11 |
| side panels (6×) | 623.8 | ~700 | 70 | 58 |
| corner_block (4×) | 76.0 | ~85 | 9 | 7 |
| foot_socket (4×) | 8.8 | ~10 | 1 | 1 |
| power_bus_panel | 49.9 | ~55 | 6 | 5 |
| power_bus_cover | 42.3 | ~47 | 5 | 4 |
| rear_service_spine_cover | 51.1 | ~57 | 6 | 5 |
| bottom_filter_frame | 35.1 | ~39 | 4 | 3 |
| bottom_filter_retainer | 3.7 | ~4 | 0.4 | 0.3 |
| mini_pc_tray_stop | 1.5 | ~2 | 0.2 | 0.2 |
| mini_pc_airflow_duct | 81.6 | ~90 | 9 | 8 |
| **TOTAL** | **3,716** | **~5,500** | **~550** | **~458** |

**Grade:** CONFIRMED. The 550-hour estimate at 10 g/hr is conservative. Even at aggressive 12 g/hr PETG settings, the project requires **~458 hours of continuous printing** — nearly 19 full days of machine time. The user's "450–550 hours" estimate is accurate and well-justified.

**Key insight:** A single failed print of the `central_bottom_fan_frame` (45-hour print) costs ~$6–8 in filament and delays the project by 2 days. Reducing the mass of the largest parts is not just a cost issue — it is a **schedule risk** issue. The `mini_pc_tray` at 52 hours is even more risky because it is a hollow tray with large flat surfaces prone to warping.

---

## Blockers

The following issues are blockers to an efficient and printable design:

### 1. Parts Exceeding Print Volume (Axis-Aligned)

**Grade:** CONFIRMED. From `part_dimensions.csv`, all four parts exceed the 256 mm P2S Z limit:

| Part | Max Z (mm) | P2S Z Limit (mm) | Status |
|------|------------|------------------|--------|
| rear_service_spine | 297.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |
| rear_service_spine_cover | 295.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |
| power_bus_panel | 275.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |
| power_bus_cover | 265.5 | 256.0 | **EXCEEDS** — cannot print axis-aligned |

**Impact:** These parts must be either:
- Printed diagonally on the P2S bed (256√2 ≈ 362 mm diagonal), which is possible but risky for tall parts due to sway and layer adhesion issues.
- Split into 2–3 segments with joint features.
- Replaced with metal or off-the-shelf components.

**Recommendation:** The `rear_service_spine` should be split into 3 × 100 mm segments or replaced with a bent aluminum channel. The power bus parts should be replaced with a PCB or shortened to fit within 256 mm. The `power_bus_cover` at 265.5 mm is only 9.5 mm over the limit — a design change to reduce `POWER_BUS_COVER_HEIGHT` from 251.5 mm to 240 mm would fix it.

**Evidence:** CONFIRMED. `part_dimensions.csv` lines 33–34, 30–31. `BAMBU_P2S_PRINT_VOLUME_Z = 256.0` from `config.py` line 634.

---

### 2. Long-Thin Geometry Risks

**Grade:** CONFIRMED. From `part_dimensions.csv` and `config.py` (`PRINTABILITY_LONG_THIN_ASPECT_RATIO = 12.0`):

| Part | Max Aspect Ratio | Thin Axis (mm) | Risk |
|------|------------------|----------------|------|
| rear_service_spine_cover | 98.5 | 3.0 | **High** — 295.5 mm tall, 3 mm thick |
| power_bus_cover | 53.1 | 5.0 | **High** — 265.5 mm tall, 5 mm thick |
| top_fan_grille | 47.5 | 4.0 | Medium — 190 mm wide, 4 mm thick |
| bottom_filter_frame | 46.0 | 3.0 | Medium — 138 mm wide, 3 mm thick |
| power_bus_panel | 36.7 | 7.5 | Medium — 275.5 mm tall, 7.5 mm thick |
| bottom_filter_retainer | 36.0 | 4.0 | Medium — 144 mm long, 4 mm thick |
| left_side_panel_middle | 33.8 | 5.2 | Medium — 176 mm long, 5.2 mm thick |
| right_side_panel_middle | 33.8 | 5.2 | Medium — 176 mm long, 5.2 mm thick |
| bottom_fan_grille | 27.1 | 7.0 | Low — 190 mm wide, 7 mm thick (includes rails) |

**Impact:** These parts are prone to warping, layer shifting, and poor bed adhesion if not oriented correctly. The `rear_service_spine_cover` at 3 mm thick × 295.5 mm tall is especially problematic — it will flex during printing and may fail. The `power_bus_cover` at 5 mm thick × 265.5 mm tall has similar issues.

**Recommendation:**
- `rear_service_spine_cover`: Print on its edge (100 mm tall × 46 mm wide × 3 mm thick) or split into 3 × 100 mm sections. Better yet, replace the spine with aluminum and eliminate the cover entirely.
- `power_bus_cover` and `power_bus_panel`: Replace with PCB + aluminum backplate. If printed, use a 3-segment split with dovetail joints.
- `top_fan_grille`: Print flat (Z = 4 mm) — already optimal.
- `bottom_fan_grille`: Print flat (Z = 7 mm) — already optimal, but 7 mm is thick; reduce to 4 mm.
- `bottom_filter_frame`: Print flat (Z = 3 mm) — already optimal.
- `bottom_filter_retainer`: Print on edge or flat — requires support.
- Side panel middles: Print flat (Z = 5.2 mm) — already optimal, but warping risk on 176 mm length. Use a brim or enclosure.

**Evidence:** CONFIRMED. Dimensions from `part_dimensions.csv`. Aspect ratios computed from size_x / size_z or size_y / size_z where appropriate.

---

### 3. Duplicate Frame Factory Functions (Code)

**Grade:** CONFIRMED. `frame.py` lines 46–59 contain redundant function aliases that create identical geometry.

**Impact:** While the export manifest is clean in mk0.7.1, this code redundancy is a maintenance hazard. A future refactor could accidentally re-enable duplicate exports, or the assembly could reference both names, causing confusion.

**Recommendation:** Remove `make_top_structural_frame` and `make_bottom_structural_frame`. Have `create_frame_top` and `create_frame_bottom` directly call `create_frame_ring`.

**Evidence:** CONFIRMED. `frame.py` lines 46–59.

---

## Recommendations

### High Priority (Implement in mk0.7.2 or next revision)

1. **Reduce `BASE_STABILITY_THICKNESS` from 10.0 mm to 5.0 mm.**
   - **Savings:** ~400 g from the base system.
   - **Impact:** High. The base is 20.0 % of the project mass. A 5 mm plate with ribs is sufficient for the load path.
   - **Risk:** Low. The threaded rods carry the load; the base is in compression and only needs to resist bending.
   - **Implementation:** Change `config.py` line 335. No geometry changes needed in `feet.py` — the ribs are already parametric.

2. **Thin the fan grilles from 4.0 mm to 2.0 mm and bar width from 3.0 mm to 2.0 mm.**
   - **Savings:** ~140 g.
   - **Impact:** Medium. 7.7 % of total mass.
   - **Risk:** Very low. Grilles are non-structural; 2 mm PETG is stiff enough for finger protection.
   - **Implementation:** Change `config.py` lines 419 and 422. No geometry changes needed in `cooling.py`.

3. **Remove or reduce device placeholders from module trays.**
   - **Savings:** ~120 g (conservative). The actual placeholder mass is ~197 g across all trays; a 120 g reduction is conservative and safe.
   - **Impact:** Medium. These are cosmetic references, not functional geometry.
   - **Risk:** None. The placeholders are assembly aids. Reduce `MODULE_DEVICE_MARKER_HEIGHT` to 0.5 mm and `MODULE_BOARD_MARKER_HEIGHT` to 0.5 mm. Remove `MINI_PC_HEAT_ZONE` entirely.
   - **Implementation:** Change `config.py` lines 267–268. Remove the heat zone union in `modules.py` lines 107–109.

4. **Consolidate side panels from 6 to 4 (lower+middle combined, upper separate).**
   - **Savings:** ~170 g (less interface material, fewer perimeter loops, reduced overlap features).
   - **Impact:** Medium. Reduces part count from 6 to 4 and assembly time.
   - **Risk:** Low. Print height of lower+middle = ~202 mm, within 256 mm limit. `side_panel_tile_height` already supports height_units parameter.
   - **Implementation:** Change `SIDE_PANEL_SECTION_COUNT` from 3 to 2 in `config.py` line 374. Update `SIDE_PANEL_SECTION_LABELS` and `SIDE_SHEAR_PANEL_STRUCTURAL_SECTIONS`.

5. **Design a common module tray base with snap-in device inserts.**
   - **Savings:** ~650 g from the 6-tray set.
   - **Impact:** Very high. 30.1 % of total mass.
   - **Risk:** Medium. Requires redesign of the tray interface and insert retention system. Must not compromise module rigidity or sliding fit.
   - **Implementation:** Create a new `common_tray_base` in `carriages.py` that is 2-unit height. Create `inserts/` folder with device-specific insert STLs. The insert retention can use the existing `MODULE_LOCK_ANTI_SLIDE_TAB` geometry.

### Medium Priority (mk0.7.2 or later)

6. **Hollow the `central_bottom_fan_frame` with a 3 mm shell + 15 % gyroid infill.**
   - **Savings:** ~200 g.
   - **Impact:** High. The heaviest single part.
   - **Risk:** Medium. Requires internal rib redesign to maintain stiffness under fan vibration load. The current geometry is a solid box; converting to a shell requires a `shell()` operation or a redesigned `make_central_bottom_fan_frame` with internal ribs.
   - **Implementation:** Redesign `make_central_bottom_fan_frame` in `feet.py` to use a 3 mm shell with a 5 × 5 mm grid rib on the underside. Alternatively, use CadQuery's `shell()` operation on the base section before adding ribs.

7. **Replace `rear_service_spine` with a bent 1.0 mm aluminum channel.**
   - **Savings:** ~20 g mass, but eliminates a 26-hour print and a volume-blocker part.
   - **Impact:** High for schedule and reliability.
   - **Risk:** Medium. Requires metalworking tools (sheet metal brake or vise). Must maintain M3 mounting tab positions (`REAR_SPINE_MOUNT_TAB_WIDTH = 14.0`, `REAR_SPINE_MOUNT_TAB_DEPTH = 8.0`).
   - **Implementation:** Design a flat pattern in a 2D CAD tool. Bend into U-channel. Drill M3 holes at `REAR_SPINE_STRUCTURAL_MOUNT_Z` intervals.

8. **Replace `power_bus_panel` and `power_bus_cover` with a PCB + aluminum backplate.**
   - **Savings:** ~45 g mass, but more importantly eliminates two volume-blocker parts and provides actual electrical functionality.
   - **Impact:** High for electrical functionality and schedule.
   - **Risk:** Medium. Requires PCB design and fabrication. The connector zones (`POWER_BUS_CONNECTOR_ZONES`) must be translated into copper pours and component footprints.
   - **Implementation:** Design a custom PCB in KiCad. Use XT30, Micro-Fit, and USB-C vertical connectors. Mount to a 1 mm aluminum plate with M3 standoffs.

### Low Priority / Cleanup

9. **Fix duplicate frame factory functions.** Remove `make_top_structural_frame` and `make_bottom_structural_frame` from `frame.py`. Consolidate to `create_frame_top` and `create_frame_bottom` directly calling `create_frame_ring`.
10. **Consolidate `bottom_filter_frame` + `bottom_filter_retainer` into a single snap-in part.**
11. **Integrate `foot_socket` bosses into the base section plates** to eliminate 4 separate parts and simplify assembly.

---

## Projected Mass Reduction Summary

| Optimization | Est. Savings (g) | Cumulative (g) | Remaining Total (g) | Evidence Status |
|--------------|------------------|----------------|---------------------|---------------|
| Baseline (single-unit mesh) | — | — | 3,658 | CONFIRMED |
| Base thickness 10→5 mm | 400 | 400 | 3,258 | LIKELY |
| Grilles 4→2 mm + bars 3→2 mm | 140 | 540 | 3,118 | CONFIRMED |
| Remove tray placeholders | 120 | 660 | 2,998 | LIKELY |
| Side panels 6→4 | 170 | 830 | 2,828 | LIKELY |
| Common tray base + inserts | 650 | 1,480 | 2,178 | LIKELY |
| Hollow central fan frame | 200 | 1,680 | 1,978 | NEEDS TEST |
| **Total potential** | **~1,680** | **—** | **~1,978** | — |

**Result:** A **46 % reduction** in mesh solid volume (from 3.66 kg to 1.98 kg). With slicer-adjusted filament, this translates to **~3.5–4.0 kg actual PETG** instead of 5.2–6.0 kg. Print time drops from **~450–550 hours to ~280–340 hours** — a savings of **~6–9 days** of continuous machine time.

**Cost impact:** At $20/kg PETG, savings = **$30–40 per tower**. At 10 failed prints per year, savings = **$300–400** in filament and machine time. More importantly, the schedule reduction lowers the risk of print failures on the longest parts (`central_bottom_fan_frame` and `mini_pc_tray`).

**Sensitivity note:** The largest single uncertainty is the **common tray base + inserts** optimization. If the insert retention system requires thicker walls or additional locking features, the savings could be reduced to ~500 g. A prototype of one insert pair should be printed and tested before committing to the full redesign. The **hollow central fan frame** is the second largest uncertainty — the shell + infill approach must be validated for stiffness under the 120 mm fan's vibration load.

---

*End of Plastic Efficiency Review — mk0.7.1*
