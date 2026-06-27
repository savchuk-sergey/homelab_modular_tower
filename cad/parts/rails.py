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


def create_rail_end_mount() -> cq.Workplane:
    """Printed rough bracket that captures a rail end against a frame."""
    mount = cq.Workplane("XY").box(
        cfg.RAIL_END_MOUNT_WIDTH,
        cfg.RAIL_END_MOUNT_DEPTH,
        cfg.RAIL_END_MOUNT_HEIGHT,
    )
    rail_slot = cq.Workplane("XY").box(
        cfg.METAL_RAIL_WIDTH + cfg.METAL_RAIL_FRAME_CLEARANCE,
        cfg.METAL_RAIL_THICKNESS + cfg.METAL_RAIL_FRAME_CLEARANCE,
        cfg.RAIL_END_MOUNT_HEIGHT + cfg.FILLET_RADIUS,
    )
    mount = mount.cut(rail_slot)
    mount = mount.faces(">Y").workplane(centerOption="CenterOfBoundBox").hole(cfg.M3_CLEARANCE)
    return mount.edges("|Z").chamfer(cfg.FILLET_RADIUS).tag("rail_end_mount")


def create_tray_support_ledge() -> cq.Workplane:
    """Small printed ledge for rough tray vertical support at each module level."""
    ledge = cq.Workplane("XY").box(
        cfg.RAIL_SUPPORT_LEDGE_WIDTH,
        cfg.RAIL_SUPPORT_LEDGE_DEPTH,
        cfg.RAIL_SUPPORT_LEDGE_HEIGHT,
    )
    ledge = ledge.faces(">Z").workplane(centerOption="CenterOfBoundBox").hole(cfg.M3_CLEARANCE)
    return ledge.edges("|Z").chamfer(cfg.FILLET_RADIUS).tag("tray_support_ledge")
