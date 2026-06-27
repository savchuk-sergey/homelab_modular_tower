# Engineering Decisions For mk0.2

Date: 2026-06-27

## Recessed Carriage Grip

Decision: use a recessed grip pocket integrated into the tray front plate.

Reason: the handle becomes a service interface without increasing tower depth or creating a protruding feature that can snag during installation.

## Common Tray Front Interface

Decision: apply the same front plate and handle path through the generic tray generator.

Reason: all modules should share one carriage standard. Future locks, plugs, magnets, or labels can be added consistently.

## Prepared Lock Boss Only

Decision: add M3-compatible lock geometry but do not implement a full latch in mk0.2.

Reason: retention method should be selected after pull-force and access testing.

## Removable Side Service Panels

Decision: side panels remain separate removable parts and are not part of the primary strength path.

Reason: module access and repairability are more important than using side skins as structural members.

## X-Style Side Ribs

Decision: add diagonal ribs inside a perimeter frame.

Reason: this improves panel handling stiffness and reduces large unsupported flat areas without changing the core tower load path.

## Screw Mounting For mk0.2

Decision: use simple M3 mounting holes and bosses.

Reason: screws are predictable for early prototypes. Snap-fit and latch geometry can come later after real tolerances are known.
