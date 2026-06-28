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


def _rib(length: float, width: float, height: float, x: float, y: float, base_thickness: float) -> cq.Workplane:
    rib = cq.Workplane("XY").box(length, width, height)
    return rib.translate((x, y, -base_thickness / 2 - height / 2))


def _add_base_ribs(base: cq.Workplane, width: float, depth: float, base_thickness: float) -> cq.Workplane:
    rib_h = cfg.BASE_STABILITY_RIB_HEIGHT
    rib_t = cfg.BASE_STABILITY_RIB_THICKNESS
    inset = cfg.BASE_STABILITY_PERIMETER_RIB_INSET
    x_len = width - 2 * inset
    y_len = depth - 2 * inset

    for y in (-(depth / 2 - inset), depth / 2 - inset):
        base = base.union(_rib(x_len, rib_t, rib_h, 0, y, base_thickness))
    for x in (-(width / 2 - inset), width / 2 - inset):
        base = base.union(_rib(rib_t, y_len, rib_h, x, 0, base_thickness))

    fan = cfg.BASE_STABILITY_FAN_RIB_OFFSET
    for y in (-fan, fan):
        base = base.union(_rib(cfg.BASE_STABILITY_FAN_CLEARANCE_DIAMETER, rib_t, rib_h, 0, y, base_thickness))
    for x in (-fan, fan):
        base = base.union(_rib(rib_t, cfg.BASE_STABILITY_FAN_CLEARANCE_DIAMETER, rib_h, x, 0, base_thickness))
    return base


def _cut_intake(part: cq.Workplane, base_thickness: float) -> cq.Workplane:
    intake = (
        cq.Workplane("XY")
        .circle(cfg.BASE_STABILITY_FAN_CLEARANCE_DIAMETER / 2)
        .extrude(base_thickness + cfg.BASE_STABILITY_RIB_HEIGHT + cfg.FILLET_RADIUS * 2)
        .translate((0, 0, -cfg.BASE_STABILITY_RIB_HEIGHT / 2 - cfg.FILLET_RADIUS))
    )
    return part.cut(intake)


def _add_frame_mounts(part: cq.Workplane) -> cq.Workplane:
    for x, y in rod_positions():
        part = part.faces(">Z").workplane().pushPoints([(x, y)]).hole(cfg.ROD_CLEARANCE)

    frame_mounts = []
    for x in (-cfg.BASE_STABILITY_FRAME_MOUNT_X, cfg.BASE_STABILITY_FRAME_MOUNT_X):
        for y in (-cfg.BASE_STABILITY_FRAME_MOUNT_Y, cfg.BASE_STABILITY_FRAME_MOUNT_Y):
            frame_mounts.append((x, y))
    return part.faces(">Z").workplane().pushPoints(frame_mounts).hole(cfg.M3_CLEARANCE)


def _add_wing_fasteners(part: cq.Workplane, horizontal: bool) -> cq.Workplane:
    points = []
    spacing = cfg.BASE_WING_FASTENER_SPACING / 2
    edge = cfg.BASE_WING_FASTENER_OFFSET
    if horizontal:
        for x in (-spacing, spacing):
            for y in (-edge, edge):
                points.append((x, y))
    else:
        for x in (-edge, edge):
            for y in (-spacing, spacing):
                points.append((x, y))
    return part.faces(">Z").workplane().pushPoints(points).hole(cfg.M3_CLEARANCE)


def _make_base_section(
    width: float,
    depth: float,
    name: str,
    include_intake: bool = False,
    thickness: float = cfg.BASE_STABILITY_THICKNESS,
) -> cq.Workplane:
    part = (
        cq.Workplane("XY")
        .box(width, depth, thickness)
        .edges("|Z")
        .chamfer(cfg.BASE_STABILITY_CORNER_RADIUS)
    )
    if include_intake:
        part = _cut_intake(part, thickness)
    return part.tag(name)


def make_central_bottom_fan_frame() -> cq.Workplane:
    section = _make_base_section(
        cfg.BASE_CENTER_FRAME_WIDTH,
        cfg.BASE_CENTER_FRAME_DEPTH,
        "central_bottom_fan_frame",
        include_intake=True,
        thickness=cfg.BASE_CENTER_FRAME_THICKNESS,
    )
    section = _add_frame_mounts(section)
    return _add_base_ribs(section, cfg.BASE_CENTER_FRAME_WIDTH, cfg.BASE_CENTER_FRAME_DEPTH, cfg.BASE_CENTER_FRAME_THICKNESS)


def make_left_foot_extension() -> cq.Workplane:
    section = _make_base_section(cfg.FOOT_EXTENSION_X + cfg.BASE_WING_OVERLAP, cfg.OUTER_DEPTH, "left_foot_extension")
    return _add_wing_fasteners(section, horizontal=False)


def make_right_foot_extension() -> cq.Workplane:
    section = _make_base_section(cfg.FOOT_EXTENSION_X + cfg.BASE_WING_OVERLAP, cfg.OUTER_DEPTH, "right_foot_extension")
    return _add_wing_fasteners(section, horizontal=False)


def make_front_stability_wing() -> cq.Workplane:
    section = _make_base_section(cfg.BASE_STABILITY_WIDTH, cfg.FOOT_EXTENSION_Y + cfg.BASE_WING_OVERLAP, "front_stability_wing")
    return _add_wing_fasteners(section, horizontal=True)


def make_rear_stability_wing() -> cq.Workplane:
    section = _make_base_section(cfg.BASE_STABILITY_WIDTH, cfg.FOOT_EXTENSION_Y + cfg.BASE_WING_OVERLAP, "rear_stability_wing")
    return _add_wing_fasteners(section, horizontal=True)


def make_base_stability_plate() -> cq.Workplane:
    """Create assembled mk0.6 sectional stability base without blocking the 120 mm intake."""
    base = (
        cq.Workplane("XY")
        .box(cfg.BASE_STABILITY_WIDTH, cfg.BASE_STABILITY_DEPTH, cfg.BASE_STABILITY_THICKNESS)
        .edges("|Z")
        .chamfer(cfg.BASE_STABILITY_CORNER_RADIUS)
    )

    base = _cut_intake(base, cfg.BASE_STABILITY_THICKNESS)
    base = _add_frame_mounts(base)

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

    return _add_base_ribs(base, cfg.BASE_STABILITY_WIDTH, cfg.BASE_STABILITY_DEPTH, cfg.BASE_STABILITY_THICKNESS).tag("base_stability_plate")


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


# mk0.9.x aliases for explicit naming

def make_tpu_foot_placeholder() -> cq.Workplane:
    """Non-printed TPU foot placeholder (same geometry as make_foot)."""
    return make_wide_tpu_foot_placeholder().tag("tpu_foot_placeholder")


def make_foot_mounts_for_base_module() -> cq.Workplane:
    """Create foot socket bosses suitable for integration into the base module frame.

    This is the same geometry as base_module.make_foot_mounts; it is provided
    here so that base_module can import it when it is refactored.
    """
    mounts = None
    boss_radius = (cfg.FOOT_DIAMETER + cfg.FOOT_MOUNT_BOSS_EXTRA_DIAMETER) / 2
    x = cfg.TOWER_WIDTH / 2 - boss_radius
    y = cfg.TOWER_DEPTH / 2 - boss_radius
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        boss = cq.Workplane("XY").circle(boss_radius).extrude(cfg.FLOOR_THICKNESS).translate((px, py, 0))
        socket = cq.Workplane("XY").circle((cfg.FOOT_DIAMETER + cfg.FOOT_TPU_CLEARANCE) / 2).extrude(cfg.FLOOR_THICKNESS + cfg.FILLET_RADIUS).translate((px, py, 0))
        mount = boss.cut(socket)
        mounts = mount if mounts is None else mounts.union(mount)
    return mounts.tag("foot_mounts")
