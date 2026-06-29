# mk0.12 MVP Engineering Spec

> NOTE:
> This file is the consolidated mk0.12 specification snapshot.
> The active revision-scoped documents are now located under `revisions/mk0.12/`.
> For new CAD work, read `revisions/mk0.12/README.md` first.
>
> ACTIVE SOURCE OF TRUTH:
> For new mk0.12 CAD work, use the revision-scoped documents under `revisions/mk0.12/`.
> This file is a consolidated legacy/reference snapshot only.
> If this file conflicts with the revision-scoped documents, the revision-scoped documents win.
> If a requirement appears ambiguous, preserve the stricter interpretation and verify against `VALIDATION_GATES.md`.

This document is the concrete engineering specification for the future mk0.12 CAD implementation. It supersedes `REFERENCE_APPLICATION_PLAN.md` as the technical input for CAD work, while `REFERENCE_APPLICATION_PLAN.md` remains the reference-pattern and decision context.

No CAD geometry is implemented by this document. No STEP/STL/PNG export is required by this document.

## 1. Scope

mk0.12 is an MVP-2M stack-through-rod construction for:

- `rpi_ssd_stack_module`
- `minipc_stack_module`

Stack order, bottom to top:

```text
Z
238  top_cap top plane
212  top_cap bottom / minipc_stack_module top
107  minipc_stack_module bottom / rpi_ssd_stack_module top
32   rpi_ssd_stack_module bottom / base_pedestal top
0    base_pedestal bottom plane
```

Plastic parts are not the primary structural material. The primary load path is:

```text
M5 rods -> washers -> nuts -> compression pads -> top/bottom contact interfaces -> reinforced corner zones
```

Plastic parts provide:

- module positioning;
- device support;
- airflow geometry;
- cable routing geometry;
- washer/compression interfaces;
- future side-adapter/rail reserve zones without active rails.

Airflow rule for mk0.12:

```text
Base and top must provide 120 x 120 fan-compatible intake/exhaust zones.
Internal modules are not required to preserve a completely empty 120 x 120 vertical shaft.
Internal airflow may be implemented as equivalent distributed airflow area using:
- raised device supports;
- ribs;
- perforated trays;
- side bypass channels;
- bottom gaps under devices;
- ducted/split airflow around the mini PC.
```

Engineering intent: mk0.12 uses 120 x 120 fan-compatible inlet/outlet geometry, but equivalent distributed airflow through modules.

Fan envelope rule:

```text
FAN_ENVELOPE_SIZE = 120
FAN_SCREW_PATTERN = 105
FAN_SCREW_CENTER_OFFSET = 52.5
FAN_SCREW_BOSS_DIAMETER_MIN_ASSUMPTION = 10
FAN_SCREW_BOSS_DIAMETER_MAX_ASSUMPTION = 14
FAN_AIRFLOW_CUTOUT_DIAMETER_MIN_ASSUMPTION = 100
FAN_AIRFLOW_CUTOUT_DIAMETER_MAX_ASSUMPTION = 110

FAN_ENVELOPE_SIZE is not the same as a full square airflow cutout.
120 mm fan-compatible zone means the part reserves a 120 x 120 fan envelope and 105 x 105 screw pattern.
The actual airflow cutout must preserve material around fan screw bosses.
Do not implement the airflow cutout as a full 120 x 120 square void if fan mounting holes are implemented.
Use a circular, rounded-square, grille, or segmented cutout that preserves screw boss material around (+/-52.5, +/-52.5).
```

## 2. Coordinate System

All dimensions are in millimetres.

```text
X      left/right
Y      front/back
Z      vertical
Origin center of tower footprint at base bottom plane
Front  negative Y
Rear   positive Y
Left   negative X
Right  positive X
```

Global footprint:

```text
Outer X range = -95 to +95
Outer Y range = -95 to +95
Rear service zone = Y +65 to +95
Front device/service-free edge = Y -95
Base/top fan-compatible airflow zone = X -60 to +60, Y -60 to +60
M5 rod centers = (-80, -80), (+80, -80), (-80, +80), (+80, +80)
```

Fan-aligned zone terminology:

```text
FAN_ALIGNED_AIRFLOW_ZONE is not the same as ACTUAL_FAN_AIRFLOW_CUTOUT.
The zone reserves the 120 x 120 fan envelope and alignment area.
The actual cutout is separate geometry and must preserve fan screw boss material around the 105 x 105 screw pattern.
Do not interpret the 120 x 120 zone as an instruction to cut a full 120 x 120 square void.
```

Rear service rule:

```text
Rear service zone is a reserved Y envelope, not a completely empty full-width rectangular prism.
Rear M5 rods and compression pads create keepout zones inside this envelope.
Cable paths must be segmented around rear rod/compression-pad keepouts.
Primary cable routing should prefer the central rear region, away from X +/-80 rod columns.
```

## 3. Assumptions and Current Config Comparison

`cad/config.py` currently reports `CURRENT_REVISION = "mk0.9.3"`. mk0.12 constants are not yet implemented in CAD. Therefore this document freezes the requested mk0.12 starting values as engineering assumptions for the next CAD task.

| Parameter | mk0.12 Spec Value | Current `cad/config.py` Nearby Value | Status | Note |
| --- | ---: | ---: | --- | --- |
| `TOWER_OUTER_WIDTH` | 190 | `TOWER_WIDTH = 190.0`, `OUTER_WIDTH = 190.0` | PASS | Matches current global footprint. |
| `TOWER_OUTER_DEPTH` | 190 | `TOWER_DEPTH = 190.0`, `OUTER_DEPTH = 190.0` | PASS | Matches current global footprint. |
| `REAR_SERVICE_DEPTH` | 30 | `REAR_RESERVED_DEPTH = 30.0` | PASS | Matches current rear reserve. |
| `PREFERRED_DEVICE_ZONE_WIDTH` | 150 | no exact mk0.12 constant | ASSUMPTION | Preferred non-hard X -75 to +75 planning zone. Device-specific validated clearance envelopes are authoritative. |
| `PREFERRED_DEVICE_ZONE_DEPTH` | 140 | no exact mk0.12 constant | ASSUMPTION | Preferred non-hard Y -75 to +65 planning zone; rear edge touches service boundary. |
| `FAN_ALIGNED_AIRFLOW_ZONE_WIDTH` | 120 | `AIRFLOW_CHANNEL_WIDTH = 125.0` | PARTIAL | mk0.12 uses a 120 mm base/top fan-aligned zone, not an internal mandatory empty shaft. |
| `FAN_ALIGNED_AIRFLOW_ZONE_DEPTH` | 120 | `AIRFLOW_CHANNEL_DEPTH = 125.0` | PARTIAL | mk0.12 uses a 120 mm base/top fan-aligned zone, not an internal mandatory empty shaft. |
| `M5_ROD_DIAMETER` | 5 | `ROD_DIAMETER = 5.0` | PASS | Matches. |
| `M5_ROD_CLEARANCE_DIAMETER` | 5.6 | `ROD_CLEARANCE = 5.6` | PASS | Matches. |
| `M5_ROD_CENTER_OFFSET_X/Y` | 80 | `ROD_CENTER_OFFSET = 14.0` | FAIL | Current mk0.9.3 rod model is not the requested corner through-rod pattern. |
| `M5_WASHER_OUTER_DIAMETER` | 12 | `M5_WASHER_DIAMETER = 12.0` | PASS | Matches. |
| `M5_WASHER_SEAT_DIAMETER` | 13 | no exact current constant | ASSUMPTION | Seat diameter is washer diameter + 1 mm clearance. |
| `M5_WASHER_SEAT_DEPTH` | 1.2 | `M5_WASHER_SEAT_DEPTH = 1.8` | PARTIAL | mk0.12 requested value is shallower. |
| `BASE_PEDESTAL_HEIGHT` | 32 | `BASE_PEDESTAL_HEIGHT = 24.0`, `BASE_MODULE_HEIGHT = 48.0` | FAIL | mk0.12 requested base is a new MVP dimension. |
| `RPI_SSD_MODULE_HEIGHT` | 75 | `RPI_SSD_MODULE_HEIGHT = 70.0` | PARTIAL | mk0.12 adds 5 mm service/clearance height. |
| `MINIPC_MODULE_HEIGHT` | 105 | `MINI_PC_MODULE_HEIGHT = 82.0` | FAIL | mk0.12 needs more height for mini PC clearance. |
| `TOP_CAP_HEIGHT` | 26 | `TOP_CAP_HEIGHT = 20.0`, `ROOF_MODULE_HEIGHT = 46.0` | PARTIAL | mk0.12 uses a new cap height. |
| `MINI_PC_PLACEHOLDER` | 130 x 130 x 55 | current `MINI_PC_PLACEHOLDER_* = 130 x 130 x 55` | PASS | Matches current placeholder. |
| Raspberry Pi 3B board | 85 x 56 | `RPI3B_BOARD_WIDTH = 85.0`, `RPI3B_BOARD_DEPTH = 56.0` | PASS | Matches current board constants. |

ASSUMPTION: all mk0.12 values in this document must later be moved into `cad/config.py` with explicit names before CAD part functions are implemented.

## 4. Frozen MVP Dimensions

```text
TOWER_OUTER_WIDTH = 190
TOWER_OUTER_DEPTH = 190
REAR_SERVICE_DEPTH = 30
REAR_SERVICE_ZONE_Y_MIN = +65
REAR_SERVICE_ZONE_Y_MAX = +95
REAR_ROD_KEEPOUT_CENTER_Y = +80
REAR_ROD_KEEPOUT_CENTER_X = +/-80
REAR_ROD_KEEPOUT_RADIUS_MIN_ASSUMPTION = 12
REAR_ROD_KEEPOUT_RADIUS_MAX_ASSUMPTION = 15
PRIMARY_REAR_CABLE_CORRIDOR_X_MIN_PREFERRED = -60
PRIMARY_REAR_CABLE_CORRIDOR_X_MAX_PREFERRED = +60
PRIMARY_REAR_CABLE_CORRIDOR_X_MIN_ABSOLUTE_ASSUMPTION = -65
PRIMARY_REAR_CABLE_CORRIDOR_X_MAX_ABSOLUTE_ASSUMPTION = +65

PREFERRED_DEVICE_ZONE_WIDTH = 150
PREFERRED_DEVICE_ZONE_DEPTH = 140

FAN_ALIGNED_AIRFLOW_ZONE_WIDTH = 120
FAN_ALIGNED_AIRFLOW_ZONE_DEPTH = 120
INTERNAL_AIRFLOW_STRATEGY = "equivalent_distributed_airflow"
FAN_ENVELOPE_SIZE = 120
FAN_SCREW_PATTERN = 105
FAN_SCREW_CENTER_OFFSET = 52.5
FAN_SCREW_BOSS_DIAMETER_MIN_ASSUMPTION = 10
FAN_SCREW_BOSS_DIAMETER_MAX_ASSUMPTION = 14
FAN_AIRFLOW_CUTOUT_DIAMETER_MIN_ASSUMPTION = 100
FAN_AIRFLOW_CUTOUT_DIAMETER_MAX_ASSUMPTION = 110

M5_ROD_DIAMETER = 5
M5_ROD_CLEARANCE_DIAMETER = 5.6
M5_ROD_CENTER_OFFSET_X = 80
M5_ROD_CENTER_OFFSET_Y = 80

M5_WASHER_OUTER_DIAMETER = 12
M5_WASHER_SEAT_DIAMETER = 13
M5_WASHER_SEAT_DEPTH = 1.2

CORNER_COMPRESSION_PAD_SIZE_X = 24
CORNER_COMPRESSION_PAD_SIZE_Y = 24
CORNER_COMPRESSION_PAD_HEIGHT = 3

BASE_PEDESTAL_HEIGHT = 32
RPI_SSD_MODULE_HEIGHT = 75
MINIPC_MODULE_HEIGHT = 105
TOP_CAP_HEIGHT = 26

TOTAL_STACK_HEIGHT = 238
ROD_EXTRA_THREAD_ALLOWANCE_BOTTOM = 8
ROD_EXTRA_THREAD_ALLOWANCE_TOP = 12
MINIMUM_FUNCTIONAL_M5_ROD_LENGTH = 260
RECOMMENDED_M5_ROD_LENGTH = 270
SAFE_CUT_TO_FIT_M5_ROD_LENGTH = 280
```

Preferred device zone rule:

```text
PREFERRED_DEVICE_ZONE is not a hard keepout.
Validated device clearance envelopes may extend outside it if they remain inside the 190 x 190 footprint and do not violate M5 rod keepouts, rear service zone, airflow requirements, or tool/access constraints.
Device-specific clearance envelopes in Component Geometry are the source of truth for placement validation.
Do not move device placements in this specification cleanup.
```

M5 rod length interpretation:

```text
260 mm is a functional minimum for CAD envelope validation only.
For physical build, use 270-280 mm rods and trim if needed.
The final physical rod length depends on washer thickness, nut type, thread engagement, PETG tolerances, possible nyloc nuts, and actual stack compression.
```

Baseline geometry freeze:

```text
M5 rod pattern remains frozen at +/-80 for mk0.12.
Do not move rods inward in this documentation update.
If washer/compression validation fails, reinforce washer/compression zones locally instead of changing the rod pattern.
```

## Footprint Containment Rules

All active PETG mk0.12 stack bodies must remain inside the frozen 190 x 190 mm footprint.

Allowed XY bounds for printable plastic:

```text
X = -95 to +95
Y = -95 to +95
```

No active PETG printable feature of `base_pedestal`, `rpi_ssd_stack_module`, `minipc_stack_module`, or `top_cap` may extend outside the frozen 190 x 190 mm footprint.

Separate TPU feet, future wider foot extensions, or future stability parts must be documented as separate printable parts and exported separately. They must not be silently merged into the active PETG stack body.

For active mk0.12 PETG stack bodies:

- expected bounding box X size = 190 mm maximum;
- expected bounding box Y size = 190 mm maximum;
- any printable body bounding box above 190.5 mm in X or Y is FAIL;
- any active PETG feature outside X/Y +/-95.25 is FAIL;
- separate future extension parts are out of active mk0.12 printable body unless explicitly documented;
- review/render artifacts may include reference geometry outside the footprint only if it is not part of printable STL/body.

The previous CAD skeleton behavior where printable parts grew to approximately 205 x 205 mm is a design failure. Ribbed-frame construction must reduce mass without breaking the frozen outer interface.

Naming note for future config:

```text
Do not use CENTRAL_AIRFLOW_OPENING_* for internal mandatory empty shaft logic.
Use FAN_ALIGNED_AIRFLOW_ZONE_* for base/top fan-compatible zones.
Use INTERNAL_AIRFLOW_STRATEGY for module airflow strategy.

INTERNAL_AIRFLOW_STRATEGY is a named strategy value for config/documentation use, not a geometric object by itself.
CAD must implement this strategy through real openings, slots, perforations, side bypass channels, bottom gaps, or ducted/split airflow.

CENTRAL_AIRFLOW_OPENING_* must not be introduced as active mk0.12 config constants unless a future breaking interface revision explicitly changes the airflow model.
```

## Printed Part Construction Rules

mk0.12 CAD skeleton v3 must transition from solid block / closed slab geometry to ribbed-frame / open tray construction.

Required construction rule:

```text
mk0.12 printed modules must be ribbed-frame parts, not solid monolithic blocks.
Each module must be printable as a connected lightweight structure.
Large solid slabs are prohibited unless explicitly justified by a structural function.
Device placeholders must not be part of printable geometry.
Printable STL exports must contain only printable plastic geometry.
Reference geometry must be separate and used only in assembly/review.
```

Baseline PETG/FDM thickness assumptions for mk0.12 CAD skeleton v3:

```text
NOMINAL_WALL_THICKNESS = 3.0
STRUCTURAL_WALL_THICKNESS = 4.0
TRAY_FLOOR_THICKNESS = 3.0
LOCAL_REINFORCED_LAND_THICKNESS_MIN = 5.0
LOCAL_REINFORCED_LAND_THICKNESS_MAX = 6.0
RIB_THICKNESS = 3.0
RIB_HEIGHT_MIN = 8.0
RIB_HEIGHT_MAX = 15.0
MIN_PRINTABLE_WEB_THICKNESS = 2.4
MIN_AIRFLOW_SLOT_WIDTH = 8.0
MIN_CABLE_WINDOW_WIDTH = 12.0
MIN_CABLE_WINDOW_HEIGHT = 10.0
PREFERRED_CABLE_WINDOW_HEIGHT = 15.0
MIN_REAR_SERVICE_VERTICAL_PASSAGE_HEIGHT_PER_MODULE = 20.0
MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN = 20.0
MIN_SERVICE_ACCESS_WINDOW_WIDTH = 25.0
```

Interpretation:

- 3 mm is the normal starting wall/floor thickness for PETG MVP parts;
- 4 mm is reserved for loaded walls, frames, and compression paths;
- 5 to 6 mm is allowed only for local washer seats, bosses, compression lands, and tool-access pads;
- do not make an entire module 6+ mm thick;
- reinforcement must be local through ribs, bosses, pads, and lands instead of a monolithic block.

### Minimum Rib Layout

Each printable module must include a clear load-path-aware rib layout. Ribs are not decorative. They must connect compression, frame, device-support, airflow-window, and service-window zones.

Each printable module must include:

- outer perimeter frame using nominal or structural wall thickness;
- four M5 corner compression islands;
- ribs from each M5 corner compression island to adjacent perimeter frame walls;
- at least two transverse ribs connecting left/right frame walls where they do not block device placement;
- at least two longitudinal ribs connecting front/rear frame walls where they do not block rear service windows;
- device support ribs or rails instead of a solid tray;
- rear service window edges reinforced by ribs or frame lips;
- airflow openings framed by ribs so they do not create floppy unsupported webs.

Base and top cap minimum rib layout:

```text
Base and top cap must behave like frame plates with local compression lands, not solid slabs.
Fan cutout/opening edges must be connected to perimeter/corner structure through ribs or a frame ring.
```

RPi/SSD module minimum rib layout:

```text
RPi/SSD support must use bosses, local pads, ribs, and open tray regions.
A full solid floor under the Pi/SSD is not allowed unless perforated and justified.
```

Mini PC module minimum rib layout:

```text
Mini PC support must use rails/ribs/pads with visible bottom/side airflow gaps.
A full solid floor under the Mini PC is not allowed unless perforated and paired with side bypass.
```

Rib layout status criteria:

```text
No clear rib path from M5 compression islands to frame: FAIL.
Device support implemented as near-solid tray without airflow relief: FAIL.
Rib layout exists but blocks service/cable windows: PARTIAL or FAIL depending severity.
```

#### M5 Compression Island Rib Direction Rules

M5 compression islands are located near the footprint corners at X/Y +/-80. They are not central nodes. Therefore ribs must not be generated radially in all directions.

Ribs from corner M5 compression islands may connect only to:

- adjacent perimeter frame walls inside the 190 x 190 footprint;
- inward ribs toward the internal frame;
- diagonal inward ribs toward a fan ring, device support frame, or internal cross-rib;
- local reinforced lands around washer seats.

Ribs from M5 compression islands must not:

- protrude outside X/Y +/-95;
- extend outward beyond the perimeter frame;
- create external tabs or spikes;
- terminate outside the printable footprint;
- become decorative star-shaped spokes around the M5 tower.

Criteria:

```text
Any outward rib or tab from an M5 compression island that extends beyond the frozen footprint is FAIL.
Any M5 rib that does not connect to a valid load path is FAIL.
Any automatically generated radial rib pattern around a corner rod guide is FAIL unless all outward directions are clipped and the remaining ribs connect to valid structural nodes.
```

#### Rib Endpoint Validity Rules

Every structural rib must have two valid endpoints.

A valid rib endpoint may connect to:

- outer perimeter frame;
- M5 compression island;
- local reinforced land;
- fan ring / airflow opening frame;
- transverse rib;
- longitudinal rib;
- device support rail or boss pad;
- rear service window frame lip;
- cable window frame lip;
- internal frame ring;
- another documented structural rib junction.

Invalid endpoints:

- free-floating end in open air;
- tiny isolated tab;
- endpoint outside the 190 x 190 footprint;
- endpoint that touches only reference geometry;
- endpoint that terminates in an unsupported thin web below MIN_PRINTABLE_WEB_THICKNESS;
- endpoint that blocks cable/service/airflow access without documented reason.

Criteria:

```text
A rib with one invalid endpoint is FAIL.
A rib that visually appears to hang in air must be treated as FAIL until CAD topology proves it is connected to a valid structural node.
A rib that connects only to reference geometry does not count as structurally connected.
```

#### Dangling, Floating, Decorative, or Unfinished Ribs

Dangling, floating, decorative, or unfinished ribs are not allowed.

A rib must exist for one of these reasons:

- transferring compression load from M5 island to perimeter/internal frame;
- supporting a device boss/pad/rail;
- framing an airflow opening;
- framing a rear service/cable window;
- tying fan ring/screw boss material to the perimeter frame;
- preventing a known flexible web from vibrating or warping.

Ribs that do not serve one of these roles are not part of the engineering skeleton and should be removed.

Criteria:

```text
Decorative rib without clear structural/service/airflow role: PARTIAL or FAIL.
Floating rib: FAIL.
Rib that blocks required airflow/cable/service access: FAIL.
Rib that creates a sharp external protrusion: FAIL.
```

Connected printable body rule:

```text
Each printable module STL should normally be one connected printable body.
Disconnected bodies are FAIL unless explicitly documented as intentionally separate printable sub-parts.
Reference placeholders do not count as printable bodies.
```

Current mk0.12 printable-body expectation:

```text
base_pedestal: one connected PETG printable body
rpi_ssd_stack_module: one connected printable body
minipc_stack_module: one connected printable body
top_cap: one connected printable body
TPU feet: separate TPU printable parts, not part of the PETG base_pedestal body
```

TPU feet separation rule:

```text
base_pedestal is one connected PETG printable body.
TPU feet are separate TPU printable parts.
TPU feet must not be included in the PETG base_pedestal STL.
base_pedestal may include PETG sockets, pads, pilot holes, or mounting features for TPU feet.
Disconnected TPU feet are allowed because they are separate printable parts, not part of the PETG base body.
```

## Printable STL Topology Requirements

Each printable STL/body must be:

- one connected printable component;
- watertight/manifold;
- free of self-intersections;
- free of non-manifold edges;
- free of zero-thickness faces;
- free of floating internal fragments;
- free of reference geometry.

Watertight failure is FAIL for printable parts.

The previous CAD skeleton v2 produced a not-watertight `rpi_ssd_stack_module`. This is a blocking defect and must not be repeated.

Criteria:

```text
Connected component count != 1: FAIL.
Watertight == false: FAIL.
Printable STL contains reference objects: FAIL.
```

## Printable vs Reference Geometry Separation

Printable geometry and reference geometry must be separated before the next CAD skeleton cleanup is accepted.

Requirements:

```text
Printable part builders must not include device placeholders.
Device placeholders must be built by separate reference functions.
M5 rods, washers, nuts, Raspberry Pi, SSD, and Mini PC placeholders are non-printable assembly/reference geometry.
STL exports for printed parts must exclude all reference geometry.
Assembly may include reference geometry for visual checking.
```

Desired future builder split:

```python
build_base_pedestal()
build_rpi_ssd_stack_module()
build_minipc_stack_module()
build_top_cap()

build_rpi3b_placeholder()
build_external_ssd_placeholder()
build_minipc_placeholder()
build_120mm_fan_placeholder()
build_120mm_fan_screw_pattern_placeholder()
build_m5_rods_placeholder()
build_washers_placeholder()
build_nuts_placeholder()
```

If current or future CAD functions already use similar names, they must be brought into this principle: printable builders return printable plastic only, while reference builders return review/assembly geometry only.

Fan reference rule:

```text
Fan placeholder/reference solids must not be part of printable STL.
Fan screw holes/bosses are printable geometry only if fan mounting is active in the corresponding part.
Fan placeholder geometry is for assembly/review only.
The fan-aligned 120 x 120 zone is a placement/alignment envelope, not a full square cutout instruction.
```

## Assembly and Device Mounting Access

Modules must not become closed boxes around devices. A real device must be installable, connected, inspected, and removed without cutting plastic or forcing cables through closed walls.

Global access requirements:

```text
Modules must include service/access windows sufficient for mounting and cable routing.
A device must be installable without cutting plastic or forcing cables through closed walls.
Mounting screws/bosses must be reachable by tool or fingers.
Cable exits must be open before final stack compression.
No module may be a closed box around the device unless a removable cover/access path is defined.
```

Minimum tool/finger access envelope:

```text
MIN_TOOL_ACCESS_DIAMETER_AROUND_M2_5_BOSS = 8.0
MIN_TOOL_ACCESS_DIAMETER_AROUND_M3_BOSS = 9.0
MIN_FINGER_ACCESS_SLOT_WIDTH = 18.0
MIN_STRAP_PULL_TAB_ACCESS_WIDTH = 15.0
MIN_STRAP_PULL_TAB_ACCESS_DEPTH = 20.0
MIN_RETAINER_CLEARANCE_AROUND_SCREW_OR_CLIP = 10.0
```

Access requirements:

```text
Mounting bosses must not be surrounded by walls that prevent screwdriver access.
SSD straps, retainers, and Mini PC retainers must have finger/tool access.
A screw or clip that can only be reached before another permanent/stacked part is installed must be documented as assembly-order dependent.
```

Access status criteria:

```text
Tool access below minimum: FAIL.
Tool access meets minimum but is only possible before stack compression: PARTIAL and must be documented.
Tool access remains possible during normal pre-compression assembly: PASS.
```

RPi/SSD module access requirements:

```text
Raspberry Pi mounting area must have tool access to mounting bosses.
SSD strap/retainer area must be reachable from top/front/side.
USB/power cable route to rear service zone must be visible and open.
The module must not be a closed solid tray under the Pi/SSD.
```

Mini PC module access requirements:

```text
Mini PC must be insertable/removable before final stack compression.
Retainers/straps must be accessible.
Rear ports must have open cable exit toward rear service zone.
There must be a visible bottom/side airflow gap around the Mini PC.
The module must not fully enclose the Mini PC without a removable access strategy.
```

### Stack Assembly Service Model

mk0.12 is a stack-through-rod MVP, not a hot-swappable blade chassis.

Requirements:

```text
mk0.12 is not hot-swappable.
Middle module removal without loosening the stack is out of scope.
Therefore, all primary device installation and cable connection operations must be possible before final stack compression.
After final stack compression, only inspection, external cable adjustment, and minor strain relief adjustment are expected.
The CAD must not require primary device installation after the stack has already been fully compressed.
```

Failure criteria:

```text
If a device cannot be installed into its module before stack compression, the design is FAIL.
If a cable cannot be routed to the rear service zone before final compression, the design is FAIL.
If a retainer/strap requires access that becomes blocked by the next module, the required assembly order must be documented.
```

## Airflow and Rear Service Open-Geometry Requirements

Distributed airflow must be represented by real open geometry, not only by labels, annotations, or visual placeholders.

Airflow requirements:

```text
Each module must include actual airflow openings, slots, perforations, or bypass channels.
A solid tray under a heat-producing device is not acceptable unless it includes perforation, side bypass, or bottom gap.
Mini PC module must include explicit side/bottom/top airflow clearance.
RPi/SSD module must include perforation or open ribbed tray regions.
Total internal open area is not numerically frozen in mk0.12, but airflow path must be visibly open in CAD skeleton v3.
Airflow windows must not compromise M5 compression pads.
Airflow windows must not remove fan screw boss material.
```

Effective airflow open-area sanity gate:

```text
Distributed airflow must not be represented by symbolic or tiny openings.
CAD skeleton v3 must expose a minimum effective open area per module.
This is not CFD validation, but a geometric sanity check.

MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_ABSOLUTE = 2500 mm2
MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_PREFERRED = 4000 mm2
MINIPC_MODULE_AIRFLOW_OPEN_AREA_MIN = 5000 mm2
```

Reference areas:

```text
A circular opening of diameter 100 mm is approximately 7850 mm2.
A circular opening of diameter 110 mm is approximately 9500 mm2.
Small token slots are not acceptable if their total area is below the absolute minimum.
```

Open-area status criteria:

```text
Below absolute minimum: FAIL.
Between absolute and preferred: PARTIAL, requires review.
Above preferred: PASS for geometric open-area sanity, thermal testing still required.
```

Open area must not remove or weaken:

- M5 compression pads;
- fan screw boss material;
- device mounting bosses;
- rear rod keepout structure.

Rear service requirements:

```text
Each module must provide real rear service windows into the reserved zone.
Cable route must not be represented only by an annotation.
Rear service access must avoid rear rod keepouts.
Cable windows must remain open through the stack unless intentionally blocked by a documented feature.
Cable windows must be defined by both width and height.
A cable window that only satisfies width but has insufficient height is not acceptable.
Mini PC rear cable exit must reserve enough vertical space for power/Ethernet/USB/HDMI connector bodies and bend relief.

MIN_CABLE_WINDOW_WIDTH = 12.0
MIN_CABLE_WINDOW_HEIGHT = 10.0
PREFERRED_CABLE_WINDOW_HEIGHT = 15.0
MIN_REAR_SERVICE_VERTICAL_PASSAGE_HEIGHT_PER_MODULE = 20.0
MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN = 20.0
MIN_SERVICE_ACCESS_WINDOW_WIDTH = 25.0
PRIMARY_REAR_CABLE_CORRIDOR_X_MIN_PREFERRED = -60
PRIMARY_REAR_CABLE_CORRIDOR_X_MAX_PREFERRED = +60
```

Cable-window status criteria:

```text
Cable window height below 10 mm: FAIL.
Cable window height 10-15 mm: PARTIAL.
Cable window height >=15 mm: PASS for skeleton geometry, physical cable test still required.
Mini PC rear cable exit height below MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN is FAIL unless specific low-profile/angled cables are documented.
```

## Volume and Mass Sanity Requirements

CAD skeleton v3 must avoid kilogram-scale solid printed modules. The goal is not final mass optimization, but no MVP skeleton part should resemble a near-solid 190 x 190 x module-height block.

Requirements:

```text
Large solid volumes are FAIL unless justified by an explicit structural function.
Printed parts should use frames, ribs, bosses, pads, and local lands.
Base/top should be obviously frame-like, not solid slabs.
RPi/SSD and Mini PC modules should be open trays/frames, not solid filled volumes.
Volume/mass check should be added to CAD review.
Final production-optimized mass is not frozen.
However, mk0.12 CAD skeleton v3 mass sanity gates are frozen for validation.
```

Warning-level mass sanity thresholds:

```text
Any single printable module estimated above 300-500 g PETG should be flagged PARTIAL for review.
Any single printable module estimated above 800 g PETG should be flagged FAIL unless explicitly justified.
```

mk0.12 CAD skeleton v3 must use per-part mass budget as a sanity gate. The values below are not final production optimization targets, but they prevent accidental return to near-solid printed blocks.

| Printable part | Target PETG mass | Soft review limit | Hard FAIL limit |
| --- | ---: | ---: | ---: |
| `base_pedestal` | 120-220 g | 300 g | >500 g |
| `rpi_ssd_stack_module` | 150-300 g | 400 g | >800 g |
| `minipc_stack_module` | 250-450 g | 600 g | >800 g |
| `top_cap` | 100-200 g | 300 g | >500 g |
| total printed PETG | 620-1170 g | ~1600 g | >2500 g NO-GO |

Mass budget interpretation:

```text
If a part exceeds the soft review limit, it must be flagged PARTIAL and justified.
If a part exceeds the hard FAIL limit, the CAD iteration is rejected unless the mass is explicitly justified by a structural function and approved in review.
The previous kilogram-scale skeleton behavior is considered a design failure, not an optimization detail.
```

## 5. Required Engineering Decisions

### Decision 1

mk0.12 uses custom stack-through-rod architecture, not an external CAD base.

Status: PASS

### Decision 2

No active rails, no sliding carriage, no POM-C shoe sockets in mk0.12.

Status: PASS

### Decision 3

MVP contains exactly two real modules:

- Raspberry Pi + SSD
- Mini PC

Status: PASS

### Decision 4

Rear service spine is reserved but not monolithic in MVP.

Status: PASS

### Decision 5

Future expansion is achieved by:

- adding new stack modules;
- using longer M5 rods;
- keeping the same M5 pattern;
- keeping the same outer footprint;
- keeping the same rear service zone.

Status: PASS

### Decision 6

Middle module removal without stack loosening is explicitly out of scope for MVP.

Status: PASS

## 6. Component Table

| Component | Qty | Outer Size | Height | Main Function | Critical Interfaces | MVP Status |
| --- | ---: | --- | ---: | --- | --- | --- |
| `base_pedestal` | 1 | 190 x 190 | 32 | Bottom structural locator, intake, lower washer/nut zones | M5 rods, lower washers/nuts, RPi/SSD bottom interface, TPU foot sockets/pads | SPECIFIED |
| `rpi_ssd_stack_module` | 1 | 190 x 190 | 75 | Raspberry Pi 3B + SSD open tray/frame carrier layer | M5 rods, compression pads, rear service windows, airflow openings, mounting/tool access, base/minipc contact planes | SPECIFIED WITH ASSUMPTIONS |
| `minipc_stack_module` | 1 | 190 x 190 | 105 | Mini PC open tray/frame carrier and thermal-priority layer | M5 rods, compression pads, rear service windows, airflow openings, mounting/tool access, RPi/top contact planes | SPECIFIED WITH ASSUMPTIONS |
| `top_cap` | 1 | 190 x 190 | 26 | Top compression cap and exhaust plane | M5 rods, top washers/nuts, minipc top interface, exhaust opening | SPECIFIED |
| M5 threaded rod | 4 | diameter 5 | 260 functional minimum, 270 recommended, 280 safe cut-to-fit | Primary vertical structural member | All stack layers, washers, nuts | SPECIFIED |
| M5 washer | 8 minimum | OD 12 | n/a | Load spreader at base and top | Washer seats, compression pads | SPECIFIED |
| M5 nut | 8 minimum | M5 | n/a | Stack compression | Rod ends, tool access zones | SPECIFIED |
| TPU foot | 4 separate TPU parts | ASSUMPTION: 20 x 20 pad minimum | 6-12 assumed | Vibration isolation and base stability | Base underside sockets/pads, future wider foot extension | ASSUMPTION |
| future rear service cover | 0 in MVP | width TBD, depth <= 30 | module-dependent | Future cable cover | Rear service zone only | FUTURE |
| future wider foot extension | 0 in MVP | TBD | TBD | Future stability extension | Base foot pilot points | FUTURE |

## 7. Interface Table

| Interface | Components | Geometry | Constraint | Status |
| --- | --- | --- | --- | --- |
| Base <-> RPi/SSD module | `base_pedestal`, `rpi_ssd_stack_module` | Contact plane at Z = 32; footprint 190 x 190; M5 holes at +/-80 X/Y | Planes must mate without device protrusion below RPi module | PASS |
| RPi/SSD module <-> Mini PC module | `rpi_ssd_stack_module`, `minipc_stack_module` | Contact plane at Z = 107; same M5 pattern and compression pads | Pi/SSD cable exits must stay below or inside module envelope | PARTIAL |
| Mini PC module <-> Top cap | `minipc_stack_module`, `top_cap` | Contact plane at Z = 212; same M5 pattern and compression pads | Mini PC top clearance must remain below Z = 212 | PASS by envelope assumption |
| M5 rods <-> all stack layers | rods, all printed layers | Four clearance holes diameter 5.6 at (-80,-80), (80,-80), (-80,80), (80,80) | Rod pattern must not change after spec freeze | PASS |
| Rear service zone <-> all modules | all printed layers | Y +65 to +95, depth 30, continuous Z 0 to 238 | Cable windows per module; no monolithic spine in MVP | PARTIAL |
| Fan-aligned inlet/outlet + distributed internal airflow <-> base/modules/top | base, modules, top | Base/top 120 x 120 fan-compatible zones; internal modules use equivalent distributed airflow through real openings | Devices may overlap the centered XY zone only if raised/perforated/bypass/ducted airflow is preserved as open geometry | PARTIAL |
| Printable geometry <-> reference geometry | printed parts, placeholders, hardware references | Printable STL contains only plastic body; assembly may include reference geometry | Device/hardware placeholders must be separate from printable builders | NOT VERIFIED |
| Mounting/service access <-> all device modules | `rpi_ssd_stack_module`, `minipc_stack_module` | Top/front/side tool access windows; rear cable exits before stack compression | Devices, retainers, straps, bosses, and cables must be reachable without cutting plastic | NOT VERIFIED |
| Washer/nut <-> base/top | rods, washers, nuts, `base_pedestal`, `top_cap` | Washer seat diameter 13, depth 1.2, centered on M5 holes | Seat must remain within corner pad and tool access zone | PARTIAL |
| Future side-adapter zones <-> modules | future adapters, stack modules | Reserved outside active MVP device/airflow zones, no active rails | Must not affect MVP M5 pattern | NOT VERIFIED |

## 8. Component Geometry

### 8.1 `base_pedestal`

Purpose:

- lower structural and positioning element;
- bottom intake;
- lower washer/nut zones;
- M5 rod pattern origin;
- TPU foot pads;
- future wider foot extension pilot points.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 0 to 32
M5 holes: 4 x diameter 5.6 at (-80,-80), (+80,-80), (-80,+80), (+80,+80)
Washer seats: diameter 13, depth 1.2, coaxial with M5 holes
Corner compression pads: 24 x 24 x 3, centered on each M5 rod
Fan-compatible intake zone: 120 x 120 envelope.
Actual intake cutout must preserve material if bottom fan mounting holes are implemented.
Full 120 x 120 square void is not allowed if fan mounting holes are implemented.
Preferred MVP intake cutout: circular, rounded-square, grille, or segmented opening with effective airflow area.
Rear service clearance: Y +65 to +95, depth 30, segmented around rear rod/compression keepouts
Construction: ribbed frame or open pedestal, not a solid 190 x 190 x 32 slab
Base frame ring and fan cutout edges must be tied to corner compression zones with ribs.
Base target mass: 120-220 g PETG
Base soft review mass limit: 300 g PETG
Base hard FAIL mass limit: >500 g PETG
TPU foot pad assumption: 4 separate TPU pads, not part of the PETG base STL.
For 20 x 20 TPU feet, foot center offset +/-72 is not preferred and should be treated as PARTIAL/FAIL unless intake clearance is explicitly validated.
TPU_FOOT_CENTER_OFFSET_MIN_PREFERRED = 76
TPU_FOOT_CENTER_OFFSET_MAX_PREFERRED = 78
Foot geometry must preserve at least 3 to 5 mm clearance from the fan-compatible intake zone.
Future wider foot pilot points: outside or near foot pads, exact diameter NOT VERIFIED
```

Base pedestal rib topology:

```text
No external ribs or tabs outside X/Y +/-95.
Corner compression islands must connect inward to perimeter frame and fan/intake ring.
Fan/intake ring must connect to perimeter frame through ribs.
Rear service clearance must not be blocked by rib endpoints.
Base must not use outward star ribs around M5 rod guides.
```

Required checks:

| Check | Status | Reason |
| --- | --- | --- |
| Central intake vs M5 holes | PASS | Rod centers are 80 mm from origin; airflow half-size is 60 mm; hole radius is 2.8 mm; clearance from airflow edge to hole edge is 17.2 mm. |
| Base intake cutout vs optional fan screw bosses | PARTIAL | If bottom fan mounting is implemented, a full 120 x 120 square void would remove material at the 105 x 105 screw centers. CAD must preserve boss material or treat bottom fan mounting as future/not implemented. |
| Rear service zone vs M5 compression pads | PARTIAL | Rear pads centered at Y +80 extend Y +68 to +92, which lies inside the rear service zone Y +65 to +95. This is acceptable only if rear service clearance is segmented around corner pads. |
| Washer seats inside corner pads | PASS | Washer seat radius 6.5 fits inside 12 mm half-pad with 5.5 mm pad margin. |
| Washer seats vs outer boundary | PARTIAL | Material from washer seat edge to outer boundary is 8.5 mm. This may be low for PETG and needs coupon validation. |
| Foot pads vs intake | PARTIAL | Foot centers near +/-72 with 20 x 20 pads leave only about 2 mm to the fan-compatible intake boundary, so +/-72 is not preferred and should be PARTIAL/FAIL unless explicitly validated. Preferred foot center offset is 76-78 or actual foot size must preserve 3-5 mm clearance. |
| Base is not a blind slab | PASS | Fan-compatible intake zone must use circular, rounded-square, grille, or segmented effective airflow geometry plus rear service clearance. |
| Base printable body connectivity | NOT VERIFIED | Printable STL must be one connected plastic body after removing reference hardware/placeholders. |

### 8.2 `rpi_ssd_stack_module`

Purpose:

- holds Raspberry Pi 3B;
- holds external SSD or 2.5 inch SSD / USB SSD through strap zone;
- provides airflow clearance;
- routes USB/power/cables rearward;
- stack layer between base and mini PC module.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 32 to 107
Height: 75
M5 holes: same as base, diameter 5.6
Top/bottom compression pads: 24 x 24 x 3 at rod centers
Internal airflow target: equivalent distributed airflow area connected to base/top 120 x 120 fan-compatible zones
Rear service zone: Y +65 to +95, continuous in Z but segmented in XY around rear rod/compression keepouts
Construction: ribbed-frame / open tray, not a closed solid tray under Pi/SSD
Nominal tray floor thickness: 3
Rib thickness: 3
Rib height: 8 to 15
Minimum airflow slot width: 8
Minimum cable window width: 12
Minimum cable window height: 10
Preferred cable window height: 15
Minimum service access window width: 25
Minimum effective airflow open area: 2500 mm2 absolute, 4000 mm2 preferred
Tool access around Pi bosses: 8 mm minimum for M2.5, 9 mm minimum for M3
SSD strap pull-tab access: 15 x 20 mm minimum
Rib layout: required path from M5 compression zones to perimeter frame
```

RPi/SSD module rib topology:

```text
No external ribs or tabs outside X/Y +/-95.
M5 compression islands must connect to perimeter frame and internal rib network.
Pi support bosses/pads must connect to local ribs or tray rails.
SSD support/strap zones must connect to local ribs or tray rails.
Cable corridor to rear service zone must remain open.
Ribs must not cross or block Pi/SSD mounting/tool access envelopes.
Ribs must not terminate inside Pi/SSD reference envelope unless they are device support features.
```

Raspberry Pi 3B placement:

```text
Board envelope: 85 x 56
Board clearance envelope: 95 x 66
ASSUMPTION board center: X -35, Y -35
Board clearance X range: -82.5 to +12.5
Board clearance Y range: -68 to -2
Mounting boss height: 5 to 8
Pilot holes: M2.5 or M3, exact coordinates NOT VERIFIED for mk0.12 CAD
Mounting boss tool access: required from top/front/side, exact route NOT VERIFIED
```

SSD placement:

```text
External SSD placeholder envelope: 110 x 45 x 12 minimum
ASSUMPTION external SSD preferred center: X +15, Y -35
External SSD preferred X range: -40 to +70
External SSD preferred Y range: -57.5 to -12.5
External SSD alternate center: X +25, Y -35
External SSD alternate X range: -30 to +80
External SSD alternate Y range: -57.5 to -12.5
Alternate center X +25 is allowed only if rod keepout, strap geometry, cable route, and slicer review pass validation.

2.5 inch SSD fallback envelope: 100 x 70 x 7
2.5 inch SSD exact placement: NOT VERIFIED
```

Cable path:

```text
Pi/SSD cable corridor target width: 12 to 15
ASSUMPTION primary cable corridor: X +45 to +60, Y -35 to +65
Minimum bend clearance behind device: target 20 if possible
Rear service entry: Y +65
Cable path must be visibly open and must not pass through a closed wall.
```

Required checks:

| Check | Status | Reason |
| --- | --- | --- |
| Raspberry Pi envelope vs M5 rods | PASS | Pi clearance envelope X -82.5 to +12.5, Y -68 to -2. Nearest rod (-80,-80) is outside by 12 mm in Y; after 2.8 mm hole radius, clearance is about 9.2 mm. |
| Raspberry Pi envelope vs rear service zone | PASS | Pi clearance rear edge is Y -2; rear service starts at Y +65. |
| SSD envelope vs M5 rods | PARTIAL | Preferred SSD X range is -40 to +70, leaving 10 mm from right rod center X +80 before hole/keepout allowance. This lowers risk, but strap/rib geometry must still avoid rod keepouts. Alternate X +25 reaches X +80 and is allowed only after keepout validation. |
| SSD envelope vs internal distributed airflow | PARTIAL | SSD occupies part of the nominal fan-aligned XY area. This is not a blocker if CAD uses raised supports, perforation, or split-channel airflow instead of a solid tray. |
| Pi envelope vs internal distributed airflow | PARTIAL | Pi placement overlaps the nominal fan-aligned XY area. This is acceptable only if CAD preserves equivalent open area around/under the Pi. |
| Cable corridor to rear service zone | PARTIAL | Proposed X +45 to +60 corridor reaches Y +65, but it shares area near the airflow opening. Needs cable-window coupon and physical cable bend check. |
| Compression pads vs device envelopes | PASS | Rod pads are centered at +/-80 X/Y and are outside proposed Pi/SSD Y ranges except near SSD X +80; retaining geometry must maintain local keep-out. |
| Stack above base | PASS | Z range starts at base top plane Z = 32 with no planned downward device protrusion. |
| RPi/SSD mounting and strap access | NOT VERIFIED | Pi bosses and SSD retainers must be reachable by tool or fingers without cutting plastic or removing unrelated stack layers. |
| RPi/SSD open tray construction | NOT VERIFIED | CAD skeleton v3 must show real airflow/cable windows and must not be a solid or closed tray under the devices. |
| RPi/SSD printable body connectivity | NOT VERIFIED | Printable STL must be one connected plastic body after excluding Pi/SSD placeholders. |
| RPi/SSD effective airflow open area | NOT VERIFIED | Module must expose at least 2500 mm2 effective open area, with 4000 mm2 preferred. |
| RPi/SSD cable window height | NOT VERIFIED | Cable windows must be at least 10 mm high, with 15 mm preferred. |
| RPi/SSD rib load path | NOT VERIFIED | M5 compression islands must connect to the perimeter frame through ribs without blocking device/cable access. |

### 8.3 `minipc_stack_module`

Purpose:

- holds mini PC;
- provides dedicated airflow reserve;
- routes power/USB/Ethernet/HDMI cables rearward;
- heaviest and highest-heat MVP module;
- allows future adaptation to a different mini PC.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 107 to 212
Height: 105
M5 holes: same as base, diameter 5.6
Top/bottom compression pads: 24 x 24 x 3 at rod centers
Internal airflow target: equivalent distributed airflow area using side bypass, bottom gap, perforated support, or ducted/split flow around the mini PC
Rear service zone: Y +65 to +95, continuous in Z but segmented in XY around rear rod/compression keepouts
Construction: ribbed-frame / open tray, not a closed mini PC box
Tray floor thickness: 3
Rib thickness: 3
Rib height: 8 to 15
Minimum airflow slot width: 8
Minimum cable window width: 12
Rear cable exit height: at least MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN
Minimum service access window width: 25
Minimum effective airflow open area: 5000 mm2 minimum
Finger access slot width: 18 mm minimum for retainers/straps
Mini PC support must use rails/ribs/pads with bottom or side airflow gaps.
Rib layout: required path from M5 compression zones to perimeter frame
```

Mini PC module rib topology:

```text
No external ribs or tabs outside X/Y +/-95.
No front protrusions beyond Y -95.
M5 compression islands must connect to perimeter frame and internal rib network.
Mini PC support must use rails/ribs/pads with visible airflow gaps.
Rear cable exit from Y +40 to Y +65 must remain open.
Rear service windows must not be blocked by rib endpoints.
Ribs must not cross required retainer/finger access zones.
Any support rib under Mini PC must preserve bottom/side airflow paths.
```

Mini PC placement:

```text
Default mini PC footprint: 130 x 130
Default mini PC height: 55
Clearance envelope: 140 x 140 x 65
ASSUMPTION physical mini PC center: X 0, Y -25
Physical mini PC X range: -65 to +65
Physical mini PC Y range: -90 to +40
Clearance envelope X range: -70 to +70
Clearance envelope Y range: -95 to +45
Bottom gap under mini PC: 5 to 8 if lifted on ribs
Side/top clearance: at least 5
Rear cable distance from physical rear ports to rear service boundary: 25
Visible bottom/side airflow gap: required
```

Mini PC front clearance rule:

```text
Mini PC clearance envelope may touch Y -95 only as a keepout envelope.
No front retainer, lip, rib, stop, tab, or other printable feature may protrude beyond Y -95.
If front retention is required, use side retainers, top strap geometry, or internal features that remain inside the 190 x 190 footprint.
Do not move Mini PC placement in this documentation cleanup.
```

Retainers and cable exits:

```text
Side retainers / strap slots: outside main airflow path where possible
Retainers must avoid M5 rod keep-out radius around +/-80 X/Y
Rear cable exit target: Y +40 to +65 from mini PC rear ports into rear service zone
Cable bend clearance target: 25 mm before rear service zone
Mini PC must be insertable/removable before final stack compression.
Retainers/straps must remain accessible.
```

Required checks:

| Check | Status | Reason |
| --- | --- | --- |
| Mini PC clearance envelope vs M5 rods | PASS | Clearance X range is -70 to +70 and rods are at X +/-80. Minimum X gap to rod center is 10 mm; after 2.8 mm hole radius, clearance is about 7.2 mm. |
| Mini PC physical envelope vs rear service zone | PASS | Physical rear edge is Y +40; rear service starts at Y +65, leaving 25 mm cable bend placeholder. |
| Mini PC clearance envelope vs rear service zone | PARTIAL | Clearance envelope rear edge is Y +45, leaving 20 mm to rear service start. This is acceptable only if the physical port face, not the full clearance envelope, defines cable bend start. |
| Mini PC cable exit vs compression pads | PARTIAL | Rear compression pads at Y +80 occupy the rear service zone. Cable exits must be centered away from X +/-80 corner pads. |
| Mini PC fully blocks vertical airflow | PARTIAL | 130 x 130 mini PC overlaps the fan-aligned 120 x 120 XY area. This is not a blocker if CAD implements distributed/bypass airflow through side channels, bottom gap, perforated support, or ducting. |
| Module height vs mini PC + clearance | PASS | 105 mm module height supports 55 mm device, 5-8 mm bottom gap, 5 mm top clearance, and tray/retainer structure. |
| Stack above RPi/SSD module | PASS | Module starts at Z = 107, matching RPi/SSD top plane. |
| Center of mass risk | PARTIAL | Mini PC mass is high and placed above the Pi module. Physical tilt test and future wider foot options are required. |
| Mini PC mounting and retainer access | NOT VERIFIED | Device insertion, retainers, straps, and rear cable exits must be accessible before final stack compression. |
| Mini PC open tray construction | NOT VERIFIED | CAD skeleton v3 must show bottom/side/top airflow clearance and must not fully enclose the Mini PC without a removable access strategy. |
| Mini PC printable body connectivity | NOT VERIFIED | Printable STL must be one connected plastic body after excluding Mini PC placeholder geometry. |
| Mini PC effective airflow open area | NOT VERIFIED | Module must expose at least 5000 mm2 effective open area as a geometry sanity gate. |
| Mini PC rear cable exit height | NOT VERIFIED | Rear exit must reserve at least 20 mm vertical clearance unless low-profile/angled cables are documented. |
| Mini PC rib load path | NOT VERIFIED | M5 compression islands must connect to the perimeter frame through ribs without blocking service windows. |

### 8.4 `top_cap`

Purpose:

- upper structural and positioning element;
- closes the stack;
- top washer/nut zones;
- exhaust opening;
- optional future 120 mm fan support.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 212 to 238
Height: 26
M5 holes: same as base, diameter 5.6
Washer seat diameter: 13
Washer seat depth: 1.2
Fan-compatible exhaust zone: 120 x 120 envelope.
Actual airflow cutout must preserve fan screw boss material around the 105 x 105 screw pattern.
Full 120 x 120 square void is not allowed if fan mounting holes are implemented.
Preferred MVP cutout: circular, rounded-square, grille, or segmented opening with effective airflow area, not a full square that removes screw boss material.
Rear service continuation clearance: Y +65 to +95, segmented around rear corner pads
Construction: ribbed frame or open cap, not a solid 190 x 190 x 26 slab
Fan screw boss material must be preserved.
Fan opening edges must be reinforced by ribs or ring geometry.
Top cap target mass: 100-200 g PETG
Top cap soft review mass limit: 300 g PETG
Top cap hard FAIL mass limit: >500 g PETG
Optional fan envelope: 120 x 120
Optional fan screw pattern: 105 x 105, centers at (+/-52.5, +/-52.5)
Optional fan screw boss diameter assumption: 10 to 14
Optional fan thickness: 25 external/above preferred unless internal placement is documented
```

Top cap rib topology:

```text
No external ribs or tabs outside X/Y +/-95.
Top M5 compression islands must connect inward to perimeter frame and fan/exhaust ring.
Fan screw bosses must connect to frame/ring through ribs or lands.
Exhaust cutout must preserve screw boss material.
Top cap must not use outward star ribs around M5 rod guides.
```

Required checks:

| Check | Status | Reason |
| --- | --- | --- |
| Exhaust vs M5 holes | PASS | Same clearance as base intake: 17.2 mm from airflow edge to rod hole edge. |
| Washer seats vs fan screw pattern | PASS | Fan screw centers at +/-52.5 are 27.5 mm from rod centers at +/-80 along each axis; no direct coaxial conflict. |
| Fan airflow cutout vs fan screw bosses | PARTIAL | A full 120 x 120 square cutout would remove material at the 105 x 105 fan screw centers. CAD must preserve screw boss material or treat fan mounting as future/not implemented. |
| Top cap closes airflow | PASS | 120 x 120 fan-compatible exhaust zone is required, but the actual cutout must preserve screw boss material and frame stiffness. |
| Top cap aligns with module below | PASS | Same 190 x 190 footprint and M5 pattern as `minipc_stack_module`. |
| Top cap printable body connectivity | NOT VERIFIED | Printable STL must be one connected plastic body after excluding fan/hardware reference geometry. |

### 8.5 M5 Hardware Set

Purpose: primary structural load path.

Hardware:

```text
4 x M5 threaded rods
Minimum functional rod length for CAD envelope validation: 260
Recommended physical rod length: 270
Safe cut-to-fit physical rod length: 280
8 x M5 washers minimum
8 x M5 nuts minimum
Optional nyloc nuts: allowed if tool access is confirmed
Optional printed or metal spacers: NOT INCLUDED unless documented in later CAD spec
```

Stack compression rule:

```text
Stack compression must be hand-tight only.
Tighten nuts only until visible stack play disappears.
Do not apply high torque.
Recommended assembly rule: hand-tight + small final adjustment only.
Nyloc nuts or threadlocker may be considered only if tool access is verified.
```

Required checks:

| Check | Status | Reason |
| --- | --- | --- |
| Rod length vs stack height | PASS | 238 mm stack + 8 mm bottom allowance + 12 mm top allowance = 258 mm minimum; 260 mm is the functional CAD minimum, while 270 mm is the physical recommendation and 280 mm is safe cut-to-fit stock. |
| Rods pass through all modules | PASS | All stack layers use the same four coordinates and 5.6 mm clearance holes. |
| Washer OD fits washer seat | PASS | 12 mm washer OD fits 13 mm seat diameter with 0.5 mm radial clearance. |
| Nuts have tool access | NOT VERIFIED | Access envelope is now defined as an assumption in this spec, but CAD and physical validation are still required before full print. |

### 8.6 Nut and Tool Access Assumptions

Purpose: prevent blind nut pockets and unreachable compression hardware.

Assumptions:

```text
M5 nut across flats: approximately 8
M5_NUT_HEIGHT_MIN_ASSUMPTION = 4
M5_NUT_HEIGHT_MAX_ASSUMPTION = 5
Washer OD: 12
Washer seat diameter: 13
M5_NUT_ACCESS_DIAMETER_MIN_ASSUMPTION = 12
M5_NUT_ACCESS_DIAMETER_MAX_ASSUMPTION = 14
M5_SOCKET_ACCESS_DIAMETER_MIN_PREFERRED = 14
M5_SOCKET_ACCESS_DIAMETER_MAX_PREFERRED = 16
TOP_NUT_ACCESS_CLEARANCE_Z_MIN = 8
BOTTOM_NUT_ACCESS_CLEARANCE_Z_MIN = 8
BOTTOM_NUT_SIDE_ACCESS_POCKET_ALLOWED = true
```

Requirement:

```text
CAD must not create blind nut pockets that cannot be reached by fingers, wrench, socket, or nut driver.
```

Status: NOT VERIFIED until represented in validation checks and reviewed in CAD.

### 8.7 Rear Service Zone

Purpose:

- power cables;
- USB;
- Ethernet;
- fan wires;
- cable ties;
- future DC power bus.

Geometry:

```text
Reserved depth: 30
Y range: +65 to +95
X range: reserved across width, but segmented around M5 corner pads and rear rod keepouts
Z continuity: 0 to 238 across base, RPi/SSD module, Mini PC module, top cap
Rear rod keepout centers: X +/-80, Y +80
Rear rod keepout radius minimum assumption: 12
Rear rod keepout radius maximum assumption: 15
Primary rear cable corridor absolute assumption: X -65 to +65
Primary rear cable corridor preferred conservative: X -60 to +60
No monolithic rear spine in MVP
Each module must provide a cable window into this zone
Cable tie slots: future or MVP geometry, exact slot dimensions NOT VERIFIED
```

Primary corridor rule:

```text
Primary rear cable corridor should be centered between rear rod keepouts.
With rear rod keepout radius up to 15 mm around X +/-80, the approximate central usable corridor is X -65 to +65.
For conservative validation, use X -60 to +60 as the preferred primary cable corridor.
```

Required checks:

| Check | Status | Reason |
| --- | --- | --- |
| Service zone vs M5 rods | PARTIAL | Rear rods at X +/-80, Y +80 lie inside the Y +65 to +95 service envelope. Cable paths must be segmented around 12-15 mm keepout radii and should prefer the central rear region away from rod columns. |
| Service zone continuous in Z | PASS by specification | Every layer reserves Y +65 to +95 from Z 0 to 238, continuous in Z but segmented in XY around rear rods/compression pads. |
| Primary rear cable corridor vs rear rod keepouts | PARTIAL | Preferred rear cable corridor X -60 to +60 avoids rear rod keepouts around X +/-80 with 12-15 mm radius, but real cable bundle thickness must be validated. |
| Device cable exits reach service zone | PARTIAL | Pi/SSD and mini PC have proposed rearward paths, but real cable bend tests are required. |
| Service zone blocks vertical airflow | PASS | Service zone is behind the base/top fan-aligned airflow zone Y -60 to +60 and starts at Y +65, leaving a 5 mm nominal separator. |

Cable assumption:

```text
30 mm rear service depth assumes flexible or angled cables where needed.
Straight stiff HDMI, thick DC barrel plugs, and rigid USB adapters are not guaranteed.
Cable bend test with actual cables is mandatory before full print.
```

## 9. Required Calculations

### 9.1 Total Stack Height

```text
BASE_PEDESTAL_HEIGHT = 32
RPI_SSD_MODULE_HEIGHT = 75
MINIPC_MODULE_HEIGHT = 105
TOP_CAP_HEIGHT = 26

TOTAL_STACK_HEIGHT = 32 + 75 + 105 + 26 = 238 mm
```

Status: PASS

### 9.2 Recommended Rod Length

```text
TOTAL_STACK_HEIGHT = 238
BOTTOM_ALLOWANCE = 8
TOP_ALLOWANCE = 12

CALCULATED_MIN_ROD_LENGTH = 238 + 8 + 12 = 258 mm
MINIMUM_FUNCTIONAL_M5_ROD_LENGTH = 260 mm
RECOMMENDED_M5_ROD_LENGTH = 270 mm
SAFE_CUT_TO_FIT_M5_ROD_LENGTH = 280 mm
```

Status: PASS

Interpretation:

```text
260 mm is a functional minimum for CAD envelope validation only.
For physical build, use 270-280 mm rods and trim if needed.
The final physical rod length depends on washer thickness, nut type, thread engagement, PETG tolerances, possible nyloc nuts, and actual stack compression.
```

### 9.3 M5 Rod vs Airflow Clearance

```text
Rod center offset = 80 mm
Airflow half-size = 60 mm
Rod clearance hole radius = 2.8 mm

Clearance from airflow edge to rod hole edge:
80 - 60 - 2.8 = 17.2 mm
```

Status: PASS

### 9.4 M5 Rod vs Outer Wall Clearance

```text
Outer half-size = 95 mm
Rod center offset = 80 mm
Rod clearance hole radius = 2.8 mm

Material from rod hole edge to outer boundary:
95 - 80 - 2.8 = 12.2 mm
```

Status: PASS

### 9.5 Washer Seat vs Outer Boundary

```text
Outer half-size = 95 mm
Rod center offset = 80 mm
Washer seat radius = 6.5 mm

Material from washer seat edge to outer boundary:
95 - 80 - 6.5 = 8.5 mm
```

Status: PARTIAL

Reason: 8.5 mm outer material may be low for PETG around repeated compression. M5 rod pattern remains frozen at +/-80 for mk0.12; do not move rods inward in this documentation update.

Recommended mitigations:

- reinforce washer/compression zones locally with thickened lands;
- connect each compression pad to adjacent frame walls using ribs;
- keep the baseline 24 x 24 pad, but allow CAD to increase local reinforced land to 28 x 28 or 30 x 30 inward if validation requires it;
- reduce washer seat diameter only if washer fit still passes;
- accept as MVP only after M5 corner coupon compression validation.

### 9.6 Rear Service Zone Depth

```text
Rear service zone depth = 30 mm
Usable central depth before rear service = 160 mm
Front outer boundary = Y -95
Rear service start = Y +65
Depth from front boundary to rear service start = 65 - (-95) = 160 mm
```

Status: PARTIAL

Reason: 30 mm is plausible for USB/Ethernet/power bend placeholders if cable windows are aligned, cables are flexible or angled where needed, and routes are not stacked directly behind rods. Straight stiff HDMI, thick DC barrel plugs, and rigid USB adapters are not guaranteed. Mini PC placement reserves 25 mm from physical rear port face to service boundary; Pi/SSD cable bend remains ASSUMPTION.

### 9.7 Primary Rear Cable Corridor

```text
Rear rod center X = +/-80
Rear rod keepout radius maximum assumption = 15

Approximate inner edge of rear rod keepouts:
80 - 15 = 65 mm

Approximate central usable corridor:
X -65 to +65

Preferred conservative cable corridor for validation:
X -60 to +60
```

Status: PARTIAL

Reason: X -60 to +60 avoids the assumed rear rod keepout radius, but the effective bundle width depends on actual cable count, connector stiffness, tie slots, and strain relief geometry.

### 9.8 Printable Volume and Mass Sanity

CAD skeleton v3 must include a printable volume/mass sanity review before coupon printing is treated as the next gate.

Status: NOT VERIFIED

Reason: current CAD skeleton review identified risk that modules can become heavy monolithic volumes. mk0.12 must treat near-solid 190 x 190 x module-height printed parts as a design failure, not an optimization detail.

Warning-level interpretation:

```text
Single printable module above 300-500 g PETG: PARTIAL, engineering review required.
Single printable module above 800 g PETG: FAIL unless explicitly justified.
Final production-optimized mass is not frozen.
mk0.12 CAD skeleton v3 mass sanity gates are frozen for validation.
```

Required evidence:

- volume/mass estimate per printable STL;
- visual confirmation that base/top are frame-like, not solid slabs;
- visual confirmation that RPi/SSD and Mini PC modules are open trays/frames;
- documented justification for any large solid volume that remains.

### 9.9 Per-Part Mass Budget

Expected status before CAD skeleton v3: NOT VERIFIED

CAD skeleton v3 must calculate or estimate PETG mass for each printable part and compare it to the mk0.12 sanity budget:

| Printable part | Target PETG mass | Soft review limit | Hard FAIL limit |
| --- | ---: | ---: | ---: |
| `base_pedestal` | 120-220 g | 300 g | >500 g |
| `rpi_ssd_stack_module` | 150-300 g | 400 g | >800 g |
| `minipc_stack_module` | 250-450 g | 600 g | >800 g |
| `top_cap` | 100-200 g | 300 g | >500 g |
| total printed PETG | 620-1170 g | ~1600 g | >2500 g NO-GO |

Criteria:

```text
At or below target range: PASS for mass sanity.
Above target but at or below soft review limit: PASS/PARTIAL depending geometry and print risk.
Above soft review limit: PARTIAL and must be justified.
Above hard FAIL limit: FAIL unless explicitly justified by structural function and approved in review.
Total printed PETG above 2500 g: NO-GO.
```

### 9.10 Minimum Effective Airflow Open Area

Expected status before CAD skeleton v3: NOT VERIFIED

CAD skeleton v3 must estimate effective open area per module from real openings, slots, perforations, bypasses, and visible gaps. This is a geometric sanity check, not CFD validation.

Required thresholds:

```text
MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_ABSOLUTE = 2500 mm2
MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_PREFERRED = 4000 mm2
MINIPC_MODULE_AIRFLOW_OPEN_AREA_MIN = 5000 mm2
```

Criteria:

```text
Below absolute minimum: FAIL.
Between absolute and preferred: PARTIAL, requires review.
Above preferred: PASS for geometric open-area sanity, thermal testing still required.
Mini PC module below 5000 mm2: FAIL unless a documented dedicated duct/bypass strategy is reviewed.
Open area that removes M5 compression pads, fan screw boss material, device mounting bosses, or rear rod keepout structure does not count as valid open area.
```

### 9.11 Cable Window Height

Expected status before CAD skeleton v3: NOT VERIFIED

CAD skeleton v3 must report both width and height for rear service/cable windows. Width-only compliance is not sufficient.

Required thresholds:

```text
MIN_CABLE_WINDOW_WIDTH = 12.0
MIN_CABLE_WINDOW_HEIGHT = 10.0
PREFERRED_CABLE_WINDOW_HEIGHT = 15.0
MIN_REAR_SERVICE_VERTICAL_PASSAGE_HEIGHT_PER_MODULE = 20.0
MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN = 20.0
```

Criteria:

```text
Cable window height below 10 mm: FAIL.
Cable window height 10-15 mm: PARTIAL.
Cable window height >=15 mm: PASS for skeleton geometry, physical cable test still required.
Mini PC rear cable exit height below MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN is FAIL unless specific low-profile/angled cables are documented.
```

### 9.12 Minimum Access Envelope

Expected status before CAD skeleton v3: NOT VERIFIED

CAD skeleton v3 must represent and visually check tool/finger access envelopes around bosses, screws, clips, straps, retainers, and cable exits.

Required thresholds:

```text
MIN_TOOL_ACCESS_DIAMETER_AROUND_M2_5_BOSS = 8.0
MIN_TOOL_ACCESS_DIAMETER_AROUND_M3_BOSS = 9.0
MIN_FINGER_ACCESS_SLOT_WIDTH = 18.0
MIN_STRAP_PULL_TAB_ACCESS_WIDTH = 15.0
MIN_STRAP_PULL_TAB_ACCESS_DEPTH = 20.0
MIN_RETAINER_CLEARANCE_AROUND_SCREW_OR_CLIP = 10.0
```

Criteria:

```text
Tool/finger access below minimum: FAIL.
Access meets minimum but is possible only before stack compression: PARTIAL and must be documented in assembly order.
Access remains possible during normal pre-compression assembly: PASS.
Primary device installation after final stack compression required by CAD: FAIL.
Cable routing to rear service zone after final stack compression required by CAD: FAIL.
```

### 9.13 Bounding Box and Protrusion Check

CAD skeleton v3 must calculate printable bounding boxes for each part.

Expected:

```text
base_pedestal: X <= 190.5, Y <= 190.5, Z = 32
rpi_ssd_stack_module: X <= 190.5, Y <= 190.5, Z = 75
minipc_stack_module: X <= 190.5, Y <= 190.5, Z = 105
top_cap: X <= 190.5, Y <= 190.5, Z = 26
```

Any printable feature outside X/Y +/-95.25 is FAIL unless it is an explicitly documented separate future extension part and excluded from the active mk0.12 printable body.

The CAD review must report maximum X/Y extents and identify any protruding feature class:

- rib;
- tab;
- guide;
- boss;
- foot pad;
- cable feature;
- reference object.

The previous 205 x 205 style growth from rib/tower generation is a regression, not acceptable lightening behavior.

### 9.14 Rib Topology Validation

CAD skeleton v3 must perform a manual or scripted rib topology review.

Required evidence:

- top-view render with footprint boundary overlay;
- top-view render with rib endpoints visible;
- list of M5 compression island connections;
- confirmation that no ribs extend outside footprint;
- confirmation that each rib has valid endpoints;
- confirmation that no rib blocks rear service windows;
- confirmation that no rib blocks required airflow windows;
- confirmation that no rib blocks device mounting/tool access.

Criteria:

```text
Outward rib outside footprint: FAIL.
Dangling/floating rib: FAIL.
Rib endpoint outside footprint: FAIL.
Rib ending in unsupported thin web: FAIL.
Rib blocking required cable/airflow/access window: FAIL.
Rib topology load path unclear: PARTIAL.
```

## 10. Assembly Conflict Check

Allowed statuses:

```text
PASS
PARTIAL
FAIL
NOT VERIFIED
```

### 10.1 XY Conflicts

| Check | Status | Reason |
| --- | --- | --- |
| M5 rods vs base/top airflow openings | PASS | Rod centers at +/-80 are outside base/top fan-compatible airflow half-size 60; clearance to 5.6 mm hole edge is 17.2 mm. |
| M5 rods vs Raspberry Pi envelope | PASS | Proposed Pi clearance envelope is X -82.5 to +12.5, Y -68 to -2; nearest rod clearance remains about 9.2 mm in Y. |
| M5 rods vs SSD envelope | PARTIAL | Preferred SSD X range is -40 to +70, reducing the right rod conflict risk. Alternate X +25 reaches X +80 and requires rod keepout, strap geometry, cable route, and slicer validation. |
| M5 rods vs mini PC envelope | PASS | Mini PC clearance envelope X -70 to +70; rods at +/-80 leave about 7.2 mm to hole edge. |
| Rear service zone vs device envelopes | PASS for physical devices | Pi/SSD are front/center; mini PC physical rear edge is Y +40 and rear service starts Y +65. |
| Rear service zone vs compression pads | PARTIAL | Rear compression pads occupy Y +68 to +92 inside the rear service zone; rear service must be segmented around them. |
| Primary rear cable corridor vs rear rod keepouts | PARTIAL | Preferred rear cable corridor X -60 to +60 avoids rear rod keepouts around X +/-80 with 12-15 mm radius, but real cable bundle thickness must be validated. |
| Fan screw pattern vs M5 rods | PASS | Fan screw centers at +/-52.5 do not coincide with rod centers at +/-80 and remain outside washer seats. |
| Fan airflow cutout vs fan screw bosses | PARTIAL | A full 120 x 120 square cutout would remove material at the 105 x 105 fan screw centers. CAD must preserve screw boss material or treat fan mounting as future/not implemented. |
| Printed modules vs reference placeholders | NOT VERIFIED | Device and hardware placeholders must be excluded from printable part builders and printable STL exports. |
| Printed module bodies vs disconnected geometry | NOT VERIFIED | Each printable module STL should be one connected plastic body unless separate sub-parts are explicitly documented. |

### 10.2 Z Stack Conflicts

| Check | Status | Reason |
| --- | --- | --- |
| Base top plane vs RPi/SSD bottom plane | PASS | Base top is Z = 32 and RPi/SSD bottom is Z = 32. |
| RPi/SSD top plane vs Mini PC bottom plane | PASS | RPi/SSD top is Z = 107 and Mini PC bottom is Z = 107. |
| Mini PC top plane vs top_cap bottom plane | PASS | Mini PC module top is Z = 212 and top cap bottom is Z = 212. |
| Device vertical envelope vs RPi/SSD module height | PARTIAL | Pi and SSD envelopes fit within 75 mm, but exact boss, strap, cable, and connector heights are not finalized. |
| Device vertical envelope vs Mini PC module height | PASS | 105 mm module height fits 55 mm mini PC, 5-8 mm bottom gap, 5 mm top clearance, and tray/retainer allowance. |
| Washer/nut protrusion vs adjacent component clearance | NOT VERIFIED | Washer seat depth is specified, but nut height, tool access, and printed recess geometry are not finalized. |
| Rod length vs total stack height | PASS | 260 mm functional minimum exceeds the calculated 258 mm minimum; 270 mm is the physical recommendation and 280 mm is safe cut-to-fit stock. |

### 10.3 Airflow Conflicts

| Check | Status | Reason |
| --- | --- | --- |
| Base intake connects to RPi/SSD airflow path | PARTIAL | Base has a 120 x 120 fan-compatible intake, but Pi/SSD devices overlap the nominal fan-aligned XY area. This is not a blocker if CAD implements equivalent distributed airflow through raised supports, ribs, perforated tray areas, or side bypass. |
| RPi/SSD airflow path connects to Mini PC airflow path | PARTIAL | The mini PC footprint overlaps the nominal fan-aligned XY area; transition must become distributed, ducted, or split airflow rather than a clear empty shaft. |
| Mini PC airflow path connects to top exhaust | PARTIAL | Top has a 120 x 120 fan-compatible exhaust, but mini PC placement needs side/bottom/top gaps or ducting to avoid full blockage. |
| Mini PC fully blocks vertical airflow | PARTIAL | Mini PC 130 x 130 footprint is larger than the 120 x 120 fan-compatible zone. This remains acceptable only if airflow routes around/under/along sides. |
| SSD/Pi placement closes central channel | PARTIAL | Pi and SSD overlap the nominal fan-aligned area. Raised ribs, perforation, bottom gaps, or split-channel geometry are required. |
| Fan-compatible zone vs actual cutout | PARTIAL | 120 x 120 is the fan envelope/aligned zone, not necessarily the actual cutout. Actual cutout must preserve screw boss material and sufficient top/base frame stiffness. |
| Airflow represented only by annotation | FAIL if present | Distributed airflow must be real open geometry: slots, perforations, bypass channels, or visible gaps. Labels or placeholders alone are not acceptable. |
| Solid tray under heat-producing device | FAIL unless justified | A solid tray under Pi/SSD or Mini PC is acceptable only if it includes perforation, side bypass, or bottom gap that keeps airflow visibly open. |
| Effective airflow open area per module | NOT VERIFIED | CAD skeleton v3 must calculate/estimate open area. Below absolute minimum is FAIL. |

### 10.4 Cable Conflicts

| Check | Status | Reason |
| --- | --- | --- |
| Raspberry Pi cables route to rear service zone | PARTIAL | Proposed corridor X +45 to +60 reaches Y +65, but exact connector orientation and bend radius are not verified. |
| SSD USB cable routes to rear service zone | PARTIAL | External SSD placement allows rearward routing, but strap/rib geometry must preserve a 12-15 mm path. |
| Mini PC power/Ethernet/USB/HDMI exit rearward | PASS by placement assumption | Physical mini PC rear edge at Y +40 gives 25 mm to rear service start at Y +65. |
| Rear service zone depth supports cable bend placeholder | PARTIAL | 30 mm depth assumes flexible or angled cables where needed. Straight stiff HDMI, thick DC barrel plugs, and rigid USB adapters are not guaranteed and must be tested. |
| Cable path crosses through M5 rods | PARTIAL | Rear rods occupy Y +80; cable windows must be centered away from X +/-80 and cannot pass through rod keep-outs. |
| Rear service represented only by annotation | FAIL if present | Every module must provide real rear service windows into Y +65 to +95, preferably within X -60 to +60 and away from rear rod keepouts. |
| Cable exits blocked before final compression | FAIL if present | Cable exits must remain open before final stack compression; closed walls requiring forced cable routing are not acceptable. |
| Cable window height | NOT VERIFIED | Windows must satisfy minimum height, not only width. |
| Mini PC rear cable exit height | NOT VERIFIED | Mini PC rear cable exit must reserve at least 20 mm vertical clearance. |

### 10.5 Mounting and Service Access Conflicts

| Check | Status | Reason |
| --- | --- | --- |
| Pi boss tool access | NOT VERIFIED | M2.5 bosses need at least 8 mm access diameter; M3 bosses need at least 9 mm access diameter. |
| SSD strap pull-tab access | NOT VERIFIED | Strap pull-tab access must be at least 15 x 20 mm and reachable before final stack compression. |
| Mini PC retainer access | NOT VERIFIED | Retainers/straps need at least 18 mm finger slot width and 10 mm clearance around screws/clips. |
| Device installation before stack compression | NOT VERIFIED | Primary devices must be installed into modules before final M5 stack compression. |
| Cable routing before stack compression | NOT VERIFIED | Device cables must route to rear service windows before final M5 stack compression. |
| M5 compression island rib load path | NOT VERIFIED | Each compression island must have a visible rib/load path to adjacent perimeter frame walls. |

## 11. Assembly Constraints and Risk Notes

Cable routing before compression:

```text
Route and test all cables before final stack compression.
Do not fully tighten the M5 stack before confirming:
- Pi cables reach rear service zone;
- SSD cable reaches rear service zone;
- Mini PC power/Ethernet/USB/HDMI cables exit without rod collision;
- top cap can be installed without pinching cables.
```

PETG compression risk:

| Risk | Status | Impact | Mitigation | Validation |
| --- | --- | --- | --- | --- |
| Over-tightening M5 nuts may crush PETG washer seats, deform compression pads, or cause layer splitting | PARTIAL | Loss of pad flatness, cracked layers, distorted stack alignment | Use washers, enlarged local compression lands, ribbed pad connections, coupon compression tests, and hand-tight torque discipline | M5 corner coupon and reduced-height stack compression test |
| Blind or undersized nut pockets may block assembly tools | NOT VERIFIED | Stack cannot be tightened or serviced reliably | Preserve 12-14 mm nut access diameter minimum and 14-16 mm socket access diameter preferred | Hardware access mock before full print |
| Rear cable routing may be pinched during final stack compression | PARTIAL | Cable damage, blocked top cap, or forced rod collision | Route cables before final tightening and inspect top cap fit before final compression | Cable mock with actual cables |
| Closed/monolithic module geometry may block device mounting, cable routing, or inspection | FAIL if present | Real devices cannot be installed or serviced reliably | Use ribbed-frame/open tray construction with access windows and reachable retainers/bosses | Mounting access visual check before coupon printing |
| Excessive solid plastic volume may create impractical print time, warping risk, and kilogram-scale PETG waste | FAIL if severe | MVP skeleton becomes expensive, slow, and mechanically misleading | Use 3 mm walls/floors, 4 mm structural frames, local 5-6 mm lands, and ribs instead of bulk | Printable volume/mass sanity check |

## 12. Future Expansion Without Reprinting Old Modules

Principle: future modules are added by printing a new stack layer, replacing rods with longer M5 rods, and preserving the 190 x 190 footprint, M5 pattern at +/-80, and rear service zone Y +65 to +95.

| Scenario | New Printed Parts | Change M5 Rods | Change Base/Top | Change Old Modules | Risks | Realism Status |
| --- | --- | --- | --- | --- | --- | --- |
| Add SSD expansion module | New `ssd_expansion_stack_module`; optional cable window coupon | Yes, longer rods by new module height | No, unless stability test fails | No | Rear service crowding, distributed airflow obstruction, extra cable bend | REALISTIC |
| Add MikroTik module | New `mikrotik_stack_module`; device-specific retainers | Yes, longer rods by module height | No, unless port access forces rear/top changes | No | Ethernet cable bundle density in rear service zone | REALISTIC WITH CABLE TEST |
| Add UPS/power module | New `ups_power_stack_module`; power bus brackets; possible lower module order change | Yes | Maybe, if UPS mass requires base stability extension | No, but stack order may change | UPS mass likely belongs near bottom; heat and safety constraints | PARTIAL |
| Add second Mini PC module | New second `minipc_stack_module` variant or duplicate | Yes, significantly longer rods | Maybe, wider feet may be required | No | Higher center of mass, more heat, rear cable congestion | PARTIAL |

## 13. NO-GO for mk0.12

- no direct external CAD copy;
- no active rails;
- no sliding carriage;
- no POM-C shoes;
- no final UPS module;
- no final MikroTik module;
- no decorative side panels before structural validation;
- no monolithic rear spine;
- no full print before coupon tests;
- no changing M5 rod pattern after engineering spec freeze.
- no treating the 120 x 120 fan-aligned zone as a full square fan cutout; actual cutout geometry must be separate and must preserve screw boss material when fan mounting is active.
- no monolithic solid printed modules;
- no closed/gutted modules without mounting access;
- no device placeholders inside printable STL;
- no disconnected printable components unless intentionally separate parts are documented;
- no airflow represented only as annotation without real openings;
- no rear service route represented only as annotation without real cable windows;
- no kilogram-scale or near-solid printed MVP modules unless explicitly justified by a structural function.
- no printable part above hard FAIL mass budget without explicit structural justification and review approval;
- no module below minimum effective airflow open area;
- no cable window with width-only compliance but insufficient height;
- no M5 compression island without rib/load path connection to perimeter frame;
- no device-support tray implemented as solid plate without airflow relief;
- no inaccessible mounting bosses, retainers, straps, or cable exits;
- no CAD design that requires primary device installation after final stack compression.
- no printable feature outside the frozen 190 x 190 footprint;
- no printable body bounding box above 190.5 mm in X or Y for active mk0.12 parts;
- no outward ribs or tabs from M5 compression islands;
- no radial star-rib pattern around corner rod guides unless outward directions are clipped and all remaining ribs connect to valid structural nodes;
- no dangling, floating, decorative, or unfinished ribs;
- no rib with invalid endpoint;
- no rib endpoint outside the footprint;
- no rib connected only to reference geometry;
- no rib blocking required airflow, rear service, cable, or mounting access windows;
- no non-watertight printable STL;
- no non-manifold printable geometry;
- no repeated 205 x 205 style footprint expansion from rib/tower generation.
- no active "CAD skeleton v2" wording for future implementation or validation gates;
- no treating the 120 x 120 fan-aligned zone as a full square airflow cutout;
- no mixed text/numeric constants in future config-oriented values;
- no treating `PREFERRED_DEVICE_ZONE_*` as a hard device keepout;
- no TPU feet inside the PETG `base_pedestal` STL;
- no front Mini PC retainer, lip, rib, stop, tab, or other printable feature protruding beyond Y -95;
- no 260 mm M5 rod described as the physical build recommendation;
- no fan placeholder/reference geometry inside printable STL.

## 14. Physical Validation Plan

Before physical coupon tests, mk0.12 must pass pre-coupon CAD skeleton v3 checks. Coupon printing must not be treated as the next step while printable/reference separation, open geometry, mass sanity, footprint containment, rib topology, and watertight printable bodies remain unresolved.

| Step | Test | Required Evidence | Status Before CAD |
| ---: | --- | --- | --- |
| 0.1 | CAD skeleton v3 printable/reference separation check | Printable part builders exclude device/hardware placeholders; assembly/review may include separate reference geometry | REQUIRED BEFORE COUPONS |
| 0.2 | STL connected-component check for each printable part | `base_pedestal`, `rpi_ssd_stack_module`, `minipc_stack_module`, and `top_cap` each export as one connected printable plastic component unless documented as separate printable sub-parts | REQUIRED BEFORE COUPONS |
| 0.3 | Printable volume/mass sanity check | Estimated printed mass is within reasonable MVP range or explicitly flagged; near-solid modules are not accepted silently | REQUIRED BEFORE COUPONS |
| 0.4 | Mounting access visual check | Pi bosses, SSD retainers, Mini PC retainers, straps, and hardware access zones are reachable by tool or fingers | REQUIRED BEFORE COUPONS |
| 0.5 | Airflow window visual check | Generated views show real airflow openings, perforations, side bypasses, or bottom/top gaps rather than annotations only | REQUIRED BEFORE COUPONS |
| 0.6 | Rear service window visual check | Generated views show real rear cable windows into Y +65 to +95, preferably in X -60 to +60 and away from rear rod keepouts | REQUIRED BEFORE COUPONS |
| 0.7 | Per-part mass budget check | Mass estimate per printable part compared to target/soft/hard limits | REQUIRED BEFORE COUPONS |
| 0.8 | Effective airflow open-area check | Open airflow area estimate per module, with Mini PC checked against its 5000 mm2 minimum | REQUIRED BEFORE COUPONS |
| 0.9 | Cable window width/height check | Cable windows report width and height; Mini PC rear exit reports vertical clearance | REQUIRED BEFORE COUPONS |
| 0.10 | Rib load-path visual check | Generated views show ribs connecting M5 compression islands to perimeter frame and reinforcing service/airflow window edges | REQUIRED BEFORE COUPONS |
| 0.11 | Tool/finger access envelope check | Generated views show access envelopes for Pi bosses, SSD strap, Mini PC retainers, screws/clips, and cable exits | REQUIRED BEFORE COUPONS |
| 0.12 | Stack assembly order check | Assembly notes describe when devices and cables are installed relative to stack compression | REQUIRED BEFORE COUPONS |
| 0.13 | Footprint containment / bounding box check | Bounding box report shows each printable body within 190.5 x 190.5 mm and no printable feature outside X/Y +/-95.25 | REQUIRED BEFORE COUPONS |
| 0.14 | Protrusion classification check | CAD review lists protruding feature classes, if any: rib, tab, guide, boss, foot pad, cable feature, or reference object | REQUIRED BEFORE COUPONS |
| 0.15 | Rib endpoint validity check | Report confirms each rib has two valid endpoints and no rib endpoint is outside the footprint or connected only to reference geometry | REQUIRED BEFORE COUPONS |
| 0.16 | M5 compression island rib direction check | Report lists rib directions from each M5 compression island and confirms no outward ribs/tabs from M5 towers | REQUIRED BEFORE COUPONS |
| 0.17 | Dangling/floating rib check | Generated views show rib endpoints and report confirms no dangling, floating, decorative, unfinished, or unsupported rib features | REQUIRED BEFORE COUPONS |
| 0.18 | Watertight/manifold STL check | Printable STL/body review confirms one connected component, watertight/manifold geometry, no self-intersections, no zero-thickness faces, and no reference geometry in printable bodies | REQUIRED BEFORE COUPONS |
| 1 | Print M5 corner coupon | Corner pad, 5.6 mm hole, 13 mm washer seat, 1.2 mm seat depth | REQUIRED AFTER CAD SKELETON V3 |
| 2 | Test M5 rod clearance | M5 rod passes without force after PETG cooling | REQUIRED |
| 3 | Test washer seat fit | 12 mm washer fits 13 mm seat without rocking or excessive slop | REQUIRED |
| 4 | Test PETG shrink/tolerance | Measured hole and seat diameters recorded | REQUIRED |
| 5 | Print rear cable window coupon | 30 mm rear reserve and segmented corner clearance represented | REQUIRED |
| 6 | Test cable bend with actual Mini PC power cable, Ethernet cable, HDMI/DisplayPort cable if used, USB cable, and SSD cable | Cables bend within Y +65 to +95 zone without rod collision; record whether straight or angled connectors are required | REQUIRED |
| 7 | Print reduced-height stack module | M5 holes align through at least two stacked layers | REQUIRED |
| 8 | Test stack compression with rods/washers/nuts | Hand-tight only; no visible crushing, cracking, or major layer separation at pads | REQUIRED |
| 9 | Place real Raspberry Pi and SSD mock/envelope | Board/SSD envelopes fit; cable path remains open | REQUIRED |
| 10 | Place real mini PC mock/envelope | 130 x 130 x 55 device and cable exits fit | REQUIRED |
| 11 | Slicer preview for full modules | No unsupported long bridges, impossible overhangs, or hidden solid airflow blockage | REQUIRED |
| 12 | Fan cutout / screw boss review | Slicer/CAD review confirms that fan screw boss material remains around 105 x 105 screw centers if fan mounting holes are implemented | REQUIRED |
| 13 | Foot pad / intake clearance check | TPU foot geometry leaves at least 3 to 5 mm clearance from the fan-compatible intake boundary | REQUIRED |
| 14 | Only then print full MVP parts | Full print allowed only after steps 0.1-0.18 and 1-13 pass or are explicitly waived | BLOCKED UNTIL VALIDATED |

## 15. Open Assumptions to Verify

| Assumption | Why It Matters | Verification |
| --- | --- | --- |
| Pi center at X -35, Y -35 | Avoids rear service zone and rods while leaving cable route | Place real Pi or printed board envelope in reduced-height module |
| External SSD preferred center at X +15, Y -35 | Reduces right rod column conflict while keeping SSD in front/center module region | SSD envelope and strap/rib CAD review |
| External SSD alternate center at X +25, Y -35 | May be useful for cable/strap layout but reaches X +80 rod axis | Allowed only if rod keepout, strap geometry, cable route, and slicer review pass validation |
| 2.5 inch SSD fallback placement | Larger 100 x 70 envelope may conflict with airflow/rods | Separate layout sketch before CAD |
| Rear service zone segmented around rear rods | Rear rods occupy the nominal rear service depth | Rear cable coupon with 12-15 mm rear rod keepout assumption |
| 30 mm cable bend zone is enough | Straight stiff HDMI, thick DC barrel plugs, and rigid USB adapters may need more than 30 mm | Cable bend test with actual Mini PC power, Ethernet, HDMI/DisplayPort if used, USB, and SSD cables |
| 8.5 mm material outside washer seat is enough in PETG | Washer seat is close to outer boundary | M5 corner coupon compression test |
| Mini PC airflow can be ducted around device | Mini PC footprint overlaps the nominal fan-aligned zone, so modules must use distributed airflow instead of an empty shaft | Slicer preview and physical thermal observation |
| TPU foot dimensions | Foot pad size and height are not frozen | Foot coupon or base underside mock |
| TPU foot center offset 76 to 78 if using 20 x 20 feet | Centers near +/-72 may leave only about 2 mm from the intake/fan boundary | Foot pad / intake clearance check |
| Fan airflow cutout preserves screw boss material | Full 120 x 120 square void would remove 105 x 105 screw boss material | Fan cutout / screw boss review |
| Tool access to nuts | Nut/wrench clearance is not yet dimensioned | Hardware access mock |

## 16. CAD Implementation Notes for Future Task

Future files may include, but must not be created by this documentation task:

```text
cad/parts/stack_interface.py
cad/parts/base_pedestal.py
cad/parts/top_cap.py
cad/parts/module_rpi_ssd.py
cad/parts/module_minipc.py
cad/assembly/mvp_2_module_stack.py
```

Future reference files/functions may include, but must stay separate from printable part builders:

```text
cad/parts/placeholders.py or cad/parts/reference_geometry.py
build_rpi3b_placeholder()
build_external_ssd_placeholder()
build_minipc_placeholder()
build_120mm_fan_placeholder()
build_120mm_fan_screw_pattern_placeholder()
build_m5_rods_placeholder()
build_washers_placeholder()
build_nuts_placeholder()
build_tpu_foot()
build_tpu_feet_set()
```

Future CAD rules:

- all dimensions must move into `cad/config.py`;
- no magic numbers inside part functions;
- each component must have a separate part function;
- printed part builders must return printable plastic geometry only;
- reference placeholder builders must remain separate from printable STL exports;
- each printable module should normally export as one connected printable body;
- printed modules must use ribbed-frame/open tray construction, not solid slabs or closed blocks;
- CAD views must show real airflow openings and real rear service cable windows;
- CAD review must include printable volume/mass sanity checks;
- assembly must be separate from part definitions;
- STEP/STL/PNG remain derived artifacts;
- do not implement active rails, sliding carriage, POM-C shoes, UPS final module, or MikroTik final module in mk0.12.
- 120 x 120 fan-aligned zones must not be treated as full square cutouts;
- preferred device zone is not a hard keepout; device-specific clearance envelopes remain authoritative;
- TPU feet are separate TPU printable parts and must not be included in PETG base STL;
- 260 mm rod length is only the CAD functional minimum, not the physical build recommendation;
- fan placeholders and fan screw pattern references must remain out of printable STL.
- each printable part must declare intended print orientation before export/review.

Suggested baseline print orientation:

- `base_pedestal`: bottom face on build plate unless CAD review justifies otherwise;
- `rpi_ssd_stack_module`: bottom face on build plate unless CAD review justifies otherwise;
- `minipc_stack_module`: bottom face on build plate unless CAD review justifies otherwise;
- `top_cap`: orientation must be explicitly selected based on fan cutout, washer seats, nut access, and support minimization.

Printability rule:

```text
Avoid unsupported long bridges, hidden downward-facing pockets, inaccessible support traps, and PETG-hostile overhangs unless explicitly documented and reviewed in slicer preview.
```

## 17. Final Recommendation

Proceed to mk0.12 CAD skeleton cleanup v3, not directly to coupon parts.

The next CAD iteration must implement:

- ribbed-frame / open tray construction;
- printable/reference geometry separation;
- connected printable bodies;
- real airflow windows, perforations, bypasses, or gaps;
- real rear service windows into Y +65 to +95;
- mounting and service access for devices, bosses, retainers, straps, nuts, and cables;
- printable volume/mass sanity checks;
- per-part mass budget gates;
- effective airflow open-area checks;
- cable window width/height checks;
- mass/airflow/cable/access validation reports;
- load-path-aware rib layout;
- tool/finger access envelopes;
- stack assembly order notes for the stack-through-rod service model.

Do not proceed to coupon parts until CAD skeleton v3 demonstrates:

- airflow is real open geometry, not annotation only;
- rear service routes are real cable windows, segmented around rear rods;
- device placeholders are excluded from printable STL;
- per-part mass stays within target/soft limits or is explicitly justified, and never exceeds hard FAIL limits without review approval;
- each module meets minimum effective airflow open-area thresholds;
- cable windows satisfy width and height requirements;
- M5 compression islands have rib/load path connection to perimeter frame;
- device support is not a solid plate without airflow relief;
- bosses, retainers, straps, and cable exits satisfy minimum access envelopes;
- primary device installation and cable routing happen before final stack compression;
- SSD preferred placement is used or alternate placement passes keepout validation;
- nut/tool access assumptions are represented in validation checks;
- fan envelope, actual airflow cutout, and 105 x 105 screw pattern are represented as separate validation concepts;
- primary rear cable corridor X -60 to +60 is checked against rear rod keepouts and cable bundle size;
- foot pad geometry preserves 3 to 5 mm clearance from the fan-compatible intake boundary;
- footprint containment keeps every active printable body inside 190 x 190 mm;
- printable body bounding boxes remain at or below 190.5 mm in X and Y;
- no outward ribs or tabs are generated from M5 compression islands;
- radial star-rib patterns around corner rod guides are clipped and filtered so only valid inward/load-path ribs remain;
- every rib has two valid endpoints;
- no dangling, floating, decorative, or unfinished ribs remain;
- no rib endpoint lies outside the footprint or connects only to reference geometry;
- no rib blocks airflow, rear service, cable, mounting, retainer, or tool access windows;
- printable STLs are watertight/manifold and contain no reference geometry;
- 120 x 120 fan-aligned zones are not implemented as full square cutouts;
- `PREFERRED_DEVICE_ZONE_*` is treated as a preferred planning zone, not a hard keepout;
- TPU feet are exported as separate TPU printable parts, not inside PETG `base_pedestal`;
- 260 mm M5 rods are treated only as CAD functional minimum, with 270-280 mm used for physical build planning;
- fan placeholders and fan screw pattern references remain out of printable STL.

Next recommended Codex task:

```text
mk0.12 CAD skeleton cleanup v3:
- rib topology repair;
- footprint containment;
- removal of outward M5 guide ribs/tabs;
- valid rib endpoints;
- no dangling/floating ribs;
- watertight printable bodies;
- protrusion/bounding-box validation.
- mass/airflow/cable/access validation reports.
```

Coupon parts remain blocked until CAD skeleton v3 passes:

- 0 FAIL in validation;
- footprint containment;
- rib topology validation;
- watertight STL checks;
- no outward/dangling ribs;
- no reference geometry in printable bodies;
- mass and airflow checks remain within accepted limits.

Only after this cleanup passes review should the project move to coupon parts.

Final document status:

```text
SPECIFICATION: PASS FOR CAD SKELETON V3 INPUT
CAD IMPLEMENTATION: NOT STARTED
COUPON PARTS: BLOCKED
FULL PRINT: BLOCKED
NEXT STEP: mk0.12 CAD skeleton cleanup v3
```
