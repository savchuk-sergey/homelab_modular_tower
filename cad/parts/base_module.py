"""mk0.9 Base Module with bottom intake, filter tray and TPU foot mounts."""

import cadquery as cq

from .. import config as cfg
from . import module_interface


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
    base = _frame_body(c.BASE_MODULE_HEIGHT, c)
    rib_z = -c.BASE_MODULE_HEIGHT / 2 + c.FLOOR_THICKNESS / 2
    usable_y = -c.REAR_RESERVED_DEPTH / 2
    for x in (-c.AIRFLOW_CHANNEL_WIDTH / 2 - c.RIB_THICKNESS, c.AIRFLOW_CHANNEL_WIDTH / 2 + c.RIB_THICKNESS):
        base = base.union(cq.Workplane("XY").box(c.RIB_THICKNESS, c.MODULE_USABLE_DEPTH, c.FLOOR_THICKNESS).translate((x, usable_y, rib_z)))
    for y in (
        usable_y - c.AIRFLOW_CHANNEL_DEPTH / 2 - c.RIB_THICKNESS,
        usable_y + c.AIRFLOW_CHANNEL_DEPTH / 2 + c.RIB_THICKNESS,
    ):
        base = base.union(cq.Workplane("XY").box(c.MODULE_USABLE_DEPTH, c.RIB_THICKNESS, c.FLOOR_THICKNESS).translate((0, y, rib_z)))
    return base.tag("base_frame")


def make_base_fan_mount(c=cfg) -> cq.Workplane:
    plate = cq.Workplane("XY").box(c.FAN_120_SIZE + 22.0, c.FAN_120_SIZE + 22.0, c.FLOOR_THICKNESS)
    plate = plate.faces(">Z").workplane().circle(c.FAN_120_SIZE / 2).cutThruAll()
    d = c.FAN_120_HOLE_SPACING / 2
    return plate.faces(">Z").workplane().pushPoints([(x, y) for x in (-d, d) for y in (-d, d)]).hole(c.FAN_SCREW_CLEARANCE).tag("base_fan_mount")


def make_bottom_grill(c=cfg) -> cq.Workplane:
    grill = cq.Workplane("XY").box(c.FAN_120_SIZE + 18.0, c.FAN_120_SIZE + 18.0, c.FLOOR_THICKNESS)
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
    mounts = None
    boss_radius = (c.FOOT_DIAMETER + 8.0) / 2
    x = c.TOWER_WIDTH / 2 - boss_radius
    y = c.TOWER_DEPTH / 2 - boss_radius
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        boss = cq.Workplane("XY").circle(boss_radius).extrude(c.FLOOR_THICKNESS).translate((px, py, 0))
        socket = cq.Workplane("XY").circle((c.FOOT_DIAMETER + c.FOOT_TPU_CLEARANCE) / 2).extrude(c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((px, py, 0))
        mount = boss.cut(socket)
        mounts = mount if mounts is None else mounts.union(mount)
    return mounts.tag("foot_mounts")


def make_base_module(c=cfg) -> cq.Workplane:
    module = make_base_frame(c)
    fan_y = -c.REAR_RESERVED_DEPTH / 2
    z_floor = -c.BASE_MODULE_HEIGHT / 2 + c.FLOOR_THICKNESS / 2
    module = module.union(make_base_fan_mount(c).translate((0, fan_y, z_floor)))
    return module_interface.apply_module_interface_features(module, c, top=True, bottom=False).tag("base_module")
