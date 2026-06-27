"""Metal guide rail placeholders and rail layout."""

import cadquery as cq

from .. import config as cfg


def guide_rail_positions() -> list[tuple[float, float]]:
    x = cfg.METAL_RAIL_X_OFFSET
    return [
        (-x, cfg.METAL_RAIL_Y_FRONT),
        (x, cfg.METAL_RAIL_Y_FRONT),
        (-x, cfg.METAL_RAIL_Y_REAR),
        (x, cfg.METAL_RAIL_Y_REAR),
    ]


def create_metal_guide_rail(height: float = cfg.METAL_RAIL_HEIGHT) -> cq.Workplane:
    """Placeholder steel/aluminium tray rail with M3 fixing holes."""
    rail = cq.Workplane("XY").box(cfg.METAL_RAIL_WIDTH, cfg.METAL_RAIL_THICKNESS, height)
    z_values = []
    z = -height / 2 + cfg.METAL_RAIL_M3_SPACING / 2
    while z < height / 2:
        z_values.append(z)
        z += cfg.METAL_RAIL_M3_SPACING
    for z in z_values:
        rail = rail.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).hole(cfg.M3_CLEARANCE)
    return rail
