"""mk0.11 generic module carriage.

The generic module carriage is a device-agnostic open-frame carriage that
slides on the aluminum U-channel rail standard using POM-C Ø8 mm round shoes.

It wraps make_lightweight_open_frame_carriage() from carriages.py without
adding any device-specific features (no standoffs, no SSD retainers, no
device pads). This keeps the carriage geometry clean for interface validation.

Rail standard (frozen from mk0.9.3):
- Profile: aluminum U-channel 15×10×10×2 mm
- Runner: POM-C Ø8×12 mm, purchased, non-printed
- Clamp: M3 screw into PETG boss / heat-set insert
- Primary thread: never directly into POM-C material

Shoe arrangement: GENERIC_MODULE_SHOES_PER_SIDE per side (2 × 2 = 4 total).

Usage:
    from cad.parts.module_carriage import make_generic_module_carriage
    carriage = make_generic_module_carriage()
"""

import cadquery as cq

from .. import config as cfg
from . import carriages


def make_generic_module_carriage(c=cfg) -> cq.Workplane:
    """Open-frame carriage for the generic module.

    Identical geometry to the mk0.9.3 RPi/SSD carriage, but with
    no device-specific pads or retainers.  Uses GENERIC_MODULE_SHOES_PER_SIDE
    (2) shoes per side for a total of 4 POM-C runners.

    Features inherited from make_lightweight_open_frame_carriage():
    - Peripheral open frame (no solid floor — airflow unrestricted).
    - Reinforced shoe boss sockets for POM-C Ø8 mm shoes on both sides.
    - M3 clamp screw clearance hole in each shoe boss bridge.
    - Front pull lip (CARRIAGE_PULL_LIP_*) for ergonomic extraction.
    - M3 front lock screw hole for optional carriage retention.
    - Rear cable exit cutout aligned with REAR_CABLE_EXIT_WIDTH.

    No modifications to the carriage standard are made here.  If device-
    specific features are needed, a new function (e.g.
    make_rpi_ssd_module_carriage_mk011) should be added as a separate
    function that calls this one and adds its features on top.
    """
    return carriages.make_lightweight_open_frame_carriage(
        name="generic_module_carriage",
        shoes_per_side=c.GENERIC_MODULE_SHOES_PER_SIDE,
        device_mode="generic",
        c=c,
    ).tag("generic_module_carriage")
