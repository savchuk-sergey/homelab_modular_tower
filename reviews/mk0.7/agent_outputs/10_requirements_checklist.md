# Requirements Checklist Review

**Review Date:** 2026-06-27 (inferred from revision context)  
**Reviewer:** Requirements Checklist Reviewer (Agent)  
**Revision:** mk0.7 (branch `cad/mk0.7`)  
**Source of Truth:** `AGENTS.md` (project requirements), `cad/config.py`, `cad/assembly/tower_assembly.py`, `cad/exporters/part_registry.py`, `cad/exporters/export_parts.py`, revision documentation under `revisions/mk0.7/`

---

## Executive Summary

mk0.7 advances the project with a well-engineered bottom intake fan cartridge, dust-filter provisions, engineering placeholders for the 120 mm fan and Raspberry Pi 3B, and a clean export taxonomy. The codebase remains strongly parametric and the CadQuery architecture is sound. However, three issues prevent full compliance: (1) **corner blocks are placed at the vertical center of the tower instead of the top and bottom frame corners**, undermining their primary structural role; (2) **the top 120 mm exhaust fan is missing** (only a passive grille exists), leaving the active chimney airflow unverified; and (3) **no CFD or physical airflow verification** has been performed.

The revision is not blocked from progressing, but the corner-block placement and the missing top exhaust fan are real engineering gaps that should be addressed before any load-bearing or thermal validation is claimed.

---

## Requirement Evaluations

### 1. Modularity — **PASS**

**Evidence:**
- All six modules (`ups_power_tray`, `external_ssd_bay`, `ssd_expansion_tray`, `raspberry_pi_tray`, `mikrotik_tray`, `mini_pc_tray`) share the same standard interface defined in `config.py`: `MODULE_WIDTH = 170.0`, `MODULE_DEPTH = 176.0`, `MODULE_HEIGHT_STEP = UNIT_HEIGHT`, `RAIL_SPACING = METAL_RAIL_X_OFFSET * 2`, `TRAY_FRONT_HANDLE_WIDTH = 64.0`, `TRAY_LOCK_HOLE_DIAMETER = SCREW_CLEARANCE_M3`, and anti-slide tab parameters (`MODULE_LOCK_ANTI_SLIDE_TAB_WIDTH`, etc.).
- The assembly (`tower_assembly.py`) places each module on the same vertical metal guide rails at identical X/Y offsets, with vertical stacking controlled by `TRAY_STACK`. Because tray side-wall height (`MODULE_SIDE_WALL_HEIGHT = 12.0`) is well below the allocated slot pitch (`UNIT_HEIGHT = 35.0`), there is physical clearance between trays. This allows any module to slide forward on the shared rails without interference from modules above or below it.
- `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0` and the tray stop explicitly demonstrate front-service extraction capability.

**Grade:** A- — The module standard is fully codified and geometrically consistent. Front extraction is possible. A dedicated retention/lock mechanism is visible in config parameters but not fully modeled in the assembly for every module; however, the geometry does not block independent removal.

---

### 2. Repairability — **PASS**

**Evidence:**
- All fasteners use standard metric sizes: M5 threaded rods (`ROD_DIAMETER = 5.0`, `ROD_CLEARANCE = 5.6`), M3 screws (`M3_CLEARANCE = 3.4`), M4 (`M4_CLEARANCE = 4.4`), M5 washers (`M5_WASHER_DIAMETER = 12.0`), and heat-set inserts (`HEAT_SET_INSERT_M3_DIAMETER = 5.2`).
- TPU feet are explicitly designed as replaceable: `FOOT_SOCKET_CLEARANCE`, `FOOT_SCREW_DIAMETER`, `FOOT_COUNTERBORE_DIAMETER`.
- The bottom fan is in a removable `bottom_fan_cartridge`; no glue or permanent fastening is implied anywhere in the CAD code or documentation.
- Side panels are sectioned into three independently replaceable parts (`lower`, `middle`, `upper`).

**Grade:** A — No adhesives, no exotic fasteners, all key wear parts (feet, fan cartridge, panels) are individually replaceable.

---

### 3. Structural Stiffness — **PARTIAL**

**Evidence:**
- **M5 rods:** Present. `create_m5_threaded_rod` is placed at all four rod positions (`rod_positions()`) spanning the full `ROD_LENGTH = TOWER_HEIGHT`.
- **Metal guide rails:** Present. `create_metal_guide_rail` is placed at four positions with full height `METAL_RAIL_HEIGHT = TOWER_HEIGHT - 34.0`.
- **Top/bottom frames:** Present. `make_bottom_structural_frame` (Z=0) and `make_top_structural_frame` (Z=`TOWER_HEIGHT`).
- **Corner blocks:** **FAILING.** `create_corner_block` is placed at `z = cfg.TOWER_HEIGHT / 2` (~160.8 mm on a ~321.5 mm tower) with `CORNER_BLOCK_HEIGHT = 28.0`. This means the four "corner blocks" sit horizontally at the tower corners but vertically in the middle of the structure. They do **not** connect the top and bottom frames to the rods at the frame corners. Their primary stiffness role—tying the rod-to-frame joints—is not fulfilled.

**Grade:** C — The rods, rails, and frames are present, but the critical corner-block element is mis-located. Plastic parts (side panels, base wings) add stiffness but should not be primary load-bearing elements. Without corner blocks at the frame corners, the frame-to-rod connection relies on through-hole clearance fit alone, which is insufficient for primary stiffness.

---

### 4. Airflow — **PARTIAL**

**Evidence:**
- **Bottom 120 mm intake:** Fully modeled. `bottom_fan_cartridge` (removable), `bottom_fan_grille`, `bottom_filter_frame`, `bottom_filter_retainer`, and `fan_120x120x25_placeholder` with `FAN_120_SIZE = 120.0`, `FAN_120_HOLE_SPACING = 105.0`, `FAN_120_HOLE_DIAMETER = 4.4`. The intent is clear and parametrically complete.
- **Top 120 mm exhaust:** **INCOMPLETE.** Only `top_fan_grille` exists at `TOWER_HEIGHT + TOP_FAN_PANEL_Z_OFFSET`. There is **no** top `fan_120x120x25_placeholder`, no top fan cartridge, and no active exhaust modeled. A passive grille does not guarantee the required chimney effect.
- **Mini PC separate duct:** Present. `mini_pc_airflow_duct_placeholder` is placed in the assembly with dedicated duct parameters (`DUCT_WIDTH`, `DUCT_HEIGHT`, `DUCT_WALL`).
- **Rear Service Spine:** Positioned at the rear (`rear_y = OUTER_DEPTH/2 - REAR_SPINE_DEPTH/2`) and does not intersect the central vertical flow path.
- **No verification:** `KNOWN_ISSUES.md` explicitly states: "Нет CFD и нет физической проверки расхода воздуха." `BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO = 0.58` is a review threshold, not a validated performance metric.

**Grade:** C+ — Bottom intake is well engineered. The missing top exhaust fan is a clear gap. Without CFD or physical testing, the airflow claim is unverified.

---

### 5. Serviceability — **PASS**

**Evidence:**
- **Bottom fan:** `bottom_fan_cartridge` is a separate part located below the base frame (`BOTTOM_FAN_CARTRIDGE_Z`). The revision notes explicitly state it is "обслуживаемый cartridge" and does not require tower disassembly.
- **Side panels:** Three sections per side (`SIDE_PANEL_SECTION_COUNT = 3`) with individual labels (`lower`, `middle`, `upper`). They are mounted outside the rod envelope and can be removed without touching the M5 rods.
- **Modules:** All trays have `TRAY_FRONT_HANDLE_DEPTH` and are on rails. `MINI_PC_TRAY_SERVICE_TRAVEL` proves front-slide serviceability.

**Grade:** A- — Service access is designed in at all three levels (bottom fan, side panels, front modules). Top fan serviceability is N/A because the top fan is missing.

---

### 6. Parametric Design — **PASS**

**Evidence:**
- `config.py` is 639 lines and contains **all** dimensional constants: tower envelope, materials, fasteners, structural frame, rails, module interface, placeholders, cooling, spine, power bus, and export settings.
- No hardcoded dimensions appear in `tower_assembly.py` or `export_parts.py`; all values are read from `cfg.*`.
- Every part has its own factory function in `part_registry.py`: 58 distinct entries across plastic, metal, placeholders, and review geometry.
- Assembly is isolated in `cad/assembly/tower_assembly.py`.
- Export is isolated in `cad/exporters/export_parts.py` and `cad/exporters/part_registry.py`.
- No part/assembly/export logic is mixed in a single file.

**Minor note:** A few unexplained constants exist in `config.py` itself (e.g., `TOWER_HEIGHT = TOTAL_UNITS * UNIT_HEIGHT + 24.0` where `24.0` is not annotated; `STACK_START_Z = 18.0` with no derivation comment). These are not magic numbers hidden in part functions, but they could benefit from inline comments.

**Grade:** A — Fully parametric, clean separation of concerns.

---

### 7. Scalability — **PASS**

**Evidence:**
- `UNIT_HEIGHT = 35.0` and `MODULE_SLOT_COUNT = 6` define a unit-based grid. Any new module can be added by adding an entry to `TRAY_STACK` with a unit count.
- `MODULE_WIDTH`, `MODULE_DEPTH`, `RAIL_SPACING`, and the lock interface are fixed for all modules. A new module only needs a new tray factory and placeholder factory.
- `TRAY_FACTORIES` and `placeholder_factories` are dictionaries; adding a new module type is a simple key-value addition.

**Grade:** A — The architecture is explicitly designed for future module additions.

---

### 8. Rear Service Spine — **PASS**

**Evidence:**
- `create_rear_service_spine`, `create_rear_service_spine_cover`, `create_power_bus_panel`, `create_power_bus_cover` are all in the assembly.
- Cable management features: `REAR_SPINE_CABLE_SLOT_WIDTH`, `REAR_SPINE_TIE_SLOT_WIDTH`, `SPINE_CABLE_TIE_SLOT_HEIGHT`, horizontal tie slots at multiple Z levels (`REAR_SPINE_HORIZONTAL_TIE_Z`), and backbone ribs (`REAR_SPINE_BACKBONE_RIB_X`).
- Power bus zones: `POWER_BUS_RAIL_LABELS` (19V, 12V, 5V, GND), `POWER_BUS_CONNECTOR_ZONES` (XT30, MicroFit, USB-C), `POWER_BUS_FUSE_BLOCK_WIDTH`, `POWER_BUS_TERMINAL_BLOCK_WIDTH`.
- Module trays have `REAR_CABLE_EXIT_WIDTH = 66.0` and `REAR_CABLE_EXIT_HEIGHT = 20.0`, forcing cables to exit rearward into the spine.
- `KNOWN_ISSUES.md` notes that "Реальный routing провода вентилятора в Rear Service Spine пока не детализирован"—a documentation gap, but the structural pathway exists.

**Grade:** A- — The spine geometry, cable tie provisions, and power bus zones are all parametrically modeled. Only the detailed fan wire routing remains to be documented.

---

### 9. Power System — **PASS**

**Evidence:**
- No AC/220V components exist inside the tower. The power architecture is `External AC/DC -> DC UPS -> Power Bus -> 19V/12V/5V/GND`, matching the AGENTS.md specification.
- `UPS_PLACEHOLDER_LOC`, `UPS_ZONE_MARKER_HEIGHT`, `UPS_COMPONENT_ZONES` (battery, BMS, fuse block, DC-DC, terminal blocks) provide a physical placeholder for the future DC UPS.
- Internal DC bus: `POWER_BUS_RAIL_LABELS` and `POWER_BUS_CONNECTOR_ZONES` define a serviceable bus with quick-connectors (XT30, MicroFit, USB-C) and dedicated fuse/terminal block zones.
- All modules draw from the internal bus via rear connectors; there are no external power cords running between modules.

**Grade:** A — The power architecture is fully codified and safe (no open mains). DC UPS and bus provisions are present at placeholder level, which is acceptable for this revision stage.

---

### 10. CAD Rules — **PASS**

**Evidence:**
- CadQuery is the only CAD engine used (`import cadquery as cq` everywhere).
- `config.py` is explicitly called the source of truth in its header: "STEP/STL files are derived from these CadQuery parameters and are not the source of truth."
- `export_parts.py` exports every part individually via `export_part(name, factory(), ...)`.
- `export_parts.py` also writes a `MANIFEST.md` that states: "Generated from CadQuery source. STEP/STL files are derived artifacts."
- No file mixes part geometry, assembly logic, and export logic. The directory structure (`parts/`, `assembly/`, `exporters/`) enforces separation.

**Grade:** A — Strict compliance with the CAD source-of-truth rules.

---

### 11. Revision Structure — **PASS**

**Evidence:**
- All five required documents are present in `revisions/mk0.7/`:
  - `REVISION.md`
  - `CALCULATIONS.md`
  - `DECISIONS.md`
  - `KNOWN_ISSUES.md`
  - `CHANGELOG.md`
- `REVISION.md` clearly states the revision goal and changed CAD areas.
- `CHANGELOG.md` lists Added, Changed, and Verified items.
- No evidence of retroactive changes to `mk0.1` or other older revisions.
- The export path is `exports/mk0.7/`, keeping derived artifacts revision-scoped.

**Grade:** A — Complete, well-organized revision documentation.

---

### 12. Export Organization — **PASS**

**Evidence:**
- `EXPORT_CATEGORIES` in `part_registry.py` defines five distinct directories:
  - `printable/plastic` — all PETG/PLA parts (frame, trays, panels, cartridge, filter, spine).
  - `non_printable/metal_reference` — M5 rods and metal guide rails.
  - `placeholders/devices` — Raspberry Pi, Mini PC, MikroTik, SSD, UPS placeholders.
  - `placeholders/fans` — 120 mm fan reference.
  - `review` — airflow path, blocked zones, stability, printability, and open-area review geometry.
- `REVISION.md` confirms assemblies are exported separately to `assemblies/assembly.step`.
- `export_parts.py` uses `export_categorized_parts` to write each category into its own folder, plus `MANIFEST.md`.

**Grade:** A — The export taxonomy prevents accidental printing of non-printable reference geometry and clearly separates review artifacts from production parts.

---

## Overall Compliance Score

| Requirement | Result | Weight | Points |
|-------------|--------|--------|--------|
| 1. Modularity | PASS | 1 | 1.0 |
| 2. Repairability | PASS | 1 | 1.0 |
| 3. Structural Stiffness | PARTIAL | 1 | 0.5 |
| 4. Airflow | PARTIAL | 1 | 0.5 |
| 5. Serviceability | PASS | 1 | 1.0 |
| 6. Parametric Design | PASS | 1 | 1.0 |
| 7. Scalability | PASS | 1 | 1.0 |
| 8. Rear Service Spine | PASS | 1 | 1.0 |
| 9. Power System | PASS | 1 | 1.0 |
| 10. CAD Rules | PASS | 1 | 1.0 |
| 11. Revision Structure | PASS | 1 | 1.0 |
| 12. Export Organization | PASS | 1 | 1.0 |
| **Total** | | **12** | **10.0** |

**Overall Compliance Score: 10.0 / 12 = 83.3%**

**Rating:** Satisfactory with reservations. The parametric foundation, export discipline, and modular standard are strong. The thermal and structural stories are incomplete and need hardening before any physical build or higher revision.

---

## Blockers

The following issues are **true blockers** for claiming mk0.7 is structurally and thermally ready for a physical build or merge to `master`:

1. **Corner blocks at tower center (structural integrity)**
   - `corner_block` objects are placed at `z = TOWER_HEIGHT / 2` (~160 mm), with height 28 mm. They do not contact the top or bottom structural frames.
   - In a rod-and-frame tower, the highest stress concentrations are at the frame corners where rods pass through. Corner blocks must be at those joints to distribute load, prevent frame tear-out, and provide clamping surfaces for the rods.
   - **Risk:** Without corner blocks at the top and bottom frames, the M5 rods bear directly on frame holes; the frame can wobble, and the through-hole fit is the only load path. This violates the AGENTS.md requirement that plastic must not be the sole structural element, because the frame-to-rod connection becomes a plastic bearing surface without reinforcement.
   - **Fix:** Either add eight corner blocks (four at top frame, four at bottom frame) or redesign the corner blocks as integral frame bosses with nut seats.

2. **Missing top 120 mm exhaust fan (thermal performance)**
   - Only `top_fan_grille` exists. There is no `top_fan_120_placeholder`, no top cartridge, and no top fan mount.
   - A bottom intake without a matched top exhaust relies on passive convection. In a 190×190 mm cross-section tower with ~300 mm height and multiple internal modules (especially a Mini PC), passive convection is unlikely to provide adequate cooling.
   - **Risk:** The tower may suffer from thermal stagnation or hot-spots above the module stack. The Mini PC, which has the highest thermal priority, depends on a strong chimney effect.
   - **Fix:** Add a top 120 mm fan placeholder and mounting mechanism symmetric to the bottom fan cartridge. Verify total system pressure drop against the fan curve.

3. **No airflow or thermal verification (engineering validation)**
   - `KNOWN_ISSUES.md` explicitly states: "Нет CFD и нет физической проверки расхода воздуха."
   - `BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO = 0.58` is a design threshold, not a validated requirement.
   - **Risk:** The filter, grille, and module vents may create more pressure drop than anticipated, leading to insufficient flow.
   - **Fix:** At minimum, perform a hand-calculation pressure budget (filter + grille + module vents + spine) against the fan P-Q curve. Ideally, run a basic CFD or build a smoke-flow prototype.

---

## Recommendations

### High Priority (address before next revision or physical test)

1. **Redesign corner block placement**
   - Create two variants or two placements: `corner_block_top` at `z = TOWER_HEIGHT - FRAME_THICKNESS/2` and `corner_block_bottom` at `z = FRAME_THICKNESS/2`.
   - Ensure each corner block has a rod bore (`ROD_CLEARANCE`), a washer seat (`M5_WASHER_SEAT_DEPTH`), and a nut seat (`M5_NUT_SEAT_DEPTH`) so the rod clamps the frame between the corner block and a washer/nut.
   - If the current `create_corner_block` is intended to be a mid-tower cable-management block, rename it (e.g., `mid_tower_brace`) and add a separate `frame_corner_block` for the structural joints.

2. **Add top exhaust fan assembly**
   - Add `top_fan_120x120x25_placeholder` and a `top_fan_cartridge` or `top_fan_mount` part analogous to the bottom fan cartridge.
   - Ensure the top fan is removable from the top without removing side panels or rods.
   - Verify that the top grille does not obstruct the fan blades or mounting holes.

3. **Complete the pressure-drop / thermal budget in `CALCULATIONS.md`**
   - List every flow restriction: bottom filter, bottom grille, module vent slots, Mini PC duct, and any rear-spine obstructions.
   - Compare the total open area and estimated pressure drop to a real 120 mm fan P-Q curve (e.g., Noctua NF-A12x25 or similar).
   - Document the result in `CALCULATIONS.md`.

### Medium Priority (improvement before `master` merge)

4. **Detail fan wire routing in Rear Service Spine**
   - `KNOWN_ISSUES.md` flags this as missing. Add a `fan_wire_channel` or `cable_clip` geometry in the spine that routes the bottom and top fan cables from the cartridge zone to the power bus without crossing the central airflow.
   - Add a placeholder for the cable bundle in the assembly so the routing is visible during review.

5. **Add a top-layer printability check for the bottom fan cartridge**
   - The cartridge is thin and wide (`BOTTOM_FAN_CARTRIDGE_WIDTH = 142.0`). Verify in `CALCULATIONS.md` or a review script that it fits within the `BAMBU_P2S_PRINT_VOLUME` and does not require excessive supports.

6. **Annotate unexplained constants in `config.py`**
   - `TOWER_HEIGHT = TOTAL_UNITS * UNIT_HEIGHT + 24.0` — explain what `24.0` represents (e.g., top frame thickness + bottom frame thickness + clearance).
   - `STACK_START_Z = 18.0` — explain why 18 mm (e.g., bottom frame + base gap).
   - This improves maintainability and prevents future agents from treating these as magic numbers.

### Low Priority (nice-to-have)

7. **Consider a unified `TRAY_LOCK` assembly model**
   - Add a small `tray_lock_screw` or `tray_lock_boss` assembly element to `tower_assembly.py` for each module so the retention mechanism is visually confirmed during review.

8. **Add `top_intake_open_area_review` geometry**
   - Symmetric to `bottom_intake_open_area_review`, model the top exhaust open area to verify it is ≥ the bottom intake open area (or at least within a reasonable margin).
