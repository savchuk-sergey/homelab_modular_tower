# mk0.7.4 Decisions

## Split Joint Interface

Decision: lower split sections carry the positive alignment tab, while upper split sections carry a matching socket with explicit clearance.

Reason: mk0.7.3 exported both lower and upper split parts with occupying tabs at the same joint volume. A tab/socket pair removes the confirmed overlap and keeps the split interface visible for physical coupon validation.

Tradeoff: the socket adds small local print volume and still requires a coupon to validate fit, screw access, and PETG tolerance.

## Bottom Filter Retainer

Decision: replace the detached corner-clip layout with a connected rectangular retainer frame and reinforced corner pads.

Reason: the mk0.7.3 corner clips were not physically connected to the narrow retainer body. A connected frame is less elegant than a final snap-fit but is printable, inspectable, and suitable for rough mockup validation.

Tradeoff: the connected frame uses more plastic than isolated clips, but removes a confirmed impossible geometry blocker.

## Side Panel Orientation

Decision: make left and right side-panel assembly rotations explicit.

Reason: mk0.7.3 used one global `+90 deg` rotation, which made the left panel ribs and bosses face outward. The left side now uses `-90 deg`, while the right side keeps `+90 deg`.

Tradeoff: the panels are still geometrically identical parts, so future revisions should consider mirrored part functions if the interface becomes more complex.

## Rail End Mount Screw Target

Decision: add a vertical M3 screw path through the rail end mount and matching frame holes offset from the metal rail slot.

Reason: mk0.7.3 had a visible rail end mount hole without a clear mating target. The new path gives the mockup bracket an explicit CAD target while preserving the metal rail clearance slot.

Tradeoff: screw length is still `TBD after stack check` and must be validated with a rail-end coupon.

## Rough Mockup Mass Reduction

Decision: use explicit `MOCKUP_*` parameters for draft-print mass reduction instead of local thinning inside part functions.

Reason: mk0.7.4 needs a printable rough mockup without making the long-term production intent ambiguous. Central base sections, stability wings, tray bodies, side-panel ribs, rear spine depth, and fan grilles are reduced for mockup economics while metal rods, metal guide rails, screw clearances, frame rings, and module spacing remain unchanged.

Tradeoff: the reduced parts are suitable for fit and assembly validation, not for final load or abuse testing. Mini PC and UPS trays still require conservative handling until coupon and rough mockup results exist.
