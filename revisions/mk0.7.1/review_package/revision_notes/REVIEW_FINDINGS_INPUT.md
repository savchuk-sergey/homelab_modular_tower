# mk0.7.1 Review Findings Input

Revision `mk0.7.1` ingests the mk0.7 engineering review as a patch-release input. This file summarizes only findings present in the review artifacts or directly inferable from their evidence.

## Source Files

- `reviews/mk0.7/engineering_review.md`
- `reviews/mk0.7/agent_outputs/01_cad_integrity.md`
- `reviews/mk0.7/agent_outputs/02_printability.md`
- `reviews/mk0.7/agent_outputs/03_structural_integrity.md`
- `reviews/mk0.7/agent_outputs/04_airflow_cooling.md`
- `reviews/mk0.7/agent_outputs/05_modularity_serviceability.md`
- `reviews/mk0.7/agent_outputs/06_power_cable_management.md`
- `reviews/mk0.7/agent_outputs/07_plastic_efficiency.md`
- `reviews/mk0.7/agent_outputs/08_manufacturability.md`
- `reviews/mk0.7/agent_outputs/09_red_team.md`
- `reviews/mk0.7/agent_outputs/10_requirements_checklist.md`
- `revisions/mk0.7/review_package/analysis/part_dimensions.csv`
- `revisions/mk0.7/review_package/analysis/printability_check.csv`
- `revisions/mk0.7/review_package/analysis/part_volume.csv`
- `revisions/mk0.7/review_package/analysis/stl_quality.csv`
- `revisions/mk0.7/review_package/analysis/duplicate_geometry_check.csv`

## CAD Integrity

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| CAD-001 | `bottom_fan_cartridge` handle is disconnected from the body. | `01_cad_integrity.md`, `stl_quality.csv` | Review reports a 3.0 mm gap and nonmanifold printable STL. | CONFIRMED | BLOCKER | Move the handle Y offset to the cartridge edge using the rail half-width. |
| CAD-002 | `REAR_SPINE_COVER_THICKNESS` is defined twice with different values. | `01_cad_integrity.md`, `cad/config.py` | 2.0 mm then 3.0 mm; second value shadows first. | CONFIRMED | HIGH | Keep one explicit value matching exported mk0.7 intent. |
| CAD-003 | UPS battery marker makes the tray exceed the 170 mm module width. | `01_cad_integrity.md`, `part_dimensions.csv` | `ups_power_tray` exported width is 186.5 mm. | CONFIRMED | HIGH | Constrain UPS marker zones inside module width or defer deeper UPS redesign. |
| CAD-004 | Power bus cover holes do not align with panel holes. | `01_cad_integrity.md` | Cover holes at X=0, panel holes at X=+/-7.0. | CONFIRMED | HIGH | Match cover holes to the panel pad screw X offset. |
| CAD-005 | Bottom and top fan grilles overlap structural frames. | `01_cad_integrity.md` | Review reports 3.5 mm overlap at both frame interfaces. | CONFIRMED | MEDIUM | Move grille Z positions outside the frame thickness. |
| CAD-006 | Some engineering constants remain unnamed. | `01_cad_integrity.md` | Airflow arrow head ratio and rotation angle are hardcoded. | CONFIRMED | MEDIUM | Add named config values for review geometry constants. |

## Printability

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| PRN-001 | `rear_service_spine` does not fit Bambu Lab P2S in any orientation. | `02_printability.md`, `printability_check.csv` | 80 x 40 x 297.5 mm; review estimates minimum diagonal projection above 256 mm. | CONFIRMED | BLOCKER | Defer split redesign to mk0.8 unless a low-risk segmentation already exists. |
| PRN-002 | `power_bus_panel`, `power_bus_cover`, and `rear_service_spine_cover` exceed axis-aligned volume and are high-warp strips. | `02_printability.md`, `printability_check.csv` | Z dimensions 265.5-295.5 mm. | CONFIRMED | HIGH | Document as mk0.8 split work unless safe patch segmentation is implemented. |
| PRN-003 | `foot` is routed as generic plastic although it is a TPU foot. | `02_printability.md`, `cad/parts/feet.py` | Source function is `make_wide_tpu_foot_placeholder`; project rules assign TPU to feet. | CONFIRMED | HIGH | Export to `printable/tpu` and document separately. |
| PRN-004 | `TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG` is below `MIN_PRINTABLE_FEATURE`. | `02_printability.md`, `cad/config.py` | 0.5 mm vs 1.2 mm minimum. | CONFIRMED | MEDIUM | Increase to the configured minimum or document deferred tray connector redesign. |
| PRN-005 | Large flat parts have PETG warping risk. | `02_printability.md` | Frames, grilles, side panels, and wings have large thin footprints. | LIKELY | MEDIUM | Add print guidance and leave physical validation as required. |

## Structural Integrity

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| STR-001 | Dynamic tipping hazard when Mini PC tray is extended. | `engineering_review.md`, `09_red_team.md` | Tray front overhangs base by about 41 mm during service travel. | CONFIRMED | BLOCKER | Record as not fully patch-fixable; reduce claims and defer anti-tip redesign to mk0.8. |
| STR-002 | Metal guide rails lack modeled frame fastening interfaces. | `engineering_review.md`, `09_red_team.md` | Rails have holes; frames only have clearance slots. | CONFIRMED | HIGH | Defer full rail retention redesign unless a small interface patch is safe. |
| STR-003 | Corner blocks are placed at mid-height instead of frame corners. | `engineering_review.md` | Assembly uses `TOWER_HEIGHT / 2` for corner block Z. | CONFIRMED | HIGH | Move assembly placement to top and bottom frame corner positions. |
| STR-004 | Top frame clamping geometry may be reversed. | `engineering_review.md` | Review says top nut/washer seats are on wrong sides. | CONFIRMED | HIGH | Inspect before changing; patch only if local code confirms. |
| STR-005 | Foot screw interface is weak for PETG. | `09_red_team.md` | 3 mm socket with no heat-set insert. | LIKELY | HIGH | Document as required physical/test redesign; avoid risky unvalidated insert redesign in patch. |

## Airflow And Cooling

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| AIR-001 | Tray vent slots are blocked by device placeholders. | `04_airflow_cooling.md` | All devices sit directly on the base vent grid. | CONFIRMED | BLOCKER | Document as mk0.8 tray airflow redesign; patch can only improve review clarity. |
| AIR-002 | Top exhaust fan placeholder is missing from assembly. | `engineering_review.md`, `04_airflow_cooling.md` | Only top grille is present in mk0.7 assembly. | CONFIRMED | HIGH | Add top `fan_120x120x25_placeholder` to assembly/review exports only. |
| AIR-003 | Mini PC duct is placeholder-level and not connected to real Mini PC geometry. | `04_airflow_cooling.md` | Duct has no side port and is narrower than Mini PC placeholder. | CONFIRMED | HIGH | Keep as review/placeholder-level; document no CFD or thermal validation. |
| AIR-004 | Bottom filter hardware is not integrated and filter side is unresolved. | `04_airflow_cooling.md` | Filter frame/retainer not placed in assembly; rails above grille. | CONFIRMED | MEDIUM | Document limitation; avoid claiming filtered-intake readiness. |
| AIR-005 | Temperature review markers are in stagnant rear zone. | `04_airflow_cooling.md` | Points at y about 68-70 near spine front. | CONFIRMED | MEDIUM | Move review markers to central airflow path for review clarity. |

## Modularity

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| MOD-001 | Rear Service Spine cable process weakens tool-less module extraction claims. | `09_red_team.md`, `05_modularity_serviceability.md` | Module removal requires cable disconnection and cover access. | LIKELY | MEDIUM | Document service limitation; defer quick-disconnect architecture to mk0.8. |
| MOD-002 | Placeholder dimensions are not verified against real hardware. | `09_red_team.md`, `cad/config.py` | TODOs on MikroTik and Mini PC dimensions. | CONFIRMED | HIGH | Keep placeholder manifests explicit and avoid stable-fit claims. |

## Serviceability

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| SRV-001 | Bottom fan cartridge has no confirmed retention into the base. | `01_cad_integrity.md`, `09_red_team.md` | Cartridge mount holes exist but base mate is not modeled. | CONFIRMED | HIGH | Document required fit test and future retention patch. |
| SRV-002 | Fan filter replacement path is unresolved. | `04_airflow_cooling.md` | Filter material and stack position are not defined. | UNCERTAIN | MEDIUM | Record as limitation; no unsupported filter-performance claim. |

## Power And Cable Management

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| PWR-001 | DC power bus lacks modeled fuse protection and emergency isolation. | `engineering_review.md`, `09_red_team.md` | Fuse dimensions exist but no actual fuse/switch geometry. | CONFIRMED | BLOCKER | Document as safety blocker deferred to mk0.8 electrical/mechanical redesign. |
| PWR-002 | Lithium battery safety is not solved by current UPS tray placeholder. | `engineering_review.md`, `09_red_team.md` | No thermal isolation, containment, or tested BMS integration. | LIKELY | BLOCKER | Document no build approval; defer battery enclosure redesign. |
| PWR-003 | Power bus panel may bow as a tall thin printed part. | `engineering_review.md` | 3 mm thick, 275.5 mm tall. | LIKELY | MEDIUM | Record as mk0.8 stiffening/splitting task. |

## Plastic Efficiency

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| PLA-001 | Estimated filament and print time are high. | `engineering_review.md`, `07_plastic_efficiency.md` | Review estimates 5.5-7.0 kg filament and hundreds of print hours. | LIKELY | MEDIUM | Keep mk0.7.1 focused on classification and review evidence; defer mass optimization. |

## Manufacturability

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| MFG-001 | Several long strips need split joints or special print planning. | `02_printability.md`, `08_manufacturability.md` | Spine and power bus parts exceed or nearly exceed P2S constraints. | CONFIRMED | HIGH | Capture in limitations and mk0.8 backlog. |
| MFG-002 | Physical test suite is required before build approval. | `engineering_review.md` | Fit, structural, airflow, electrical, and print tests are listed as required. | CONFIRMED | HIGH | Do not label mk0.7.1 as build-ready. |

## Export Organization

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| EXP-001 | Duplicate geometry check fails for every row. | `01_cad_integrity.md`, `duplicate_geometry_check.csv` | Attribute mismatch: `DUPLICATE_VOLUME_TOLERANCE_MM` vs `DUPLICATE_VOLUME_TOLERANCE_MM3`. | CONFIRMED | BLOCKER | Fix analysis script to use the cubic-mm config name. |
| EXP-002 | Registry has missing category entries and duplicate aliases. | `01_cad_integrity.md`, `part_registry.py` | Some `PARTS` entries missing from `EXPORT_CATEGORIES`; duplicated frames/fan panels. | CONFIRMED | HIGH | Normalize exports and manifests for mk0.7.1. |
| EXP-003 | Placeholders and review geometry must not be printed. | `02_printability.md` | Risk exists if user recursively imports all exports. | LIKELY | MEDIUM | Add manifests and keep categories separated. |

## Documentation

| id | description | source | evidence | status | severity | proposed action |
| --- | --- | --- | --- | --- | --- | --- |
| DOC-001 | mk0.7 review findings need a patch-revision scope. | User request, review package | Review includes blockers, quick wins, and mk0.8-scale redesign items. | CONFIRMED | HIGH | Create mk0.7.1 scope, limitations, manifests, self-check, and changelog. |
| DOC-002 | Review package must avoid unsupported claims. | `engineering_review.md`, `04_airflow_cooling.md` | No CFD, no FEA, no physical tests were performed. | CONFIRMED | HIGH | Keep notes explicit about evidence boundaries. |
