# mk0.7.1 Engineering Decisions

## Keep mk0.7 History Immutable

mk0.7 files were used as inputs only. Patch outputs are generated under mk0.7.1 paths.

## Separate TPU Foot From Plastic Batch

The foot remains printable but is routed to `printable/tpu` instead of `printable/plastic`, because the project rules reserve TPU for feet, dampers, and similar parts.

## Do Not Patch Large Safety Architecture In mk0.7.1

Anti-tip redesign, battery containment, fuse/e-stop design, rail-retention architecture, service-spine quick disconnects, and full tray airflow redesign are too large for a safe patch release.

## Fix Low-Risk Confirmed Geometry Defects

The fan cartridge feature overlap, power bus cover hole alignment, fan grille placement constants, central review markers, and duplicate check attribute mismatch were considered low-risk patch work because each one maps directly to review evidence.

## Treat Review Geometry As Non-Printable

Review geometry may contain open markers or non-solid bodies. It must remain outside printable folders and must not be interpreted as production geometry.
