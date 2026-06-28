# mk0.9.2 Printing Notes

## Print-volume check

All printable PETG and TPU STL files fit within the configured 256 x 256 x
256 mm Bambu Lab P2S axis-aligned print volume.

## Long-thin review flags

The pipeline flagged these printable parts for orientation/support review:

- `bottom_grill`
- `dust_filter_slot`
- `foot_mounts`
- `top_filter_slot`

The flags are geometric heuristics, not print failures.

## STL quality

All printable PETG and TPU STL files were reported as watertight and manifold
by the edge-counting STL check.

The `fan_120x120x25_placeholder` has an open/nonmanifold placeholder mesh flag.
That artifact is not a printable production part.

## Required manual checks

- Slicer orientation and support strategy.
- Rail pocket bridge/perimeter quality.
- Heat-set insert boss printability.
- POM-C shoe socket tolerance coupon.
- Actual PETG material use with selected infill/perimeters.
