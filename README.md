# Homelab Modular Tower

Parametric CadQuery engineering project for a compact 3D-printed mini-blade
tower homelab stack.

The design is engineering-first: removable modules, four M5 vertical rods,
rear service spine, low-voltage DC power bus, UPS/power module placeholder,
and a priority airflow duct for the Mini PC module.

---

## Current revision: mk0.11 — subsystem-first workflow

The previous mk0.10 drawing-first workflow has been cancelled.

The current active workflow is **subsystem-first / testable CAD-first**:

1. Validate the generic removable module (shell + carriage + rail interface).
2. Only after physical validation of a single module bay: integrate into full tower.

### Where to start

| Where to look | What you'll find |
|---|---|
| `revisions/mk0.11/README.md` | mk0.11 scope, decisions, frozen constraints |
| `revisions/mk0.11/VALIDATION_PLAN.md` | Step-by-step physical validation checklist |
| `revisions/mk0.11/DECISIONS.md` | Engineering decisions (D-001 through D-008) |
| `cad/legacy/README.md` | Which files are legacy and why |
| `cad/current/mk0.11/` | Placeholder directories for future mk0.11 additions |
| `docs/workflow/subsystem_first_workflow.md` | Workflow stages and rules |

### Active mk0.11 CAD files

| File | Role |
|---|---|
| `cad/config.py` | All parametric dimensions — source of truth |
| `cad/parts/generic_module.py` | Generic removable module shell |
| `cad/parts/module_carriage.py` | Generic module carriage (POM-C shoe mounts) |
| `cad/parts/pom_shoe.py` | POM-C shoe reference geometry |
| `cad/parts/rail_profile.py` | U-channel rail reference geometry |
| `cad/jigs/rail_carriage_fit_test.py` | Rail / carriage / shoe fit test jig |
| `cad/assembly/generic_module_assembly.py` | Module + carriage combined assembly |
| `cad/assembly/single_module_bay_assembly.py` | Full single-bay validation assembly |

---

## Repository structure

```
homelab_modular_tower/
  AGENTS.md                        ← LLM agent working rules
  README.md                        ← this file

  cad/
    config.py                      ← ALL dimensions (source of truth)
    parts/                         ← all part source files (active + legacy)
    assembly/                      ← assembly files
    jigs/                          ← fit test jigs
    exporters/                     ← STEP/STL export infrastructure
    utils/                         ← geometry helper utilities
    legacy/
      README.md                    ← legacy file classification
    current/
      mk0.11/
        parts/README.md            ← placeholder for new mk0.11 part files
        assemblies/README.md       ← placeholder for mk0.11 integration assemblies
        jigs/README.md             ← placeholder for additional mk0.11 jigs

  drawings/
    mk0.10/                        ← LEGACY/CANCELLED SVG planning drawings

  exports/
    mk0.11/                        ← current active exports
    mk0.7/ … mk0.9.3/              ← historical exports (reference only)

  renders/
    mk0.7/ … mk0.9.2/              ← historical renders (reference only)

  revisions/
    mk0.11/                        ← active revision documentation
    mk0.1/ … mk0.9.3/              ← historical revision documentation

  scripts/
    export_revision.py             ← export pipeline
    analyze_revision.py            ← geometry analysis
    render_views.py                ← render generator
    package_review.py              ← review package builder
    run_revision_pipeline.py       ← full pipeline runner
    generate_architecture_drawings.py  ← LEGACY/CANCELLED mk0.10 SVG generator
    analysis/                      ← analysis utility modules

  docs/
    workflow/
      subsystem_first_workflow.md  ← current active workflow description
    ARCHITECTURE.md
    BOM.md
    POWER.md
    PRINTING.md
```

---

## Install

CadQuery is the only non-standard dependency.

```powershell
python -m pip install cadquery
```

If you use Conda, the CadQuery project recommends a Conda environment:

```powershell
conda create -n cadquery cadquery -c conda-forge
conda activate cadquery
```

---

## Export

Run from the project root:

```powershell
python scripts/export_revision.py --revision mk0.11
```

Or for the mk0.11 subsystem only (faster):

```powershell
python -m cad.export --revision mk0.11
```

Generated files land in `exports/mk0.11/`:

```
exports/mk0.11/
  printed/
    plastic_modules/     ← generic_module.step / .stl
    plastic_subparts/    ← generic_module_shell, generic_module_carriage
  reference_non_printed/
    metal/               ← u_channel_rail reference
    wear_parts/          ← pom_c_shoe reference
  assemblies/            ← generic_module_assembly, single_module_bay_assembly
  jigs/                  ← rail_carriage_fit_test
```

---

## Syntax check

```powershell
python -m compileall cad scripts
```

---

## CAD revision workflow

The source of truth is:
1. CadQuery code in `cad/`;
2. git history;
3. engineering revision documentation in `revisions/`.

STEP/STL files and renders are derived artifacts. They are not the source of truth.

Each stable revision has:
- a git branch (`cad/mk0.11`) or git tag (`mk0.11`);
- a documentation folder `revisions/mkX.Y/`;
- generated exports recreated from CadQuery code when needed.

Required revision documentation (per AGENTS.md):
- `REVISION.md` or `README.md`
- `DECISIONS.md`
- `VALIDATION_PLAN.md` (for mk0.11+)
- `KNOWN_ISSUES.md`
- `CHANGELOG.md`

Do not copy the whole `cad/` tree into version-named subdirectories.
Revision history lives in git.

---

## Full tower integration: out of scope until mk0.11 single-bay validation

The full tower assembly (`cad/assembly/tower_assembly.py`) is frozen for mk0.11.
Full tower integration is explicitly out of scope until the single module bay
physical validation passes all steps in `revisions/mk0.11/VALIDATION_PLAN.md`.

See `revisions/mk0.11/DECISIONS.md` — Decision D-006.
