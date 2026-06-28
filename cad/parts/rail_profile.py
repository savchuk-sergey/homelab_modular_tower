"""Aluminum U-channel rail profile reference geometry.

Provides a standalone reference model for the aluminum U-channel rail used
as the primary side-mounted guide rail in the mk0.9.3 / mk0.11 standard.

This is a NON-PRINTED part.  The rail is a purchased aluminum extrusion
(standard U / channel profile), cut to the required length.

Rail standard (frozen from mk0.9.3):
- Profile: aluminum U-channel 15×10×10×2 mm
  - Outer width: RAIL_OUTER_WIDTH = 15 mm
  - Outer height: RAIL_OUTER_HEIGHT = 10 mm
  - Wall thickness: RAIL_WALL_THICKNESS = 2 mm
  - Inner channel width: ~11 mm (15 - 2×2)
  - Inner channel depth: ~8 mm (10 - 2)
- Rail pocket clearance: RAIL_POCKET_CLEARANCE = 0.6 mm (per side)
- Rail type identifier: RAIL_TYPE = "aluminum_u_channel_15x10x10x2"

Note: make_aluminum_u_channel_rail_placeholder() in cad/parts/rails.py and
make_aluminum_u_channel_rail_placeholder() in cad/parts/placeholders.py
both represent this same rail section.  This module wraps the rails.py
version to provide a clear, self-documenting import path for mk0.11 jigs
and assemblies.
"""

import cadquery as cq

from .. import config as cfg
from . import rails


def make_u_channel_rail_profile(length: float) -> cq.Workplane:
    """Reference aluminum U-channel rail section of the given length.

    Delegates to rails.make_aluminum_u_channel_rail_placeholder() which
    builds the U-profile from RAIL_OUTER_WIDTH, RAIL_OUTER_HEIGHT, and
    RAIL_WALL_THICKNESS without any magic numbers.

    Not printable.  Category: reference_non_printed / metal.

    Args:
        length: Rail length in mm (axis-aligned with Y in module context).
    """
    return rails.make_aluminum_u_channel_rail_placeholder(length).tag("u_channel_rail_profile")


def make_generic_module_rail(c=cfg) -> cq.Workplane:
    """Reference U-channel rail at GENERIC_MODULE_RAIL_LENGTH.

    Convenience wrapper for use in mk0.11 assemblies and the fit test jig.
    """
    return make_u_channel_rail_profile(c.GENERIC_MODULE_RAIL_LENGTH).tag(
        "generic_module_rail"
    )
