# mk0.12 - Interfaces

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: INTERFACE CONTRACTS READY FOR CAD SKELETON V3  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

Allowed status values:

```text
PASS
PARTIAL
FAIL
NOT VERIFIED
```

## Stable Interface Table

| Interface | Components | Geometry | Constraint | Status |
| --- | --- | --- | --- | --- |
| Base <-> RPi/SSD module | `base_pedestal`, `rpi_ssd_stack_module` | Contact plane at Z = 32; footprint 190 x 190; M5 holes at +/-80 X/Y | Planes must mate without device protrusion below RPi module | PASS |
| RPi/SSD module <-> Mini PC module | `rpi_ssd_stack_module`, `minipc_stack_module` | Contact plane at Z = 107; same M5 pattern and compression pads | Pi/SSD cable exits must stay below or inside module envelope | PARTIAL |
| Mini PC module <-> Top cap | `minipc_stack_module`, `top_cap` | Contact plane at Z = 212; same M5 pattern and compression pads | Mini PC top clearance must remain below Z = 212 | PASS by envelope assumption |
| M5 rods <-> all stack layers | rods, all printed layers | Four clearance holes diameter 5.6 at (-80,-80), (80,-80), (-80,80), (80,80) | Rod pattern must not change after spec freeze | PASS |
| Rear service zone <-> all modules | all printed layers | Y +65 to +95, depth 30, continuous Z 0 to 238 | Cable windows per module; no monolithic spine in MVP | PARTIAL |
| Fan-aligned inlet/outlet + distributed internal airflow <-> base/modules/top | base, modules, top | Base/top 120 x 120 fan-compatible zones; internal modules use equivalent distributed airflow through real openings | Devices may overlap the centered XY zone only if raised/perforated/bypass/ducted airflow is preserved as open geometry | PARTIAL |
| Printable geometry <-> reference geometry | printed parts, placeholders, hardware references | Printable STL contains only plastic body; assembly may include reference geometry | Device/hardware/fan placeholders must be separate from printable builders | NOT VERIFIED |
| Mounting/service access <-> device modules | `rpi_ssd_stack_module`, `minipc_stack_module` | Top/front/side tool access windows; rear cable exits before stack compression | Devices, retainers, straps, bosses, and cables must be reachable without cutting plastic | NOT VERIFIED |
| Washer/nut <-> base/top | rods, washers, nuts, `base_pedestal`, `top_cap` | Washer seat diameter 13, depth 1.2, centered on M5 holes | Seat must remain within corner pad and tool access zone | PARTIAL |
| Future side-adapter zones <-> modules | future adapters, stack modules | Reserved outside active MVP device/airflow zones, no active rails | Must not affect MVP M5 pattern | NOT VERIFIED |

## Assembly Plane Interfaces

- Base top plane Z = 32 must align with RPi/SSD bottom plane.
- RPi/SSD top plane Z = 107 must align with Mini PC bottom plane.
- Mini PC top plane Z = 212 must align with top cap bottom plane.
- Total stack height is 238 mm.

## M5 Stack Interface

All stack layers use M5 clearance holes diameter 5.6 at:

```text
(-80, -80)
(+80, -80)
(-80, +80)
(+80, +80)
```

The M5 rod pattern must not move unless a future task explicitly changes the revision architecture.

## Rear Service Interface

The rear service zone is Y +65..+95. It is continuous in Z from 0 to 238, but segmented in XY around rear rods and compression pads.

Preferred conservative primary cable corridor:

```text
PRIMARY_REAR_CABLE_CORRIDOR_X_MIN_PREFERRED = -60
PRIMARY_REAR_CABLE_CORRIDOR_X_MAX_PREFERRED = +60
PRIMARY_REAR_CABLE_CORRIDOR_X_MIN_ABSOLUTE_ASSUMPTION = -65
PRIMARY_REAR_CABLE_CORRIDOR_X_MAX_ABSOLUTE_ASSUMPTION = +65
```

Rear service represented only by annotation is FAIL. Every module must provide real rear service windows.

## Distributed Airflow Interface

Do not describe this interface as a required empty center shaft. The active interface is fan-aligned inlet/outlet plus distributed internal airflow.

Base/top fan-compatible zones are 120 x 120 mm. Actual cutouts are separate geometry and must preserve fan screw boss material. Internal module airflow can use raised supports, perforations, side bypass, bottom gaps, or ducted/split airflow.

Airflow represented only by annotation is FAIL.
