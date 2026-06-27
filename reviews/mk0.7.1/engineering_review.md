# Homelab Modular Tower Engineering Review — mk0.7.1

**Revision:** mk0.7.1  
**Branch:** `cad/mk0.7.1`  
**Date:** 2026-06-27  
**Review type:** Multi-agent engineering design review  
**Validation limits:** no CFD, no FEA, no slicer validation, no physical testing

---

## 1. Executive Summary

mk0.7.1 is a useful patch revision, but it is **not ready for printing, prototype assembly, or hardware ordering**.

**Overall verdict: NO-GO UNTIL BLOCKERS ARE FIXED.**

The revision successfully fixes several mk0.7 hygiene and geometry issues:

- `bottom_fan_cartridge` is now watertight and manifold.
- `duplicate_geometry_check.csv` is restored and populated.
- Power-bus cover holes now align with panel holes.
- Bottom/top fan grille Z placement no longer intersects the frame rings.
- `foot` is correctly classified as TPU.
- `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` is raised to `MIN_PRINTABLE_FEATURE`.
- Top fan placeholder and power-bus zone placeholder are now represented in the export/review package.

However, the review found one major regression and many inherited blockers:

- The corner block placement fix is wrong: blocks are centered at the frame mid-planes and intersect the frames.
- Side panels still cannot be mounted.
- Guide rails still have no fastening/load-transfer interface.
- Top frame clamping is still reversed/undefined.
- Tray vertical support is not modeled.
- Four tall rear-spine/power-bus parts still require split redesign for reliable P2S production.
- Tray base vents are blocked by devices.
- The Mini PC duct is still a placeholder, not a functional duct.
- Module extraction still requires rear cable disassembly.
- Power bus, fuse protection, strain relief, connector geometry, and fan cable routing remain placeholder-level.
- Dynamic tipping, lithium battery safety, unfused DC bus, and exposed rod-end risks remain unresolved.

**Recommended next step:** create a focused mk0.7.2 or mk0.8 structural/serviceability patch. Do not attempt a full print from mk0.7.1 exports.

---

## 2. Reviewed Inputs

### Agent Outputs

- `reviews/mk0.7.1/agent_outputs/01_cad_integrity.md`
- `reviews/mk0.7.1/agent_outputs/02_printability.md`
- `reviews/mk0.7.1/agent_outputs/03_structural_integrity.md`
- `reviews/mk0.7.1/agent_outputs/04_airflow_cooling.md`
- `reviews/mk0.7.1/agent_outputs/05_modularity_serviceability.md`
- `reviews/mk0.7.1/agent_outputs/06_power_cable_management.md`
- `reviews/mk0.7.1/agent_outputs/07_plastic_efficiency.md`
- `reviews/mk0.7.1/agent_outputs/08_manufacturability.md`
- `reviews/mk0.7.1/agent_outputs/09_red_team.md`

### CAD and Analysis Sources

- `cad/config.py`
- `cad/assembly/tower_assembly.py`
- `cad/parts/*.py`
- `cad/exporters/part_registry.py`
- `revisions/mk0.7.1/analysis/part_dimensions.csv`
- `revisions/mk0.7.1/analysis/plastic_estimate.csv`
- `revisions/mk0.7.1/analysis/printability_check.csv`
- `revisions/mk0.7.1/analysis/stl_quality.csv`
- `revisions/mk0.7.1/analysis/duplicate_geometry_check.csv`
- `revisions/mk0.7.1/*.md`
- `AGENTS.md`
- `docs/POWER.md`, `docs/BOM.md`, `docs/PRINTING.md`, `docs/ARCHITECTURE.md`

---

## 3. Evidence Status Legend

- **CONFIRMED** — directly supported by CAD source, CSV output, measurement from exported geometry, or revision documentation.
- **LIKELY** — strong engineering inference from geometry, material behavior, or common assembly practice.
- **UNCERTAIN** — insufficient data; assumption may be reasonable but is not proven.
- **NEEDS TEST** — requires slicer preview, physical fit check, smoke/thermal test, electrical validation, or measured hardware.

---

## 4. Requirements Checklist

| # | Requirement | Result | Grade | Evidence |
|---|-------------|--------|-------|----------|
| 1 | Modularity | **PARTIAL** | C+ | Trays share a common envelope and rail standard, but extraction still requires cable disassembly. |
| 2 | Repairability | **PARTIAL** | C | Removable trays/panels are intended, but side panels, feet, fan cartridge, and power bus access are not build-ready. |
| 3 | Structural stiffness | **FAIL** | D | M5 rods and frames exist, but corner blocks intersect frames, rails are not fastened, side panels cannot transfer shear, and top clamping is broken. |
| 4 | Airflow | **PARTIAL** | C | Intake/exhaust concept is modeled, but tray vents are blocked, top gap is tight, Mini PC duct is non-functional, and filter/fan cable details are incomplete. |
| 5 | Serviceability | **FAIL** | D+ | Modules are geometrically removable but cable routing forces cover removal, untie/disconnect steps, and tool use. |
| 6 | Parametric CAD | **PASS** | A- | Most dimensions are centralized in `config.py`; several unexplained literals and duplicate aliases remain. |
| 7 | Scalability | **PARTIAL** | B- | Software structure supports new trays, but physical stack has no spare height and fixed tray dimensions. |
| 8 | Rear Service Spine | **PARTIAL** | C | Spine geometry exists, but cable capacity, quick disconnects, fan routing, and power-bus integration are not viable. |
| 9 | Power System | **FAIL** | D | No open 220 V is modeled, but DC input, fuses, switch, real connectors, strain relief, and battery safety are missing. |
| 10 | CAD Rules | **PASS** | A- | Parts/assembly/export are separated and CadQuery remains source of truth. |
| 11 | Revision Structure | **PASS** | A | mk0.7.1 revision docs and analysis package exist. |
| 12 | Export Organization | **PASS** | A- | Export categories are cleaner; printability still does not equal build readiness. |

**Compliance score:** 6 pass/partial-pass domains, 3 partial domains, 3 fail domains. The project remains below the threshold for a physical prototype.

---

## 5. Consolidated Blockers

| ID | Blocker | Status | Evidence | Next action |
|---|---------|--------|----------|-------------|
| B-01 | Corner blocks intersect top/bottom frames | **CONFIRMED** | `tower_assembly.py` places blocks at `FRAME_THICKNESS/2` and `TOWER_HEIGHT - FRAME_THICKNESS/2`; a 28 mm block overlaps a 7 mm frame. | Move blocks outside frame thickness and verify rod/nut stack. |
| B-02 | Side panels cannot be mounted | **CONFIRMED** | Panel holes do not align with corner-block holes; corner blocks only drill `>X`/`>Y`; frames lack panel holes. | Define side-panel mounting interface across frames/corner blocks. |
| B-03 | Guide rails have no fastening interface | **CONFIRMED** | Rails have M3 holes, but no mating frame/bracket holes; rail ends do not engage frame slots. | Add rail brackets, tabs, inserts, or captured metal rail seats. |
| B-04 | Top frame clamping is incorrect | **CONFIRMED** | Same nut/washer seat orientation is used for top and bottom frame. | Invert top-frame seat logic or create top-specific frame. |
| B-05 | Tray vertical support is missing | **CONFIRMED/LIKELY** | Vertical rails exist, but no shelves/ledges/brackets support tray weight. | Add load-bearing shelves or intermediate supports. |
| B-06 | Four tall parts are not production-printable as one piece | **CONFIRMED** for axis-aligned overflow; **NEEDS SLICER TEST** for arbitrary orientation | `rear_service_spine`, `rear_service_spine_cover`, `power_bus_panel`, `power_bus_cover` exceed 256 mm axis-aligned. Diagonal placement may fit some bounding boxes in theory, but warping/support risk remains unacceptable. | Split all four parts with engineered joints. |
| B-07 | Floating feet / missing sectional-base foot attachment | **CONFIRMED** | `foot_socket` exists but sectional base assembly does not integrate sockets/holes. | Add socket geometry to base sections or revise base architecture. |
| B-08 | Fan cartridge handle overlap is only 1.2 mm | **LIKELY** structural failure | Fix makes STL manifold, but the overlap is the minimum printable feature, not a robust service pull feature. | Increase overlap to >= 4 mm or add a mechanical interlock. |
| B-09 | Tray vents are blocked by device placeholders | **CONFIRMED** | Devices sit directly on tray bases over vent slots. | Raise devices, create side/bypass flow, or redesign tray ventilation. |
| B-10 | Mini PC duct is not functional | **CONFIRMED** | Duct is a placeholder tube without a side port matched to the real Mini PC intake. | Redesign around measured Mini PC inlet/outlet geometry. |
| B-11 | Rear Service Spine traps module cables | **CONFIRMED** | Extraction requires removing covers, untieing cables, and disconnecting rear connectors. | Add quick disconnects, pigtails, or hinged/tool-less service spine. |
| B-12 | Power bus lacks real electrical protection | **CONFIRMED** | Fuse/switch/e-stop are placeholder or absent; no real holder geometry. | Model fuse holders, switch, DC input, and rail protection. |
| B-13 | Power bus panel/cover are mechanically inadequate | **CONFIRMED/LIKELY** | Tall thin PETG panel/cover, minimal screw support, connector clearance collision. | Move to metal plate/PCB or stiffen and increase connector clearance. |
| B-14 | Rear spine cable capacity is insufficient | **CONFIRMED** | 52 x 30 mm spine with internal power bus cannot carry expected 15+ cables cleanly. | Widen spine, move bus outside, or reduce cable count. |
| B-15 | Fan cable routing is undefined | **CONFIRMED** | No modeled path from bottom/top fans into Rear Service Spine. | Add dedicated fan cable channels and strain relief. |
| B-16 | Dynamic tipping hazard remains | **CONFIRMED/LIKELY** | Mini PC service travel and high COM remain unresolved. | Reduce travel, add lockout, add counter-support, or test stability. |
| B-17 | Battery/UPS safety remains placeholder-level | **CONFIRMED/NEEDS TEST** | UPS zones overlap; no thermal containment, BMS mounting, fuse access, or real battery dimensions. | Design around selected UPS/battery hardware and safety constraints. |
| B-18 | BOM and assembly process are incomplete | **CONFIRMED** | BOM lacks quantities; no `docs/ASSEMBLY.md`; rod length is not realistic for nuts/washers. | Add quantitative BOM and assembly sequence before ordering hardware. |

---

## 6. Domain Findings

### CAD Integrity

mk0.7.1 improves export hygiene and resolves several clear mk0.7 defects. `stl_quality.csv` confirms the fan cartridge is manifold; duplicate geometry checking now works; TPU foot classification is corrected.

Remaining CAD issues:

- **CONFIRMED:** corner block placement creates a new frame intersection.
- **CONFIRMED:** `SPINE_COVER_THICKNESS` still has a confusing dead/alias definition.
- **CONFIRMED:** several unexplained constants remain in `config.py` (`+24.0`, `-34.0`, `* 6.5`, `* 2.2`, `* 0.52`, `+22.0`).
- **CONFIRMED:** redundant registry/function aliases remain (`frame_top`/`top_structural_frame`, `bottom_fan_panel`/`bottom_fan_grille`, etc.).

### Printability

mk0.7.1 resolves the nonmanifold fan cartridge and material misclassification blockers, but not production printability.

Key findings:

- **CONFIRMED:** four parts exceed the P2S 256 mm axis-aligned build volume.
- **CONFIRMED:** all four should be split for reliable production, even where a diagonal placement might fit a simplified bounding box.
- **CONFIRMED:** large flat PETG parts remain high-warp risk: fan grilles, frames, base wings, side panels.
- **CONFIRMED/LIKELY:** all six trays need support for the front handle pocket.
- **NEEDS TEST:** slicer validation is still absent; print times and supports are estimates, not proven toolpaths.

### Structural Integrity

The intended architecture (M5 rods, metal rails, top/bottom frames) is directionally correct, but load paths are incomplete.

Key findings:

- **CONFIRMED:** top frame clamping geometry is wrong.
- **CONFIRMED:** side panels cannot carry shear because they cannot be attached.
- **CONFIRMED:** guide rails are not structurally fastened to frames.
- **CONFIRMED:** tray vertical support is not modeled.
- **LIKELY:** torsion resistance is inadequate until side panels or diagonal braces become real load paths.
- **NEEDS TEST:** PETG creep under M5 preload and tray-stop impact behavior require physical checks.

### Airflow and Cooling

The vertical chimney concept is present, but the current CAD does not prove adequate airflow.

Key findings:

- **CONFIRMED:** bottom intake grille openness is acceptable as bare geometry.
- **UNCERTAIN:** filter pressure drop is unknown because no filter material is specified.
- **CONFIRMED:** tray base vents are blocked by devices, so air must flow around modules rather than through trays.
- **CONFIRMED:** Mini PC duct is a placeholder and does not mate to real device vents.
- **CONFIRMED:** top exhaust fan is only a placeholder; no cartridge, wire route, or validated top clearance.
- **CONFIRMED:** top gap above the module stack is narrow and may be a meaningful constriction.

### Modularity and Serviceability

The module envelope is standardized, but the service workflow violates the project goal that modules should be removable without tower disassembly.

Key findings:

- **CONFIRMED:** cable-dependent extraction remains a blocker.
- **CONFIRMED:** rear spine cover removal and cable tie removal are required for module service.
- **CONFIRMED:** side panels are sectioned but currently unmountable.
- **CONFIRMED:** bottom fan cartridge is geometrically removable, but retention/attachment and cable routing are unresolved.
- **LIKELY:** 78 mm Mini PC service travel is useful for front access but insufficient for rear connector service.

### Power and Cable Management

The low-voltage-only architecture is the right safety direction, but the power system is still placeholder-level.

Key findings:

- **CONFIRMED:** no open 220 V is modeled inside the printed tower.
- **CONFIRMED:** no external DC input connector, cable gland, or strain relief is modeled.
- **CONFIRMED:** power bus connector zones are incompatible with real panel-mount connector depth and cover clearance.
- **CONFIRMED:** fuse geometry is absent; the fuse zone is only a marker.
- **CONFIRMED:** rear spine cable capacity is insufficient for power, Ethernet, USB, and fan wiring.
- **NEEDS TEST:** DC UPS volume and battery layout require actual hardware selection.

### Plastic Efficiency

The design is still heavy and time-consuming to print.

Key findings:

- **CONFIRMED:** mesh solid mass is approximately 3.66 kg on a single-unit export basis.
- **LIKELY:** actual filament use is roughly 5.2-6.0 kg after infill/support/brim behavior.
- **CONFIRMED:** estimated print time remains hundreds of hours.
- **CONFIRMED:** largest optimization targets are the sectional base, module trays, grilles, side panels, and rear spine.
- **NEEDS TEST:** aggressive hollowing or shell reductions must be validated for stiffness and vibration.

### Manufacturability

mk0.7.1 remains difficult to build in a home workshop.

Key findings:

- **CONFIRMED:** approximately 120+ M3 screws and 29+ heat-set inserts are still expected.
- **CONFIRMED:** quantitative BOM data is missing.
- **CONFIRMED:** real M5 rods need extra length beyond `TOWER_HEIGHT`; around 340 mm is more realistic than 321.5 mm.
- **CONFIRMED:** no assembly sequence document exists.
- **CONFIRMED:** PETG support removal from tray handle pockets is likely painful without design changes.

### Red Team Findings

The red-team review is intentionally conservative. Its main value is identifying false readiness signals.

Accepted as blockers:

- **CONFIRMED:** corner block placement is physically wrong.
- **CONFIRMED:** foot attachment is missing from the sectional base workflow.
- **LIKELY:** fan cartridge handle overlap is too small for repeated service pulls.
- **CONFIRMED/LIKELY:** power bus cover/panel geometry is not safe as a real electrical assembly.
- **CONFIRMED:** self-check overstates readiness by marking corner block placement as PASS.

Normalized note on diagonal printing: the red-team output says the four tall parts cannot fit in any orientation, while the printability output shows several simplified diagonal bounding boxes that may fit. The consolidated review treats the **axis-aligned overflow as CONFIRMED** and the **arbitrary-orientation fit as not production evidence**. The engineering decision is unchanged: **split the parts; do not rely on diagonal one-piece PETG prints.**

---

## 7. Recommended Fix Order

### P0 — Before Any Test Print

1. Fix corner block Z placement and verify no frame/rib/rod/nut intersection.
2. Define side-panel mounting to actual structure.
3. Define guide-rail fastening and tray vertical support.
4. Fix top-frame clamping orientation.
5. Add sectional-base foot attachment geometry.
6. Increase bottom fan cartridge handle overlap or add mechanical interlock.
7. Split `rear_service_spine`, `rear_service_spine_cover`, `power_bus_panel`, and `power_bus_cover`.

### P1 — Before Hardware Ordering

1. Select real power connectors, fuse holders, switch, DC input connector, and UPS/battery hardware.
2. Redesign power bus around real connector bodies and bend radii.
3. Widen or reorganize Rear Service Spine cable capacity.
4. Add fan cable routing for bottom and top fans.
5. Add quantitative BOM with exact fastener, insert, rod, rail, fan, connector, and wire requirements.
6. Correct M5 rod length in config/BOM and document nut/washer stack.

### P2 — Before Full Prototype Assembly

1. Create `docs/ASSEMBLY.md` with build order, tool list, rod tensioning notes, and insert installation notes.
2. Add slicer validation for every printable part with orientation/support/brim recommendations.
3. Print fit-test coupons/subassemblies before committing to the full print set:
   - one corner block + frame corner,
   - one rail mount,
   - one tray + handle pocket,
   - one side-panel mount,
   - fan cartridge handle,
   - foot/socket/base interface.
4. Validate Mini PC, MikroTik, UPS, and battery dimensions from actual hardware.
5. Run smoke/thermal checks or CFD only after geometry is physically plausible.

---

## 8. mk0.7.1 Verdict

mk0.7.1 is valuable as an engineering review and cleanup checkpoint. It should be kept as a documented patch revision, but it should **not** be treated as a buildable release.

**Final decision:** `NO-GO UNTIL BLOCKERS ARE FIXED`.

**Minimum next-revision goal:** convert the tower from a clean CAD/export package into a physically assemblable structure by fixing corner blocks, rail support, side-panel mounting, foot attachment, top clamping, tall-part splitting, and service-spine/power-bus basics.

