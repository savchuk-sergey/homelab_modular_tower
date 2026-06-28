"""mk0.11 generic module assembly.

Combines the generic module shell and the generic module carriage into a
single named assembly for STEP export and visual inspection.

This assembly represents one complete removable module unit:
- Generic module shell (printed PETG) at Z=0.
- Generic module carriage (printed PETG), positioned at deck level inside
  the shell, at Z = -GENERIC_MODULE_HEIGHT/2 + CARRIAGE_WALL_THICKNESS/2.

POM-C shoes and U-channel rails are NOT included here; they belong to the
single module bay assembly (single_module_bay_assembly.py) which shows the
full rail / shoe / carriage / module stack.

This assembly is the minimal unit that can be 3D-printed and inspected:
- Shell geometry validated independently.
- Carriage geometry validated independently.
- Together they show the deck-level fit and handle alignment.

Usage:
    from cad.assembly.generic_module_assembly import build_generic_module_assembly
    assembly = build_generic_module_assembly()
"""

import cadquery as cq

from .. import config as cfg
from ..parts.generic_module import make_generic_module
from ..parts.module_carriage import make_generic_module_carriage


def build_generic_module_assembly(c=cfg) -> cq.Assembly:
    """Build the generic module assembly (shell + carriage).

    The module shell is placed at the origin (Z=0 at module center).
    The carriage is placed at deck level: the carriage floor sits at the
    bottom of the module interior volume, consistent with the placement
    used for rpi_ssd_module and mini_pc_placeholder_module.
    """
    assembly = cq.Assembly(name="generic_module_assembly_mk011")

    assembly.add(
        make_generic_module(c),
        name="generic_module_shell",
        loc=cq.Location(cq.Vector(0, 0, 0)),
    )

    # Carriage deck level: bottom of module interior + half carriage wall thickness.
    deck_z = -c.GENERIC_MODULE_HEIGHT / 2 + c.CARRIAGE_WALL_THICKNESS / 2
    assembly.add(
        make_generic_module_carriage(c),
        name="generic_module_carriage",
        loc=cq.Location(cq.Vector(0, 0, deck_z)),
    )

    return assembly
