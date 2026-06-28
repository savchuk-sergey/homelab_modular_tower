"""mk0.11.2 top cap — upper structural cap for stack-through-rod tower.

Minimal upper cap that captures the top of the M5 rod stack and provides
a compression surface for the uppermost stack module.  Includes concept
clearance for future exhaust airflow without final fan geometry.
"""

import cadquery as cq

from .. import config as cfg
from . import module_interface


def _corner_rod_points(c=cfg) -> list[tuple[float, float]]:
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    return [(-x, -y), (x, -y), (x, y), (-x, y)]


def _make_frame_ring(c=cfg) -> cq.Workplane:
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    inner = (
        cq.Workplane("XY")
        .box(
            c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
            c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL,
            c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    )
    rear = (
        cq.Workplane("XY")
        .box(
            c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
            c.REAR_RESERVED_DEPTH - c.MODULE_FRAME_RAIL,
            c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
        )
        .translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    )
    return ring.cut(inner).cut(rear)


def _make_top_compression_surface(c=cfg) -> cq.Workplane:
    """Thin peripheral rim for top stack compression — open center for exhaust."""
    rim = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.FLOOR_THICKNESS)
    exhaust = (
        cq.Workplane("XY")
        .box(
            c.AIRFLOW_CHANNEL_WIDTH,
            c.AIRFLOW_CHANNEL_DEPTH,
            c.FLOOR_THICKNESS + c.FILLET_RADIUS,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    )
    return rim.cut(exhaust)


def _apply_compression_pads(part: cq.Workplane, c=cfg) -> cq.Workplane:
    pad_radius = c.STACK_MODULE_COMPRESSION_PAD_DIAMETER / 2
    pad_depth = c.STACK_MODULE_COMPRESSION_PAD_DEPTH
    for x, y in _corner_rod_points(c):
        part = part.faces("<Z").workplane(centerOption="CenterOfBoundBox").center(x, y).circle(pad_radius).cutBlind(
            -pad_depth
        )
    return part


def make_top_cap(c=cfg) -> cq.Workplane:
    """Upper structural cap for the mk0.11.2 stack prototype."""
    height = c.TOP_CAP_HEIGHT

    bottom_ring = _make_frame_ring(c).translate(
        (0, 0, -height / 2 + c.MODULE_INTERFACE_HEIGHT / 2)
    )
    top_ring = _make_frame_ring(c).translate(
        (0, 0, height / 2 - c.MODULE_INTERFACE_HEIGHT / 2)
    )
    cap = bottom_ring.union(top_ring)

    post_size = c.CORNER_POST_SIZE
    for px, py in _corner_rod_points(c):
        post = cq.Workplane("XY").box(post_size, post_size, height).translate((px, py, 0))
        cap = cap.union(post)

    z_top_rim = height / 2 + c.FLOOR_THICKNESS / 2
    cap = cap.union(_make_top_compression_surface(c).translate((0, 0, z_top_rim)))

    clearance = (
        cq.Workplane("XY")
        .box(
            c.AIRFLOW_CHANNEL_WIDTH + c.TOP_CAP_AIRFLOW_CLEARANCE,
            c.AIRFLOW_CHANNEL_DEPTH + c.TOP_CAP_AIRFLOW_CLEARANCE,
            c.TOP_CAP_AIRFLOW_CLEARANCE,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, height / 2 + c.FLOOR_THICKNESS + c.TOP_CAP_AIRFLOW_CLEARANCE / 2))
    )
    cap = cap.cut(clearance)

    cap = _apply_compression_pads(cap, c)
    cap = module_interface.apply_module_interface_features(cap, c, top=False, bottom=True)
    return cap.tag("top_cap")
