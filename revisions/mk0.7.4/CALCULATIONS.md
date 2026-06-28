# mk0.7.4 Calculations

## Baseline

The pre-mockup-reduction mk0.7.4 plastic estimate was `3764.4 g` PETG mesh-equivalent for `printable/plastic`.

## Split Joint Allowance

The split-joint interface uses a lower positive tab and an upper receiving socket.

- Tab depth: `SPLIT_JOINT_TAB_DEPTH`
- Tab height: `SPLIT_JOINT_TAB_HEIGHT`
- Socket wall: `SPLIT_JOINT_SOCKET_WALL`
- Socket clearance: `SPLIT_JOINT_SOCKET_CLEARANCE`

This is intended to remove overlapping exported volumes while preserving a mechanically visible alignment feature for coupon testing.

## Bottom Filter Retainer

The bottom filter retainer is changed from disconnected corner pads to a single connected rectangular retainer frame.

This closes the impossible detached-clip geometry, but PETG flexibility and filter-sheet retention remain coupon-required before full mockup printing.

## Rail End Mount Engagement

Rail end mount height is derived from the distance between the structural frame and the metal guide rail end plus `RAIL_END_MOUNT_RAIL_CAPTURE_DEPTH`.

The target capture depth is 10 mm for rough mockup validation. The bracket remains coupon-required because real rail tolerances and screw stack-up are not yet measured.

## Rough Mockup Mass Reduction

The mk0.7.4 rough-mockup parameter set reduces draft-print mass without changing the M5 rod, metal rail, frame screw, or module spacing standards.

Controlled reductions:

- Base sections: `MOCKUP_BASE_THICKNESS = 5.0 mm`
- Central bottom fan frame: `MOCKUP_CENTRAL_FRAME_THICKNESS = 5.0 mm`
- Base ribs: `MOCKUP_BASE_RIB_HEIGHT = 3.5 mm`
- Module tray bases: `MOCKUP_TRAY_BASE_THICKNESS = 2.4 mm`
- Module tray side walls: `MOCKUP_TRAY_SIDE_WALL = 2.4 mm`
- Module tray side height: `MOCKUP_TRAY_SIDE_HEIGHT = 10.0 mm`
- Non-structural side-panel rib height: `MOCKUP_SIDE_PANEL_RIB_HEIGHT = 1.8 mm`
- Structural side-panel rib height: `MOCKUP_SIDE_SHEAR_RIB_HEIGHT = 3.0 mm`
- Rear service spine depth: `MOCKUP_REAR_SPINE_DEPTH = 22.0 mm`
- Fan grille thickness: `MOCKUP_BOTTOM_GRILLE_THICKNESS = 3.0 mm`

After regenerating the mk0.7.4 pipeline, `printable/plastic` is estimated at `3070.1 g` PETG mesh-equivalent.

Estimated reduction:

```text
3764.4 g - 3070.1 g = 694.3 g
```

This is just below the 700 g lower target, but further reduction would start cutting into tray, frame, or side-panel interfaces that still need physical coupon validation. The current reduction is treated as the conservative rough-mockup stopping point.
