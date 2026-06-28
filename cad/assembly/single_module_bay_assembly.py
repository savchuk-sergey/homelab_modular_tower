"""mk0.11 single module bay assembly.

The single module bay assembly shows one complete removable module unit with
its full rail / shoe / carriage / shell stack in the correct geometric
relationship.

This is the primary validation assembly for mk0.11.  Before proceeding to
full tower integration, this assembly must be physically validated per the
steps in revisions/mk0.11/VALIDATION_PLAN.md.

Components (all in their natural positions relative to module center Z=0):
- generic_module: shell + handle + interface features (printed, PETG).
- generic_module_carriage: open-frame carriage at deck level (printed, PETG).
- rail_left / rail_right: aluminum U-channel reference sections (not printed).
- pom_c_shoe_left_N / pom_c_shoe_right_N: POM-C shoe references (not printed).

Coordinate convention (matches tower_assembly.py):
- X: lateral (± from centerline; left = negative, right = positive).
- Y: depth (front = negative, rear = positive; rear reserved zone at + side).
- Z: height (module center at Z=0; bottom at -GENERIC_MODULE_HEIGHT/2).

Usage:
    from cad.assembly.single_module_bay_assembly import build_single_module_bay_assembly
    assembly = build_single_module_bay_assembly()
"""

import cadquery as cq

from .. import config as cfg
from ..parts import rails
from ..parts.generic_module import make_generic_module
from ..parts.module_carriage import make_generic_module_carriage
from ..parts.pom_shoe import make_pom_c_shoe


def _shoe_y_offsets(shoes_per_side: int, c=cfg) -> list[float]:
    """Y offsets of POM-C shoes along the carriage depth axis."""
    side_length = c.MODULE_DEPTH - c.CARRIAGE_SHOE_END_INSET
    if shoes_per_side <= 1:
        return [0.0]
    spacing = side_length / (shoes_per_side - 1)
    return [-side_length / 2 + i * spacing for i in range(shoes_per_side)]


def build_single_module_bay_assembly(c=cfg) -> cq.Assembly:
    """Build the single module bay assembly.

    Places the generic module shell and carriage at Z=0 (module center),
    then adds rail and shoe references in their physically correct positions.

    Rail placement: rails run along the Y axis, centered at the rear-reserved-
    zone midpoint (-REAR_RESERVED_DEPTH/2), at the X positions determined by
    u_channel_rail_x_offset().

    Shoe placement: shoes protrude laterally from the carriage side walls into
    the U-channel inner channel.  Each shoe center is at the carriage boss
    height midpoint (CARRIAGE_RUNNER_BOSS_THICKNESS / 2) above the carriage floor.
    """
    assembly = cq.Assembly(name="single_module_bay_assembly_mk011")

    # ---- printed parts ----

    assembly.add(
        make_generic_module(c),
        name="generic_module",
        loc=cq.Location(cq.Vector(0, 0, 0)),
    )

    deck_z = -c.GENERIC_MODULE_HEIGHT / 2 + c.CARRIAGE_WALL_THICKNESS / 2
    assembly.add(
        make_generic_module_carriage(c),
        name="generic_module_carriage",
        loc=cq.Location(cq.Vector(0, 0, deck_z)),
    )

    # ---- reference non-printed parts ----

    x_rail = rails.u_channel_rail_x_offset()
    y_center = -c.REAR_RESERVED_DEPTH / 2

    # Rail Z: shoe center is at deck_z + CARRIAGE_RUNNER_BOSS_THICKNESS / 2.
    # Rail is positioned so its axis aligns with the shoe contact mid-height.
    z_shoe = deck_z + c.CARRIAGE_RUNNER_BOSS_THICKNESS / 2

    rail_solid = rails.make_aluminum_u_channel_rail_placeholder(c.GENERIC_MODULE_RAIL_LENGTH)

    for side, sign in [("left", -1), ("right", 1)]:
        assembly.add(
            rail_solid,
            name=f"rail_{side}",
            loc=cq.Location(
                cq.Vector(sign * x_rail, y_center, z_shoe),
                cq.Vector(1, 0, 0),
                90,
            ),
        )

    # POM-C shoe references.
    # X center: rail outer face + half shoe protrusion from carriage.
    x_shoe = x_rail + c.RAIL_OUTER_WIDTH / 2 + c.RUNNER_PROTRUSION_FROM_CARRIAGE / 2
    shoe_y_offsets = _shoe_y_offsets(c.GENERIC_MODULE_SHOES_PER_SIDE, c)

    for side, sign in [("left", -1), ("right", 1)]:
        for idx, y_off in enumerate(shoe_y_offsets):
            assembly.add(
                make_pom_c_shoe(c),
                name=f"pom_c_shoe_{side}_{idx}",
                loc=cq.Location(
                    cq.Vector(sign * x_shoe, y_center + y_off, z_shoe),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )

    return assembly
