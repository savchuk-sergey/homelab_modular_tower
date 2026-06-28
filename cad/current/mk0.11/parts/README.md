# cad/current/mk0.11/parts — Active mk0.11 Part Files

This directory is the intended home for **new** mk0.11 part files that go
beyond the initial generic module prototype.

## What belongs here

- Device-specific variants derived from `cad/parts/generic_module.py`
  (e.g., a RPi-specific shell, a Mini PC shell) — but only after the generic
  module is physically validated.
- Future adapter parts that connect mk0.11 generic modules to the full tower frame.
- Any new part created specifically for mk0.11 that does not fit cleanly into
  the existing `cad/parts/` flat structure.

## What does NOT belong here

- Changes to `cad/parts/generic_module.py` — edit that file directly.
- Changes to `cad/parts/module_carriage.py` — edit that file directly.
- Full-tower parts (frame, panels, spine) — those live in `cad/parts/` and
  are classified as legacy in `cad/legacy/README.md`.

## Current active mk0.11 part files (in cad/parts/)

| File | Role |
|---|---|
| `cad/parts/generic_module.py` | Generic removable module shell |
| `cad/parts/module_carriage.py` | Generic module carriage (POM-C shoe mounts) |
| `cad/parts/pom_shoe.py` | POM-C shoe reference geometry |
| `cad/parts/rail_profile.py` | U-channel rail reference geometry |
| `cad/parts/carriages.py` | Open-frame carriage builder |
| `cad/parts/rails.py` | Rail geometry |

## Next steps after generic module is validated

1. Create device-specific module shells in this directory.
2. Add them to the part registry in `cad/exporters/part_registry.py`.
3. Test each new part against the same validation checklist as the generic module.

## AGENTS.md rules that apply here

- All dimensions must be in `cad/config.py` — no magic numbers.
- Each part in its own function.
- No mixing of parts, assembly, and export in one file.
