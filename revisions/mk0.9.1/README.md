# mk0.9.1 — Corrective revision after mk0.9 review

## Summary

`mk0.9.1` is a **corrective** CAD revision.  It does not add new modules;
instead it fixes the structural and manufacturability issues that were
identified during the `mk0.9` engineering review.

## Goals

1. **Lighten** the `base_module` — remove the massive floor slab.
2. **Lighten** the `roof_module` — keep it a thin structural frame.
3. **Restore feet** — TPU foot mounts must be present for intake clearance,
   stability, and vibration isolation.
4. **Restore carriages** — every payload module must have a removable tray
   (carriage) that can slide out for service.
5. **Introduce a rail / carriage subsystem** — no more PETG-on-aluminum
   sliding surfaces.
6. **Use commercial aluminum U-channel rails** (15 × 10 × 10 × 2 mm).
7. **Use commercial POM-C Ø8 mm shoes** as the wear surface.
8. **Keep the large vertical airflow path** intact.
9. **Preserve the M5 vertical rod architecture**.
10. **Do not** implement power distribution, router, UPS, or a full rear
    service spine in this revision.

## What changed from mk0.9

| Area | mk0.9 | mk0.9.1 |
|------|-------|---------|
| Base | massive frame + floor ribs | frame only + fan mount + bottom grill + filter slot + foot mounts |
| Roof | already fairly light | kept light, no major change |
| Feet | present but not integrated into base module | explicitly integrated into base module |
| RPi/SSD tray | solid floor with vent slots | open-frame carriage with 4 POM-C shoes |
| Mini PC tray | solid floor with pad | open-frame carriage with 6 POM-C shoes |
| Rails | legacy 10 × 3 mm flat bar (placeholder) | aluminum U-channel 15 × 10 × 10 × 2 mm |
| Runners | none (PETG directly on metal) | perpendicular POM-C Ø8 mm replaceable shoes |
| Retention | none / glue | M3 clamp screw into PETG boss (no threading into POM-C) |
| Weight target | ≤ 900 g PETG | same, but now realistically achievable |

## What is still placeholder-based

* **Mini PC dimensions** — the mini PC carriage is sized from the current
  placeholder volume.  It will be refined in `mk1.0` after physical
  measurements.
* **Power / router / UPS modules** — reserved zones are present but no
  geometry is finalised.
* **Rear service spine** — not implemented; only structural clearances are
  kept.

## Verification

* Run `python -m cad.export --revision mk0.9.1` to export all STEP/STL files.
* Open `assembly.step` in FreeCAD / CQ-editor to inspect the full stack.
* Check that printed and non-printed parts are in separate export categories.
