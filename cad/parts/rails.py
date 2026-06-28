"""Metal guide rail placeholders and rail layout.

mk0.9.1 introduces the aluminum U-channel rail standard (15 x 10 x 10 x 2 mm)
as the primary side-mounted guide rail.  Legacy flat-bar rails are kept for
backward compatibility but are no longer the recommended path.
"""

import cadquery as cq

from .. import config as cfg


# ---------------------------------------------------------------------------
# Legacy mk0.9 flat-bar rail helpers (kept for backward compatibility)
# ---------------------------------------------------------------------------

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
    mount = mount.faces(">Z").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(0.0, cfg.RAIL_END_MOUNT_FRAME_SCREW_OFFSET_Y)]
    ).hole(cfg.M3_CLEARANCE)
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


# ---------------------------------------------------------------------------
# mk0.9.1 U-channel rail standard
# ---------------------------------------------------------------------------

def u_channel_rail_positions() -> list[tuple[float, float]]:
    """Return side-mounted U-channel rail positions for mk0.9.1.

    Rails sit at the lateral sides of the module, aligned with the
    carriage POM-C shoe runners.
    """
    x = cfg.TOWER_WIDTH / 2 - cfg.RAIL_OUTER_WIDTH / 2 - cfg.CARRIAGE_WALL_THICKNESS - 1.0
    y = -cfg.REAR_RESERVED_DEPTH / 2
    return [(-x, y), (x, y)]


def make_aluminum_u_channel_rail_placeholder(length: float) -> cq.Workplane:
    """Non-printed placeholder for aluminum U-channel rail 15 x 10 x 10 x 2 mm.

    Profile is a simple U-shape: outer width 15, outer height 10, wall 2.
    Inner channel ~ 11 mm wide, 8 mm deep (10 - 2 wall thickness).
    """
    ow = cfg.RAIL_OUTER_WIDTH
    oh = cfg.RAIL_OUTER_HEIGHT
    wt = cfg.RAIL_WALL_THICKNESS
    iw = ow - 2 * wt

    outer = cq.Workplane("XY").box(ow, oh, length)
    inner = cq.Workplane("XY").box(iw, oh - wt, length + 0.02).translate((0, wt / 2, 0))
    rail = outer.cut(inner)
    return rail.tag("aluminum_u_channel_rail_placeholder")


def make_rail_pocket_cutter(length: float) -> cq.Workplane:
    """Cutter for the side wall pocket that receives the U-channel rail.

    Pocket is slightly oversized so the rail can be slid in during assembly.
    """
    pw = cfg.RAIL_POCKET_WIDTH
    ph = cfg.RAIL_POCKET_HEIGHT
    return cq.Workplane("XY").box(pw, ph, length + 0.02)


def make_rail_end_clip() -> cq.Workplane:
    """Small printed clip that retains the U-channel rail end in the module shell.

    The clip is screwed into the module side wall with an M3 screw;
    it blocks the rail from sliding out without requiring glue.
    """
    clip = cq.Workplane("XY").box(12.0, 8.0, 6.0)
    clip = clip.faces(">Z").workplane().hole(cfg.M3_CLEARANCE)
    # small lip that overlaps the rail end
    lip = cq.Workplane("XY").box(6.0, 4.0, 3.0).translate((0, -2.0, 3.5))
    clip = clip.union(lip)
    return clip.edges("|Z").chamfer(cfg.FILLET_RADIUS).tag("rail_end_clip")
