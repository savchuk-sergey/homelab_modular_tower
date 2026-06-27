# mk0.5 Calculations and Checks

## Footprint

- Tower body footprint: `190 x 190 mm`.
- Stability base footprint: `240 x 250 mm`.
- Base width increase over body: `50 mm`.
- Base depth increase over body: `60 mm`.

The support polygon is larger than the tower footprint without changing the module envelope.

## Bottom intake clearance

- TPU foot height: `18 mm`.
- Bottom intake target clearance: `15-20 mm`.
- Base includes a `134 mm` central intake opening for the 120 mm fan path.

## Rear spine fastening

- Rear spine structural mount points: `7`.
- Cover and spine mount positions share the same Z pattern.
- Mounting points are distributed across the height instead of only top/middle/bottom.

## Shear panel fastening

- Each side panel section retains four screw points.
- Lower and upper sections use structural panel/rib parameters.
- Insert pocket dimensions are based on M3 heat-set insert parameters from `config.py`.

## Test-rig scope

The recommended partial print rig should include:

- `base_stability_plate`;
- bottom frame;
- top frame;
- four corner blocks;
- four M5 rod placeholders;
- rear spine mock or real rear spine;
- one side shear panel;
- one mini PC tray;
- tray stop.

