# Exports For mk0.1

Exports and renders are generated artifacts. They are not the source of truth for mk0.1.

Source of truth:

1. CadQuery code in `cad/`
2. Git history
3. Documentation in `revisions/mk0.1/`

The current export command writes to:

```text
exports/
    step/
    stl/
```

Current render snapshots are stored under:

```text
renders/
    front.png
    rear.png
    left.png
    right.png
    top.png
    bottom.png
    isometric.png
```

## Export Command

```powershell
python -m cad.export
```

Optional local subfolder export:

```powershell
python -m cad.export --revision mk0.1
```

## Render Command

```powershell
python scripts\render_views.py --out renders --size 1800 --tolerance 1.5
```

`exports/` and `renders/` are ignored by Git. Recreate them locally when needed.

## STEP Files

- `exports/step/assembly.step`
- `exports/step/frame_top.step`
- `exports/step/frame_bottom.step`
- `exports/step/corner_block.step`
- `exports/step/m5_threaded_rod.step`
- `exports/step/metal_guide_rail.step`
- `exports/step/ups_power_tray.step`
- `exports/step/external_ssd_bay.step`
- `exports/step/ssd_expansion_tray.step`
- `exports/step/raspberry_pi_tray.step`
- `exports/step/mikrotik_tray.step`
- `exports/step/mini_pc_tray.step`
- `exports/step/power_bus_panel.step`
- `exports/step/rear_service_spine.step`
- `exports/step/left_side_panel.step`
- `exports/step/right_side_panel.step`
- `exports/step/bottom_fan_panel.step`
- `exports/step/top_fan_panel.step`
- `exports/step/mini_pc_airflow_duct.step`

## STL Files

The same individual part names are exported to `exports/stl/`.

## Render Files

- `renders/front.png`
- `renders/rear.png`
- `renders/left.png`
- `renders/right.png`
- `renders/top.png`
- `renders/bottom.png`
- `renders/isometric.png`
