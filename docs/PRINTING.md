# Printing Notes

Recommended material: PETG.

Baseline FDM settings:

- nozzle: 0.4 mm or 0.6 mm
- layer height: 0.2-0.28 mm
- perimeters: 3-5
- infill: 25-40%
- structural frame/corner parts: 40% or more

The M5 threaded rods and 10 x 3 mm guide rails are not printed load-bearing substitutes. They are metal hardware represented as CAD placeholders.

## Orientation

- Trays: print flat on the base. This keeps the tray bottom flat and makes guides strong enough for normal service loads.
- Side panels: print flat. Vent slots should need no supports.
- Fan panels: print flat. Grille bars are simple rectangular bridges.
- Corner blocks: print with the M5 rod hole vertical. This keeps rod compression aligned with layer stacking.
- Rear service spine: print on its back or side depending on slicer support preview.
- Mini PC duct: print with the duct opening along the bed if possible; use supports only where your slicer cannot bridge the rectangular channel cleanly.

Check the rail clearance slots in the trays after slicing. They should not create unsupported fragile islands around the tray edges.

## Supports

The first version avoids decorative overhangs. Use supports only for local openings if slicer preview shows poor bridges. Prefer adding chamfers and simple rectangular clearances in v2 over relying on heavy supports.

## Safety

PETG softens under heat. Check fan airflow, internal temperatures, battery temperature, and Mini PC exhaust temperature before continuous use. Do not place exposed mains AC inside the printed tower.
