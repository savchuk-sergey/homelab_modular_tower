# mk0.10 Drawing Plan

## 1. Purpose

`mk0.10` is a planning and architecture-freeze revision.

The goal of this document is to define a small set of engineering drawings that must be prepared before the next major CAD implementation step.

This drawing plan exists because the project has reached a point where direct iteration through full CadQuery tower revisions is too expensive and error-prone.

The new process is:

```text
requirements -> architecture drawings -> interface drawings -> test jigs -> CadQuery implementation -> export/review
```

The drawings in this plan are not final manufacturing drawings. They are architecture and interface drawings intended to:

- reduce ambiguity before CAD implementation;
- freeze module interfaces;
- make LLM/Codex/Kimi tasks more constrained;
- separate design thinking from 3D modelling;
- prevent accidental architectural changes;
- make future revisions easier to review.

## 2. Current Project State

Latest source revision considered by this plan:

```text
mk0.9.3
```

Current relevant source assumptions:

```text
Nominal tower width: 190 mm
Nominal tower depth: 190 mm
Rear reserved zone: 30 mm
Base module height: 48 mm
RPi/SSD module height: 70 mm
Mini PC placeholder module height: 82 mm
Roof module height: 46 mm
Current stack height: 246 mm without external rod/thread allowance
```

Current rail/carriage standard:

```text
Aluminum U-channel rail: 15 x 10 x 10 x 2 mm
Estimated inner width: 11 mm
POM-C round shoe: Ø8 x 12 mm
Runner concept: short perpendicular replaceable shoes
Retention: M3 clamp screw into PETG / heat-set insert geometry
```

Current structural principles:

```text
M5 rods provide vertical compression.
PETG parts provide interfaces, frames, holders, ducts, and local support.
PETG must not be the final sliding/wear surface.
Base and roof are structural caps, not full-height device modules.
Modules must remain removable without full tower disassembly.
```

## 3. Open-Source Design References

The drawing plan should preserve lessons learned from earlier open-source research.

### 3.1 RackStack / Rackfinity lessons

Use:

- repeated modular interface;
- stackable module logic;
- metal rods / threaded rods for global compression;
- lightweight printed parts around a stronger mechanical standard.

Avoid:

- relying on massive plastic for stiffness;
- per-module one-off interfaces;
- hidden non-standard mounting logic.

### 3.2 mini-itx-nas-case lessons

Use:

- disciplined separation of printable parts and purchased parts;
- PETG/TPU material separation;
- fan/filter/service access planning;
- explicit export and print documentation.

Avoid:

- large decorative shells before airflow and serviceability are proven;
- support-heavy geometry without reason.

### 3.3 Antmicro-style documentation lessons

Use:

- clear drawings;
- BOM;
- placeholders;
- assembly notes;
- separate manufacturing/review artifacts;
- revision-specific documentation.

Avoid:

- CAD-only decisions with no written rationale;
- generated STL/STEP artifacts without explanation.

### 3.4 N5 Mini NAS / compact electronics enclosure lessons

Use:

- compact device layout;
- removable computing tray logic;
- clear cable routing;
- local airflow priority for compute module.

Avoid:

- locking the design to placeholder dimensions before real device measurement;
- finalizing Mini PC details before measuring the real Mini PC.

## 4. Drawing Strategy

The project should use three kinds of drawings.

### 4.1 Architecture drawings

Purpose:

```text
Show the whole tower layout and main engineering decisions.
```

Used for:

- architecture freeze;
- module height planning;
- airflow planning;
- rough serviceability review.

### 4.2 Interface drawings

Purpose:

```text
Define exactly how modules, rails, rods, shoes, feet, fans and filters interface.
```

Used for:

- Codex/Kimi implementation constraints;
- test jig design;
- preventing accidental interface drift.

### 4.3 Manufacturing-support drawings

Purpose:

```text
Help with printing, assembly, and fit testing.
```

Used for:

- print manifest;
- test jig instructions;
- assembly order;
- physical validation.

`mk0.10` should focus mostly on architecture and interface drawings. Full manufacturing drawings for every part are out of scope.

## 5. Drawing Output Format

Preferred output:

```text
drawings/mk0.10/*.svg
```

Recommended generation method:

```text
Python script -> SVG drawings
```

Suggested script:

```text
scripts/generate_architecture_drawings.py
```

The SVG drawings should be simple and parameter-driven. They do not need to be beautiful, but they must be readable.

The drawing generator should read dimensions from `cad/config.py` where possible.

CadQuery remains the source of truth for 3D geometry.

SVG drawings are a planning and interface layer, not a replacement for CadQuery.

Recommended future flow:

```text
cad/config.py
  -> scripts/generate_architecture_drawings.py
  -> drawings/mk0.10/*.svg

cad/config.py
  -> CadQuery parts
  -> STEP/STL exports
```

## 6. Required Drawings

`mk0.10` should produce the following drawings.

```text
01_architecture_layout_front.svg
02_architecture_layout_side.svg
03_module_interface_top.svg
04_module_interface_section.svg
05_rail_carriage_section.svg
06_carriage_top_view.svg
07_base_fan_filter_foot_section.svg
08_roof_exhaust_section.svg
09_rear_service_zone_top.svg
10_validation_test_jigs_plan.svg
```

The first five are mandatory.

The remaining five are recommended before the next full tower CAD integration.

## 7. Drawing 01 — Architecture Layout Front View

File:

```text
drawings/mk0.10/01_architecture_layout_front.svg
```

Purpose:

Show the tower from the front and fix the vertical stack architecture.

Must show:

- base module;
- RPi/SSD module;
- Mini PC placeholder module;
- roof module;
- M5 rod positions;
- front removable carriage direction;
- module boundaries;
- approximate module heights;
- total stack height;
- bottom foot clearance;
- top/bottom fan zones;
- current revision labels.

Required dimensions:

```text
TOWER_WIDTH
BASE_MODULE_HEIGHT
RPI_SSD_MODULE_HEIGHT
MINI_PC_MODULE_HEIGHT
ROOF_MODULE_HEIGHT
TOWER_HEIGHT
FOOT_HEIGHT
ROD_CENTER_OFFSET
```

Required annotations:

```text
Base and roof are structural caps, not device modules.
Carriages remove from the front.
Mini PC geometry is placeholder-based.
M5 rods provide compression, not positioning alone.
```

Design review questions:

- Are base and roof visually too tall?
- Are module heights proportional to their purpose?
- Does the tower still look like a modular blade stack?
- Is there enough front service access?

## 8. Drawing 02 — Architecture Layout Side View

File:

```text
drawings/mk0.10/02_architecture_layout_side.svg
```

Purpose:

Show airflow, rear service zone, device zones, and carriage direction in side view.

Must show:

- front side;
- rear side;
- rear reserved zone;
- bottom intake airflow;
- top exhaust airflow;
- central airflow channel;
- Mini PC airflow priority area;
- cable/service zone behind modules;
- fan positions.

Required dimensions:

```text
TOWER_DEPTH
REAR_RESERVED_DEPTH
MODULE_USABLE_DEPTH
AIRFLOW_CHANNEL_DEPTH
FAN_120_SIZE
FAN_120_THICKNESS
BOTTOM_AIR_INTAKE_CLEARANCE
```

Required annotations:

```text
All cables route through rear reserved zone.
No full-width solid floors across airflow path.
Mini PC airflow has priority.
Bottom fan intake and top fan exhaust must not be blocked.
```

Design review questions:

- Does the lower fan blow into an open path?
- Does the roof exhaust have enough open area?
- Does rear cable routing conflict with airflow?
- Are service zones separated from airflow zones?

## 9. Drawing 03 — Tower Module Interface Top View

File:

```text
drawings/mk0.10/03_module_interface_top.svg
```

Purpose:

Freeze the common top/bottom interface used by all stackable modules.

This is one of the most important drawings in the project.

Must show:

- nominal module footprint;
- M5 rod clearance holes;
- alignment pins;
- alignment sockets;
- local interface bolt positions;
- central airflow window;
- rear reserved zone;
- module frame rails;
- forbidden solid-floor zone.

Required dimensions:

```text
TOWER_WIDTH
TOWER_DEPTH
REAR_RESERVED_DEPTH
MODULE_USABLE_DEPTH
MODULE_FRAME_RAIL
ROD_CENTER_OFFSET
ROD_CLEARANCE
INTERFACE_PIN_DIAMETER
INTERFACE_PIN_CLEARANCE
INTERFACE_BOLT_CLEARANCE
INTERFACE_BOLT_CENTER_OFFSET
INTERFACE_LOCAL_BOLT_OFFSET_Y
AIRFLOW_CHANNEL_WIDTH
AIRFLOW_CHANNEL_DEPTH
```

Required annotations:

```text
M5 rods clamp the stack.
Alignment pins/sockets locate modules.
M3/M4 local screws only lock interfaces.
Airflow window must remain open unless explicitly justified.
Rear reserved zone is not a device tray area.
```

Frozen decisions:

```text
All future modules must use this interface unless mk1.x explicitly changes the standard.
```

Design review questions:

- Can every module share this interface?
- Are M5 rods far enough from airflow/device zones?
- Are pins and sockets separate from rod clearance?
- Is rear service zone preserved?

## 10. Drawing 04 — Module Interface Section

File:

```text
drawings/mk0.10/04_module_interface_section.svg
```

Purpose:

Show the vertical interface between two stacked modules.

Must show:

- lower module top ring;
- upper module bottom ring;
- alignment pin/socket engagement;
- M5 rod clearance;
- washer/nut zone concept;
- module interface height;
- local screw concept;
- airflow opening through the interface.

Required dimensions:

```text
MODULE_INTERFACE_HEIGHT
INTERFACE_PIN_HEIGHT
INTERFACE_SOCKET_DEPTH
ROD_CLEARANCE
M5_WASHER_DIAMETER
M5_WASHER_SEAT_DEPTH
M5_NUT_FLAT_DIAMETER
M5_NUT_SEAT_DEPTH
WALL_THICKNESS
MODULE_FRAME_RAIL
```

Required annotations:

```text
Plastic interface aligns modules.
M5 hardware compresses modules.
Interface must not become a massive solid slab.
Washer/nut zones should be local, not full-thickness mass.
```

Design review questions:

- Is the interface printable without excessive support?
- Is there enough engagement for alignment pins?
- Is the rod hole only clearance, not precision alignment?
- Can modules be removed without destroying the stack concept?

## 11. Drawing 05 — Rail / Carriage Cross-Section

File:

```text
drawings/mk0.10/05_rail_carriage_section.svg
```

Purpose:

Freeze and explain the rail/shoe/carriage concept before more CAD work.

Must show:

- aluminum U-channel rail;
- outer rail size 15 x 10 x 10 x 2;
- inner channel width around 11 mm;
- POM-C Ø8 shoe;
- PETG carriage side wall;
- POM-C socket;
- M3 clamp screw;
- heat-set insert / PETG boss concept;
- rail pocket carrier;
- clearance zones.

Required dimensions:

```text
RAIL_OUTER_WIDTH
RAIL_OUTER_HEIGHT
RAIL_WALL_THICKNESS
RAIL_INNER_WIDTH
RAIL_POCKET_WIDTH
RAIL_POCKET_HEIGHT
RAIL_POCKET_CLEARANCE
RUNNER_DIAMETER
RUNNER_SHOE_LENGTH
RUNNER_INSERT_DEPTH_INTO_CARRIAGE
RUNNER_PROTRUSION_FROM_CARRIAGE
RUNNER_SOCKET_DIAMETER
RUNNER_SOCKET_DEPTH
CARRIAGE_SIDE_WALL_THICKNESS
CARRIAGE_RUNNER_BOSS_DIAMETER
CARRIAGE_RUNNER_BOSS_THICKNESS
RUNNER_RETENTION_SCREW_DIAMETER
HEAT_SET_INSERT_M3_DIAMETER
HEAT_SET_INSERT_M3_DEPTH
```

Required annotations:

```text
Aluminum rail is non-printed.
POM-C shoe is non-printed wear part.
PETG must not be final sliding surface.
Clamp screw must not thread into POM-C as the primary retention.
Shoe must be replaceable.
```

Design review questions:

- Does Ø8 POM-C have enough clearance in the 15x10x10x2 rail?
- Can the shoe be installed and removed?
- Can the clamp screw be accessed?
- Is the PETG boss strong enough?
- Is the rail pocket printable?

Mandatory follow-up:

```text
Create rail_shoe_test_jig before relying on this interface in full tower print.
```

## 12. Drawing 06 — Carriage Top View

File:

```text
drawings/mk0.10/06_carriage_top_view.svg
```

Purpose:

Define the open-frame carriage layout.

Must show:

- carriage outer footprint;
- side beams;
- front pull lip;
- M3 front lock screw;
- rear cable exit;
- airflow window;
- POM-C shoe locations;
- device mounting pads;
- RPi 3B placeholder zone;
- external SSD placeholder zone;
- Mini PC placeholder zone variant.

Required dimensions:

```text
MODULE_WIDTH
MODULE_DEPTH
CARRIAGE_WALL_THICKNESS
CARRIAGE_SIDE_WALL_THICKNESS
CARRIAGE_RIB_THICKNESS
CARRIAGE_PULL_LIP_WIDTH
CARRIAGE_PULL_LIP_DEPTH
CARRIAGE_PULL_LIP_HEIGHT
CARRIAGE_LOCK_SCREW_CLEARANCE
CARRIAGE_SHOE_END_INSET
RUNNER_SHOES_PER_SIDE_RPI_SSD
RUNNER_SHOES_PER_SIDE_MINI_PC
REAR_CABLE_EXIT_WIDTH
REAR_CABLE_EXIT_HEIGHT
AIRFLOW_CHANNEL_WIDTH
AIRFLOW_CHANNEL_DEPTH
RPI3B_BOARD_WIDTH
RPI3B_BOARD_DEPTH
EXTERNAL_SSD_PLACEHOLDER_WIDTH
EXTERNAL_SSD_PLACEHOLDER_DEPTH
MINI_PC_PLACEHOLDER_WIDTH
MINI_PC_PLACEHOLDER_DEPTH
```

Required annotations:

```text
No solid carriage floor.
Local pads only where needed.
Airflow window remains open.
Runner bosses are reinforced locally.
Mini PC carriage is placeholder-based until real measurements.
```

Design review questions:

- Is the carriage too light around the shoe bosses?
- Is the front pull lip strong enough?
- Does the rear cable exit align with rear service zone?
- Is airflow preserved under devices?

## 13. Drawing 07 — Base Fan / Filter / Foot Section

File:

```text
drawings/mk0.10/07_base_fan_filter_foot_section.svg
```

Purpose:

Define the lower intake architecture and prevent a closed basement.

Must show:

- table surface;
- TPU/rubber foot;
- bottom air gap;
- foot mount socket;
- dust filter slot;
- bottom grill;
- 120 mm fan;
- base frame;
- M5 rod/corner zone;
- airflow direction upward.

Required dimensions:

```text
BASE_MODULE_HEIGHT
FOOT_HEIGHT
FOOT_DIAMETER
FOOT_SOCKET_DIAMETER
FOOT_SOCKET_DEPTH
BOTTOM_AIR_INTAKE_CLEARANCE
FAN_120_SIZE
FAN_120_THICKNESS
FAN_120_HOLE_SPACING
FAN_MOUNT_FRAME_MARGIN
FAN_GRILL_FRAME_MARGIN
FILTER_SLOT_HEIGHT
BASE_FILTER_TRAY_WIDTH
BASE_FILTER_TRAY_DEPTH
ROD_CLEARANCE
ROD_CENTER_OFFSET
```

Required annotations:

```text
Base must remain a light structural cap.
Foot clearance provides bottom intake gap.
Filter must be serviceable.
Bottom fan must not blow into a solid floor.
```

Design review questions:

- Is 12 mm bottom gap enough?
- Can the dust filter be removed?
- Does the fan have a clear intake?
- Is the base too tall for its function?

## 14. Drawing 08 — Roof Exhaust Section

File:

```text
drawings/mk0.10/08_roof_exhaust_section.svg
```

Purpose:

Define the upper exhaust architecture and keep roof mass under control.

Must show:

- roof frame;
- 120 mm exhaust fan;
- top grill;
- top guard/filter mesh slot;
- optional lightweight shroud;
- M5 rod/corner zone;
- airflow direction upward.

Required dimensions:

```text
ROOF_MODULE_HEIGHT
FAN_120_SIZE
FAN_120_THICKNESS
FAN_120_HOLE_SPACING
TOP_GUARD_FRAME_HEIGHT
FILTER_SLOT_HEIGHT
FAN_SHROUD_HEIGHT
FAN_SHROUD_WALL
FAN_MOUNT_FRAME_MARGIN
FAN_GRILL_FRAME_MARGIN
ROD_CLEARANCE
ROD_CENTER_OFFSET
```

Required annotations:

```text
Roof is a light structural cap.
Top mass should be minimized.
Exhaust must not be restricted by decorative plastic.
Shroud is allowed only if it helps airflow or mounting.
```

Design review questions:

- Is the roof still too massive?
- Does the fan exhaust have enough open area?
- Is the shroud justified?
- Are M5 nut/washer zones local rather than massive?

## 15. Drawing 09 — Rear Service Zone Top View

File:

```text
drawings/mk0.10/09_rear_service_zone_top.svg
```

Purpose:

Define how rear service routing coexists with modules and airflow.

Must show:

- rear reserved zone;
- cable path;
- power bus reserved path;
- Ethernet/USB cable path;
- fan cable path;
- rear exit from carriages;
- keep-out zones;
- relation to airflow window.

Required dimensions:

```text
REAR_RESERVED_DEPTH
REAR_CABLE_EXIT_WIDTH
REAR_CABLE_EXIT_HEIGHT
REAR_SPINE_WIDTH
REAR_SPINE_DEPTH
POWER_BUS_WIDTH
POWER_BUS_PAD_DEPTH
MODULE_USABLE_DEPTH
AIRFLOW_CHANNEL_WIDTH
AIRFLOW_CHANNEL_DEPTH
```

Required annotations:

```text
All cables route through rear service zone.
Rear service zone must not become random unused volume.
Power and signal should be separable in future revision.
Do not finalize power bus geometry in mk0.10.
```

Design review questions:

- Are cable exits aligned with the service zone?
- Does cable routing conflict with module extraction?
- Is there enough depth for connectors and bend radius?
- Is the rear service zone preserved across modules?

## 16. Drawing 10 — Validation Test Jigs Plan

File:

```text
drawings/mk0.10/10_validation_test_jigs_plan.svg
```

Purpose:

Define small validation prints before the next full tower iteration.

Must show at least four test jigs:

```text
1. rail_shoe_test_jig
2. module_interface_coupon
3. base_fan_filter_foot_coupon
4. carriage_stiffness_coupon
```

Each jig must have a specific question.

### 16.1 Rail/shoe test jig

Question:

```text
Does the aluminum U-channel 15x10x10x2 + POM-C Ø8 shoe + M3 clamp actually work?
```

Must test:

- rail pocket fit;
- shoe socket fit;
- clamp screw access;
- sliding clearance;
- shoe retention;
- print tolerances.

### 16.2 Module interface coupon

Question:

```text
Do alignment pins/sockets, M5 rod clearance and local bolts align correctly?
```

Must test:

- two stacked interface plates;
- rod holes;
- pins/sockets;
- local screws;
- tolerance and wobble.

### 16.3 Base fan/filter/foot coupon

Question:

```text
Does the lower intake package work before printing the full base?
```

Must test:

- foot socket;
- bottom gap;
- filter slot;
- grill;
- fan screw pattern.

### 16.4 Carriage stiffness coupon

Question:

```text
Are side beams, shoe bosses and pull lip stiff enough without a solid floor?
```

Must test:

- local runner boss stiffness;
- front pull lip;
- lock screw boss;
- mini PC placeholder load case.

Required annotations:

```text
No full tower print before critical interfaces are tested.
Test jigs are cheaper than full-module reprints.
Each jig must produce a pass/fail decision.
```

## 17. Drawing Style Rules

Drawings should be simple and engineering-focused.

Use:

- black/gray linework;
- clear labels;
- dimension arrows;
- section hatching only if helpful;
- color only for semantic zones if needed.

Suggested semantic colors if SVG generator supports them:

```text
PETG printed parts: light gray
TPU / rubber feet: dark gray
Metal parts: blue-gray
POM-C wear parts: yellow/orange
Airflow: blue arrows
Cable/service zones: purple
Keep-out zones: red outline
```

Do not use decorative rendering.

Do not use photorealistic views.

Each drawing should answer an engineering question.

## 18. Required Drawing Metadata

Each drawing should include:

```text
Project: Homelab Modular Tower
Revision: mk0.10 planning
Source basis: mk0.9.3
Drawing number
Drawing title
Units: mm
Status: planning / interface freeze / review
Date
```

Example:

```text
HMT-mk0.10-DWG-05
Rail / Carriage Cross-Section
Units: mm
Status: Interface Planning
```

## 19. Source-of-Truth Rules

CadQuery remains source of truth for 3D geometry.

The SVG drawings are not final manufacturing source.

However, drawings should be treated as source of truth for architecture decisions until replaced by a later architecture-freeze document.

Rules:

```text
If a drawing and CAD disagree, stop and resolve before continuing.
If a drawing lacks a dimension, do not let Codex/Kimi invent it silently.
If a subsystem is not shown in drawings, it should not be added to CAD automatically.
```

## 20. Out of Scope for mk0.10 Drawings

Do not draw or finalize:

- final Mini PC tray;
- final Mini PC duct;
- final Mini PC rear I/O;
- final UPS;
- final power distribution;
- final router module;
- final full Rear Service Spine;
- final side panels;
- decorative panels;
- production-grade toleranced drawings for every printed part.

These remain future work.

## 21. Acceptance Criteria

`DRAWING_PLAN.md` is complete when:

- required drawing list is defined;
- each drawing has a purpose;
- each drawing lists required dimensions;
- each drawing lists required annotations;
- each drawing has design review questions;
- drawings support the current mk0.9.3 architecture;
- open-source design lessons are reflected;
- test jigs are explicitly planned before full tower iteration;
- no drawing encourages adding new subsystems before interfaces are validated.

`mk0.10` drawing phase is complete when:

```text
01_architecture_layout_front.svg exists
02_architecture_layout_side.svg exists
03_module_interface_top.svg exists
04_module_interface_section.svg exists
05_rail_carriage_section.svg exists
```

Recommended completion before next full CAD integration:

```text
06_carriage_top_view.svg
07_base_fan_filter_foot_section.svg
08_roof_exhaust_section.svg
09_rear_service_zone_top.svg
10_validation_test_jigs_plan.svg
```

## 22. Recommended Next Implementation Step

After this document is created, the next task should be:

```text
Create scripts/generate_architecture_drawings.py for mk0.10.

The script should generate simple SVG drawings from cad/config.py:
- 01_architecture_layout_front.svg
- 02_architecture_layout_side.svg
- 03_module_interface_top.svg
- 04_module_interface_section.svg
- 05_rail_carriage_section.svg

Do not modify CadQuery geometry.
Do not change mk0.9.3 CAD.
Do not add new tower features.
Only generate planning drawings.
```

## 23. Engineering Principle

The project should not continue with full tower CAD changes until the main interfaces are visible and reviewable in 2D.

The purpose of `mk0.10` is to move the project from:

```text
LLM-driven CAD exploration
```

towards:

```text
engineering-driven product development
```

The drawings are not bureaucracy. They are a control layer that prevents repeated redesign, accidental interface drift, and expensive full-model rework.
