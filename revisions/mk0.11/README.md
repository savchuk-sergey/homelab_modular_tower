# mk0.11 — Subsystem-First Workflow

## Why the drawing-first workflow was stopped

The mk0.10 iteration attempted to drive CAD decisions through SVG planning drawings
generated from `cad/config.py` via `scripts/generate_architecture_drawings.py`.
Five SVG sheets were produced covering architecture layout, module interface, and
rail/carriage cross-sections.

The approach was declared impractical for the following reasons:

- SVG output from a parametric generator produces technically correct but visually
  flat drawings with no engineering judgment built in.
- Drawings showed dimensions correctly but gave no feedback on printability,
  assembly clearance, or structural stiffness of individual interfaces.
- Iterating on SVG drawings delayed the first physical prototype indefinitely.
- No measurable design decision was unlocked by the drawing iteration that could
  not have been answered by reading `cad/config.py` directly.

Conclusion: SVG-only planning iterations for this project type do not justify the
effort. They will not be continued for mk0.11 or later revisions.

---

## New workflow: subsystem-first / testable CAD-first

mk0.11 adopts a subsystem-first / testable CAD-first process:

1. Design one generic device-agnostic module body / tray.
2. Design the carriage for that module (open-frame, POM-C shoes, compatible with
   existing mk0.9.3 U-channel rail standard).
3. Design and verify the rail pocket / POM-C shoe interface for that carriage.
4. Build a single-module bay test assembly (module + carriage + rails + shoes).
5. Print the generic module and carriage.
6. Physically validate: stiffness, airflow path, rear clearance, rail fit.
7. Only after the single module bay is validated, proceed to full tower integration.

Every step produces a testable artifact (a printable part or a physical
validation checkpoint), not a drawing.

---

## Scope of mk0.11

### In scope

- `cad/parts/generic_module.py` — generic removable module shell
- `cad/parts/module_carriage.py` — mk0.11 generic carriage (wraps open-frame standard)
- `cad/parts/pom_shoe.py` — standalone reference POM-C shoe geometry
- `cad/parts/rail_profile.py` — standalone reference U-channel rail profile
- `cad/jigs/rail_carriage_fit_test.py` — rail/carriage/shoe interface fit test jig
- `cad/assembly/generic_module_assembly.py` — module + carriage assembled
- `cad/assembly/single_module_bay_assembly.py` — single bay: module + rails + shoes
- `revisions/mk0.11/` — this documentation set
- `cad/config.py` — mk0.11 section appended (constants only, no changes to frozen values)

### Out of scope in mk0.11

- Full tower redesign
- UPS / power bus geometry
- Router / MikroTik module
- Mini PC module
- Rear Service Spine revision
- SVG drawings
- Decorative panels or surfaces
- Changes to the existing rail standard (frozen)
- Changes to the existing module interface standard (frozen)
- Changes to existing stable module shells (base, rpi_ssd, mini_pc, roof)

---

## Frozen decisions inherited from mk0.9.3

These decisions are not re-evaluated in mk0.11:

| Decision | Value |
|---|---|
| Source of truth | CadQuery code in `cad/` |
| Primary structural material | Metal (M5 rods, U-channel rails, top/bottom caps) |
| PETG role | Connector, positioner, service element — not primary load path |
| Rail standard | Aluminum U-channel 15×10×10×2 mm |
| Runner standard | POM-C round Ø8×12 mm, 2–3 per side |
| Rear service zone | Reserved, 30 mm deep |
| Airflow direction | Vertical, bottom intake / top exhaust |
| Configuration | All dimensions in `cad/config.py` |

---

## Status

mk0.11 is a working revision. CAD baseline is from mk0.9.3.
No changes are made to existing stable module shells or the tower assembly.
