# mk0.7.4 Known Issues

## Coupon-Required Interfaces

- Split-joint tab/socket fit is CAD-coherent but not physically validated.
- Bottom filter retainer stiffness and filter-sheet grip are not physically validated.
- Rail end mount engagement and screw target are CAD-coherent but not physically validated.
- Side panel orientation and rail clearance are CAD-coherent but not physically validated.
- Coupon STLs exist, but every coupon result remains `NOT TESTED` until a physical print is inspected.
- Mockup mass reduction is CAD/export validated only; reduced walls and ribs still need coupon and rough-assembly feedback before being treated as production geometry.
- M3 screw lengths remain `TBD after stack check`; mk0.7.4 identifies hardware classes and counts but does not claim final screw lengths.
- Tray ledge misassembly is controlled by a table, not by a physical jig; a jig or indexed rail may still be needed after mockup feedback.
- Print orientations are planning recommendations only; no slicer simulation or physical print result is claimed.
- Final readiness verdict is limited to partial test print; full tower print remains gated by physical coupon results.

## Deferred Non-Goals

- Final electrical sizing and connector selection remain out of scope.
- Final Mini PC duct geometry remains out of scope until real device measurements are available.
- No CFD, FEA, slicer, or physical-test result is claimed for mk0.7.4 until generated externally.
