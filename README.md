# Homelab Modular Tower

Parametric CadQuery engineering project for a compact 3D-printed homelab stack.

The project is engineering-first: revision-scoped specifications, explicit validation gates, serviceable module architecture, four M5 through-rods where applicable, rear service routing, low-voltage DC power planning, and Mini PC cooling priority.

Do not start CAD implementation from root `README.md` alone. Always validate the active revision-scoped specification first.

---

## Current active engineering focus: mk0.12

Active revision: `mk0.12 MVP-2M stack-through-rod`

`mk0.12` is an MVP-2M revision, not a full final tower and not a hot-swappable blade chassis. The active real modules are:

- Raspberry Pi + SSD
- Mini PC

The active architecture is stack-through-rod:

- modules are stacked on four M5 rods;
- top and bottom washers/nuts compress the stack;
- a middle module cannot be removed without loosening the stack;
- this is an accepted MVP limitation documented in the revision-scoped specification;
- primary device installation and cable routing happen before final stack compression.

### Current mk0.12 status

```text
SPECIFICATION: PASS FOR CAD SKELETON V3 INPUT
CAD IMPLEMENTATION: NOT STARTED
COUPON PARTS: BLOCKED
FULL PRINT: BLOCKED
NEXT STEP: mk0.12 CAD skeleton cleanup v3
```

The next engineering step remains `mk0.12 CAD skeleton cleanup v3`, but only after the cleanup/spec workflow is accepted. Documentation-only work must not advance `CAD IMPLEMENTATION` beyond `NOT STARTED`.

### mk0.12 read order

1. `revisions/mk0.12/README.md`
2. `revisions/mk0.12/ENGINEERING_SPEC.md`
3. `revisions/mk0.12/PARTS_SPEC.md`
4. `revisions/mk0.12/INTERFACES.md`
5. `revisions/mk0.12/VALIDATION_GATES.md`
6. `revisions/mk0.12/AGENT_RULES.md`
7. `revisions/mk0.12/PHYSICAL_TEST_PLAN.md`
8. `revisions/mk0.12/KNOWN_ISSUES.md`

If those documents are missing, incomplete, contradictory, or structurally invalid, CAD work is blocked.

---

## Source-of-truth policy

For active engineering work, source-of-truth precedence is:

1. Revision-scoped documents under `revisions/<revision>/`.
2. Root `AGENTS.md` workflow rules.
3. Legacy/reference snapshots.
4. Derived artifacts such as STEP, STL, PNG, screenshots, slicer previews, and renders.

CadQuery source files in `cad/` are the CAD source of truth. STEP/STL exports, renders, drawings, screenshots, and slicer previews are generated artifacts and must not override CadQuery source or revision-scoped specifications.

---

## Repository structure

```text
homelab_modular_tower/
  AGENTS.md                        # LLM agent workflow and hard gates
  README.md                        # repository orientation

  cad/                             # active CadQuery source
    config.py                      # parametric dimensions and revision constants
    parts/                         # part builders
    assembly/                      # assembly builders
    exporters/                     # export infrastructure
    utils/                         # geometry helpers

  revisions/
    mk0.12/                        # active revision-scoped specification
      README.md
      ENGINEERING_SPEC.md
      PARTS_SPEC.md
      INTERFACES.md
      VALIDATION_GATES.md
      PHYSICAL_TEST_PLAN.md
      AGENT_RULES.md
      KNOWN_ISSUES.md
    mk0.11/                        # historical/superseded subsystem-first workflow
    mk0.1/ ... mk0.9.3/            # historical revision documentation

  docs/
    workflow/
      subsystem_first_workflow.md  # mk0.11 historical/superseded workflow reference
    KIMI_AGENTS_SWARM_PROMPT_GUIDE.md
    ARCHITECTURE.md
    BOM.md
    POWER.md
    PRINTING.md

  reviews/                         # historical review reports and agent outputs
  drawings/                        # drawing/reference artifacts
  exports/                         # generated STEP/STL artifacts
  renders/                         # generated render artifacts
  scripts/                         # validation/export/render/review helpers
```

---

## Historical workflow note

`mk0.11` used a subsystem-first / testable CAD-first workflow. That workflow is now historical/superseded for active work unless a future revision explicitly promotes it again.

Useful historical references:

- `revisions/mk0.11/README.md`
- `revisions/mk0.11/VALIDATION_PLAN.md`
- `revisions/mk0.11/DECISIONS.md`
- `docs/workflow/subsystem_first_workflow.md`
- `drawings/mk0.10/README.md` for the cancelled drawing-first planning context

Historical documents must not be treated as active `mk0.12` requirements when they conflict with the revision-scoped `mk0.12` specification. The stricter interpretation wins until the ambiguity is resolved.

---

## Install

CadQuery is the only non-standard CAD dependency.

```powershell
python -m pip install cadquery
```

If you use Conda, the CadQuery project recommends a Conda environment:

```powershell
conda create -n cadquery cadquery -c conda-forge
conda activate cadquery
```

---

## Safe documentation checks

For documentation-only cleanup, use safe git/markdown checks only:

```powershell
git diff --stat
git diff -- README.md AGENTS.md revisions/mk0.12
```

Do not run the CAD export pipeline, render generation, STEP/STL generation, or coupon-part generation as part of documentation cleanup.

---

## CAD revision workflow

The hard gate is defined in `AGENTS.md`:

1. Complete the revision-scoped specification.
2. Validate required document structure.
3. Validate internal consistency.
4. Mark conflicts, assumptions, and unverifiable requirements explicitly.
5. Only after valid specification: allow CAD planning.
6. Only after CAD planning: allow CadQuery implementation.
7. Only after CAD validation gates: allow coupon parts.
8. Only after coupon and physical tests: allow full print.

No CAD development is allowed until the active revision specification is structurally complete and internally consistent.
