# Changelog mk0.3

Date: 2026-06-27

## Added

- mk0.3 revision documentation.
- Explicit `MODULE_*` blade module standard parameters.
- M3 front lock screw and heat-set insert parameters.
- Printability baseline parameters for PETG-oriented CAD work.
- Visible assembly placeholders for Mini PC, Raspberry Pi, MikroTik hAP ax2, UPS/DC UPS, External SSD, SSD/Expansion, and power bus zone.
- `make_module_tray(...)` as the mk0.3 standardized tray factory.
- Front anti-slide tab on module trays.
- `make_top_structural_frame()` and `make_bottom_structural_frame()`.
- `make_top_fan_grille()` and `make_bottom_fan_grille()`.
- `make_mini_pc_airflow_duct_placeholder()`.
- Larger rear service spine with cable windows, tie slots, cover rails, and power/signal zone divider.
- Review renders under `renders/review/`.
- Assembly STEP export under `exports/assembly/assembly.step`.

## Changed

- Current revision updated from `mk0.2` to `mk0.3`.
- M5 rod length and assembly placement now follow the tower height instead of inflating the bounding box below the base.
- Fan grille bars are thinner and more open than mk0.2.
- Module trays now use the mk0.3 module standard names while retaining legacy tray aliases for compatibility.
- Export registry uses structural-frame and fan-grille names for mk0.3.

## Not changed

- Real device mounting holes are not finalized.
- Final DC UPS/power distribution implementation is not modeled.
- Side panels remain service covers, not primary structural members.
- STEP/STL/renders remain derived artifacts, not the source of truth.
