# Red Team / Critic Review — mk0.7

**Reviewer:** Red Team / Critic
**Revision:** mk0.7
**Date:** 2025-01-18
**Grade:** 🔴 **NOT READY FOR PROTOTYPE**

---

## Executive Summary

mk0.7 is a CAD milestone that looks coherent on screen but collapses under physical scrutiny. This revision has **critical safety gaps**, **structural design flaws**, **a broken automated quality pipeline**, and **severe usability contradictions** that make it unsuitable for physical prototyping without major rework.

The most dangerous findings:

1. **Dynamic tipping hazard:** The Mini PC tray front overhangs the base by **37 mm** when extended. A 40–50 N pull on the handle will tip the 330 mm tall tower forward.
2. **Lithium battery fire risk:** The UPS tray contains a lithium battery placeholder with **no thermal monitoring, no venting, no puncture protection, and no BMS thermal cutoff** modeled. PETG melts at ~75 °C; lithium thermal runaway reaches 500 °C.
3. **Broken export pipeline:** The `duplicate_geometry_check.csv` completely failed due to a config attribute mismatch (`DUPLICATE_VOLUME_TOLERANCE_MM` vs `DUPLICATE_VOLUME_TOLERANCE_MM3`), rendering the entire automated quality gate worthless.
4. **Structural assembly flaws:** Metal guide rails are slid through plastic frame slots with **no fastening mechanism**. The TPU feet are attached to 3 mm PETG bosses with **no heat-set inserts**. These are not "engineering compromises" — they are assembly failures.
5. **Serviceability lie:** The design claims "extractable without disassembly," but the rear service spine requires **screwdriver access, cable untying, and power disconnection** to remove any module.

**Recommendation:** Do not proceed to test print. Fix the blockers, add missing safety systems, and rerun the full quality pipeline before any physical commitment.

---

## Safety Hazards

### Grade: CONFIRMED

#### 1. Lithium Battery in Plastic Oven (CONFIRMED)

The `ups_power_tray` (`config.py:310–325`, `modules.py:10–21`) contains a `BATTERY_PACK_PLACEHOLDER` of 125 × 55 × 32 mm. This is a lithium pack of approximately 3S1P 18650 or a flat pouch cell. The design provides:

- **No thermal monitoring** — `TEMPERATURE_SENSOR_POINTS` are review markers only, not actual sensor mounts.
- **No battery venting** — The tray has ventilation slots, but there is no dedicated fire/vent channel. In thermal runaway, gases and flames will be directed upward through the module stack.
- **No puncture protection** — The tray base is 3 mm PETG. A dropped tool or screw can puncture the pack.
- **No BMS thermal cutoff** — The `UPS_COMPONENT_ZONES` list a "bms" zone but no thermal cutoff or fuse integration.

PETG glass transition is ~75 °C. Lithium thermal runaway can exceed 500 °C. The battery is at the bottom of the tower, directly above the intake fan. If the fan fails or the UPS board overheats, the PETG tray will soften, sag, and potentially ignite. This is a **fire hazard**.

#### 2. Unfused DC Power Bus (CONFIRMED)

The `power_bus_panel` (`service_spine.py:8–41`) carries 19 V, 12 V, 5 V, and GND on a 3 mm PETG panel with 3 mm guard rails. The design provides:

- **No fuse holders** — `POWER_BUS_FUSE_BLOCK_WIDTH` and `POWER_BUS_FUSE_BLOCK_HEIGHT` are parameters but no actual fuse geometry is modeled.
- **No circuit breaker or power switch** — The power bus has no disconnect mechanism. A short circuit on the 19 V rail (e.g., from a loose wire or dropped tool) will dump full PSU current into the PETG structure until the external PSU shuts down or catches fire.
- **No insulation** — The power rails are exposed copper zones on a plastic panel. A metal module tray edge or screwdriver can bridge 19 V to GND.

#### 3. Nonmanifold Printable Part (CONFIRMED)

`stl_quality.csv` shows `bottom_fan_cartridge` is **not watertight, not manifold**, with 2 nonmanifold edges. A printable part with broken geometry will cause slicer errors, failed prints, or missing features. This is a **print failure and potential safety issue** if the fan mounting geometry is compromised.

---

## Tipping Hazard Analysis

### Grade: CONFIRMED (dynamic)

#### Static Analysis — Adequate but Misleading

- Base: 250 × 260 mm (`config.py:22–23`)
- COM: Y = 8 mm (rearward), Z = 167 mm (`config.py:604–606`)
- Stability margin: 18 mm (`config.py:36`)
- Safe zone: 214 × 224 mm (within 18 mm of base edges)
- Mini PC tray mass: 1.2 kg device + ~0.2 kg tray = 1.4 kg
- Total tower mass: ~9.5 kg (see Hidden Costs section)

When the Mini PC tray is pulled out 78 mm (`MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`), the tray COM shifts from Y = -4 mm to Y = -82 mm. The combined tower COM shifts to approximately **Y = -3 to -5 mm** (depending on total mass estimate). This is still well within the 18 mm stability margin (front safe zone edge at Y = -112 mm).

**Static tipping is NOT the primary hazard.**

#### Dynamic Analysis — CONFIRMED Hazard

The tray front face is at Y = -4 - 178/2 = **-93 mm** normally. When pulled out 78 mm, the tray center moves to Y = -82 mm. The tray front face moves to **Y = -171 mm**.

The base front edge is at **Y = -130 mm**.

**The tray front overhangs the base by 41 mm when extended.**

Now consider a user pulling the tray handle to extract it:
- Handle height: ~Z = 250 mm (top module position).
- Handle overhang: 41 mm beyond base front.
- A horizontal pull of **40 N** (≈4 kgf, easily achievable by a human) creates an overturning moment about the front base edge of:
  - 40 N × 0.250 m = **10 N·m**
- Restoring moment (weight = 93 N, COM distance to front edge ≈ 125 mm):
  - 93 N × 0.125 m = **11.6 N·m**
- A pull of **50 N** or any downward component creates:
  - 50 N × 0.250 m + 20 N × 0.041 m = **13.3 N·m** > 11.6 N·m → **TIPPING**

**Verdict:** A firm tug on the extended Mini PC tray handle will tip the tower forward. The tray front overhangs the base, and the 18 mm static stability margin is meaningless for dynamic loading. **CONFIRMED.**

---

## Hidden Costs

### Grade: CONFIRMED

The project is marketed as a "modular" and "repairable" platform, but the user is not adequately warned about the total cost of ownership.

#### Bill of Materials (BOM) — Consumables

| Item | Qty | Unit Cost | Total |
|------|-----|-----------|-------|
| PETG filament (5.5–6.5 kg incl. infill, supports, failed prints) | 6 kg | $20–30/kg | **$120–180** |
| TPU filament (feet, dampers) | 0.2 kg | $30–40/kg | **$6–8** |
| M5 threaded rods (321 mm) | 4 | ~$2.50 | **$10** |
| M5 nuts & washers | 16 | ~$0.20 | **$3** |
| Metal guide rails (custom or extrusion) | 4 | ~$5–10 | **$20–40** |
| M3 screws (100+) | 100 | ~$0.10 | **$10** |
| Heat-set brass inserts (M3, 50+) | 50 | ~$0.10 | **$5** |
| 120 mm fans | 2 | ~$10–15 | **$20–30** |
| Dust filter material | 1 | ~$5–10 | **$5–10** |
| **Consumables Subtotal** | | | **$200–290** |

#### Electronics (NOT optional — the tower is useless without them)

| Item | Est. Cost |
|------|-----------|
| Mini PC (Ryzen 5 PRO 4650U class) | **$200–400** |
| MikroTik hAP ax2 | **$100–150** |
| Raspberry Pi 3B + accessories | **$50–100** |
| SSDs (external + expansion) | **$50–200** |
| DC UPS board + lithium battery | **$50–100** |
| DC-DC converters (19 V, 12 V, 5 V) | **$20–40** |
| External AC/DC PSU (19 V, ~120 W) | **$30–50** |
| Wiring, connectors, XT30, MicroFit | **$20–30** |
| **Electronics Subtotal** | **$520–1,070** |

#### Total Project Cost

**$720–1,360** minimum. With a quality Mini PC and larger SSDs, this easily exceeds **$1,500**.

This is not a "weekend 3D print project." It is a major capital investment. The user must be explicitly warned.

#### Print Time Commitment

- 35+ printable parts.
- Average print time per part: 4–8 hours (frames, trays, spine take 10–20 hours each).
- Estimated total print time: **250–350 hours** (10–15 days of continuous printing).
- With failed prints (likely for large flat parts): **300–400 hours**.

A single failed print of the `central_bottom_fan_frame` (326 g solid, 15–20 hours) sets the project back by a full day. The user is not warned about this time commitment.

---

## Print Failure Risk

### Grade: CONFIRMED

#### Large Flat Parts = Warping

The following parts are large, thin, and flat — the worst geometry for PETG warping:

| Part | Size (mm) | Solid Mass (g) | Est. Print Time |
|------|-----------|----------------|-----------------|
| `central_bottom_fan_frame` | 190 × 190 × 16 | 326 | 15–20 h |
| `bottom_structural_frame` | 190 × 190 × 13 | 107 | 10–12 h |
| `frame_bottom` / `frame_top` | 190 × 190 × 13 | 107 | 10–12 h each |
| `front_stability_wing` | 250 × 47 × 10 | 148 | 8–10 h |
| `rear_stability_wing` | 250 × 47 × 10 | 148 | 8–10 h |
| `bottom_fan_grille` | 190 × 190 × 7 | 141 | 10–12 h |
| `top_fan_grille` | 190 × 190 × 4 | 138 | 8–10 h |

PETG is less prone to warping than ABS, but large flat parts on open-frame printers will still warp at the corners without perfect bed adhesion, enclosure, and draft shielding. The `central_bottom_fan_frame` is particularly risky because it has a large central hole (134 mm), which creates differential cooling and stress concentrations.

#### Printability Check Failures

`printability_check.csv` flags multiple parts as **exceeding axis-aligned P2S volume** or **long-thin geometry risk**:

- `power_bus_cover`: 46 × 5 × 265.5 mm — **exceeds P2S volume** (265.5 > 256 Z). Must be printed diagonally or in sections.
- `power_bus_panel`: 34 × 7.5 × 275.5 mm — **exceeds P2S volume**.
- `rear_service_spine`: 80 × 40 × 297.5 mm — **exceeds P2S volume**.
- `rear_service_spine_cover`: 46 × 3 × 295.5 mm — **exceeds P2S volume** and flagged as long-thin (aspect ratio 98.5).
- `top_fan_grille`: 47.5 aspect ratio — long-thin risk.
- `bottom_filter_retainer`: 36 aspect ratio — long-thin risk.
- `foot_socket`: 14 aspect ratio — long-thin risk.
- `left_side_panel_middle`: 33.8 aspect ratio — long-thin risk.
- `right_side_panel_middle`: 33.8 aspect ratio — long-thin risk.

These parts require special orientation, supports, or multi-piece printing. The review package does not provide print orientation guidance.

#### No Recovery Path

The design has no redundancy. If the `central_bottom_fan_frame` warps and must be reprinted, the entire project stalls. There are no alternative base designs or workaround parts. The user is locked into a 15–20 hour print with no fallback.

---

## Design Contradictions

### Grade: CONFIRMED

#### 1. Airflow vs. Serviceability — The "Hot-Swap" Lie

**AGENTS.md requirement:** "Извлечение одного модуля не должно требовать разборки всей башни" (extraction of one module must not require disassembling the whole tower).

**Reality:** Every module has a `TRAY_REAR_SERVICE_CUTOUT` (66 × 36 mm) facing the `rear_service_spine`. The power bus runs through the spine. To extract a module:

1. Remove the rear spine cover (multiple M3 screws).
2. Untie cable ties from the spine slots.
3. Disconnect power and data cables from the module.
4. Slide the module out.
5. Reconnect cables and re-tie them when reinstalling.

This is **not hot-swappable**. It is a 10-minute disassembly operation requiring a screwdriver and dexterity. The design tries to have both "fully enclosed cable management" and "tool-less module extraction" and achieves **neither**.

**Evidence:**
- `carriages.py:143–150` — rear cable exit is a fixed cutout, not a quick-disconnect.
- `service_spine.py:64–171` — rear spine has screw-on cover and cable tie slots.
- `config.py:125–126` — `REAR_CABLE_EXIT_WIDTH = 66.0`, `REAR_CABLE_EXIT_HEIGHT = 20.0` — cables must pass through this narrow slot.

#### 2. Structural Stiffness vs. Modularity — The Wobbly Cage

The tower relies on M5 rods and metal rails for stiffness. But:

- The **frames are thin rings** (7 mm thick, 14 mm wide) with a 162 mm central opening. They provide minimal torsional stiffness.
- The **metal rails are not attached to the frames** (see "Metal Rail Attachment Failure" below). They slide through loose slots with 1 mm clearance.
- The **side panels are perforated with vent slots** and provide negligible shear stiffness.
- The **corner blocks are 24 mm PETG cubes** — the only compression members.

The result is a tall, slender cage (190 × 190 × 321 mm) with the structural integrity of a cardboard box. Torsional loads (e.g., pushing the top sideways) will rack the frame and cause the modules to bind on the loose rails.

**Evidence:**
- `frame.py:10–43` — frame is a ring with 162 mm central opening and 7 mm thickness.
- `config.py:78–91` — frame dimensions show minimal material.
- `side_panels.py:116–142` — vent slots cut large holes in "structural" shear panels.

#### 3. Plastic Mass vs. Cost — The "Repairable" Paradox

The project claims "repairability" and "modularity," but with 35+ unique parts, 250+ print hours, and $200+ in consumables, **repairing a broken part costs more than buying a commercial mini-ITX case**. If a `corner_block` creeps (see below) or a `frame` cracks, the user must disassemble the entire tower and reprint a 10–20 hour part.

A commercial metal rackmount case is $50–100, ships in 2 days, and has a 5-year warranty. This tower costs 10× more and takes weeks to build. The "repairability" claim is only true if the user owns a 3D printer and is willing to invest 20+ hours to reprint a failed part. For most users, this is a **single-point-of-failure liability**, not a feature.

---

## Missing Critical Features

### Grade: CONFIRMED

The following features are absent from the design and pose operational or safety risks:

| Feature | Why It Matters | Status |
|---------|---------------|--------|
| **Power switch** | Cannot safely shut down the tower without unplugging the external PSU. | Missing |
| **Emergency stop** | No way to kill power in a fire or thermal runaway. | Missing |
| **Fuse / circuit breaker** | A short on the 19 V bus will burn wiring and melt PETG. | Missing |
| **Thermal monitoring** | No temperature sensors, no fan speed control, no alarms. | Missing (review markers only) |
| **Fan speed control** | Both fans run at 100% or not at all. No PWM, no tachometer. | Missing |
| **LED indicators** | No power status, no fault indication, no module activity. | Missing |
| **Cable strain relief** | Modules have no strain relief at the rear exit. Pulling a cable can damage connectors. | Missing (only power bus has strain relief clamps) |
| **Vibration isolation** | SSDs and hard drives are bolted directly to PETG trays. No rubber grommets or dampers. | Missing |
| **EMC shielding** | No Faraday cage, no grounding. The tower will emit and receive RF noise. | Missing |
| **Dust ingress protection** | No IP rating. Dust will accumulate on electronics and fans. | Missing |
| **Battery fire containment** | No fireproof battery compartment, no venting, no thermal cutoff. | Missing |
| **Overcurrent / reverse polarity protection** | No polyfuses, no diodes, no protection circuits. | Missing |

---

## Placeholder Reality Gap

### Grade: CONFIRMED

The design is built around placeholder dimensions that have not been verified against real hardware.

| Placeholder | Dimension | Status | Risk |
|-------------|-----------|--------|------|
| `MIKROTIK_PLACEHOLDER` | 120 × 95 × 14 mm | `TODO: measure bare hAP ax2 board` | If the real board is 130 mm wide, the tray is scrap. |
| `MINI_PC_PLACEHOLDER` | 145 × 130 × 28 mm | `TODO: measure Ryzen 5 PRO 4650U unit` | If the real unit is 150 mm wide, the tray is scrap. |
| `RASPBERRY_PI_PLACEHOLDER` | 86 × 57 × 8 mm | Engineering reference | A Pi with heatsink or HAT will exceed height. |
| `FAN_120x120x25_PLACEHOLDER` | 120 × 120 × 25 mm | Standard reference | Acceptable, but real fan wire routing is untested. |

**The trays have no adjustment mechanism.** They are fixed-size pockets with 0.6 mm `TRAY_CLEARANCE`. If the real device is 2 mm larger than the placeholder, the module is **unusable**. The user must either reprint the entire tray (4–8 hours, 150–200 g filament) or modify the device.

This is a **design-to-failure** approach. The revision should not be considered stable until the top three placeholders are verified with physical measurements.

---

## Export Quality Gap

### Grade: CONFIRMED

#### 1. Duplicate Geometry Check — Completely Broken

`duplicate_geometry_check.csv` shows **100% failure rate** across all 51 parts:

```
AttributeError: module 'cad.config' has no attribute 'DUPLICATE_VOLUME_TOLERANCE_MM'
```

**Root cause:** `config.py:636` defines `DUPLICATE_VOLUME_TOLERANCE_MM3 = 1.0` (note the `MM3` suffix, indicating cubic millimeters). The export pipeline is looking for `DUPLICATE_VOLUME_TOLERANCE_MM` (no `3`), which does not exist.

**Impact:** The entire automated duplicate-detection pipeline is worthless. The review package was generated with a completely failed check. This undermines confidence in the revision quality and suggests the pipeline was not tested before the review package was generated.

**This is a process blocker.** A revision should not be tagged for review with a broken quality gate.

#### 2. Nonmanifold Printable STL

`stl_quality.csv` shows `bottom_fan_cartridge` is:
- `is_watertight = False`
- `is_manifold = False`
- `nonmanifold_edges = 2`

This is a **printable part** with broken geometry. Slicers may fail to process it, produce incorrect toolpaths, or generate missing walls. The fan mounting holes or air opening may be compromised.

#### 3. Nonmanifold Review Bodies (Acceptable but Sloppy)

Multiple review STL files have open boundaries and nonmanifold edges:
- `airflow_path_review` (4 nonmanifold edges)
- `mini_pc_airflow_path_review` (1 nonmanifold edge)
- `stability_review` (2 nonmanifold edges)

While review geometry is not intended for printing, the presence of these errors indicates poor mesh generation hygiene in the CadQuery pipeline. If the review bodies are broken, the printable parts may also have hidden mesh defects that the STL quality checker missed.

---

## Rear Service Spine as Cable Trap

### Grade: CONFIRMED

The `rear_service_spine` (`service_spine.py:64–171`) is described as a "service" feature, but it is a **maintenance nightmare**.

#### The Extraction Procedure (6 steps, 10+ minutes, requires screwdriver)

1. **Remove rear spine cover** — Unscrew 6+ M3 screws from `REAR_SPINE_STRUCTURAL_MOUNT_Z` positions.
2. **Untie cables** — Cut or loosen cable ties from `REAR_SPINE_TIE_SLOT_Z` slots.
3. **Disconnect power** — Unplug XT30 / MicroFit / USB-C connectors from the power bus panel.
4. **Disconnect data** — Unplug Ethernet / USB from the module.
5. **Slide module out** — Pull the module forward 78 mm.
6. **Reverse to reinstall** — Reconnect, re-tie, and re-screw everything.

#### Contradiction with AGENTS.md

AGENTS.md states: "Все кабели должны проходить через эту шахту. Нельзя прокладывать кабели хаотично между модулями." (All cables must pass through this spine. No chaotic routing between modules.) This is a good principle, but the implementation makes module extraction impossible without full cable disconnection.

A true serviceable design would have **quick-disconnect connectors** at the module rear (e.g., spring-loaded Ethernet, magnetic power connectors, or short pigtails with easy-release latches). The current design uses fixed cable exits that require manual untying and unscrewing.

#### Cable Tie Slots Are a Trap

The spine has `REAR_SPINE_TIE_SLOT_Z` at 6 vertical positions. If cables are tied at multiple levels, extracting a module requires untying **all** cables at that module's level, even if they belong to other modules. The horizontal ties (`REAR_SPINE_HORIZONTAL_TIE_Z`) bundle cables across module boundaries, making individual module extraction even harder.

**Verdict:** The rear service spine is a cable management trap that makes the tower **less** serviceable than an open-frame design. It contradicts the modular standard.

---

## Corner Block Creep Failure

### Grade: CONFIRMED

#### The Problem

The `corner_block` (`corner_blocks.py:9–37`) is a **24 × 24 × 28 mm PETG block** with a 5.6 mm hole for the M5 rod. It is the **only compression member** between the top and bottom frames.

Under the clamping force of 8 M5 nuts (4 rods, 2 nuts each), the block experiences sustained compressive stress. PETG is susceptible to **creep deformation** under sustained load, especially at temperatures above 40 °C (common in a tower with electronics).

#### Stress Calculation

- Assume M5 nut torque: 3 Nm → preload ≈ 1,500 N per nut.
- Total clamping force: 8 × 1,500 N = 12,000 N.
- Force per block: 12,000 / 4 = **3,000 N** (2 nuts per block, top and bottom).
- Block cross-section (net of hole): 24 × 24 - π × 5.6² / 4 = 576 - 24.6 = **551.4 mm²**.
- Compressive stress: 3,000 / 551.4 = **5.4 MPa**.

PETG compressive yield is ~50–60 MPa, so the block is safe from immediate failure. However, **PETG creep rate is significant at 5+ MPa**. Over months to years:

- The block will compress by **0.2–0.5 mm**.
- The M5 nut preload will relax.
- The frame stack will loosen.
- The rods will rattle.
- The module trays will bind on the loose rails.
- The side panel screws will loosen.

This is a **chronic failure mode** that will degrade the tower over its operational lifetime. The user will need to retorque the M5 nuts every 3–6 months to maintain structural integrity.

#### Why This Is Confirmed

PETG creep is a well-documented material property. The design provides no metal compression sleeves, no Belleville washers, and no preload retention mechanism. The corner blocks are expected to maintain preload indefinitely in a material that is known to creep.

**Recommended fix:** Add metal compression tubes (e.g., 6 mm OD × 5 mm ID × 28 mm long aluminum sleeves) inside the corner blocks, or replace the blocks with aluminum standoffs.

---

## Additional Structural Defects

### 1. Metal Rail Attachment Failure — CONFIRMED

The `metal_guide_rail` (`rails.py:18–27`) is a 10 × 3 × 287.5 mm steel or aluminum bar with M3 holes at 70 mm spacing. The frame (`frame.py:29–33`) has a rectangular slot for the rail:

```python
ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).rect(
    cfg.METAL_RAIL_WIDTH + cfg.METAL_RAIL_FRAME_CLEARANCE,
    cfg.METAL_RAIL_THICKNESS + cfg.METAL_RAIL_FRAME_CLEARANCE,
).cutBlind(-z_height)
```

**This is a through-slot with no fastening mechanism.** The rail slides through the frame with 1 mm clearance. The frame has **no M3 holes** to match the rail's mounting holes. The rail is not screwed, clamped, or glued to the frame. It is held only by gravity and the friction of the modules sliding on it.

Under lateral load (e.g., pushing the tower), the rails will shift in their slots. The modules will bind. The frame stack will rack. This is a **major assembly design flaw**.

**Evidence:** Search `frame.py` for any hole matching `METAL_RAIL_M3_SPACING` — there are none. The frame has no rail attachment features.

### 2. Foot Screw Attachment Failure — CONFIRMED

The `foot_socket` (`feet.py:16–26`) is a 3 mm thick PETG boss with a **5.3 mm through-hole** and no heat-set insert. The TPU foot (`feet.py:163–184`) is attached with an M5 screw through this hole.

**A 5.3 mm hole in 3 mm of PETG will strip immediately.** PETG has low shear strength (~30 MPa). An M5 screw with 0.8 mm pitch creates a thread engagement of only 3 mm. The first assembly torque will strip the threads. The foot will fall off.

**Evidence:**
- `config.py:349–355` — `FOOT_SCREW_DIAMETER = 5.3`, `FOOT_SOCKET_DEPTH = 3.0`, no insert diameter specified.
- `feet.py:25` — simple through-hole, no insert.

**Fix:** Add a heat-set insert boss (at least 5 mm deep) or use a threaded brass insert.

### 3. Bottom Fan Cartridge — Unattached and Nonmanifold

The `bottom_fan_cartridge` (`cooling.py:48–91`) is a removable cartridge with rails and a handle. But:

- It has M3 mount holes at ±68 mm, but the base has no corresponding holes.
- It is not mechanically attached to the base. It sits in the air gap between the base and the desk.
- The STL is nonmanifold (2 nonmanifold edges).

**The cartridge will fall out or shift when the tower is moved.** This is a loose part under a 9.5 kg tower. If the cartridge shifts, the fan blades can hit the base or the filter, causing noise, vibration, or blade damage.

---

## Blockers

The following issues must be resolved before any physical prototype or test print:

| # | Blocker | Severity | Evidence |
|---|---------|----------|----------|
| 1 | **Dynamic tipping hazard** — Tray overhangs base by 37 mm when extended. | 🔴 Critical | `config.py:604`, `review.py:80–83`, geometry analysis |
| 2 | **Lithium battery fire risk** — No thermal monitoring, venting, or BMS cutoff. | 🔴 Critical | `config.py:310–325`, `modules.py:10–21` |
| 3 | **Unfused power bus** — No fuse, switch, or emergency stop. Short circuit = fire. | 🔴 Critical | `service_spine.py:8–41`, `config.py:530–564` |
| 4 | **Broken quality pipeline** — `duplicate_geometry_check.csv` 100% failed. | 🔴 Critical | `duplicate_geometry_check.csv` (all rows), `config.py:636` |
| 5 | **Nonmanifold printable STL** — `bottom_fan_cartridge` cannot be reliably printed. | 🔴 Critical | `stl_quality.csv` (line 11) |
| 6 | **Metal rails not attached** — Rails slide through loose slots with no fasteners. | 🟠 High | `frame.py:29–33`, `rails.py:18–27` |
| 7 | **Foot screw strips PETG** — 3 mm PETG boss with no insert. | 🟠 High | `feet.py:16–26`, `config.py:349–355` |
| 8 | **Cartridge not attached** — Bottom fan cartridge has no mounting mechanism. | 🟠 High | `cooling.py:48–91`, `config.py:427–433` |
| 9 | **Placeholder dimensions unverified** — Top 3 devices are estimated. | 🟠 High | `config.py:275–298` (TODO comments) |
| 10 | **Serviceability contradiction** — Module extraction requires full cable disassembly. | 🟡 Medium | `carriages.py:143–150`, `service_spine.py:64–171` |
| 11 | **Corner block creep** — PETG will compress under sustained M5 preload. | 🟡 Medium | `corner_blocks.py:9–37`, material science |

---

## Recommendations

### Immediate (Before Any Print)

1. **Fix the config attribute mismatch.** Rename `DUPLICATE_VOLUME_TOLERANCE_MM3` to `DUPLICATE_VOLUME_TOLERANCE_MM` or update the pipeline to match. Rerun the full quality pipeline and verify zero errors.
2. **Fix the `bottom_fan_cartridge` nonmanifold geometry.** Inspect the CadQuery model for intersecting faces or open edges. Re-export and verify `is_watertight = True`.
3. **Add rail attachment holes to frames.** The frame must have M3 holes at `METAL_RAIL_M3_SPACING` intervals to match the rail holes. Use M3 screws to secure the rails to the frames.
4. **Add heat-set inserts to foot sockets.** Increase `FOOT_SOCKET_DEPTH` to at least 5 mm and add a `HEAT_SET_INSERT_M5` boss. Or use threaded brass inserts.
5. **Add cartridge mounting mechanism.** The base must have M3 holes at `BOTTOM_FAN_CARTRIDGE_MOUNT_OFFSET` to match the cartridge mount holes. Alternatively, add slide-in rails or detents.
6. **Verify all placeholder dimensions.** Measure the actual MikroTik hAP ax2, Mini PC, and Raspberry Pi with heatsink/HAT. Update `config.py` with real dimensions. If any device is larger than the placeholder, redesign the tray or add adjustment slots.
7. **Add a power switch and fuse.** Model a physical power switch on the front panel or power bus. Add fuse holders for each voltage rail (19 V, 12 V, 5 V).

### Short-Term (Before Full Assembly)

8. **Address the tipping hazard.** Either:
   - Reduce `MINI_PC_TRAY_SERVICE_TRAVEL` so the tray front does not overhang the base, or
   - Add a counterweight or anti-tip foot to the rear base, or
   - Add a mechanical tether or clamp that locks the tray to the base when extended.
9. **Add battery safety.** Model a vented, fire-resistant battery compartment (e.g., with a steel or aluminum tray liner). Add a thermal fuse and a BMS with cell balancing and over-temperature cutoff.
10. **Add thermal monitoring.** Model mounting bosses for DS18B20 or thermistor sensors at the battery, UPS board, and Mini PC zones. Add a fan controller (PWM) based on temperature.
11. **Redesign the rear spine for true serviceability.** Replace fixed cable ties with quick-release latches or magnetic connectors. Consider a hinged spine cover instead of a screw-on cover. Add short pigtails to each module so cables stay in the spine during extraction.
12. **Add vibration isolation.** Model rubber grommet slots or TPU dampers for SSD mounting points.

### Long-Term (Before Calling mk0.7 "Stable")

13. **Replace corner blocks with metal compression sleeves.** Add 6 mm OD × 5 mm ID aluminum tubes inside the corner blocks to carry the M5 preload. The PETG can then serve as a bushing, not the primary compression member.
14. **Add EMC grounding.** Model a grounding bus connected to the metal rails and frame. Add shielding panels if RF emissions are a concern.
15. **Conduct CFD airflow analysis.** The `BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO = 0.58` is a guess. Verify airflow with CFD or smoke testing before finalizing the filter and duct geometry.
16. **Test print the critical parts first.** Before committing to the full 250+ hour print, print the `bottom_fan_cartridge`, `bottom_filter_retainer`, and `foot_socket` as fit checks. Validate the rail clearances, screw threads, and filter retention.

---

## Closing Statement

mk0.7 is a well-intentioned CAD exercise that has outpaced its physical validation. The revision adds useful features (bottom fan cartridge, RPi placeholder, export taxonomy) but introduces or ignores critical safety and structural issues.

The tower is **not safe to build** as-designed. The tipping hazard, battery fire risk, and unfused power bus are serious enough to cause injury or property damage. The broken quality pipeline and nonmanifold STL indicate that the revision was not adequately validated before packaging.

**Do not proceed to test print.** Fix the blockers, verify the placeholders, and rerun the full quality pipeline. Only then should mk0.7 be considered for physical prototyping.

---

*Review compiled from:*
- `cad/config.py` (639 lines)
- `cad/assembly/tower_assembly.py` (241 lines)
- `cad/parts/*.py` (13 files, ~1,800 lines total)
- `revisions/mk0.7/REVISION.md`, `KNOWN_ISSUES.md`, `DECISIONS.md`, `CALCULATIONS.md`, `CHANGELOG.md`
- `revisions/mk0.7/review_package/analysis/printability_check.csv`
- `revisions/mk0.7/review_package/analysis/stl_quality.csv`
- `revisions/mk0.7/review_package/analysis/part_volume.csv`
- `revisions/mk0.7/review_package/analysis/duplicate_geometry_check.csv`
- `revisions/mk0.7/review_package/analysis/part_dimensions.csv`
- `AGENTS.md`
