# Manufacturability Review — Homelab Modular Tower mk0.7

**Reviewer:** Manufacturability Reviewer  
**Date:** 2026-01-14  
**Revision:** mk0.7  
**Grade Summary:**

| Finding | Grade |
|---|---|
| Fastener count excessive | **CONFIRMED** |
| Heat-set insert dependency high | **CONFIRMED** |
| Threaded rod assembly awkward | **CONFIRMED** |
| Guide rail mounting incomplete | **CONFIRMED** |
| Part count high | **CONFIRMED** |
| Tolerance stack-up acceptable | **LIKELY** |
| PETG shrinkage manageable / warping risk on flats | **CONFIRMED** |
| Support removal needed for trays and duct | **CONFIRMED** |
| Middle side panel exceeds aspect ratio limit | **CONFIRMED** |
| Assembly sequence missing | **CONFIRMED** |
| Side panel mounting interface missing | **BLOCKER** |
| Rail mounting interface missing | **BLOCKER** |
| BOM lacks quantities | **BLOCKER** |

---

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
