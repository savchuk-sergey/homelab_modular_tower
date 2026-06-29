# cad/current/mk0.11/assemblies — Active mk0.11 Assembly Files

This directory is the intended home for future mk0.11 integration assemblies
that go beyond the current single-bay validation scope.

## What belongs here

- Multi-bay assemblies that combine validated modules into a partial tower stack.
- Integration assemblies that connect the mk0.11 generic module bay to the
  full tower frame — but only after single-bay validation passes.
- Future mk0.12+ assembly files if the refactored directory convention is adopted.

## What does NOT belong here

- The current primary validation assemblies — those already exist at the flat level:
  - `cad/assembly/generic_module_assembly.py`
  - `cad/assembly/single_module_bay_assembly.py`
- The full tower assembly (`cad/assembly/tower_assembly.py`) — that is legacy /
  frozen for mk0.11 per Decision D-006 in `revisions/mk0.11/DECISIONS.md`.

## Current active mk0.11 assemblies (in cad/assembly/)

| File | Role |
|---|---|
| `cad/assembly/generic_module_assembly.py` | Module shell + carriage combined |
| `cad/assembly/single_module_bay_assembly.py` | Full single bay: module + rails + shoes |

## Go / No-Go gate

Do not create new assemblies in this directory until:

- Step 12 (rail/carriage fit test) in `revisions/mk0.11/VALIDATION_PLAN.md` passes.
- Step 13 (single module bay extraction/insertion) passes.

Only after those steps is full tower integration in scope.
