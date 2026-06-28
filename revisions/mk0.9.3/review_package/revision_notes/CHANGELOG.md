# mk0.9.3 Changelog

- Changed `CURRENT_REVISION` / `REVISION` to `mk0.9.3`.
- Restored and normalized rail, runner, carriage, fan, base, roof, and foot parameters in `cad/config.py`.
- Set base and roof target heights to 52 mm and reduced the roof fan shroud height.
- Kept lightweight open-frame carriage factories available for RPi + SSD and mini PC placeholder modules.
- Added explicit POM-C shoe socket and M3 clamp/heat-set-insert retention geometry to the carriage subsystem.
- Replaced fan mount, fan grill, and foot boss magic numbers with named config parameters.
- Split export categories into printed modules, printed subparts, TPU, non-printed references, placeholders, review geometry, and legacy do-not-print parts.
- Added generated `PRINT_MANIFEST.md` support for revision exports.
- Preserved M5 rod zones, fan/filter features, foot mounts, and airflow windows.

