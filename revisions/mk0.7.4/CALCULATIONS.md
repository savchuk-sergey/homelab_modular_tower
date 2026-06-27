# mk0.7.4 Calculations

## Baseline

The baseline geometry and plastic estimates are inherited from mk0.7.3 until the mk0.7.4 pipeline is regenerated.

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
