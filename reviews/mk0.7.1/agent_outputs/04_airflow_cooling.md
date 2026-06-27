# Airflow and Cooling Review

## Executive Summary

The mk0.7.1 Homelab Modular Tower uses a vertical chimney airflow scheme: bottom 120 mm intake → central tower volume → vertical module stack → top 120 mm exhaust. The Mini PC has a dedicated side airflow duct. The Rear Service Spine and Power Bus occupy the rear zone and must not obstruct the central flow.

This review finds **multiple confirmed design-level airflow concerns** that affect the tower's ability to cool its modules. None of the findings require CFD to identify; they are discoverable through dimensional stack analysis, geometric obstruction checks, and cross-referencing of the assembly placement against the module placeholders.

mk0.7.1 makes **two airflow-related improvements** over mk0.7:

1. **Temperature sensor review markers are now placed at y = 0** (central airflow), correcting the mk0.7 placement in the stagnant rear zone.
2. **A top exhaust fan placeholder is now added to the assembly**, clarifying the exhaust-side intent.

However, the underlying structural airflow issues from mk0.7 remain **unresolved** in mk0.7.1.

**Top-level findings:**

1. **Bottom intake openness is acceptable** (≈ 86 % open area ratio vs. fan face) **but the filter hardware is not integrated into the assembly** and the filter rails are on the wrong side of the grille for a bottom intake.
2. **Basement blockage is minimal** — the base hole (134 mm) and frame opening (162 mm) are both larger than the fan air opening (112 mm), so they do not add constriction.
3. **Fan placement fits within the 32 mm foot height** but leaves only **7 mm table clearance** and no provision for a filter beneath the fan.
4. **Tray base ventilation slots are completely blocked by the devices** on every module. This is the single most critical airflow design flaw. Air must flow around the modules, not through them.
5. **Mini PC duct is a placeholder geometry** that does not connect to the Mini PC placeholder. It is 58 mm wide vs. a 145 mm wide device and is open at both ends with no side port.
6. **Rear Service Spine does not block the central 112 mm fan column** but it blocks the rear bypass path, which is one of the two main routes around the modules.
7. **Top exhaust fan placeholder is now present in the assembly**, but the **7 mm gap above the top module remains a narrow constriction**.
8. **UPS/Power tray has the largest thermal mass at the bottom** (good) but its vent slots are blocked by the battery.
9. **Temperature sensor placement is now in the central airflow** — all three points are at y = 0, which is a confirmed improvement over mk0.7.

---

## Bottom Intake Openness

**Grade: CONFIRMED (acceptable without filter; UNCERTAIN with filter)**

### Geometry

| Component | Hole / Opening Size | Area (mm²) |
|---|---|---|
| Fan air opening (reference) | 112 mm dia | 9 852 |
| Bottom grille hole | 120 mm dia | 11 310 |
| Grille bars (10 × 102 × 3, minus 25 × 3 × 3 overlap) | — | 2 835 |
| **Grille net open area** | — | **8 475** |
| Base stability hole | 134 mm dia | 14 095 |
| Bottom structural frame opening | 162 × 162 mm | 26 244 |
| BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO threshold | 0.58 of 112 mm = 65.0 mm dia | 3 318 |

### Analysis

The bottom fan grille is a 190 × 190 × 4 mm plate with a 120 mm through-hole and ten 3 mm × 102 mm protective bars (five in X, five in Y). The bar overlap area is 25 × 3 × 3 = 225 mm². Net open area:

- Bar total = 5 × 306 + 5 × 306 − 225 = **2 835 mm²**
- Grille open area = π × 60² − 2 835 = **8 475 mm²**
- Ratio vs. 112 mm fan face = 8 475 / 9 852 = **0.860**
- Ratio vs. 120 mm grille hole = 8 475 / 11 310 = **0.749**

Both ratios comfortably exceed the review threshold of 0.58. The **bottom intake openness is CONFIRMED adequate** for the bare grille.

### Filter Issue

The `bottom_filter_frame` (138 × 138 × 3 mm, 112 mm hole) and `bottom_filter_retainer` are **not placed in the assembly** (`tower_assembly.py` does not instantiate them). `KNOWN_LIMITATIONS.md` explicitly states:

> Filter material, pressure drop, and service position remain unresolved.

If a filter is added, its open area ratio depends on the filter mesh. A typical 40 PPI polyurethane foam filter has an open area ratio of 0.75–0.85, which would drop the overall intake ratio to ≈ 0.65–0.73, still above 0.58. A finer filter (e.g., HEPA) could drop below the threshold. **This is UNCERTAIN until a filter material is specified and its pressure drop/open area is measured.**

### Filter Rail Placement Issue

The `bottom_fan_grille` is placed at `BOTTOM_FAN_PANEL_Z = −8.5` (below the base plate). The filter rails are added on the **+Z face** of the grille (`cfg.FAN_GRILLE_THICKNESS / 2 + cfg.FILTER_RAIL_HEIGHT / 2`). For a bottom intake, air enters from below the base. The filter should be on the **intake side** (below the fan). The current geometry places the filter rails **above** the grille, inside the tower, on the wrong side of the airflow. **This is a design error.**

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
| Bottom fan grille | −10.5 … −6.5 | 4 | 120 mm dia − bars |
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
Bottom fan grille (4 mm) ............................. z = −10.5 … −6.5
Bottom structural frame (7 mm) ....................... z = −3.5 … +3.5
```

### Clearance findings

1. **Fan-to-table clearance: 7 mm**. A 120 mm × 25 mm fan sits with its bottom face 7 mm above the table. This is the minimum recommended for unrestricted intake. It is adequate for a bare fan but **insufficient for a filter placed below the fan**. A typical 3–5 mm foam filter would leave only 2–4 mm, which is marginal.

2. **Fan-to-base clearance: 0 mm**. The fan top is flush with the base bottom (`z = −14.0`). The cartridge rails extend 5 mm into the base hole. This is correct — the fan is clamped against the base by the cartridge.

3. **Total occupied height from table to base top: 42 mm**. The feet are 32 mm; the base is 10 mm. The fan (25 mm) plus cartridge (8 mm) occupies 33 mm of the 32 mm foot height, but the cartridge overlaps the fan top, so the actual physical stack is 25 + 3 = 28 mm of fan below the base, plus 5 mm of rails inside the base. The numbers work.

4. **Filter placement is unresolved**. There is no physical space for a filter frame (3 mm) or retainer (4 mm) below the base within the 32 mm foot envelope, unless the fan is raised or the feet are taller. The `KNOWN_LIMITATIONS.md` confirms this requires print-fit testing.

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

The module stack occupies the central 170 × 176 mm cross-section inside the 162 × 162 mm frame opening. The tray width (170 mm) is **larger** than the frame inner opening (162 mm). The trays fit because of 18 × 18 mm corner clearances (`cut_structural_clearances`), but the side walls are at x = ±83.5, which is **outside** the frame opening at x = ±81. This means the tray side walls are in the gap between the frame rails and the tower outer wall.

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
- Raise devices on standoffs so air can pass through the slots beneath the device.
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

### KNOWN_LIMITATIONS confirmation

`KNOWN_LIMITATIONS.md` explicitly states:

> Mini PC duct geometry remains a placeholder and is not matched to measured Mini PC vents.

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
| Top module (Mini PC) slot top | ≈ 315.5 | — |
| Gap to top frame | 315.5 … 321.5 | ~7 mm vertical gap |
| Top structural frame | 321.5 ± 3.5 | 162 × 162 mm |
| Top fan grille | 325.0 … 329.0 | 120 mm dia − bars |
| Top fan placeholder | 329.0 … 354.0 | 120 mm dia |

### Gap analysis

The module stack top is at approximately 315.5 mm. The top structural frame bottom is at 318.0 mm. The vertical gap is **~7 mm** (frame center at 321.5 minus the module stack top).

The air flowing up the tower must pass through this 7 mm gap above the top module before reaching the top frame opening. The 7 mm gap area (perimeter of the module stack × 7 mm) is approximately:

- Module stack perimeter ≈ 2 × (170 + 176) = 692 mm
- Gap area ≈ 692 × 7 = **4 844 mm²**
- Fan air opening area = 9 852 mm²
- Gap-to-fan area ratio = 4 844 / 9 852 = **0.49**

This is a **significant constriction**. The air must accelerate by a factor of ~2 to pass through the gap. This creates a pressure drop that reduces the overall chimney flow.

### Top frame, grille, and fan

The top frame opening is 162 × 162 mm, which is larger than the 112 mm fan opening. The top grille has the same bar pattern as the bottom grille, with an open area ratio of ≈ 0.80. The top fan placeholder is now present in the assembly at `TOP_FAN_PLACEHOLDER_Z = 341.5`, sitting directly above the grille. This clarifies the exhaust intent but does not remove the 7 mm gap constriction below.

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
- Front: battery front is at y = −25 − 27.5 = −52.5. Tray front is at y = −92. Gap = 39.5 mm.
- Right: battery right edge at x = −38 + 62.5 = +24.5. Tray right at x = 85. Gap = 60.5 mm.

The air has ample space to flow around the battery. The UPS module's thermal performance is **likely acceptable** due to its position at the bottom of the stack, but the blocked vent slots are a design inconsistency.

### Other heat sources

The UPS component zones (board, BMS, DC-DC, fuse, terminals) are all small blocks (< 60 × 40 mm) scattered around the tray. They do not significantly obstruct airflow. The DC-DC and terminal blocks are at the rear (y = 58, 62), near the spine. Their heat may accumulate in the rear corner.

**Recommendation:** The UPS module should be monitored during prototype testing. If the battery or DC-DC runs hot, consider adding side vents to the tray walls or raising the battery on standoffs.

---

## Temperature Sensor Placement

**Grade: CONFIRMED — now in the central airflow, improved from mk0.7**

### Sensor locations

| Sensor | Coordinates (x, y, z) | Location | Assessment |
|---|---|---|---|
| 1 | (−42.0, 0.0, 90.0) | z = 90: inside UPS module. y = 0: central chimney. | Central airflow |
| 2 | (42.0, 0.0, 215.0) | z = 215: inside SSD Expansion / Raspberry Pi / MikroTik range. y = 0: central chimney. | Central airflow |
| 3 | (0.0, 0.0, 310.0) | z = 310: near top exhaust. y = 0: central chimney. | Central airflow |

### Analysis

All three sensors are now at **y = 0.0**, which is the **centerline of the main chimney flow**. In mk0.7, all three sensors were at y ≈ 68–70 mm, which placed them at the stagnant front face of the Rear Service Spine. The mk0.7.1 correction is a **confirmed improvement**.

The central airflow is the primary path for the bottom-to-top chimney effect. Sensors at y = 0 will measure the temperature of the air that is actually cooling the modules, not the stagnant rear zone.

### Recommendation

The y = 0 placement is correct. For future revisions, consider adding:
- A fourth sensor at the **inlet** (y = 0, z ≈ 10) to measure intake temperature and compute delta-T.
- A fifth sensor at the **Mini PC rear** (y ≈ 50, z ≈ 270) to monitor the highest-priority device.

---

## Blockers

This section lists items that must be resolved before the design can be considered thermally validated.

| # | Blocker | Grade | Evidence |
|---|---|---|---|
| 1 | **Tray base vent slots are blocked by all devices** | CONFIRMED | Every device placeholder footprint exceeds the vent grid area; devices sit flush on the 3 mm base. `carriages.py` `cut_vent_slots` + `modules.py` device placeholders. |
| 2 | **Mini PC duct is a non-functional placeholder** | CONFIRMED | Duct is open at both ends with no side port to the Mini PC. Duct width (58 mm) << Mini PC width (145 mm). `KNOWN_LIMITATIONS.md` line 24. |
| 3 | **Filter hardware is not in the assembly and rails are on wrong side** | CONFIRMED | `bottom_filter_frame` / `retainer` not in `tower_assembly.py`. Filter rails on +Z face of grille, which is inside the tower for a bottom intake. `cooling.py` lines 29–36. |
| 4 | **Top exhaust fan is only a placeholder** | CONFIRMED | Top fan placeholder is present in `tower_assembly.py` but has no mounting cartridge, no wire routing, and no validated system curve. `KNOWN_LIMITATIONS.md` line 27. |
| 5 | **Top gap above module stack is only ~7 mm** | CONFIRMED | Module stack top at z ≈ 315.5; top frame at z = 321.5. Gap ≈ 7 mm. `config.py` STACK_START_Z + TRAY_STACK. |
| 6 | **No CFD or physical flow testing** | CONFIRMED | `CALCULATIONS.md` line 8 and `KNOWN_LIMITATIONS.md` line 9 both state this explicitly. |

**Note:** The mk0.7 blocker "Temperature sensors are in stagnant rear zone" is **resolved** in mk0.7.1 and has been removed from this list.

---

## Recommendations

### P1 — Must fix before prototype

1. **Redesign tray base ventilation**. The current "solid base with central slots" approach fails because devices sit on the base. Options:
   - **Preferred:** Add a grid of raised standoffs (e.g., 4 mm tall posts) under each device so air can pass through the slots beneath the device.
   - Alternative: Move vent slots to the tray side walls (not the base) so they are not blocked.
   - Alternative: Replace the solid base with a lattice or honeycomb structure.

2. **Integrate Mini PC duct with actual device geometry**. The placeholder duct must be replaced with a design based on the real Mini PC's intake vent location and size. The duct must have a side outlet that mates with the intake.

3. **Fix temperature sensor placement** — this is already done in mk0.7.1. Preserve the y = 0 placement in future revisions.

### P2 — Should fix before production

4. **Increase top gap above module stack**. The 7 mm gap is a flow bottleneck. Consider raising the top frame by 5–10 mm or shortening the top module by one unit (but this affects the modular standard).

5. **Resolve filter placement**. Either:
   - Add a filter slot **below** the fan (between fan and table), or
   - Raise the fan to make room for a filter below it, or
   - Increase foot height to 40 mm to accommodate fan + filter.

6. **Add rear ventilation for the Mini PC**. The Mini PC rear is only 8 mm from the spine. Consider a cutout or channel in the spine to allow hot air from the Mini PC rear to escape upward.

7. **Add a top exhaust fan cartridge**. The bottom fan has a cartridge (`make_bottom_fan_cartridge`) for retention and service. The top fan placeholder does not. Add a top cartridge with matching mounting and service pull geometry.

### P3 — Nice to have

8. **Add side panel ventilation** aligned with the module side gaps to create a secondary cross-flow path. This would reduce reliance on the narrow chimney gap.

9. **Consider UPS battery thermal isolation**. If the battery runs hot, consider a separate airflow path for the UPS module to prevent it from preheating the upstream air for other modules.

10. **Document the pressure drop budget**. Once a filter material and fan model are selected, create a simple pressure-drop estimate (grille + filter + module stack + top gap) to ensure the fan can overcome the system resistance. This is not CFD — it is a standard fan curve vs. system curve calculation.

---

## References

| File | Line(s) | Relevance |
|---|---|---|
| `cad/config.py` | 403–458 | Cooling parameters, duct dimensions, filter dimensions, sensor points |
| `cad/config.py` | 338–339, 356–359 | Base stability fan clearance, foot height, Z positions |
| `cad/config.py` | 606 | Temperature sensor points at y = 0 |
| `cad/config.py` | 619–620 | Top fan placeholder and panel Z positions |
| `cad/parts/cooling.py` | 8–37, 94–117 | Grille, filter frame, filter retainer geometry |
| `cad/parts/cooling.py` | 128–146 | Mini PC duct placeholder (still open at both ends) |
| `cad/parts/feet.py` | 102–110, 133–160 | Base frame, ribs, intake cut, foot positions |
| `cad/parts/carriages.py` | 8–15, 189–236 | Tray vent slot geometry, module tray creation |
| `cad/parts/modules.py` | 10–121 | Device placeholders sitting on tray bases |
| `cad/parts/frame.py` | 10–43 | Frame ring dimensions, inner opening |
| `cad/parts/review.py` | 21–30 | Airflow arrows and temperature sensor bosses |
| `cad/parts/service_spine.py` | 64–171 | Rear spine dimensions, channel, windows |
| `cad/assembly/tower_assembly.py` | 237–241 | Top fan placeholder added in mk0.7.1 |
| `cad/assembly/tower_assembly.py` | 228–242 | Assembly placement — filter parts still absent |
| `revisions/mk0.7.1/CALCULATIONS.md` | 24–26 | Temperature marker positions moved to y=0 |
| `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` | 22–28 | Deferred airflow blockers confirmed by this review |
| `revisions/mk0.7.1/review_package/analysis/part_dimensions.csv` | Multiple | Exported bounding boxes confirming Z-stacks and overlaps |
