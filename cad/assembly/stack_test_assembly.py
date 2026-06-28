"""mk0.11.2 stack test assembly — layer-cake prototype without carriage/rails.

Assembles base_pedestal + generic_stack_module + top_cap with reference
M5 threaded rods.  This is the primary validation assembly for mk0.11.2.

Does NOT include active carriage, rails, or POM-C shoes.
"""

import cadquery as cq

from .. import config as cfg
from ..parts.base_pedestal import make_base_pedestal
from ..parts.generic_stack_module import make_generic_stack_module
from ..parts.rods import create_m5_threaded_rod, rod_positions
from ..parts.top_cap import make_top_cap


def build_stack_test_assembly(c=cfg) -> cq.Assembly:
    """Build the mk0.11.2 stack-through-rod test assembly."""
    assembly = cq.Assembly(name="stack_test_assembly_mk0112")

    z_base = c.BASE_PEDESTAL_HEIGHT / 2
    z_module = c.BASE_PEDESTAL_HEIGHT + c.GENERIC_STACK_MODULE_HEIGHT / 2
    z_cap = c.BASE_PEDESTAL_HEIGHT + c.GENERIC_STACK_MODULE_HEIGHT + c.TOP_CAP_HEIGHT / 2

    assembly.add(
        make_base_pedestal(c),
        name="base_pedestal",
        loc=cq.Location(cq.Vector(0, 0, z_base)),
    )
    assembly.add(
        make_generic_stack_module(c),
        name="generic_stack_module",
        loc=cq.Location(cq.Vector(0, 0, z_module)),
    )
    assembly.add(
        make_top_cap(c),
        name="top_cap",
        loc=cq.Location(cq.Vector(0, 0, z_cap)),
    )

    rod = create_m5_threaded_rod(c.STACK_TEST_ROD_LENGTH)
    for idx, (x, y) in enumerate(rod_positions()):
        assembly.add(
            rod,
            name=f"m5_threaded_rod_{idx}",
            loc=cq.Location(cq.Vector(x, y, 0)),
        )

    return assembly
