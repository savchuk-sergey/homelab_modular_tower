# Homelab Modular Tower v1

Parametric CadQuery prototype of a compact 3D-printed mini-blade tower for a home homelab stack.

The design is intentionally engineering-first: removable trays, four M5 vertical rods, rear service spine, low-voltage DC power bus placeholder, UPS/power module at the bottom, and a priority airflow duct for the Mini PC module.

## Structure

- `cad/config.py` - all key dimensions and placeholder component sizes.
- `cad/frame.py` - top/bottom frame rings, M5 corner block, M5 threaded rod placeholder, and metal guide rail placeholder.
- `cad/trays.py` - generic tray generator and device-specific tray variants.
- `cad/power_bus.py` - rear service spine and low-voltage power bus placeholder.
- `cad/panels.py` - side panels and 120 mm fan panels.
- `cad/airflow.py` - removable Mini PC airflow duct.
- `cad/assembly.py` - complete tower assembly.
- `cad/export.py` - STEP/STL export entrypoint.

## Install

CadQuery is the only non-standard dependency.

```powershell
python -m pip install cadquery
```

If you use Conda, the CadQuery project usually recommends a Conda environment:

```powershell
conda create -n cadquery cadquery -c conda-forge
conda activate cadquery
```

## Export

From the project root:

```powershell
python -m cad.export
```

Generated files:

- STEP parts: `exports/step/`
- STL parts: `exports/stl/`
- Assembly: `exports/step/assembly.step`

Open `exports/step/assembly.step` in FreeCAD, CAD Assistant, or another STEP viewer.

`exports/` and `renders/` are current generated artifacts and are ignored by Git. Recreate them from CadQuery code when needed.

## CAD Revision Workflow

The source of truth is:

1. CadQuery code in `cad/`;
2. Git history;
3. engineering revision documentation in `revisions/`.

The `cad/` directory contains the current working CAD model. Do not copy the whole CAD tree into `cad/mk0.1`, `cad/mk0.2`, or similar folders for revision history.

Each stable CAD revision should have:

- a git branch or git tag;
- a documentation folder `revisions/mkX.Y/`;
- generated exports/renders recreated only when needed.

Required revision documentation:

- `REVISION.md`
- `CALCULATIONS.md`
- `DECISIONS.md`
- `KNOWN_ISSUES.md`
- `CHANGELOG.md`

Branch naming rule:

```text
cad/mk0.1
cad/mk0.2
cad/mk0.3
cad/mk1.0
cad/mk1.1
```

Each next revision starts from the previous revision.

Revision history is never changed retroactively.

Design changes are always made in a new branch.

STEP/STL files and PNG renders are derived artifacts. They are not the source of truth.

## Measurements Needed For v2

- Actual Mini PC PCB/chassis dimensions, port locations, cooler height, and 19 V input connector.
- MikroTik hAP ax2 bare board dimensions, Ethernet jack position, DC input position, and antenna keep-out zones.
- Raspberry Pi standoff pattern and exact connector clearance for the chosen Pi revision.
- DC UPS board, BMS, fuse block, terminal block, and DC-DC converter footprints.
- Real connector footprints for XT30, JST-VH or Molex MicroFit, USB-C panel/cable routing.
- Exact LiFePO4 pack dimensions and safe retention method.
- Metal guide rail material, screw spacing, and whether 10 x 3 mm flat bar is stiff enough or should become aluminium profile.
