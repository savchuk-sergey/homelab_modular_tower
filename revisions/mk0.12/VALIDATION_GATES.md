# mk0.12 - Validation Gates

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: CAD SKELETON V3 GATES REQUIRED BEFORE COUPONS  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Gate Policy

CAD skeleton v3 must pass required validation gates before coupon parts. Any FAIL blocks coupon parts unless explicitly waived in review.

```text
COUPON PARTS: BLOCKED until CAD skeleton v3 passes validation.
FULL PRINT: BLOCKED until CAD skeleton v3 and physical validation pass.
```

## Thresholds

```text
bbox X/Y <= 190.5
active PETG features inside X/Y +/-95.25
MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_ABSOLUTE = 2500 mm2
MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_PREFERRED = 4000 mm2
MINIPC_MODULE_AIRFLOW_OPEN_AREA_MIN = 5000 mm2
MIN_CABLE_WINDOW_WIDTH = 12.0
MIN_CABLE_WINDOW_HEIGHT = 10.0
PREFERRED_CABLE_WINDOW_HEIGHT = 15.0
MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN = 20.0
MIN_TOOL_ACCESS_DIAMETER_AROUND_M2_5_BOSS = 8.0
MIN_TOOL_ACCESS_DIAMETER_AROUND_M3_BOSS = 9.0
MIN_FINGER_ACCESS_SLOT_WIDTH = 18.0
MIN_STRAP_PULL_TAB_ACCESS_WIDTH = 15.0
MIN_STRAP_PULL_TAB_ACCESS_DEPTH = 20.0
MIN_RETAINER_CLEARANCE_AROUND_SCREW_OR_CLIP = 10.0
```

## Mass Budget

| Printable part | Target PETG mass | Soft review limit | Hard FAIL limit |
| --- | ---: | ---: | ---: |
| `base_pedestal` | 120-220 g | 300 g | >500 g |
| `rpi_ssd_stack_module` | 150-300 g | 400 g | >800 g |
| `minipc_stack_module` | 250-450 g | 600 g | >800 g |
| `top_cap` | 100-200 g | 300 g | >500 g |
| total printed PETG | 620-1170 g | ~1600 g | >2500 g NO-GO |

Final production-optimized mass is not frozen. CAD skeleton v3 mass sanity gates are frozen for validation.

## CAD Validation Gate Table

| ID | Check | PASS Criteria | FAIL Criteria | Required Evidence |
| --- | --- | --- | --- | --- |
| V-GEO-001 | Footprint containment | All active PETG stack body features stay inside X/Y +/-95.25 | Any active PETG feature outside X/Y +/-95.25 | Top-view render with footprint boundary; coordinate/bbox report |
| V-GEO-002 | Bounding box | Each active PETG stack body has X <= 190.5 and Y <= 190.5 | Any active PETG stack body exceeds 190.5 in X or Y | Per-part bounding box report |
| V-GEO-003 | Protrusion classification | No active protrusions; any separate TPU/future extension is documented and exported separately | Undocumented rib, tab, guide, boss, foot pad, cable feature, or reference object protrudes from active body | Protrusion report by feature class |
| V-REF-001 | Printable/reference separation | Printable builders include printable plastic only | Device, rod, washer, nut, or fan placeholder in printable STL | Builder list and STL inspection |
| V-STL-001 | Watertight/manifold STL | Printable STL/body is watertight/manifold, no self-intersections, no non-manifold edges, no zero-thickness faces | Watertight false, non-manifold edges, self-intersection, zero-thickness face | STL quality report |
| V-STL-002 | Connected printable body | Each active PETG part is one connected printable component unless explicitly documented otherwise | Disconnected active PETG bodies or floating fragments | Connected-component report |
| V-RIB-001 | M5 compression island rib direction | Corner M5 islands connect inward or to adjacent perimeter/internal structural nodes | Outward ribs/tabs, external spikes, radial star-rib pattern around corner guides | Top-view rib map; M5 connection list |
| V-RIB-002 | Rib endpoint validity | Every structural rib has two valid endpoints | Any rib endpoint outside footprint, free-floating, connected only to reference geometry, or ending in unsupported thin web | Rib endpoint review |
| V-RIB-003 | Dangling/floating/decorative ribs | No dangling, floating, decorative, or unfinished ribs | Decorative rib without role, floating rib, rib blocking access/airflow/cables | Annotated top/render views |
| V-RIB-004 | Load-path-aware rib topology | Rib structure ties compression, frame, device-support, airflow-window, and service-window zones | Load path unclear or auto-generated pattern without structural purpose | Reviewer notes and rib map |
| V-AIR-001 | Effective open area per module | Each module >=2500 mm2 absolute, >=4000 mm2 preferred where applicable | Any module below 2500 mm2 | Open-area estimate/report |
| V-AIR-002 | Mini PC open area | Mini PC module >=5000 mm2 unless documented duct/bypass reviewed | Mini PC module below 5000 mm2 without approved strategy | Open-area estimate plus airflow views |
| V-AIR-003 | Fan zone vs cutout | 120 x 120 fan-compatible zone is not used as full square cutout; screw boss material preserved | Full square cutout removes boss material | Fan cutout review and screw pattern overlay |
| V-CBL-001 | Cable window width/height | Width >=12.0, height >=10.0, preferred height >=15.0 | Width below 12.0 or height below 10.0 | Cable window measurement report |
| V-CBL-002 | Mini PC rear cable exit | Rear exit height >= MINIPC_REAR_CABLE_EXIT_HEIGHT_MIN | Rear exit height below threshold unless specific low-profile/angled cable is documented | Rear exit measurement |
| V-ACC-001 | Tool/finger access | Bosses, screws, clips, straps, retainers, and cable exits meet access thresholds | Access below minimum or only possible after final compression | Access envelope views |
| V-MASS-001 | Per-part mass budget | Part masses at target/soft limit or explicitly justified | Hard FAIL limit exceeded or total >2500 g | Volume/mass report |
| V-ASM-001 | Stack assembly order | Devices and cables install/route before final stack compression | CAD requires primary install/routing after final compression | Assembly order note and exploded view |
| V-PRN-001 | Print orientation | Each printable part declares intended print orientation before export/review | Missing orientation or orientation causes unreviewed support traps/bridges | Orientation notes and slicer preview |
| V-PRN-002 | Slicer preview | No unsupported long bridges, hidden downward pockets, inaccessible support traps, or PETG-hostile overhangs unless documented | Unreviewed support traps, long bridges, impossible overhangs | Slicer preview screenshots/report |

## Required Evidence Summary

- top-view render with footprint boundary overlay;
- top-view render with rib endpoints visible;
- list of M5 compression island connections;
- printable/reference builder split;
- per-part bounding box report;
- protrusion classification report;
- STL watertight/manifold report;
- connected-component report;
- effective airflow open-area report;
- cable window width/height report;
- tool/finger access envelope views;
- per-part mass report;
- declared print orientation for each printable part;
- slicer preview report.

## NO-GO Conditions

- active future validation references to CAD skeleton v2;
- treating fan-compatible zone as full square cutout;
- treating distributed airflow as a required empty center shaft;
- active PETG feature outside footprint;
- PETG stack body bbox above 190.5 mm in X or Y;
- TPU feet merged into PETG `base_pedestal` STL;
- outward M5 island ribs/tabs;
- invalid rib endpoint;
- dangling/floating/decorative ribs;
- non-watertight or non-manifold printable STL;
- reference geometry in printable STL;
- rear service or airflow represented only as annotation;
- cable/window/access thresholds below minimum;
- 260 mm rod described as physical build recommendation.
