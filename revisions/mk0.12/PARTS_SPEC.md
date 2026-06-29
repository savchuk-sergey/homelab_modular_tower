# mk0.12 - Parts Spec

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: PART REQUIREMENTS READY FOR CAD SKELETON V3  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Common Printable Body Rules

Active PETG stack bodies:

- `base_pedestal`;
- `rpi_ssd_stack_module`;
- `minipc_stack_module`;
- `top_cap`.

All active PETG stack bodies must stay inside the frozen 190 x 190 mm footprint. Any active PETG feature outside X/Y +/-95.25 is FAIL. Any active PETG body bounding box above 190.5 mm in X or Y is FAIL.

Each active printable PETG body should normally be one connected printable body and must exclude device placeholders, rods, washers, nuts, fan placeholders, and other reference geometry.

Separate TPU feet, future wider foot extensions, or future stability parts must be documented and exported as separate printable parts. They must not be silently merged into the active PETG stack body.

## PETG/FDM Baseline Assumptions

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
```

## Rib Topology Rules

Ribs are structural/service/airflow geometry, not decoration. Every structural rib must have two valid endpoints.

Valid endpoints include:

- outer perimeter frame;
- M5 compression island;
- local reinforced land;
- fan ring or airflow opening frame;
- transverse or longitudinal rib;
- device support rail or boss pad;
- rear service or cable window frame lip;
- internal frame ring;
- documented structural rib junction.

Invalid endpoints include free-floating ends, tiny isolated tabs, endpoints outside the 190 x 190 footprint, endpoints touching only reference geometry, endpoints in unsupported thin webs below `MIN_PRINTABLE_WEB_THICKNESS`, or endpoints blocking cable/service/airflow access without documented reason.

M5 compression islands are near the footprint corners at X/Y +/-80 and are not central nodes. Ribs from corner M5 islands may connect only to adjacent perimeter frame walls inside the footprint, inward ribs, diagonal inward ribs toward structural nodes, or reinforced washer lands. Outward ribs/tabs, external spikes, and decorative star-shaped spokes are FAIL.

## `base_pedestal`

Purpose:

- lower structural locator;
- bottom intake;
- lower washer/nut zones;
- M5 rod pattern origin;
- PETG sockets/pads for separate TPU feet;
- future wider foot extension pilot points.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 0 to 32
Height: 32
M5 holes: 4 x diameter 5.6 at (-80,-80), (+80,-80), (-80,+80), (+80,+80)
Washer seats: diameter 13, depth 1.2, coaxial with M5 holes
Corner compression pads: 24 x 24 x 3, centered on each M5 rod
Fan-compatible intake zone: 120 x 120 envelope
Construction: ribbed frame or open pedestal, not a solid slab
Target mass: 120-220 g PETG
Soft review mass limit: 300 g PETG
Hard FAIL mass limit: >500 g PETG
```

Requirements:

- actual intake cutout must preserve fan screw boss material if bottom fan mounting holes are active;
- full 120 x 120 square void is not allowed as an interpretation of the fan-aligned zone;
- rear service clearance Y +65..+95 must be segmented around rear rod/compression keepouts;
- base frame ring and fan cutout edges must tie to corner compression zones with ribs;
- no external ribs or tabs outside X/Y +/-95;
- corner compression islands must connect inward to perimeter frame and fan/intake ring;
- rear service clearance must not be blocked by rib endpoints;
- outward star ribs around M5 rod guides are not allowed.

TPU feet:

- TPU feet are separate TPU printable parts;
- TPU feet must not be included in PETG `base_pedestal` STL;
- base may include PETG sockets, pads, pilot holes, or mounting features for TPU feet;
- 20 x 20 feet at offset +/-72 are not preferred and should be PARTIAL/FAIL unless intake clearance is explicitly validated;
- preferred 20 x 20 TPU foot center offset is +/-76 to +/-78;
- foot geometry must preserve 3 to 5 mm clearance from the fan-compatible intake zone.

Required checks remain NOT VERIFIED until CAD skeleton v3: printable body connectivity, fan boss material preservation, rear service segmentation, foot pad/intake clearance, washer seat compression strength, and print orientation.

## `rpi_ssd_stack_module`

Purpose:

- holds Raspberry Pi 3B;
- holds external SSD or 2.5 inch SSD/USB SSD through strap zone;
- provides airflow clearance;
- routes USB/power/cables rearward;
- stack layer between base and Mini PC module.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 32 to 107
Height: 75
M5 holes: same as base, diameter 5.6
Top/bottom compression pads: 24 x 24 x 3 at rod centers
Construction: ribbed-frame/open tray, not closed solid tray
Minimum effective airflow open area: 2500 mm2 absolute, 4000 mm2 preferred
```

Raspberry Pi placement:

```text
Board envelope: 85 x 56
Board clearance envelope: 95 x 66
ASSUMPTION board center: X -35, Y -35
Board clearance X range: -82.5 to +12.5
Board clearance Y range: -68 to -2
Mounting boss height: 5 to 8
Pilot holes: M2.5 or M3, exact coordinates NOT VERIFIED
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
```

Requirements:

- no external ribs or tabs outside X/Y +/-95;
- M5 compression islands must connect to perimeter frame and internal rib network;
- Pi support bosses/pads must connect to local ribs or tray rails;
- SSD support/strap zones must connect to local ribs or tray rails;
- cable corridor to rear service zone must remain open;
- ribs must not cross/block Pi/SSD mounting/tool access envelopes;
- ribs must not terminate inside Pi/SSD reference envelope unless they are device support features;
- cable path must be visibly open and must not pass through a closed wall.

Required checks remain NOT VERIFIED until CAD skeleton v3: Pi boss access, SSD strap access, open tray construction, printable body connectivity, effective airflow open area, cable window height, rib load path, and print orientation.

## `minipc_stack_module`

Purpose:

- holds Mini PC;
- provides dedicated airflow reserve;
- routes power/USB/Ethernet/HDMI cables rearward;
- thermal-priority and highest-mass MVP module.

Geometry:

```text
Outer footprint: 190 x 190
X range: -95 to +95
Y range: -95 to +95
Z range: 107 to 212
Height: 105
M5 holes: same as base, diameter 5.6
Top/bottom compression pads: 24 x 24 x 3 at rod centers
Construction: ribbed-frame/open tray, not a closed Mini PC box
Minimum effective airflow open area: 5000 mm2
MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN = 20.0
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
```

Mini PC front clearance rule:

```text
Mini PC clearance envelope may touch Y -95 only as a keepout envelope.
No front retainer, lip, rib, stop, tab, or other printable feature may protrude beyond Y -95.
If front retention is required, use side retainers, top strap geometry, or internal features that remain inside the 190 x 190 footprint.
Do not move Mini PC placement in documentation or cleanup tasks.
```

Requirements:

- no external ribs or tabs outside X/Y +/-95;
- no front protrusions beyond Y -95;
- M5 compression islands must connect to perimeter frame and internal rib network;
- support must use rails/ribs/pads with visible airflow gaps;
- rear cable exit from Y +40 to Y +65 must remain open;
- rear service windows must not be blocked by rib endpoints;
- ribs must not cross retainer/finger access zones;
- support ribs under Mini PC must preserve bottom/side airflow paths.

Required checks remain NOT VERIFIED until CAD skeleton v3: mounting/retainer access, open tray construction, printable body connectivity, effective airflow open area, rear cable exit height, rib load path, and print orientation.

## `top_cap`

Purpose:

- upper structural and positioning element;
- stack closure;
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
Fan-compatible exhaust zone: 120 x 120 envelope
Target mass: 100-200 g PETG
Soft review mass limit: 300 g PETG
Hard FAIL mass limit: >500 g PETG
```

Requirements:

- actual airflow cutout must preserve fan screw boss material around the 105 x 105 screw pattern if fan mounting is active;
- full 120 x 120 square void is not allowed as an interpretation of the fan-aligned zone;
- rear service continuation clearance Y +65..+95 must be segmented around rear corner pads;
- construction must be ribbed frame/open cap, not solid slab;
- fan screw bosses must connect to frame/ring through ribs or lands;
- top M5 compression islands must connect inward to perimeter frame and fan/exhaust ring;
- outward star ribs around M5 rod guides are not allowed.

Required checks remain NOT VERIFIED until CAD skeleton v3: printable body connectivity, fan boss material preservation, nut/tool access, and selected print orientation.

## M5 Hardware Set

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

260 mm is only a CAD functional minimum, not the physical build recommendation. Final physical rod length depends on washer thickness, nut type, thread engagement, PETG tolerances, possible nyloc nuts, and actual stack compression.

## Nut and Tool Access Assumptions

```text
M5 nut across flats: approximately 8
M5_NUT_HEIGHT_MIN_ASSUMPTION = 4
M5_NUT_HEIGHT_MAX_ASSUMPTION = 5
M5_NUT_ACCESS_DIAMETER_MIN_ASSUMPTION = 12
M5_NUT_ACCESS_DIAMETER_MAX_ASSUMPTION = 14
M5_SOCKET_ACCESS_DIAMETER_MIN_PREFERRED = 14
M5_SOCKET_ACCESS_DIAMETER_MAX_PREFERRED = 16
TOP_NUT_ACCESS_CLEARANCE_Z_MIN = 8
BOTTOM_NUT_ACCESS_CLEARANCE_Z_MIN = 8
BOTTOM_NUT_SIDE_ACCESS_POCKET_ALLOWED = true
```

CAD must not create blind nut pockets unreachable by fingers, wrench, socket, or nut driver.

## Reference Placeholders and Builders

Printable builders return printable plastic only. Reference builders return review/assembly geometry only.

Future reference files/functions may include:

```text
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

Fan placeholder/reference solids must not be part of printable STL. Fan screw holes/bosses are printable geometry only if fan mounting is active in the corresponding part.
