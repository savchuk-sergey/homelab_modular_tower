"""mk0.11.2 base pedestal — lower structural cap for stack-through-rod tower.

Minimal lower cap that captures the bottom of the M5 rod stack and provides
a compression surface for the first stack module.  Includes concept clearance
for bottom airflow intake without final fan/filter geometry.
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


def _make_bottom_compression_surface(c=cfg) -> cq.Workplane:
    """Thin peripheral rim for bottom stack compression — open center for intake."""
    rim = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.FLOOR_THICKNESS)
    intake = (
        cq.Workplane("XY")
        .box(
            c.AIRFLOW_CHANNEL_WIDTH,
            c.AIRFLOW_CHANNEL_DEPTH,
            c.FLOOR_THICKNESS + c.FILLET_RADIUS,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    )
    return rim.cut(intake)


def _apply_compression_pads(part: cq.Workplane, c=cfg) -> cq.Workplane:
    pad_radius = c.STACK_MODULE_COMPRESSION_PAD_DIAMETER / 2
    pad_depth = c.STACK_MODULE_COMPRESSION_PAD_DEPTH
    for x, y in _corner_rod_points(c):
        part = part.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(x, y).circle(pad_radius).cutBlind(
            -pad_depth
        )
    return part


def make_base_pedestal(c=cfg) -> cq.Workplane:
    """Lower structural cap for the mk0.11.2 stack prototype."""
    height = c.BASE_PEDESTAL_HEIGHT

    bottom_ring = _make_frame_ring(c).translate(
        (0, 0, -height / 2 + c.MODULE_INTERFACE_HEIGHT / 2)
    )
    top_ring = _make_frame_ring(c).translate(
        (0, 0, height / 2 - c.MODULE_INTERFACE_HEIGHT / 2)
    )
    pedestal = bottom_ring.union(top_ring)

    post_size = c.CORNER_POST_SIZE
    for px, py in _corner_rod_points(c):
        post = cq.Workplane("XY").box(post_size, post_size, height).translate((px, py, 0))
        pedestal = pedestal.union(post)

    z_bottom_rim = -height / 2 - c.FLOOR_THICKNESS / 2
    pedestal = pedestal.union(_make_bottom_compression_surface(c).translate((0, 0, z_bottom_rim)))

    clearance = (
        cq.Workplane("XY")
        .box(
            c.AIRFLOW_CHANNEL_WIDTH + c.BASE_PEDESTAL_AIRFLOW_CLEARANCE,
            c.AIRFLOW_CHANNEL_DEPTH + c.BASE_PEDESTAL_AIRFLOW_CLEARANCE,
            c.BASE_PEDESTAL_AIRFLOW_CLEARANCE,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, -height / 2 - c.FLOOR_THICKNESS - c.BASE_PEDESTAL_AIRFLOW_CLEARANCE / 2))
    )
    pedestal = pedestal.cut(clearance)

    pedestal = _apply_compression_pads(pedestal, c)
    # top=False: front alignment pin positions (±57, −61) fall inside the
    # airflow channel where the ring has no solid material.  M5 rod posts
    # provide full column alignment for the mk0.11.2 prototype.
    pedestal = module_interface.apply_module_interface_features(pedestal, c, top=False, bottom=False)
    return pedestal.tag("base_pedestal")
