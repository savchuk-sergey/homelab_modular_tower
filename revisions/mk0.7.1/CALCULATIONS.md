# mk0.7.1 Calculations And Checks

## Print Volume

The generated `printability_check.csv` confirms that these printable plastic parts still exceed the configured Bambu Lab P2S axis-aligned envelope:

- `power_bus_cover`
- `power_bus_panel`
- `rear_service_spine`
- `rear_service_spine_cover`

These are retained as mk0.8 split-design work rather than risky patch changes.

## STL Quality

The generated `stl_quality.csv` reports `bottom_fan_cartridge` as watertight and manifold after the mk0.7.1 geometry overlap fix.

Open/nonmanifold results remain for fan placeholder and review geometry. These are non-printable/reference artifacts and are documented as review/package limitations, not production STL approval failures.

## Duplicate Geometry

The duplicate geometry check now uses `DUPLICATE_VOLUME_TOLERANCE_MM3`, matching the config unit. The mk0.7.1 CSV is generated without the mk0.7 `AttributeError`.

## Airflow Review

Central temperature marker positions were moved to y=0 review coordinates. This clarifies the intended chimney path for review, but it is not airflow validation.
