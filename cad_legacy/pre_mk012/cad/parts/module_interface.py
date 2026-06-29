"""Tower Module Interface v1 draft features for mk0.9 stackable modules."""

import cadquery as cq

from .. import config as cfg


def _corner_points(c=cfg) -> list[tuple[float, float]]:
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    return [(x, y), (-x, y), (-x, -y), (x, -y)]


def _alignment_points(c=cfg) -> list[tuple[float, float]]:
    x = c.TOWER_WIDTH / 2 - c.INTERFACE_BOLT_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.INTERFACE_LOCAL_BOLT_OFFSET_Y
    return [(-x, -y), (x, -y), (-x, y), (x, y)]


def _interface_bolt_points(c=cfg) -> list[tuple[float, float]]:
    x = c.TOWER_WIDTH / 2 - c.INTERFACE_BOLT_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.INTERFACE_LOCAL_BOLT_OFFSET_Y
    return [(0.0, -y), (0.0, y), (-x, 0.0), (x, 0.0)]


def make_module_interface_top(c=cfg) -> cq.Workplane:
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    airflow = cq.Workplane("XY").box(
        c.AIRFLOW_CHANNEL_WIDTH,
        c.AIRFLOW_CHANNEL_DEPTH,
        c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
    ).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(
        c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
        c.REAR_RESERVED_DEPTH,
        c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
    ).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    return ring.cut(airflow).cut(rear).tag("module_interface_top")


def make_module_interface_bottom(c=cfg) -> cq.Workplane:
    return make_module_interface_top(c).tag("module_interface_bottom")


def make_alignment_pins(c=cfg) -> cq.Workplane:
    pins = None
    for x, y in _alignment_points(c):
        pin = cq.Workplane("XY").circle(c.INTERFACE_PIN_DIAMETER / 2).extrude(c.INTERFACE_PIN_HEIGHT).translate((x, y, 0))
        pins = pin if pins is None else pins.union(pin)
    return pins.tag("alignment_pins")


def make_alignment_sockets(c=cfg) -> cq.Workplane:
    sockets = None
    for x, y in _alignment_points(c):
        socket = cq.Workplane("XY").circle(c.INTERFACE_PIN_CLEARANCE / 2).extrude(c.INTERFACE_SOCKET_DEPTH).translate((x, y, 0))
        sockets = socket if sockets is None else sockets.union(socket)
    return sockets.tag("alignment_sockets")


def make_interface_bolt_holes(c=cfg) -> cq.Workplane:
    holes = None
    for x, y in _interface_bolt_points(c):
        hole = cq.Workplane("XY").circle(c.INTERFACE_BOLT_CLEARANCE / 2).extrude(c.FRAME_HEIGHT).translate((x, y, 0))
        holes = hole if holes is None else holes.union(hole)
    return holes.tag("interface_bolt_holes")


def make_rod_clearance_holes(c=cfg) -> cq.Workplane:
    holes = None
    for x, y in _corner_points(c):
        hole = cq.Workplane("XY").circle(c.ROD_CLEARANCE / 2).extrude(c.FRAME_HEIGHT).translate((x, y, 0))
        holes = hole if holes is None else holes.union(hole)
    return holes.tag("rod_clearance_holes")


def apply_module_interface_features(part: cq.Workplane, c=cfg, top: bool = True, bottom: bool = True) -> cq.Workplane:
    """Apply shared TMI holes, bottom sockets and top alignment pins."""
    bbox = part.val().BoundingBox()
    cutter_height = bbox.zlen + c.FILLET_RADIUS * 4
    z_min = bbox.zmin - c.FILLET_RADIUS
    z_max = bbox.zmax

    for x, y in _corner_points(c):
        part = part.cut(cq.Workplane("XY").circle(c.ROD_CLEARANCE / 2).extrude(cutter_height).translate((x, y, z_min)))
    for x, y in _interface_bolt_points(c):
        part = part.cut(cq.Workplane("XY").circle(c.INTERFACE_BOLT_CLEARANCE / 2).extrude(cutter_height).translate((x, y, z_min)))
    if bottom:
        for x, y in _alignment_points(c):
            part = part.cut(
                cq.Workplane("XY")
                .circle(c.INTERFACE_PIN_CLEARANCE / 2)
                .extrude(c.INTERFACE_SOCKET_DEPTH + c.FILLET_RADIUS)
                .translate((x, y, bbox.zmin - c.FILLET_RADIUS / 2))
            )
    if top:
        for x, y in _alignment_points(c):
            part = part.union(
                cq.Workplane("XY")
                .circle(c.INTERFACE_PIN_DIAMETER / 2)
                .extrude(c.INTERFACE_PIN_HEIGHT)
                .translate((x, y, z_max))
            )
    return part
