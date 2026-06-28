# Subsystem-First / Testable CAD-First Workflow

## Overview

Starting with mk0.11, this project uses a **subsystem-first / testable CAD-first**
engineering workflow.

This replaces the mk0.10 drawing-first workflow, which was cancelled because
SVG planning drawings did not provide usable engineering clarity faster than
reading `cad/config.py` directly.

---

## Workflow stages

```
1. Requirements
      ↓
2. CAD subsystem (isolated, parametric, printable)
      ↓
3. Fit test jig (validates geometric interface)
      ↓
4. Physical validation (print, measure, test assembly)
      ↓
5. Integration (only after physical validation)
```

Each stage produces a testable artifact — a printable part or a physical
validation checkpoint. No stage produces only documentation without a
corresponding physical or CAD output.

---

## Stage 1 — Requirements

Before starting a new subsystem CAD file:

- Identify the one interface constraint that drives the geometry.
- Write down go/no-go criteria for physical validation.
- Record all relevant config.py parameters.

Do NOT start CAD until the interface constraints are clear.

**Output:** Engineering decision recorded in `revisions/mkX.Y/DECISIONS.md`.

---

## Stage 2 — CAD subsystem

Rules:
- One part per Python file.
- All dimensions in `cad/config.py` — no magic numbers.
- No mixing of parts, assembly, and export in one file.
- New parts go in `cad/parts/` (or `cad/current/mkX.Y/parts/` for new revisions).
- Run `python -m compileall cad scripts` after every edit.

**Output:** A new `.py` part file in `cad/parts/` or `cad/current/mkX.Y/parts/`.

---

## Stage 3 — Fit test jig

For every new interface, create a minimal test jig that isolates just that interface.

Rules:
- Jig goes in `cad/jigs/` (or `cad/current/mkX.Y/jigs/`).
- Jig must be smaller than the full part — print it first, not the full part.
- Jig validates only the interface dimension being tested.
- Export jig to `exports/mkX.Y/jigs/`.

**Output:** A jig `.py` file and a STEP export.

Example: `cad/jigs/rail_carriage_fit_test.py` tests the U-channel rail pocket
fit without requiring a full-height module to be printed first.

---

## Stage 4 — Physical validation

Print the jig or prototype. Measure. Test assembly.

Rules:
- Print in PLA for first prototype (not PETG until geometry is confirmed).
- Record actual measurements in `revisions/mkX.Y/VALIDATION_PLAN.md`.
- If fit fails: change config.py clearance value. Re-export. Re-print. Retest.
- Do NOT change geometry inside part functions to fix clearance issues.
  Change `cad/config.py` instead.

**Output:** Filled-in validation checklist in `VALIDATION_PLAN.md`.

---

## Stage 5 — Integration

Only after physical validation passes:

- Integrate the subsystem into a higher-level assembly.
- Update `cad/assembly/` with the new integration assembly.
- Run full export pipeline: `python scripts/export_revision.py --revision mkX.Y`.
- Open STEP in viewer and verify geometry before declaring the revision stable.

Rules:
- Do NOT modify the validated subsystem geometry during integration.
- If integration reveals a geometry problem, return to Stage 2 / Stage 3.
- Record the integration decision in `revisions/mkX.Y/DECISIONS.md`.

**Output:** Updated assembly files and updated `exports/mkX.Y/assemblies/`.

---

## Current status (mk0.11)

| Stage | Status |
|---|---|
| Stage 1 — Requirements | DONE — generic module requirements frozen in DECISIONS.md |
| Stage 2 — CAD subsystem | DONE — generic_module.py, module_carriage.py, pom_shoe.py, rail_profile.py |
| Stage 3 — Fit test jig | DONE — rail_carriage_fit_test.py exported |
| Stage 4 — Physical validation | PENDING — Steps 5–13 in VALIDATION_PLAN.md |
| Stage 5 — Integration | BLOCKED — awaiting physical validation |

---

## Key files for the current subsystem

| File | Stage | Role |
|---|---|---|
| `cad/config.py` | All | All dimensions, no magic numbers |
| `cad/parts/generic_module.py` | 2 | Generic module shell |
| `cad/parts/module_carriage.py` | 2 | Generic module carriage |
| `cad/parts/pom_shoe.py` | 2 | POM-C shoe reference |
| `cad/parts/rail_profile.py` | 2 | U-channel rail reference |
| `cad/jigs/rail_carriage_fit_test.py` | 3 | Rail/carriage/shoe fit jig |
| `cad/assembly/generic_module_assembly.py` | 5 | Module + carriage assembly |
| `cad/assembly/single_module_bay_assembly.py` | 5 | Full single-bay assembly |
| `revisions/mk0.11/VALIDATION_PLAN.md` | 4 | Physical validation checklist |
| `revisions/mk0.11/DECISIONS.md` | 1 | Engineering decisions |

---

## Anti-patterns to avoid

| Anti-pattern | Why it fails |
|---|---|
| Iterate SVG drawings before CAD | Does not expose printability or clearance issues |
| Build full tower before validating one module bay | Integration failures are expensive to debug |
| Hardcode clearances inside part functions | Cannot be tuned without editing the function |
| Mix part geometry with assembly logic | Prevents independent testing of each subsystem |
| Print PETG on first prototype | Wastes material if geometry needs adjustment |
