# Engineering Decisions For mk0.1

## Decision: Use CadQuery As Model Source

CadQuery code in `cad/` is the model source of truth.

Reason: the project must remain parametric and reproducible. STEP/STL exports are derived artifacts.

## Decision: Use Git For CAD-Code History

Revision history for geometry and CAD code is stored in Git.

Reason: copying the full `cad/` tree for every revision would duplicate code and make future fixes ambiguous.

## Decision: Store Revision State In `revisions/mkX.Y/`

Each engineering revision gets documentation under `revisions/mkX.Y/`.

Reason: revision folders capture decisions, assumptions, known issues, and changelog without becoming a second CAD source tree.

## Decision: Keep mk0.1 As First Engineering Freeze

mk0.1 is frozen as the first engineering CAD checkpoint.

Reason: it contains a complete first-pass model with modular trays, M5 rod placeholders, guide rail placeholders, rear service spine, power bus placeholder, fan panels, and Mini PC duct.

## Decision: Use Metal Structural Elements

The design uses M5 rods and metal guide rails as explicit structural placeholders.

Reason: the tower must not rely only on PETG for stiffness.

## Decision: Keep Power Bus As Placeholder

The power bus is mechanical placeholder geometry in mk0.1.

Reason: final electrical parts, connector footprints, fuse sizing, wire gauge, and retention need real component selection and validation.

## Decision: Keep Exports And Renders Generated

`exports/` and `renders/` are generated and ignored by Git.

Reason: they are heavy, reproducible artifacts and not the source of truth.
