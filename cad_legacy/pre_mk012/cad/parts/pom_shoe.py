"""POM-C Ø8 × 12 mm round shoe runner reference geometry.

Provides a standalone reference model for the POM-C round shoe used as the
sliding interface between the open-frame carriage and the aluminum U-channel rail.

This is a NON-PRINTED part.  The shoe is a purchased POM-C (polyoxymethylene
copolymer) round rod section, cut to RUNNER_SHOE_LENGTH.

Rail standard (frozen from mk0.9.3):
- Shoe diameter: RUNNER_DIAMETER = 8.0 mm
- Shoe length: RUNNER_SHOE_LENGTH = 12.0 mm
- Insert depth into carriage: RUNNER_INSERT_DEPTH_INTO_CARRIAGE = 6.0 mm
- Protrusion from carriage into rail channel: RUNNER_PROTRUSION_FROM_CARRIAGE = 6.0 mm
- Socket in carriage: RUNNER_SOCKET_DIAMETER = 8.3 mm (0.3 mm clearance)

Primary thread never goes directly into POM-C.
M3 clamp screw passes through the PETG boss bridge and clamps the shoe in place.

Note: make_pom_c_shoe_placeholder() in cad/parts/placeholders.py also represents
this same shoe.  This module is provided as a dedicated standalone reference
for use in the mk0.11 subsystem jigs and assemblies, with explicit documentation
of the full shoe geometry and interface standard.
"""

import cadquery as cq

from .. import config as cfg


def make_pom_c_shoe(c=cfg) -> cq.Workplane:
    """Reference geometry for one POM-C Ø8 × 12 mm shoe runner.

    Plain cylinder Ø8 mm × 12 mm.  Centered at Z=0 (shoe midpoint).

    This geometry represents the full purchased POM-C shoe before insertion
    into the carriage socket.  In the assembled state:
    - 6 mm of the shoe is inside the carriage socket.
    - 6 mm of the shoe protrudes into the U-channel rail inner channel.

    Not printable.  Category: reference_non_printed / wear_parts.
    """
    return (
        cq.Workplane("XY")
        .circle(c.RUNNER_DIAMETER / 2)
        .extrude(c.RUNNER_SHOE_LENGTH)
        .translate((0, 0, -c.RUNNER_SHOE_LENGTH / 2))
    ).tag("pom_c_shoe")
