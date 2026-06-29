"""mk0.9.2 lightweight Base Module with bottom intake, filter tray and TPU foot mounts.

The base is no longer a massive slab.  It is a frame-only structure with
local ribs, a fan mount plate, a bottom grill, and replaceable TPU foot
mounts.  All stiffness comes from the frame geometry, corner posts, and
the M5 rod system—not from thick PETG walls.
"""

import cadquery as cq

from cad import config as cfg
from cad.parts import module_interface


def _frame_body(height: float, c=cfg) -> cq.Workplane:
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    inner = cq.Workplane("XY").box(
        c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
        c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL,
        c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
    ).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(
        c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
        c.REAR_RESERVED_DEPTH - c.MODULE_FRAME_RAIL,
        c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
    ).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    ring = ring.cut(inner).cut(rear)
    body = ring.translate((0, 0, -height / 2 + c.MODULE_INTERFACE_HEIGHT / 2)).union(
        ring.translate((0, 0, height / 2 - c.MODULE_INTERFACE_HEIGHT / 2))
    )
    post_size = c.CORNER_POST_SIZE
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        body = body.union(cq.Workplane("XY").box(post_size, post_size, height).translate((px, py, 0)))
    return body


def make_base_frame(c=cfg) -> cq.Workplane:
    """Lightweight frame-only base structure.  No solid floor."""
    base = _frame_body(c.BASE_MODULE_HEIGHT, c)
    # mk0.9.x: keep the base off the massive floor ribs that were added in mk0.9.
    # Stiffness is provided by the frame rings, corner posts, and M5 rods.
    return base.tag("base_frame")


def make_base_fan_mount(c=cfg) -> cq.Workplane:
    plate = cq.Workplane("XY").box(
        c.FAN_120_SIZE + 2 * c.FAN_MOUNT_FRAME_MARGIN,
        c.FAN_120_SIZE + 2 * c.FAN_MOUNT_FRAME_MARGIN,
        c.FLOOR_THICKNESS,
    )
    plate = plate.faces(">Z").workplane().circle(c.FAN_120_SIZE / 2).cutThruAll()
    d = c.FAN_120_HOLE_SPACING / 2
    return plate.faces(">Z").workplane().pushPoints([(x, y) for x in (-d, d) for y in (-d, d)]).hole(c.FAN_SCREW_CLEARANCE).tag("base_fan_mount")


def make_bottom_grill(c=cfg) -> cq.Workplane:
    grill = cq.Workplane("XY").box(
        c.FAN_120_SIZE + 2 * c.FAN_GRILL_FRAME_MARGIN,
        c.FAN_120_SIZE + 2 * c.FAN_GRILL_FRAME_MARGIN,
        c.FLOOR_THICKNESS,
    )
    grill = grill.faces(">Z").workplane().circle(c.FAN_120_SIZE / 2).cutThruAll()
    for offset in c.FAN_GRILLE_BAR_X:
        grill = grill.union(cq.Workplane("XY").box(c.RIB_THICKNESS, c.FAN_120_SIZE - c.FAN_GRILLE_BAR_LENGTH_INSET, c.FLOOR_THICKNESS).translate((offset, 0, 0)))
        grill = grill.union(cq.Workplane("XY").box(c.FAN_120_SIZE - c.FAN_GRILLE_BAR_LENGTH_INSET, c.RIB_THICKNESS, c.FLOOR_THICKNESS).translate((0, offset, 0)))
    return grill.tag("bottom_grill")


def make_dust_filter_slot(c=cfg) -> cq.Workplane:
    slot = cq.Workplane("XY").box(c.BASE_FILTER_TRAY_WIDTH, c.BASE_FILTER_TRAY_DEPTH, c.FILTER_SLOT_HEIGHT)
    window = cq.Workplane("XY").box(
        c.BASE_FILTER_TRAY_WIDTH - 2 * c.FILTER_FRAME_MARGIN,
        c.BASE_FILTER_TRAY_DEPTH - 2 * c.FILTER_FRAME_MARGIN,
        c.FILTER_SLOT_HEIGHT + c.FILLET_RADIUS,
    )
    pull = cq.Workplane("XY").box(c.BASE_FILTER_TRAY_WIDTH * 0.45, c.BASE_FILTER_TRAY_PULL_DEPTH, c.FILTER_SLOT_HEIGHT).translate(
        (0, -c.BASE_FILTER_TRAY_DEPTH / 2 - c.BASE_FILTER_TRAY_PULL_DEPTH / 2, 0)
    )
    return slot.cut(window).union(pull).tag("dust_filter_slot")


def make_foot_mounts(c=cfg) -> cq.Workplane:
    """PETG socket bosses for replaceable TPU feet at the four corners."""
    mounts = None
    boss_radius = (c.FOOT_DIAMETER + c.FOOT_MOUNT_BOSS_EXTRA_DIAMETER) / 2
    x = c.TOWER_WIDTH / 2 - boss_radius
    y = c.TOWER_DEPTH / 2 - boss_radius
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        boss = cq.Workplane("XY").circle(boss_radius).extrude(c.FLOOR_THICKNESS).translate((px, py, 0))
        socket = cq.Workplane("XY").circle((c.FOOT_DIAMETER + c.FOOT_TPU_CLEARANCE) / 2).extrude(c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((px, py, 0))
        mount = boss.cut(socket)
        mounts = mount if mounts is None else mounts.union(mount)
    return mounts.tag("foot_mounts")


def make_base_module(c=cfg) -> cq.Workplane:
    """Assembled lightweight base module.

    Components from bottom to top:
    1. Foot mounts (TPU feet attach here)
    2. Bottom grill (intake protection)
    3. Dust filter slot (removable filter tray)
    4. Fan mount (120 mm intake fan)
    5. Frame (M5 rod posts + module interface)
    """
    module = make_base_frame(c)
    fan_y = -c.REAR_RESERVED_DEPTH / 2

    # Fan mount sits just above the bottom of the frame
    z_fan_mount = -c.BASE_MODULE_HEIGHT / 2 + c.FLOOR_THICKNESS / 2
    module = module.union(make_base_fan_mount(c).translate((0, fan_y, z_fan_mount)))

    # Bottom grill sits below the fan mount
    z_grill = z_fan_mount - c.FLOOR_THICKNESS
    module = module.union(make_bottom_grill(c).translate((0, fan_y, z_grill)))

    # Dust filter slot sits below the grill
    z_filter = z_grill - c.FLOOR_THICKNESS / 2 - c.FILTER_SLOT_HEIGHT / 2
    module = module.union(make_dust_filter_slot(c).translate((0, fan_y, z_filter)))

    # Foot mounts sit on the very bottom face of the frame
    z_feet = -c.BASE_MODULE_HEIGHT / 2 - c.FLOOR_THICKNESS / 2
    module = module.union(make_foot_mounts(c).translate((0, 0, z_feet)))

    return module_interface.apply_module_interface_features(module, c, top=True, bottom=False).tag("base_module")
