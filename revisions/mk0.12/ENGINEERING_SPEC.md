# mk0.12 - Engineering Spec

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: PASS FOR CAD SKELETON V3 INPUT  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Purpose

mk0.12 defines an MVP two-module stack-through-rod construction for the Homelab Modular Tower. It is the engineering input for `mk0.12 CAD skeleton cleanup v3`.

The build target is not a hot-swappable blade chassis. It is a stack of printable PETG bodies aligned by four M5 threaded rods, compressed through washers, nuts, local compression pads, and reinforced corner zones.

## Frozen Architecture

```text
Architecture: mk0.12 MVP-2M stack-through-rod
Footprint: 190 x 190 mm
X range: -95 to +95
Y range: -95 to +95

Stack:
base_pedestal: Z 0..32
rpi_ssd_stack_module: Z 32..107
minipc_stack_module: Z 107..212
top_cap: Z 212..238
Total height: 238 mm

M5 rods:
(-80, -80)
(+80, -80)
(-80, +80)
(+80, +80)

Rear service zone:
Y +65..+95

Fan-compatible zones:
base/top 120 x 120 fan-compatible zones
internal modules use equivalent distributed airflow
```

## Load Path

Primary structural load path:

```text
M5 rods -> washers -> nuts -> compression pads -> top/bottom contact interfaces -> reinforced corner zones
```

Plastic parts are not the primary structural material. PETG parts provide:

- module positioning;
- device support;
- airflow geometry;
- cable routing geometry;
- washer/compression interfaces;
- future side-adapter reserve zones without active rails.

## Scope

In scope:

- `base_pedestal`;
- `rpi_ssd_stack_module`;
- `minipc_stack_module`;
- `top_cap`;
- M5 rods, washers, nuts as reference/assembly hardware;
- separate TPU feet;
- separate reference placeholders for devices, rods, washers, nuts, and fans;
- rear service windows and cable routing geometry;
- fan-aligned base/top inlet/outlet zones;
- distributed internal airflow through real geometry.

Out of scope:

- hot swapping;
- middle module removal without loosening the stack;
- active rails;
- sliding carriage;
- POM-C shoes;
- final UPS module;
- final MikroTik module;
- decorative side panels before structural validation;
- final rear service spine;
- coupon parts before CAD skeleton v3 validation.

Required service model:

```text
mk0.12 is not hot-swappable.
Middle module removal without loosening the stack is out of scope.
Primary device installation and cable routing must happen before final stack compression.
```

## Airflow Philosophy

Base and top provide 120 x 120 fan-compatible intake/exhaust zones. These zones are alignment envelopes, not automatic full square cutouts.

`FAN_ALIGNED_AIRFLOW_ZONE` is not the same as `ACTUAL_FAN_AIRFLOW_CUTOUT`. Actual cutouts must preserve fan screw boss material around the 105 x 105 screw pattern.

Internal modules do not need to preserve a mandatory central airflow shaft. They must provide equivalent distributed airflow through real openings:

- raised device supports;
- ribs;
- perforated trays;
- side bypass channels;
- bottom gaps under devices;
- ducted or split airflow around the Mini PC.

`INTERNAL_AIRFLOW_STRATEGY = "equivalent_distributed_airflow"` is a named strategy value for config/documentation use, not a geometric object by itself.

## Rear Service Philosophy

The rear service zone is Y +65..+95. It is a reserved routing envelope, not a completely empty full-width prism. Rear M5 rods and compression pads create local keepouts. Cable paths must be segmented around rear rod/compression-pad keepouts and should prefer the central rear corridor.

## Frozen Config-Oriented Values

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

`PREFERRED_DEVICE_ZONE_*` is a preferred planning zone, not a hard keepout. Device-specific clearance envelopes in `PARTS_SPEC.md` are authoritative.

## Engineering Decisions

- mk0.12 uses a custom stack-through-rod architecture, not an external CAD base.
- No active rails, sliding carriage, or POM-C shoe sockets are included in mk0.12.
- MVP contains exactly two real device modules: Raspberry Pi + SSD, and Mini PC.
- Rear service spine is reserved but not monolithic in MVP.
- Future expansion happens by adding stack modules, using longer M5 rods, preserving the M5 pattern, preserving the footprint, and preserving the rear service zone.
- Middle module removal without stack loosening is out of scope for MVP.

## Final Recommendation

Proceed to `mk0.12 CAD skeleton cleanup v3`, not coupon parts.

The next CAD iteration must implement rib topology repair, footprint containment, removal of outward M5 guide ribs/tabs, valid rib endpoints, no dangling/floating ribs, watertight printable bodies, protrusion/bounding-box validation, and mass/airflow/cable/access validation reports.

```text
SPECIFICATION: PASS FOR CAD SKELETON V3 INPUT
CAD IMPLEMENTATION: NOT STARTED
COUPON PARTS: BLOCKED
FULL PRINT: BLOCKED
NEXT STEP: mk0.12 CAD skeleton cleanup v3
```
