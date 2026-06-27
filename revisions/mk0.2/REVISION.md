# Homelab Modular Tower CAD Revision mk0.2

Date: 2026-06-27

## Purpose

mk0.2 develops mk0.1 without rewriting the project. The revision focuses on two serviceability areas:

- standardized removable-carriage handles;
- removable side service panels.

The source of truth remains the CadQuery code in `cad/`, git history, and this revision documentation. STEP/STL files and renders are derived artifacts.

## Improved carriage handles

All module trays now use the same front service interface through the generic tray generator. The former protruding handle geometry is replaced by a front carriage plate with a recessed grip pocket.

The front plate stays inside the tray envelope, so the handle does not increase the outside depth of the tower. The grip pocket has rounded corners and local ribs around the pull zone. A prepared M3-compatible boss is included behind the front plate for a future screw, TPU plug, latch, or magnet.

## Improved side panels

Side panels are modeled as removable service covers, not as primary structural members. The tower stiffness still depends on the M5 rods, metal guide rails, top and bottom frame rings, and corner blocks.

Each side panel now has:

- a thin protective base;
- an external perimeter frame;
- X-style diagonal ribs for local anti-racking stiffness;
- M3 mounting bosses and clearance holes;
- controlled ventilation slots;
- a reserved keep-out band for the future Mini PC airflow duct.

## Design rationale

The carriage handle is a service interface, not a decoration. A recessed pocket is preferred because it avoids increasing the tower envelope and reduces snagging during module insertion.

The side panel is deliberately separated from the structural frame. Removing it must not break the load path. Ribs and a perimeter frame help the panel resist warping and handling loads, but they are not required for the tower to stand.

Ventilation is limited to slot rows outside the future Mini PC duct zone. This keeps the baseline vertical intake-to-exhaust airflow concept intact while still allowing side-panel variants in later revisions.

## Trade-offs

- The recessed handle is simpler and safer than a protruding loop, but the grip depth must be validated physically.
- The M3 lock boss is only a prepared feature; mk0.2 does not define the final latch strategy.
- X-ribs improve panel stiffness, but they add print time and make the panel less visually clean.
- Controlled ventilation reduces flat panel area, but the exact airflow effect is not validated yet.
- Screw-mounted side panels are reliable for mk0.2, but slower to remove than future latch or quarter-turn designs.

## Impact on strength

The tray front plate is thicker than the old lip and has local reinforcement near the grip pocket. Rounded handle corners reduce stress concentration when pulling a loaded module.

The side panels add local stiffness only. Primary tower strength remains with the metal and frame load path, so the panel can be removed for service without compromising the core structure.

## Impact on printability

Both changes are PETG-friendly first-pass geometry. The recessed handle avoids tall unsupported loops. Side-panel ribs reduce broad flat warping risk, but the full panel still needs physical print validation.

The side panel should be printed with the service face upward or with a tested orientation that keeps the ribs dimensionally stable and avoids excessive support material.

## Impact on assembly

The carriage front interface is common across all trays, which simplifies module handling and future latch design.

The side panels use simple M3 screw holes to mount to the frame/corner-block area. mk0.2 avoids complex snap features because screw access, tolerances, and panel flatness need validation first.

## Remaining risks

- Grip pocket ergonomics may be too shallow or too narrow for comfortable use.
- The tray front plate may still need more local material after pull-force testing.
- PETG shrink and rail friction may change the force needed to extract a module.
- Large side panels may warp during printing.
- Side ventilation may disturb vertical airflow more than expected.
- Mini PC duct geometry is still provisional.
- Screw access may be awkward after all modules and cables are installed.

## What to validate with prototype

- Pull comfort with one and two fingers.
- Pull force on a fully loaded module.
- Cracking around the handle pocket and lock boss.
- PETG clearances between carriage, rails, and front plate.
- Side-panel flatness after printing.
- Whether X-ribs reduce panel flex enough.
- Airflow path from bottom 120 mm intake to top 120 mm exhaust with side panels installed.
- Clearance between side panels, rear service spine, cable bundle, and future Mini PC duct.
- M3 screw accessibility with the tower fully assembled.

## Recommendations for mk0.3

- Select and prototype the final carriage retention method.
- Add measured latch, magnet, or TPU plug geometry after physical tests.
- Add alternate side-panel variants: solid, vented, filtered, and inspection-window.
- Validate mini PC duct dimensions against the real Mini PC.
- Add panel filter retention if thermal testing shows side intake is useful.
- Add tolerance rules for PETG shrink, inserts, screw clearance, and rail friction.
