# mk0.9 Design Notes

mk0.9 moves away from a semi-monolithic tower and toward a stack of smaller FDM-friendly modules.

## Tower Module Interface v1 Draft

TMI v1 draft defines the shared 190 x 190 mm footprint, M5 rod clearance holes, local interface bolt holes, alignment pins, alignment sockets, rear reserved zone and central airflow channel.

The interface is intentionally draft-level. It must be finalized in mk1.0 after the real mini PC is measured.

## Engineering Sources

- RackStack: stackability, small modules, FDM-friendly module separation.
- Rackfinity / mini-rack community: metal threaded rods as the main vertical tie path.
- mini-itx-nas-case: PETG-first printing, TPU feet, 120 mm fan support and separate exports.
- Antmicro Scalenode: open-hardware discipline, STEP/BOM/documentation separation and placeholder models.
- N5 Mini NAS: compact compute/NAS layout and replaceable compute block thinking.

## Structural Direction

Plastic parts are connector, locator and service geometry. The vertical tie path is reserved for M5 threaded rods, with top and bottom module frames carrying local stiffness.

The design prioritizes modularity, airflow and future service access over external appearance.

