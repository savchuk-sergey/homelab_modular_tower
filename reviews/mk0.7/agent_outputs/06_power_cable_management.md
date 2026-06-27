# Power and Cable Management Review

**Reviewer:** Power and Cable Management Reviewer (Agent)  
**Revision:** mk0.7  
**Date:** 2025-06-28  
**Scope:** Power bus panel, power bus cover, strain relief, connector zones, rear service spine cable routing, cable exit alignment, DC UPS integration, mains isolation, fuse protection, fan cable routing.

---

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
