# mk0.12 CAD Skeleton V2 Review

> NOTE:
> This review is a historical CAD skeleton v2 snapshot.
> It is superseded by the mk0.12 revision-scoped documents in this directory.
> Later inspection found footprint, rib-topology, and STL-topology blockers.
> Coupon parts remain BLOCKED until CAD skeleton v3 passes `VALIDATION_GATES.md`.

## Summary

mk0.12 CAD skeleton cleanup v2 replaces the previous monolithic placeholder-heavy geometry with printable-only ribbed-frame / open-tray builders and separate non-printable reference geometry.

Result:

- `scripts/validate_mk012_spec.py`: 0 FAIL, 5 PARTIAL, 11 PASS.
- `scripts/validate_mk012_cad_skeleton.py`: 0 FAIL, 0 PARTIAL, 29 PASS.
- Historical result at the time of this review: coupon parts were considered next as CAD skeleton validation coupons, not as final production STL release.
- Superseding status: this conclusion is no longer active; coupon parts are BLOCKED until CAD skeleton v3 passes `VALIDATION_GATES.md`.

## Files Changed

- `cad/config.py`
- `cad/parts/stack_interface.py`
- `cad/parts/base_pedestal.py`
- `cad/parts/module_rpi_ssd.py`
- `cad/parts/module_minipc.py`
- `cad/parts/top_cap.py`
- `cad/parts/reference_geometry.py`
- `cad/assembly/mvp_2_module_stack.py`
- `scripts/validate_mk012_cad_skeleton.py`
- `scripts/export_mk012_visual_models.py`
- `scripts/render_mk012_review_views.py`
- `revisions/mk0.12/CAD_SKELETON_V2_REVIEW.md`

## Current Active CAD Structure

Printable builders:

- `build_base_pedestal()`
- `build_rpi_ssd_stack_module()`
- `build_minipc_stack_module()`
- `build_top_cap()`

Reference-only builders:

- `build_rpi3b_placeholder()`
- `build_external_ssd_placeholder()`
- `build_minipc_placeholder()`
- `build_m5_rods_placeholder()`
- `build_washers_placeholder()`
- `build_nuts_placeholder()`

Assembly:

- `cad/assembly/mvp_2_module_stack.py`

## Printable / Reference Separation Result

PASS.

Printable part builders return printable plastic only. Raspberry Pi, SSD, Mini PC, M5 rods, washers, and nuts are separated into `cad/parts/reference_geometry.py` and are only added by the assembly for review.

STL review exports include only printable parts:

- `base_pedestal.stl`
- `rpi_ssd_stack_module.stl`
- `minipc_stack_module.stl`
- `top_cap.stl`

## Connected Component Result

| Part | Connected printable solids |
| --- | ---: |
| `base_pedestal` | 1 |
| `rpi_ssd_stack_module` | 1 |
| `minipc_stack_module` | 1 |
| `top_cap` | 1 |

## Mass Estimate

PETG density: `1.27 g/cm3`.

| Part | Estimate | Budget result |
| --- | ---: | --- |
| `base_pedestal` | 202.7 g | PASS, target 120-220 g |
| `rpi_ssd_stack_module` | 289.0 g | PASS, target 150-300 g |
| `minipc_stack_module` | 379.4 g | PASS, target 250-450 g |
| `top_cap` | 187.9 g | PASS, target 100-200 g |
| Total printed PETG | 1059.1 g | PASS, total target 620-1170 g |

## Effective Airflow Open Area

| Part | Effective area | Result |
| --- | ---: | --- |
| `base_pedestal` | 8411 mm2 | PASS |
| `rpi_ssd_stack_module` | 10964 mm2 | PASS |
| `minipc_stack_module` | 18060 mm2 | PASS |
| `top_cap` | 8411 mm2 | PASS |

These are geometric sanity estimates, not CFD or thermal validation.

## Cable Window Checks

| Window | Size | Result |
| --- | ---: | --- |
| Rear service window | 120 x 20 mm | PASS |
| RPi/SSD cable window | 28 x 18 mm | PASS |
| Mini PC rear cable exit | 70 x 22 mm | PASS |

Mini PC rear cable exit height is above the 20 mm minimum.

## Rib Load-Path Review

PASS.

Each printable part includes:

- outer perimeter frame;
- four M5 compression islands at +/-80 mm;
- ribs from compression islands to adjacent frame walls;
- at least two transverse ribs;
- at least two longitudinal ribs;
- framed fan/rear-service/cable openings where applicable.

Device supports use ribs, bosses, rails, retainers, and local anchors instead of solid device trays.

## Tool / Finger Access Review

| Feature | Result |
| --- | --- |
| RPi M2.5 boss access envelope | PASS, 8 mm represented |
| SSD strap pull-tab access | PASS, 15 x 20 mm reserved |
| Mini PC retainer/finger access | PASS, 18 mm finger slot and 10 mm clearance represented |

Access remains a skeleton geometry review result. Hardware mock validation is still required.

## Stack Assembly Order Notes

Assembly service order is documented in `cad/assembly/mvp_2_module_stack.py`:

1. Install devices into modules before final stack compression.
2. Route Pi/SSD/Mini PC cables to rear service windows before final compression.
3. Stack modules on M5 rods.
4. Verify no cable collision with rear rod keepouts.
5. Hand-tight compression only.

## Validation Command Results

```text
C:\Users\ghery\miniforge3\envs\cadquery\python.exe scripts\validate_mk012_spec.py
Summary: 0 FAIL, 5 PARTIAL, 11 PASS

C:\Users\ghery\miniforge3\envs\cadquery\python.exe scripts\validate_mk012_cad_skeleton.py
Summary: 0 FAIL, 0 PARTIAL, 29 PASS
```

## Generated Renders / Exports

Review exports:

- `exports/mk0.12/review/step/`
- `exports/mk0.12/review/stl/`
- `exports/mk0.12/review/EXPORT_MANIFEST.md`

Review renders:

- `renders/mk0.12/assembly_front.png`
- `renders/mk0.12/assembly_rear.png`
- `renders/mk0.12/assembly_left.png`
- `renders/mk0.12/assembly_right.png`
- `renders/mk0.12/assembly_top.png`
- `renders/mk0.12/assembly_iso.png`
- `renders/mk0.12/base_pedestal_top.png`
- `renders/mk0.12/base_pedestal_iso.png`
- `renders/mk0.12/rpi_ssd_stack_module_top.png`
- `renders/mk0.12/rpi_ssd_stack_module_iso.png`
- `renders/mk0.12/minipc_stack_module_top.png`
- `renders/mk0.12/minipc_stack_module_iso.png`
- `renders/mk0.12/top_cap_top.png`
- `renders/mk0.12/top_cap_iso.png`
- `renders/mk0.12/rpi_ssd_stack_module_xy_edges.png`
- `renders/mk0.12/minipc_stack_module_xy_edges.png`
- `renders/mk0.12/rear_service_windows_check.png`
- `renders/mk0.12/airflow_open_area_check.png`

## Remaining PARTIAL / NOT VERIFIED Items

- PETG compression around washer seats remains PARTIAL until M5 corner coupon testing.
- Fan screw boss material remains PARTIAL until slicer/CAD review with actual fan screw hardware.
- Rear cable routing around rods remains PARTIAL until cable coupon and real cable bend tests.
- Real cable bundle thickness, connector strain relief, and tie routing remain PARTIAL.
- SSD strap geometry is still skeleton-level and needs hardware/cable mock review.
- Mini PC thermal behavior remains NOT VERIFIED; current airflow result is geometric only.
- Nut/tool access remains NOT VERIFIED until hardware mock.

## Recommendation

SUPERSEDED HISTORICAL RECOMMENDATION FROM V2 REVIEW.

This historical recommendation is no longer active. Later inspection found footprint, rib-topology, and STL-topology blockers. Coupon parts remain BLOCKED until CAD skeleton v3 passes `VALIDATION_GATES.md`.

Do not treat the review STL files as final production exports.
