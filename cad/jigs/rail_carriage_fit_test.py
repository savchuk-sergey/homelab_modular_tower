"""Rail / carriage / POM-C shoe fit test jig for mk0.11.

This jig assembles a short rail section, the generic module carriage,
and POM-C shoe references into a single cq.Assembly for visual and
dimensional inspection in a STEP viewer.

Purpose:
- Verify U-channel rail pocket clearance (RAIL_POCKET_CLEARANCE).
- Verify POM-C shoe socket diameter (RUNNER_SOCKET_DIAMETER vs RUNNER_DIAMETER).
- Verify carriage-to-rail lateral clearance.
- Verify shoe protrusion geometry (RUNNER_PROTRUSION_FROM_CARRIAGE).

This is NOT a printable production part.  Category: jig / reference.

Exported to: exports/<revision>/review/ or exports/<revision>/jigs/

Usage:
    from cad.jigs.rail_carriage_fit_test import build_rail_carriage_fit_test
    assembly = build_rail_carriage_fit_test()
"""

import cadquery as cq

from .. import config as cfg
from ..parts import rails
from ..parts.module_carriage import make_generic_module_carriage
from ..parts.pom_shoe import make_pom_c_shoe


def _shoe_positions_for_carriage(shoes_per_side: int, c=cfg) -> list[float]:
    """Y offsets of POM-C shoes along the carriage depth axis."""
    side_length = c.MODULE_DEPTH - c.CARRIAGE_SHOE_END_INSET
    if shoes_per_side <= 1:
        return [0.0]
    spacing = side_length / (shoes_per_side - 1)
    return [-side_length / 2 + i * spacing for i in range(shoes_per_side)]


def build_rail_carriage_fit_test(c=cfg) -> cq.Assembly:
    """Assemble rail section + generic carriage + POM-C shoe references.

    Assembly components:
    - generic_module_carriage: the open-frame carriage.
    - rail_left / rail_right: reference U-channel rail sections at
      GENERIC_MODULE_RAIL_LENGTH. Positioned at the carriage lateral sides,
      matching the u_channel_rail_x_offset() location.
    - pom_c_shoe_left_N / pom_c_shoe_right_N: shoe references showing
      each shoe's seated position in the carriage socket, protruding into
      the rail channel.

    All positions follow the same coordinate conventions as tower_assembly.py:
    - X: lateral (± from centerline)
    - Y: depth (front = negative, rear = positive; rear reserved zone offset)
    - Z: height (Z=0 at carriage floor / deck level)

    The carriage is placed at Z=0 (its natural origin).
    The rails are positioned at shoe contact height.
    """
    assembly = cq.Assembly(name="rail_carriage_fit_test_mk011")

    # ---- carriage ----
    assembly.add(
        make_generic_module_carriage(c),
        name="generic_module_carriage",
        loc=cq.Location(cq.Vector(0, 0, 0)),
    )

    # ---- rail placement ----
    # Rail center X: same offset used by module shell rail pocket carriers.
    x_rail = rails.u_channel_rail_x_offset()
    # Y center: rails run along depth axis; centered at rear-reserved-zone midpoint.
    y_center = -c.REAR_RESERVED_DEPTH / 2

    # Z of rail: shoe sits at carriage boss thickness / 2 above carriage floor.
    # Rail vertical center aligns with shoe protrusion midpoint.
    z_rail_shoe_mid = c.CARRIAGE_RUNNER_BOSS_THICKNESS / 2

    rail_solid = rails.make_aluminum_u_channel_rail_placeholder(c.GENERIC_MODULE_RAIL_LENGTH)

    for side, sign in [("left", -1), ("right", 1)]:
        assembly.add(
            rail_solid,
            name=f"rail_{side}",
            loc=cq.Location(
                cq.Vector(sign * x_rail, y_center, z_rail_shoe_mid),
                cq.Vector(1, 0, 0),
                90,
            ),
        )

    # ---- POM-C shoe placement ----
    # Shoes are inserted perpendicular to the rail axis (along X).
    # Each shoe protrudes RUNNER_PROTRUSION_FROM_CARRIAGE into the rail channel.
    shoe_y_offsets = _shoe_positions_for_carriage(c.GENERIC_MODULE_SHOES_PER_SIDE, c)

    # X position: shoe center is at rail inner-wall midpoint.
    # The shoe sits half inside the carriage socket and half inside the rail channel.
    x_shoe_center = x_rail + c.RAIL_OUTER_WIDTH / 2 + c.RUNNER_PROTRUSION_FROM_CARRIAGE / 2

    for side, sign in [("left", -1), ("right", 1)]:
        for idx, y_off in enumerate(shoe_y_offsets):
            assembly.add(
                make_pom_c_shoe(c),
                name=f"pom_c_shoe_{side}_{idx}",
                loc=cq.Location(
                    cq.Vector(sign * x_shoe_center, y_center + y_off, z_rail_shoe_mid),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )

    return assembly
