# Exports For mk0.1

mk0.1 exports are stored under:

```text
exports/
    mk0.1/
        step/
        stl/
```

Render snapshots are stored under:

```text
renders/
    mk0.1/
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

Equivalent explicit command:

```powershell
python -m cad.export --revision mk0.1
```

## Render Command

```powershell
python scripts\render_views.py --out renders\mk0.1 --size 1800 --tolerance 1.5
```

## STEP Files

- `exports/mk0.1/step/assembly.step`
- `exports/mk0.1/step/frame_top.step`
- `exports/mk0.1/step/frame_bottom.step`
- `exports/mk0.1/step/corner_block.step`
- `exports/mk0.1/step/m5_threaded_rod.step`
- `exports/mk0.1/step/metal_guide_rail.step`
- `exports/mk0.1/step/ups_power_tray.step`
- `exports/mk0.1/step/external_ssd_bay.step`
- `exports/mk0.1/step/ssd_expansion_tray.step`
- `exports/mk0.1/step/raspberry_pi_tray.step`
- `exports/mk0.1/step/mikrotik_tray.step`
- `exports/mk0.1/step/mini_pc_tray.step`
- `exports/mk0.1/step/power_bus_panel.step`
- `exports/mk0.1/step/rear_service_spine.step`
- `exports/mk0.1/step/left_side_panel.step`
- `exports/mk0.1/step/right_side_panel.step`
- `exports/mk0.1/step/bottom_fan_panel.step`
- `exports/mk0.1/step/top_fan_panel.step`
- `exports/mk0.1/step/mini_pc_airflow_duct.step`

## STL Files

The same individual part names are exported to `exports/mk0.1/stl/`.

## Render Files

- `renders/mk0.1/front.png`
- `renders/mk0.1/rear.png`
- `renders/mk0.1/left.png`
- `renders/mk0.1/right.png`
- `renders/mk0.1/top.png`
- `renders/mk0.1/bottom.png`
- `renders/mk0.1/isometric.png`
