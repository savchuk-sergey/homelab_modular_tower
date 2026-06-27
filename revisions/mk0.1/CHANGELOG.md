# Changelog For mk0.1

## 2026-06-27

Initial engineering CAD freeze.

Added project structure:

- `cad/`
- `docs/`
- `scripts/`
- `revisions/mk0.1/`

Added first-pass CadQuery model:

- top and bottom frame rings
- corner blocks
- M5 threaded rod placeholders
- metal guide rail placeholders
- UPS / Power Distribution tray
- External SSD Bay tray
- SSD / Expansion tray
- Raspberry Pi tray
- MikroTik hAP ax2 tray
- Mini PC tray
- rear service spine
- power bus placeholder
- side panels
- bottom 120 mm intake fan panel
- top 120 mm exhaust fan panel
- Mini PC airflow duct

Added generated-artifact workflow:

- `python -m cad.export`
- `python scripts\render_views.py --out renders --size 1800 --tolerance 1.5`

Updated project workflow:

- Git stores CAD-code and geometry history.
- `cad/` remains the current working CAD model.
- `revisions/mkX.Y/` stores engineering documentation only.
- `exports/` and `renders/` are ignored generated artifacts.
