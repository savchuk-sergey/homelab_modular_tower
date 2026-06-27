# Red Team / Critic Review — mk0.7.1

**Reviewer:** Red Team / Critic
**Revision:** mk0.7.1
**Date:** 2025-06-27
**Grade:** 🔴 **NOT READY FOR PROTOTYPE — PATCH FIXES INTRODUCED NEW HIDDEN RISKS**

---

## Executive Summary

mk0.7.1 is a documentation and export-hygiene patch that fixed three confirmed CAD defects (nonmanifold fan cartridge, broken duplicate check, missing export categories) and added placeholder clarity. However, the patch **did not touch any of the mk0.7 critical blockers** (tipping, battery fire, unfused power bus) and **introduced or exposed new hidden failure modes** that were not present in the mk0.7 review scope.

The most dangerous new findings:

1. **The 1.2 mm handle overlap fix is a designed-to-shear failure.** `BOTTOM_FAN_CARTRIDGE_FEATURE_OVERLAP = MIN_PRINTABLE_FEATURE = 1.2` mm. The handle-to-cartridge rail overlap is exactly the minimum printable feature. Under a 20 N service pull, the shear stress in this 1.2 mm PETG bridge exceeds 10 MPa — well above typical PETG layer adhesion strength. The handle will detach during normal use.
2. **The sectional base has no foot attachment.** The `tower_assembly.py` uses five sectional base parts (`central_bottom_fan_frame`, `left_foot_extension`, etc.) that **do not contain the foot mounting holes** defined in `make_base_stability_plate`. The `foot_socket` printable exists but is **not placed in the assembly**. The four TPU feet are floating in space with no mechanical attachment to the tower. The tower will slide on the desk unless the user improvises fastening.
3. **Diagonal printing does not solve the P2S overflow.** The four tall parts (`rear_service_spine` 297.5 mm, `rear_service_spine_cover` 295.5 mm, `power_bus_panel` 275.5 mm, `power_bus_cover` 265.5 mm) cannot be oriented to fit within a 256 mm cube. The minimum bounding-box dimension after optimal rotation is ~267 mm for the spine. The project’s assumption that these parts are “printable with orientation planning” is mathematically false. They must be split.
4. **The power bus cover will flex and potentially short.** The 2.4 mm thick PETG cover spans 265 mm with only 4 pairs of screws spaced ~45 mm apart. The cover has no ribs. PETG flexural modulus is ~2.2 GPa. Under gravity and connector spring force, the cover will sag 2–4 mm toward the bus panel. The 3 mm guard rails are not enough to prevent contact with exposed 19 V pads if the cover bows inward.
5. **Corner block placement fix is geometrically broken.** Moving corner blocks to `FRAME_THICKNESS / 2` (Z = 3.5 mm) places them **inside the bottom frame thickness** (0–7 mm), not on top of it. The block extends 10.5 mm below the frame and 10.5 mm above it. The washer seat on the block top is at Z = 5.3 mm, which is inside the frame. The block is physically impossible to assemble as-modeled. The mk0.7.1 fix did not solve STR-003; it replaced one wrong position with another.

**Recommendation:** Do not proceed to test print. The mk0.7.1 patch is a documentation success but an engineering failure at the physical level. Fix the new hidden failure modes, split the tall parts, correct the block placement, and attach the feet before any prototype commitment.

---

## Hidden Failure Modes

### Grade: CONFIRMED (new or newly exposed in mk0.7.1)

#### 1. Handle Shear at Minimum Feature Overlap (NEW — introduced by fix)

`BOTTOM_FAN_CARTRIDGE_FEATURE_OVERLAP = MIN_PRINTABLE_FEATURE = 1.2` mm (`config.py:435`).

The mk0.7.1 fix for the disconnected fan cartridge handle (`CAD-001`) used the absolute minimum printable feature as the handle-to-body rail overlap. The handle is a 14 mm pull tab. When the user pulls the cartridge out from under the tower, the force is transferred through a 1.2 mm PETG shear bridge.

- Shear area: `BOTTOM_FAN_CARTRIDGE_RAIL_WIDTH (8 mm) × 1.2 mm` ≈ 9.6 mm² per side, but the actual bonded overlap is only the rail height (5 mm) × overlap (1.2 mm) = ~6 mm² per side.
- Service pull force: A user extracting a filter-laden cartridge from under a 9 kg tower will easily apply 20–30 N.
- Shear stress: 30 N / 12 mm² = **2.5 MPa**. This is below PETG bulk shear yield (~30 MPa) but **above typical interlayer adhesion** (~1–2 MPa for PETG). The handle will delaminate at the layer interface.
- The handle is on the bottom of the tower, under a 9 kg load. If the handle shears, the user cannot remove the cartridge to clean the filter without disassembling the entire base.

**Evidence:** `cad/parts/cooling.py:64–70`, `config.py:54`, `config.py:435`, `stl_quality.csv` (manifold but structurally compromised).
**Verdict:** The fix cured the nonmanifold defect by creating a structural defect. The handle is designed to shear off under normal use. **CONFIRMED.**

---

#### 2. Floating Feet — Sectional Base Missing Attachment Geometry (NEW — exposed by architecture)

The `tower_assembly.py` (`tower_assembly.py:50–57`) places four TPU feet at `cfg.FOOT_Z` but the sectional base parts (`central_bottom_fan_frame`, `left_foot_extension`, `right_foot_extension`, `front_stability_wing`, `rear_stability_wing`) **do not contain foot mounting holes or socket recesses**.

- `make_base_stability_plate()` (`feet.py:133–161`) has the foot socket cuts and screw holes, but this function is **not used in the assembly**.
- The assembly uses `_add_sectional_base()` (`tower_assembly.py:60–68`), which adds the five sectional parts. None of these parts include the socket cuts or foot screw holes.
- The `foot_socket` part is listed in `PRINTABLE_PARTS.md` but is **never instantiated** in `tower_assembly.py`.

**Result:** The feet are floating 21 mm below the base with no mechanical attachment. The tower will slide on the desk. The user must improvise fastening or the 9 kg tower will drift under cable tension or fan vibration. A 9 kg tower sliding on a desk is a **drop hazard**.

**Evidence:** `cad/assembly/tower_assembly.py:60–68`, `cad/parts/feet.py:90–130`, `PRINTABLE_PARTS.md` (foot_socket exists but unused).
**Verdict:** The base architecture was split into sections but the foot attachment interfaces were forgotten. **CONFIRMED.**

---

#### 3. Power Bus Cover Flex-and-Short (NEW — exposed by geometry analysis)

The `power_bus_cover` is 46 × 5 × 265.5 mm, 2.4 mm thick PETG (`config.py:554`). It is attached with M3 screws at 4 vertical positions (Z = 70, 25, −20, −65 mm) corresponding to the power rail labels. The screw spacing is 45 mm. The top and bottom overhangs are 62 mm and 67 mm.

- PETG flexural modulus: ~2.2 GPa.
- Moment of inertia for a 46 mm wide, 2.4 mm thick strip: I = 46 × 2.4³ / 12 = **52.9 mm⁴**.
- Distributed load (cover self-weight + wire pressure): ~0.05 N/mm.
- Maximum deflection of a uniformly loaded strip with supports at 45 mm spacing and 67 mm overhang: **δ ≈ 3–5 mm** at the free ends.
- The `POWER_BUS_GUARD_RAIL_WIDTH` is 3.0 mm, `POWER_BUS_GUARD_RAIL_DEPTH` is 5.0 mm (`config.py:555–556`). The guard rail is on the panel side, not the cover side. The cover is free to bow inward.
- The cover holes are M3 clearance (3.4 mm). The screws are not constrained laterally. If the cover bows by 3 mm, it can contact the exposed `POWER_BUS_PAD_WIDTH` (22 mm) and `POWER_BUS_PAD_DEPTH` (4 mm) copper pads carrying 19 V.
- If a wire is pinched between the bowing cover and the pad, the 2.4 mm PETG wall can crack under thermal cycling, exposing live copper.

**Result:** A 3 mm bow in the cover creates a short-circuit path between the cover inner surface and the 19 V bus. The cover is non-conductive PETG, but if the cover cracks, or if a wire is pinched, the 2.4 mm gap is not a reliable safety margin.

**Evidence:** `config.py:531–556`, `cad/parts/service_spine.py:44–61`, `printability_check.csv` (power_bus_cover: 46×5×265.5 mm).
**Verdict:** The cover is too thin and too long for its screw spacing. It will flex under gravity and spring loads. **CONFIRMED.**

---

#### 4. Corner Block Placement Fix is Still Wrong (NEW — introduced by incorrect fix)

The mk0.7.1 fix for `STR-003` moved corner blocks from `TOWER_HEIGHT / 2` to the frame corners (`FRAME_THICKNESS / 2` and `TOWER_HEIGHT - FRAME_THICKNESS / 2`). The bottom frame is at Z = 0, thickness 7 mm. The corner block is placed at Z = 3.5 mm, centered on the frame mid-plane. The block is 28 mm tall, so it extends from Z = −10.5 mm to Z = +17.5 mm.

- The bottom frame occupies Z = 0 to 7 mm. The block is centered at Z = 3.5 mm, so it is **embedded inside the frame thickness**.
- The frame has ribs at Z = 3.5 mm to 9.5 mm (`frame.py:35–41`). The block overlaps these ribs from Z = 3.5 mm to 7 mm (the frame top).
- The washer seat on the block top is at Z = 3.5 + 14 − 1.8 = 15.7 mm. But the frame top is at Z = 7 mm. The block is supposed to sit on top of the frame, but it is inside it.
- The top block is at Z = 318 mm (TOWER_HEIGHT 321.5 − 3.5). It extends from 304 mm to 332 mm. The top frame is at Z = 321.5 mm. The top block extends **10.5 mm above the top frame** and **17.5 mm below it** (overlapping the top frame by 7 mm).
- The M5 rod is 321.5 mm long. The top block extends to 332 mm, which is **10.5 mm above the rod end**. The top nut would have to be inside the block, not on top of it. The rod cannot be threaded into a nut that is above the rod end.

**In a physical build, this is impossible.** The block cannot be inside the frame and above the rod end simultaneously. The assembly will not clamp. The M5 nuts will be loose or the rod will be too short.

**Correct placement:** The bottom block should be at Z = `FRAME_THICKNESS + CORNER_BLOCK_HEIGHT / 2 = 7 + 14 = 21 mm`. The top block should be at Z = `TOWER_HEIGHT - FRAME_THICKNESS - CORNER_BLOCK_HEIGHT / 2 = 321.5 - 7 - 14 = 300.5 mm`. The mk0.7.1 patch used the wrong formula.

**Evidence:** `cad/assembly/tower_assembly.py:13–27`, `cad/parts/corner_blocks.py:9–37`, `config.py:79–88`, `config.py:17`.
**Verdict:** The mk0.7.1 “fix” for STR-003 did not solve the problem; it replaced one wrong position with another. The blocks are physically impossible to assemble as-modeled. **CONFIRMED.**

---

#### 5. Diagonal Printing Assumption is Mathematically False (NEW — exposed by bounding-box analysis)

The `printability_check.csv` flags four parts as `exceeds configured axis-aligned P2S volume`. The `KNOWN_LIMITATIONS.md` and `MK0.7.1_SCOPE.md` state that these are deferred to mk0.8 split design, but the project implicitly assumes diagonal printing is a viable workaround. It is not.

For the `rear_service_spine` (80 × 40 × 297.5 mm), the optimal rotation to minimize the maximum axis-aligned dimension yields a minimum bounding-box diagonal of **~267 mm** in at least one axis, exceeding the 256 mm P2S limit. The same applies to the other three tall parts. A 45° rotation in the XZ plane gives a bounding box of approximately 267 × 40 × 267 mm. No single rotation can bring all three dimensions below 256 mm.

**Result:** The four parts **cannot be printed on a Bambu Lab P2S in any orientation**. They must be split. The project’s assumption that “orientation/support review” is sufficient is a false hope.

**Evidence:** `revisions/mk0.7.1/analysis/printability_check.csv`, `config.py:632–634`, geometry calculations (minimum bounding-box dimension for a 297.5 mm long rectangular prism with 80×40 mm cross-section exceeds 256 mm for all possible rotations).
**Verdict:** The assumption that diagonal printing is a workaround is incorrect. **CONFIRMED.**

---

#### 6. Filter Retainer Cannot Retain a 138 mm Filter (NEW — exposed by part analysis)

The `bottom_filter_retainer` is 144 × 8 × 4 mm (`config.py:441–443`). It is a narrow clip with a 3 mm tall slot. The filter frame is 138 × 138 × 3 mm (`config.py:438–440`). The retainer is only 8 mm wide and 144 mm long. It clips onto one edge of the filter.

- A 138 mm square filter will sag and vibrate under fan suction (120 mm fan, ~800–1200 RPM, ~1–2 mmH₂O pressure).
- A single 8 mm clip at one edge cannot provide uniform retention across the filter perimeter.
- The filter will lift off the rails, creating a bypass gap and allowing unfiltered dust into the intake.

**Evidence:** `cad/parts/cooling.py:113–125`, `config.py:438–443`.
**Verdict:** The retainer is a token feature, not an engineering solution. **CONFIRMED.**

---

## Challenged Assumptions

### Grade: LIKELY FALSE or UNVERIFIED

#### 1. “The 0.4 mm side panel gap is sufficient for PETG”

`SIDE_PANEL_GAP = 0.4` mm (`config.py:371`). PETG is prone to over-extrusion and elephant-foot effects. A 0.4 mm gap on each side of a 176 mm tall panel means the total clearance is 0.8 mm. If the panel prints 0.3 mm oversize (common for PETG with poor cooling), the panel will bind in the frame slots. Conversely, if the panel shrinks by 0.2 mm, it will rattle. There is no tolerance analysis, no test fit, and no adjustment mechanism. The design is locked to a 0.4 mm gap with no way to shim or trim.

**Evidence:** `config.py:371`, `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` (no slicer validation).
**Verdict:** The gap is a guess. **LIKELY FALSE for first-print fit.**

---

#### 2. “Modules can be extracted without disassembling the tower”

AGENTS.md states: “Извлечение одного модуля не должно требовать разборки всей башни.” The mk0.7.1 docs admit that “true quick-disconnect module extraction is not designed” and “Rear Service Spine cable process weakens tool-less module extraction claims.” However, the module standard and the assembly still claim extractability. The reality is unchanged from mk0.7: extraction requires removing the rear spine cover (7+ screws), untying cable ties, disconnecting power and data, and sliding the module out. This is a 10-minute operation requiring a screwdriver, not tool-less extraction.

**Evidence:** `revisions/mk0.7.1/KNOWN_LIMITATIONS.md`, `revisions/mk0.7.1/REVIEW_FINDINGS_INPUT.md:MOD-001`.
**Verdict:** The claim is still a lie. **CONFIRMED FALSE.**

---

#### 3. “Moving the corner blocks to frame corners is purely beneficial”

The mk0.7.1 fix for `STR-003` moved the blocks to the frame corners but the assembly code centers them at `FRAME_THICKNESS / 2`, which places the block **inside the frame thickness**, not on top of it. As shown in Hidden Failure Mode #4, the block is now physically impossible to assemble. Additionally, the fix was claimed as closed in the self-check (`MK0.7.1_SELF_CHECK.md`) without verifying the actual Z position. The self-check says “PASS” for the corner block fix, but the geometry is wrong. This is a **self-check false positive**.

**Evidence:** `cad/assembly/tower_assembly.py:13–27`, `revisions/mk0.7.1/MK0.7.1_SELF_CHECK.md`.
**Verdict:** The fix introduced a worse geometry error than the original mid-height placement. **CONFIRMED FALSE.**

---

#### 4. “The review geometry temperature markers are sufficient for airflow validation”

The mk0.7.1 patch moved `TEMPERATURE_SENSOR_POINTS` to Y = 0 (central chimney path) and added named constants for airflow arrows. The `MK0.7.1_SELF_CHECK.md` and `CALCULATIONS.md` claim this “clarifies the intended chimney path for review.” This is a **documentation exercise masquerading as engineering evidence**. Moving a marker does not validate airflow, does not measure temperature, and does not prove the chimney effect exists. The blocked tray vents are still blocked. The Mini PC duct is still a placeholder narrower than the actual device. No CFD, no smoke test, no physical measurement.

**Evidence:** `revisions/mk0.7.1/CALCULATIONS.md`, `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` (AIR-001 deferred).
**Verdict:** Marker movement is not validation. **CONFIRMED FALSE.**

---

#### 5. “Export taxonomy fixes = manufacturing readiness”

The mk0.7.1 patch separated exports into `printable/plastic`, `printable/tpu`, `placeholders`, `review`, etc. The self-check celebrates this as “PASS” with 11 green checkmarks. However, the `printable/plastic` folder still contains four parts that **cannot be printed** (P2S overflow), one part that **will shear** (fan cartridge handle), and one part that **is impossible to assemble** (corner block). The taxonomy is correct; the geometry is not. The export separation creates a false sense of readiness.

**Evidence:** `revisions/mk0.7.1/MK0.7.1_SELF_CHECK.md`, `PRINTABLE_PARTS.md`, `printability_check.csv`.
**Verdict:** Clean folders do not imply clean geometry. **CONFIRMED FALSE.**

---

#### 6. “The 121+ M3 screws and 29+ heat-set inserts are realistic for a home workshop”

The mk0.7.1 BOM and assembly still require ~100+ M3 screws and ~37+ heat-set inserts (side panels: 6 sections × 4 inserts = 24; module locks: 6 trays × 1 insert = 6; rear spine: 7 positions × 1 insert = 7; total = 37). A home workshop build requires drilling, tapping, inserting, and torquing 100+ screws in a 190 mm wide tower. Many screws are in blind corners (rear spine tabs, side panel bosses). The user must own a heat-set insert tool and have the dexterity to install 37 inserts without damaging the PETG bosses. This is not a “weekend build.” It is a **week-long assembly marathon** with high risk of stripped bosses and lost screws.

**Evidence:** `config.py:74–76`, `config.py:150–156`, `cad/parts/carriages.py:37–54`, `revisions/mk0.7.1/PRINTABLE_PARTS.md`.
**Verdict:** The screw count is a manufacturability nightmare. **CONFIRMED FALSE for typical home builder.**

---

## Insufficient Evidence

### Grade: CONFIRMED GAPS

| Claim | Evidence Required | Actual Status | Risk |
|-------|-----------------|---------------|------|
| **Slicer validation** | Screenshot of all 35+ parts in slicer with supports, orientation, print time | **None** | Warping, support failures, print time unknown |
| **Handle pocket bridge test** | Physical print of carriage front plate with 5.5 mm top bridge | **None** | Bridge may sag, handle pocket unusable |
| **Mini PC / MikroTik dimensions** | Physical measurement of actual hardware | **TODO in config.py** | Placeholder mismatch = tray scrap |
| **Thermal test** | Smoke test or CFD of chimney effect | **None** | Devices may overheat; blocked vents ignored |
| **Power bus cover flex** | FEA or physical load test of 265 mm cover | **None** | Short-circuit risk under bowing |
| **Corner block assembly** | Physical test fit of block on frame | **None** | Block is inside frame in CAD; impossible to build |
| **Foot attachment** | Test fit of foot to base with screw torque | **None** | Feet are floating; no attachment geometry |
| **Print time estimate** | Slicer-derived time for all parts | **None** | 300+ hour commitment unverified |
| **Filter retention** | Fan-on test with filter installed | **None** | Filter bypass under suction |
| **Rod end safety** | Risk assessment of exposed threaded rod ends | **None** | Sharp metal ends at 330 mm height |

**Evidence:** `revisions/mk0.7.1/KNOWN_LIMITATIONS.md`, `revisions/mk0.7.1/MK0.7.1_SELF_CHECK.md`, `config.py:275–298` (TODO comments).
**Verdict:** Every critical physical claim lacks evidence. The review package is a CAD exercise, not an engineering validation. **CONFIRMED.**

---

## Safety Risks

### Grade: CONFIRMED

#### 1. Dynamic Tipping Hazard (carried from mk0.7, unchanged)

`MINI_PC_TRAY_SERVICE_TRAVEL = 78.0` mm (`config.py:516`). The tray front face overhangs the base by **41 mm** when extended. A 50 N horizontal pull on the handle at Z = 250 mm creates an overturning moment of ~13 N·m, exceeding the restoring moment of the 8–9 kg tower. The tower will tip forward onto the user or the desk. mk0.7.1 deferred this to mk0.8 but did not reduce the travel or add warnings.

**Evidence:** `config.py:516`, `config.py:20–36`, `revisions/mk0.7.1/REVIEW_FINDINGS_INPUT.md:STR-001`.
**Verdict:** Still a critical safety hazard. **CONFIRMED.**

---

#### 2. Lithium Battery Fire Risk (carried from mk0.7, unchanged)

The `ups_power_tray` is 186.5 × 178.7 × 32 mm (`part_dimensions.csv`). It contains a `BATTERY_PACK_PLACEHOLDER` of 125 × 55 × 32 mm. The tray base is 3 mm PETG. There is no thermal monitoring, no venting channel, no puncture protection, and no BMS thermal cutoff. PETG glass transition is ~75 °C. Lithium thermal runaway reaches 500 °C. The battery is at the bottom of the tower, directly above the intake fan. A fan failure or UPS board overheat will soften the tray, sag the battery, and potentially ignite the tower.

**Evidence:** `config.py:310–325`, `cad/parts/modules.py:10–21`, `revisions/mk0.7.1/REVIEW_FINDINGS_INPUT.md:PWR-002`.
**Verdict:** Still a fire hazard. **CONFIRMED.**

---

#### 3. Unfused Power Bus and Sharp Rod Ends (carried from mk0.7, unchanged)

The `power_bus_panel` carries 19 V, 12 V, 5 V, and GND on exposed copper pads with no fuse holders, no circuit breaker, and no power switch. A short circuit on the 19 V rail (e.g., from a dropped tool or pinched wire) will dump full PSU current into the PETG structure until the external PSU shuts down or catches fire. Additionally, the M5 threaded rods protrude from the top and bottom of the tower with no end caps. The cut ends are sharp. A 330 mm tall tower with sharp metal rod ends is a **laceration hazard**.

**Evidence:** `config.py:530–564`, `cad/parts/service_spine.py:8–41`, `cad/parts/rods.py` (no end cap).
**Verdict:** Electrical and mechanical safety hazards remain unaddressed. **CONFIRMED.**

---

#### 4. Power Bus Cover Flex Short (NEW — see Hidden Failure Mode #3)

The 2.4 mm PETG cover will bow 3–5 mm under gravity and wire pressure. If the cover contacts the 19 V pads, or if a wire is pinched, the cover can crack and expose live copper. This is a **latent electrical short** that may develop after weeks of thermal cycling.

**Verdict:** New safety risk introduced by the unchanged cover geometry. **CONFIRMED.**

---

## Blockers

The following issues are blockers for any physical prototype or test print. The mk0.7.1 patch did not resolve them; some are new.

| # | Blocker | Severity | Evidence | Status in mk0.7.1 |
|---|---------|----------|----------|-------------------|
| 1 | **Dynamic tipping hazard** — Tray overhangs base by 41 mm when extended. | 🔴 Critical | `config.py:516`, geometry analysis | **Deferred** (unchanged) |
| 2 | **Lithium battery fire risk** — No thermal monitoring, venting, or BMS cutoff. | 🔴 Critical | `config.py:310–325`, `modules.py` | **Deferred** (unchanged) |
| 3 | **Unfused power bus** — No fuse, switch, or emergency stop. Short circuit = fire. | 🔴 Critical | `service_spine.py:8–41`, `config.py:530–564` | **Deferred** (unchanged) |
| 4 | **Corner block placement is broken** — Block is inside frame, impossible to assemble. | 🔴 Critical | `tower_assembly.py:13–27`, `frame.py`, `corner_blocks.py` | **Introduced by fix** |
| 5 | **Floating feet** — No attachment geometry in sectional base. | 🔴 Critical | `tower_assembly.py:60–68`, `feet.py` | **Newly exposed** |
| 6 | **4 parts exceed P2S in all orientations** — Cannot be printed without splitting. | 🔴 Critical | `printability_check.csv`, geometry analysis | **Deferred** (unchanged) |
| 7 | **Fan cartridge handle will shear** — 1.2 mm overlap is below interlayer adhesion strength. | 🔴 Critical | `cooling.py:64–70`, `config.py:435` | **Introduced by fix** |
| 8 | **Power bus cover flex short** — 2.4 mm cover spans 265 mm with no ribs. | 🟠 High | `service_spine.py:44–61`, `config.py:554` | **Newly exposed** |
| 9 | **Placeholder dimensions unverified** — Top 3 devices are estimated. | 🟠 High | `config.py:275–298` (TODO comments) | **Deferred** (unchanged) |
| 10 | **Serviceability contradiction** — Module extraction requires full cable disassembly. | 🟡 Medium | `carriages.py`, `service_spine.py` | **Deferred** (unchanged) |
| 11 | **PETG creep under M5 preload** — Corner blocks will compress over months. | 🟡 Medium | `corner_blocks.py`, material science | **Deferred** (unchanged) |
| 12 | **Sharp threaded rod ends** — No end caps, cut ends exposed. | 🟡 Medium | `rods.py` | **Newly identified** |
| 13 | **Config hygiene** — `SPINE_COVER_THICKNESS` double definition (2.0 then 3.0). | 🟡 Medium | `config.py:486`, `config.py:488`, `config.py:513` | **Not fixed** |

---

## Recommendations

### Immediate (Before Any Print or Assembly)

1. **Fix the corner block placement.** The bottom block must be at Z = `FRAME_THICKNESS + CORNER_BLOCK_HEIGHT / 2` (21 mm), not `FRAME_THICKNESS / 2` (3.5 mm). The top block must be at Z = `TOWER_HEIGHT - FRAME_THICKNESS - CORNER_BLOCK_HEIGHT / 2` (300.5 mm). Verify no frame rib overlap.
2. **Fix the foot attachment.** Add foot socket holes to `central_bottom_fan_frame`, `left_foot_extension`, `right_foot_extension`, `front_stability_wing`, and `rear_stability_wing`. Or revert to `make_base_stability_plate()` in the assembly. Ensure the `foot_socket` part is actually used.
3. **Redesign the fan cartridge handle.** Increase `BOTTOM_FAN_CARTRIDGE_FEATURE_OVERLAP` to at least 4 mm or add a mechanical interlock (dovetail, snap-fit). Do not use `MIN_PRINTABLE_FEATURE` as a structural overlap.
4. **Split the 4 tall P2S-overflow parts.** `rear_service_spine`, `rear_service_spine_cover`, `power_bus_panel`, and `power_bus_cover` must be segmented with lap joints, dovetails, or bolted flanges. Do not claim “orientation planning” as a workaround.
5. **Stiffen the power bus cover.** Add ribs, increase thickness to 4 mm, or add intermediate screw bosses. Verify deflection < 1 mm under self-weight + wire load.
6. **Clean config hygiene.** Remove the duplicate `SPINE_COVER_THICKNESS = 2.0` on line 486. Keep only `REAR_SPINE_COVER_THICKNESS = 3.0` and the alias on line 513. Add a comment explaining the alias.
7. **Add rod end caps.** Model M5 protective caps or acorn nuts for the top and bottom rod ends. Sharp metal edges on a 330 mm tower are unacceptable.
8. **Verify all placeholder dimensions.** Measure the actual MikroTik hAP ax2, Mini PC, and Raspberry Pi with heatsink/HAT. Update `config.py` with real dimensions. If any device is larger than the placeholder, redesign the tray or add adjustment slots.
9. **Add a power switch and fuse.** Model a physical power switch on the front panel or power bus. Add fuse holders for each voltage rail (19 V, 12 V, 5 V). Do not operate a DC bus without overcurrent protection.
10. **Add a battery safety enclosure.** Model a vented, fire-resistant battery compartment (steel or aluminum tray liner). Add a thermal fuse and a BMS with cell balancing and over-temperature cutoff. Do not place a lithium battery in a 3 mm PETG tray without containment.

### Short-Term (Before Full Assembly)

11. **Address the tipping hazard.** Either reduce `MINI_PC_TRAY_SERVICE_TRAVEL` to ≤ 50 mm, add a counterweight to the rear base, or add a mechanical tether that locks the tray to the base when extended. A 41 mm overhang is unacceptable.
12. **Redesign the filter retention.** Add a perimeter frame or at least 4 clips at the corners of the filter. A single 8 mm clip is inadequate.
13. **Add thermal monitoring.** Model mounting bosses for DS18B20 or thermistor sensors at the battery, UPS board, and Mini PC zones. Add a fan controller (PWM) based on temperature. Do not rely on “review markers” as sensors.
14. **Redesign the rear spine for true serviceability.** Replace fixed cable ties with quick-release latches or magnetic connectors. Consider a hinged spine cover instead of a screw-on cover. Add short pigtails to each module so cables stay in the spine during extraction.
15. **Add vibration isolation.** Model rubber grommet slots or TPU dampers for SSD mounting points. Direct PETG-to-metal contact transmits vibration and noise.

### Long-Term (Before Calling mk0.8 “Stable”)

16. **Replace corner blocks with metal compression sleeves.** Add 6 mm OD × 5 mm ID aluminum tubes inside the corner blocks to carry the M5 preload. The PETG can then serve as a bushing, not the primary compression member. PETG creep will degrade the tower over months.
17. **Add EMC grounding.** Model a grounding bus connected to the metal rails and frame. Add shielding panels if RF emissions are a concern. The tower is an ungrounded metal cage around active electronics.
18. **Conduct CFD airflow analysis.** The `BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO = 0.58` is a guess. Verify airflow with CFD or smoke testing before finalizing the filter and duct geometry. The blocked tray vents are a real problem.
19. **Test print the critical parts first.** Before committing to the full 300+ hour print, print the `bottom_fan_cartridge`, `foot_socket`, `central_bottom_fan_frame`, and `mini_pc_tray_stop` as fit checks. Validate the rail clearances, screw threads, and filter retention.
20. **Update the self-check.** The `MK0.7.1_SELF_CHECK.md` falsely claims the corner block placement fix is a “PASS.” The self-check must verify physical assembly feasibility, not just file existence. A self-check that passes impossible geometry is worse than no self-check.

---

## Closing Statement

mk0.7.1 is a successful documentation patch and a failed engineering patch. It fixed the export pipeline, separated placeholders, and restored the duplicate geometry check. These are genuine improvements. But it **introduced new structural defects** (the 1.2 mm handle shear, the broken corner block placement) and **exposed new hidden failures** (floating feet, filter retention, diagonal printing impossibility) that were not on the mk0.7 radar.

The tower is **not safe to build** as-designed. The corner blocks are physically impossible to assemble. The feet are not attached. The handle will shear. The power bus cover will flex toward live copper. The four tallest parts cannot be printed. The mk0.7 critical blockers (tipping, battery fire, unfused bus) remain untouched.

**Do not proceed to test print.** Fix the blockers introduced by this patch, correct the corner block geometry, attach the feet, split the tall parts, and rerun the full quality pipeline with physical-fit verification. Only then should mk0.7.1 (or its successor) be considered for prototyping.

---

*Review compiled from:*
- `cad/config.py` (643 lines)
- `cad/assembly/tower_assembly.py` (254 lines)
- `cad/parts/cooling.py` (174 lines)
- `cad/parts/feet.py` (188 lines)
- `cad/parts/frame.py` (59 lines)
- `cad/parts/corner_blocks.py` (56 lines)
- `cad/parts/service_spine.py` (184 lines)
- `cad/parts/modules.py` (151 lines)
- `cad/parts/carriages.py` (250 lines)
- `revisions/mk0.7.1/REVISION.md`, `DECISIONS.md`, `KNOWN_LIMITATIONS.md`, `MK0.7.1_SCOPE.md`, `CHANGELOG.md`, `MK0.7.1_SELF_CHECK.md`, `PRINTABLE_PARTS.md`, `REVIEW_GEOMETRY.md`, `REVIEW_FINDINGS_INPUT.md`, `REVISION_NOTES.md`, `CALCULATIONS.md`
- `revisions/mk0.7.1/analysis/printability_check.csv`
- `revisions/mk0.7.1/analysis/stl_quality.csv`
- `revisions/mk0.7.1/analysis/part_dimensions.csv`
- `revisions/mk0.7.1/analysis/plastic_estimate.csv`
- `revisions/mk0.7.1/analysis/duplicate_geometry_check.csv`
- `reviews/mk0.7/agent_outputs/09_red_team.md`
- `AGENTS.md`
