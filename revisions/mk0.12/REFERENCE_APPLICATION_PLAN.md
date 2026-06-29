# mk0.12 Reference Application Plan

## 1. Executive Summary

mk0.12 is planned as an MVP-2M reference-informed revision for Homelab Modular Tower. It is not a copy, fork, or adaptation of any single external project.

No external project is selected as a direct CAD base.
mk0.12 remains a custom CadQuery stack-through-rod architecture informed by selected reference patterns.

The near-term MVP remains focused on two real modules:

- Mini PC
- Raspberry Pi + SSD

The purpose of this plan is to reduce the risk of designing every subsystem from a blank page while keeping control over the Homelab Modular Tower architecture. External projects are treated as reference patterns for serviceability, printability, documentation discipline, compact device trays, and module layering. They do not override the project constraints: CadQuery remains the source of truth, dimensions belong in `cad/config.py`, and generated STEP/STL/PNG artifacts remain derived outputs.

The active architecture for the MVP is `stack-through-rod`: a vertical compressed stack made from `base_pedestal`, `rpi_ssd_stack_module`, `minipc_stack_module`, `top_cap`, four M5 threaded rods, washers, and nuts. Plastic parts provide positioning, airflow shaping, cable routing, and compression pad geometry. They must not become the only structural path.

## 2. Reference Classification

| Reference | Role | Use | Do Not Use | Status |
| --- | --- | --- | --- | --- |
| `istergiou/nas-rack` | Stackable NAS/SBC rack concept reference | Layered compact device organization, stack/slot thinking, small NAS/SBC density cues | Direct CAD base, exact dimensions, proof of airflow or cable architecture | REFERENCE ONLY |
| `ilikecake/RPi-Rack-Case` | Donor reference for Raspberry Pi / small device module planning | Raspberry Pi tray thinking, front service access, compact 1U-style device support | Whole tower architecture, mini PC thermal layout, direct geometry | GO |
| `peter-mount/pi-rack` | Printability and load-bearing reinforcement reference | Slicer assumptions, reinforced printed load zones, higher infill logic near structural features | CAD source geometry without license verification, full module architecture | PARTIAL |
| `TheCallumInglis/Rack_Mount_Pi` | Low-priority Raspberry Pi mounting reference | Pi mounting pattern sanity checks and rack-mount Pi context | Architecture, CAD base, source geometry without license verification | PARTIAL |
| `plasmadancom/HAT-RACK` | Serviceability, power separation, and industrial discipline reference | External power mindset, separated boards, DIN-like service logic, cable/power organization | Printable tower geometry, mini PC/NAS layout, direct enclosure shape | GO |
| `plasmadancom/DINPi-RACK` | Secondary industrial mounting reference | DIN/mounting mindset and dimensional drawing discipline | Tower base, module architecture, direct geometry | PARTIAL |
| `cloudmesh-community/case` | Documentation and validation process reference | Requirements-before-CAD discipline, BOM, assembly notes, physical validation cycle | Direct geometry, material strategy, laser-cut acrylic assumptions | GO |
| N5 Mini / Jack Harvest | Candidate compact mini PC + storage layout reference | Future investigation of mini PC, storage, PETG/TPU, airflow, fan, cable, and power integration | CAD base until source, license, dimensions, and adaptation path are verified | HOLD |
| `merocle/uptime-platform-for-raspberry-pi` | Low-priority Raspberry Pi rack-platform reference | Minimal context for rack-platform Pi ideas | CAD base, primary architecture, ShareAlike-derived geometry path | PARTIAL |

## 3. Reference Pattern Map

| Pattern | Source Reference | Target Area in Homelab Modular Tower | Why Useful | Risk |
| --- | --- | --- | --- | --- |
| Stackable NAS/SBC layer concept | `istergiou/nas-rack` | Overall MVP stack organization | Supports layered thinking for compact multi-device packaging | Could tempt copying a slot architecture that does not support M5 rods, rear spine, or mini PC thermals |
| Raspberry Pi / small device tray | `ilikecake/RPi-Rack-Case`, `TheCallumInglis/Rack_Mount_Pi` | `rpi_ssd_stack_module` | Gives practical cues for Pi mounting, small-device access, and compact tray constraints | Pi-only assumptions may ignore SSD, cable exit, vertical airflow, and stack compression zones |
| Front service access | `ilikecake/RPi-Rack-Case` | Pi/SSD and Mini PC module access faces | Helps preserve access to removable media, ports, and retainers | Front access must not weaken the stack interface or block airflow |
| Load-bearing print reinforcement | `peter-mount/pi-rack` | M5 rod pads, washer seats, base/top compression areas | Reinforces printed parts around real load paths instead of treating plastic as decorative shell | Overbuilding can increase print time, warping risk, and material cost |
| External power / serviceability mindset | `plasmadancom/HAT-RACK` | Power bus planning, service separation, rear reserve zone | Keeps power and service routing deliberate instead of hiding cables between modules | Industrial layout cues may be too bulky for the MVP footprint |
| Documentation and validation discipline | `cloudmesh-community/case` | Revision docs, BOM, assembly validation, test gates | Prevents CAD-first drift and forces physical checks before full print | Process overhead can delay CAD if not kept proportional to MVP scope |
| Mini PC + storage layout | N5 Mini / Jack Harvest | `minipc_stack_module`, future storage adjacency | Useful compact packaging reference for real mini PC plus storage workflows | HOLD until source, license, and dimensions are verified |
| Cable routing / rear service discipline | `plasmadancom/HAT-RACK`, current Rear Service Spine concept | Rear service reserved zone and per-module cable exits | Reduces chaotic cable paths and protects future DC bus planning | Rear zone may become overcrowded without strict reserved envelope rules |
| Future expansion without full reprint | Own stack-through-rod architecture, `istergiou/nas-rack` | Stack interface standard and module height units | Allows adding height by changing rods and adding modules instead of reprinting old modules | Middle-module removal remains limited in MVP because the stack must be loosened |

## 4. Iterative Application Plan

### Stage 0 - Documentation Freeze

Goal: freeze the rule that mk0.12 uses reference-informed design but does not copy external CAD.

Output artifacts:

- `REFERENCE_APPLICATION_PLAN.md`
- `REFERENCE_DECISIONS.md`
- `MVP_REQUIREMENTS.md`

Required decisions:

- External references are pattern libraries only.
- mk0.12 targets MVP-2M first, not a generic universal tower.
- Direct CAD import, fork, or geometry adaptation is prohibited unless license, source format, dimensions, and adaptation path are documented.
- CAD work must not start until the stack interface assumptions are written down.

### Stage 1 - Stack Interface Standard

Goal: create or describe the common stack-interface standard before module-specific CAD.

The standard must define:

- outer footprint;
- M5 rod pattern;
- washer/compression zones;
- airflow opening;
- rear service reserved zone;
- module height unit;
- top/bottom contact interface;
- future side-adapter reserve zones.

Prohibited in this stage:

- active rails;
- active sliding carriage;
- POM-C shoe sockets.

Engineering logic:

- The M5 rod pattern is a breaking interface. It must be stable before real modules are designed.
- The stack interface must reserve airflow and rear service volume from the beginning.
- Compression zones must be designed as load transfer areas, not incidental flat surfaces.

Validation gate:

- A written interface sketch/spec exists before any new part function is created.
- Every future module can identify its four rod clearances, washer no-go zones, airflow aperture, and cable exit zone.

### Stage 2 - Raspberry Pi + SSD Module Planning

Goal: plan `rpi_ssd_stack_module`.

Reference inputs:

- `ilikecake/RPi-Rack-Case`
- `TheCallumInglis/Rack_Mount_Pi`
- `HAT-RACK`

The plan must describe:

- Raspberry Pi mounting pattern;
- SSD mounting / strap area;
- cable exit to rear service zone;
- airflow clearance;
- access to SD card / USB / power if relevant;
- serviceability constraints.

Engineering logic:

- The Pi module should be a real device tray, not a placeholder shelf.
- SSD retention must be serviceable without relying on fragile snap-only plastic.
- Cable exits must point toward the rear service reserve rather than crossing the module cavity.

Validation gate:

- Pi board envelope, SSD envelope, fastener access, and cable bend space are documented.
- The module does not violate the Stage 1 stack interface.

### Stage 3 - Mini PC Module Planning

Goal: plan `minipc_stack_module`.

Reference inputs:

- N5 Mini / Jack Harvest as HOLD reference;
- `cloudmesh-community/case` for validation discipline;
- existing Homelab Modular Tower constraints.

The plan must describe:

- mini PC cradle/tray;
- strap/retainer logic;
- rear cable exit;
- heat/airflow clearance;
- center-of-mass risk;
- possibility of second mini PC in future.

Engineering logic:

- Mini PC thermal behavior dominates the MVP. It should not inherit Pi-rack assumptions.
- The module must hold device mass through a tray/strap/retainer concept compatible with M5 compression zones.
- A second future mini PC must remain possible by preserving the stack interface and module height logic.

Validation gate:

- Mini PC mass, approximate center of mass, cable exit direction, and airflow clearance are recorded before CAD.
- N5 Mini patterns remain HOLD until source/license/dimensions are verified.

### Stage 4 - Base / Top / Rod Hardware Planning

Goal: plan the structural stack assembly.

Reference inputs:

- `peter-mount/pi-rack` for load-bearing print reinforcement;
- `cloudmesh-community/case` for validation process.

The plan must describe:

- `base_pedestal`;
- `top_cap`;
- M5 rods;
- washers/nuts;
- replaceable rod length;
- TPU feet;
- future wider foot extensions;
- physical fit tests.

Engineering logic:

- Base and top parts are compression endpoints and alignment tools.
- Rod length must be replaceable so future height changes do not require reprinting existing modules.
- TPU feet and wider foot extensions must be planned as stability and vibration features, not decorative add-ons.

Validation gate:

- M5 rod clearance, washer seat diameter, nut access, and stack compression areas are coupon-tested before full print.

### Stage 5 - Rear Service Zone Planning

Goal: plan the rear service reserve.

Reference inputs:

- `HAT-RACK` for serviceability and power separation;
- current Homelab Modular Tower Rear Service Spine concept.

The plan must describe:

- rear reserved zone;
- cable windows per module;
- tie slots;
- strain relief placeholders;
- future DC power bus;
- why full-height rear spine should not be monolithic in MVP.

Engineering logic:

- MVP needs a disciplined rear reserve, but a monolithic full-height spine would make early iteration harder.
- Per-module cable windows allow each module to be tested independently.
- Tie slots and strain relief placeholders should be present early, while the final DC bus can remain a future service node.

Validation gate:

- Each MVP module has a documented rear cable exit.
- Cable routing does not pass randomly between modules.
- Future DC bus space is reserved without finalizing UPS or MikroTik geometry in mk0.12.

### Stage 6 - Physical Validation Plan

Goal: define tests before any full print.

Reference inputs:

- `cloudmesh-community/case`;
- `peter-mount/pi-rack`.

Required validation steps:

- print small coupons first;
- M5 rod clearance test;
- washer compression test;
- PETG shrink/tolerance test;
- airflow visual continuity test;
- cable routing mock test;
- mini PC weight/tilt test;
- slicer preview requirement;
- no full print before coupon validation.

Engineering logic:

- mk0.12 should move toward physical MVP confidence, not just visual CAD completion.
- Coupon tests isolate tolerance and compression risks before wasting material on large parts.
- Slicer preview is mandatory because top/bottom rings, bridges, and long thin features can fail even when the CAD model is valid.

Validation gate:

- Full MVP print is blocked until coupon results and slicer preview are documented.

## 5. Go / No-Go Rules

Do not copy external CAD geometry directly unless license, source format, dimensions, and adaptation path are verified.
Do not introduce active rails or sliding carriage in mk0.12.
Do not make rear service spine monolithic for MVP.
Do not add decorative panels before structural validation.
Do not finalize UPS/MikroTik modules in mk0.12.
Do not change M5 rod pattern after Stage 1 without documenting a breaking interface revision.

Additional gates:

- GO only if the stack interface is stable enough for both MVP modules.
- GO only if all new dimensions can be represented in `cad/config.py`.
- PARTIAL only if a reference pattern can be translated into Homelab Modular Tower constraints without importing geometry.
- HOLD if license, source format, measured dimensions, or physical adaptation path are unclear.
- NO-GO if a pattern makes middle-module access better by breaking the MVP compression stack, rod pattern, airflow path, or rear service reserve.

## 6. CAD Impact Plan

This section lists files that may appear in a future CAD iteration. They must not be created as part of this documentation-only task.

| Future File | Purpose |
| --- | --- |
| `cad/parts/stack_interface.py` | Shared stack interface definitions and helper geometry for footprint, M5 rod pattern, washer/compression zones, airflow opening, rear service reserve, and contact surfaces. |
| `cad/parts/base_pedestal.py` | Bottom compression endpoint, rod alignment base, fan/intake or clearance planning area, TPU foot interface, and future wider-foot attachment reserve. |
| `cad/parts/top_cap.py` | Top compression endpoint, rod alignment cap, exhaust/fan or airflow clearance planning area, and washer/nut service access. |
| `cad/parts/module_rpi_ssd.py` | Raspberry Pi + SSD stack module with board mounting, SSD retention, airflow clearance, rear cable exit, and service access. |
| `cad/parts/module_minipc.py` | Mini PC stack module with cradle/tray, strap or retainer logic, heat/airflow clearance, rear cable exit, and center-of-mass considerations. |
| `cad/assembly/mvp_2_module_stack.py` | MVP-2M assembly showing `base_pedestal`, `rpi_ssd_stack_module`, `minipc_stack_module`, `top_cap`, rods, washers, and nuts. |

CAD rules for the future implementation:

- All dimensions must be defined in `cad/config.py`.
- Each part must expose separate part functions.
- Assembly must stay separate from part definitions.
- No magic numbers are allowed inside part functions.
- Export artifacts are derived and must not become the source of truth.
- STEP/STL/PNG generation should happen only after the planned CAD stage needs it.

## 7. Risks and Mitigations

| Risk | Source | Impact | Mitigation | Validation |
| --- | --- | --- | --- | --- |
| Reference projects are not direct CAD bases | External reference audit | Copying geometry could break project architecture and licensing assumptions | Treat references as patterns only | Review Stage 0 decisions before CAD starts |
| N5 Mini source/license not verified | N5 Mini / Jack Harvest | Mini PC/storage patterns may be unusable legally or technically | Keep as HOLD until source, license, and dimensions are verified | Record verification result before using any specific geometry idea |
| Stack-through-rod limits serviceability | Own MVP architecture | Middle modules cannot be removed without loosening the stack | Accept for MVP and document as known tradeoff | Assembly/service mock test |
| Adding modules requires longer rods | Own MVP architecture | Future expansion changes hardware length and stack compression setup | Use replaceable rods and stable module height units | Rod length planning table in future `MVP_REQUIREMENTS.md` |
| Rear cable zone may become overcrowded | Rear Service Spine concept | Cables may block airflow or module fit | Reserve rear envelope and define per-module windows | Cable routing mock test |
| Mini PC heat may dominate airflow | Mini PC module | Thermal throttling or heat soak in upper modules | Prioritize mini PC airflow clearance and avoid Pi-rack assumptions | Airflow visual continuity test and later thermal observation |
| Top/bottom rings may create print bridges | Base/top stack geometry | Failed prints, sagging bridges, poor washer seats | Add slicer preview gate and avoid unsupported spans | Slicer preview plus coupon print |
| PETG shrink may affect M5 clearance | PETG printing | Rods may bind or washer seats may not fit | Coupon-test rod holes and washer pockets before full print | M5 rod clearance and washer compression coupons |
| Center of mass may rise with future modules | Stack expansion | Tower tipping risk increases | Plan TPU feet and future wider foot extensions | Mini PC weight/tilt test |
| Future UPS module may require bottom placement | Power architecture | Later UPS module may force stack order changes | Do not finalize UPS in mk0.12; preserve bottom-placement option | Future revision requirement review |

## 8. Final Recommendation

Proceed with mk0.12 as MVP-2M Reference-Informed Stack.
Use external projects only as pattern references.
Do not fork or adapt any external CAD as the primary base.
First CAD implementation should target stack interface + two real modules, not a generic universal module.
