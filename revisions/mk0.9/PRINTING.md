# mk0.9 Printing

## Materials

- Main printed parts: PETG.
- Feet/dampers: TPU.
- PLA is acceptable only for early visual prototypes.

## Orientation

- Frame modules should be printed flat on the module interface plane.
- Bottom grill, dust filter slot and top filter slot are long-thin parts and need slicer orientation review.
- TPU feet should be printed upright or with the broad contact face on the bed, depending on material behavior.

## Supports

The module frames are designed to avoid heavy supports. The fan shroud, retainers and filter slots should still be checked in slicer for bridge length and first-layer stability.

## Estimated Plastic Usage

Pipeline estimate from `revisions/mk0.9/analysis/plastic_estimate.csv`:

- PETG printed parts estimate: about 1027 g.
- PETG printed parts target: <= 900 g.
- PETG hard upper limit: <= 1100 g.
- TPU feet/dampers target: <= 50 g.

Final plastic usage must be verified in slicer. If PETG usage exceeds 1100 g, geometry must be reviewed and lightened.

The current mk0.9 estimate is below the hard limit but above the preferred target, so slicer validation and another lightening pass are recommended before a full print.

