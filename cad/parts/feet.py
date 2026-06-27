"""Stability base and removable TPU feet for bottom intake clearance."""

import cadquery as cq

from .. import config as cfg
from .rods import rod_positions


def wide_foot_positions() -> tuple[tuple[float, float], ...]:
    """Return mk0.5 wide support points near the expanded base corners."""
    x = cfg.BASE_STABILITY_FOOT_OFFSET_X
    y = cfg.BASE_STABILITY_FOOT_OFFSET_Y
    return ((-x, -y), (x, -y), (x, y), (-x, y))


def make_foot_socket() -> cq.Workplane:
    """Create one PETG socket boss for a replaceable TPU foot."""
    socket = cq.Workplane("XY").circle(cfg.FOOT_SOCKET_BOSS_DIAMETER / 2).extrude(cfg.FOOT_SOCKET_DEPTH)
    socket = socket.cut(
        cq.Workplane("XY")
        .circle(cfg.FOOT_SOCKET_DIAMETER / 2)
        .extrude(cfg.FOOT_SOCKET_DEPTH + cfg.FILLET_RADIUS)
        .translate((0, 0, cfg.FILLET_RADIUS / 2))
    )
    socket = socket.faces(">Z").workplane().circle(cfg.FOOT_SCREW_DIAMETER / 2).cutThruAll()
    return socket.tag("foot_socket")


def _rib(length: float, width: float, height: float, x: float, y: float) -> cq.Workplane:
    rib = cq.Workplane("XY").box(length, width, height)
    return rib.translate((x, y, -cfg.BASE_STABILITY_THICKNESS / 2 - height / 2))


def _add_base_ribs(base: cq.Workplane) -> cq.Workplane:
    rib_h = cfg.BASE_STABILITY_RIB_HEIGHT
    rib_t = cfg.BASE_STABILITY_RIB_THICKNESS
    inset = cfg.BASE_STABILITY_PERIMETER_RIB_INSET
    x_len = cfg.BASE_STABILITY_WIDTH - 2 * inset
    y_len = cfg.BASE_STABILITY_DEPTH - 2 * inset

    for y in (-(cfg.BASE_STABILITY_DEPTH / 2 - inset), cfg.BASE_STABILITY_DEPTH / 2 - inset):
        base = base.union(_rib(x_len, rib_t, rib_h, 0, y))
    for x in (-(cfg.BASE_STABILITY_WIDTH / 2 - inset), cfg.BASE_STABILITY_WIDTH / 2 - inset):
        base = base.union(_rib(rib_t, y_len, rib_h, x, 0))

    fan = cfg.BASE_STABILITY_FAN_RIB_OFFSET
    for y in (-fan, fan):
        base = base.union(_rib(cfg.BASE_STABILITY_FAN_CLEARANCE_DIAMETER, rib_t, rib_h, 0, y))
    for x in (-fan, fan):
        base = base.union(_rib(rib_t, cfg.BASE_STABILITY_FAN_CLEARANCE_DIAMETER, rib_h, x, 0))
    return base


def make_base_stability_plate() -> cq.Workplane:
    """Create mk0.5 expanded structural base without blocking the 120 mm intake."""
    base = (
        cq.Workplane("XY")
        .box(cfg.BASE_STABILITY_WIDTH, cfg.BASE_STABILITY_DEPTH, cfg.BASE_STABILITY_THICKNESS)
        .edges("|Z")
        .chamfer(cfg.BASE_STABILITY_CORNER_RADIUS)
    )

    intake = (
        cq.Workplane("XY")
        .circle(cfg.BASE_STABILITY_FAN_CLEARANCE_DIAMETER / 2)
        .extrude(cfg.BASE_STABILITY_THICKNESS + cfg.BASE_STABILITY_RIB_HEIGHT + cfg.FILLET_RADIUS * 2)
        .translate((0, 0, -cfg.BASE_STABILITY_RIB_HEIGHT / 2 - cfg.FILLET_RADIUS))
    )
    base = base.cut(intake)

    for x, y in rod_positions():
        base = base.faces(">Z").workplane().pushPoints([(x, y)]).hole(cfg.ROD_CLEARANCE)

    frame_mounts = []
    for x in (-cfg.BASE_STABILITY_FRAME_MOUNT_X, cfg.BASE_STABILITY_FRAME_MOUNT_X):
        for y in (-cfg.BASE_STABILITY_FRAME_MOUNT_Y, cfg.BASE_STABILITY_FRAME_MOUNT_Y):
            frame_mounts.append((x, y))
    base = base.faces(">Z").workplane().pushPoints(frame_mounts).hole(cfg.M3_CLEARANCE)

    for x, y in wide_foot_positions():
        socket_cut = (
            cq.Workplane("XY")
            .circle(cfg.FOOT_SOCKET_DIAMETER / 2)
            .extrude(cfg.FOOT_SOCKET_DEPTH + cfg.FILLET_RADIUS)
            .translate((x, y, -cfg.BASE_STABILITY_THICKNESS / 2 - cfg.FILLET_RADIUS / 2))
        )
        screw_cut = (
            cq.Workplane("XY")
            .circle(cfg.FOOT_SCREW_DIAMETER / 2)
            .extrude(cfg.BASE_STABILITY_THICKNESS + cfg.BASE_STABILITY_RIB_HEIGHT + cfg.FILLET_RADIUS * 2)
            .translate((x, y, -cfg.BASE_STABILITY_RIB_HEIGHT / 2 - cfg.FILLET_RADIUS))
        )
        base = base.cut(socket_cut).cut(screw_cut)

    return _add_base_ribs(base).tag("base_stability_plate")


def make_wide_tpu_foot_placeholder() -> cq.Workplane:
    """Create one replaceable TPU foot placeholder with an M5 through-hole."""
    foot = cq.Workplane("XY").circle(cfg.FOOT_DIAMETER / 2).extrude(cfg.FOOT_HEIGHT)
    foot = foot.translate((0, 0, -cfg.FOOT_HEIGHT / 2))

    screw_cutter = cq.Workplane("XY").circle(cfg.FOOT_SCREW_DIAMETER / 2).extrude(
        cfg.FOOT_HEIGHT + cfg.FILLET_RADIUS * 2
    )
    screw_cutter = screw_cutter.translate((0, 0, -cfg.FOOT_HEIGHT / 2 - cfg.FILLET_RADIUS))
    foot = foot.cut(screw_cutter)

    counterbore = cq.Workplane("XY").circle(cfg.FOOT_COUNTERBORE_DIAMETER / 2).extrude(
        cfg.FOOT_COUNTERBORE_DEPTH + cfg.FILLET_RADIUS
    )
    counterbore = counterbore.translate((0, 0, -cfg.FOOT_HEIGHT / 2 - cfg.FILLET_RADIUS / 2))
    foot = foot.cut(counterbore)

    return foot.tag("wide_tpu_foot_placeholder")


def make_foot() -> cq.Workplane:
    return make_wide_tpu_foot_placeholder()


def create_foot() -> cq.Workplane:
    return make_foot()
