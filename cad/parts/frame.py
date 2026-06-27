"""Top and bottom structural frame rings."""

import cadquery as cq

from .. import config as cfg
from .rails import guide_rail_positions
from .rods import rod_positions


def create_frame_ring(name: str, z_height: float = cfg.FRAME_THICKNESS) -> cq.Workplane:
    """Create the top or bottom structural rectangular ring."""
    outer = cq.Workplane("XY").box(cfg.OUTER_WIDTH, cfg.OUTER_DEPTH, z_height)
    inner = cq.Workplane("XY").box(
        cfg.TOWER_WIDTH - 2 * cfg.FRAME_RAIL,
        cfg.TOWER_DEPTH - 2 * cfg.FRAME_RAIL,
        z_height + cfg.FRAME_RING_CUTTER_OVERLAP,
    )
    ring = outer.cut(inner)

    for x, y in rod_positions():
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).hole(cfg.ROD_CLEARANCE)
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).circle(
            cfg.M5_WASHER_DIAMETER / 2
        ).cutBlind(-cfg.M5_WASHER_SEAT_DEPTH)
        ring = ring.faces("<Z").workplane().pushPoints([(x, y)]).polygon(
            cfg.M5_NUT_SIDES, cfg.M5_NUT_FLAT_DIAMETER
        ).cutBlind(-cfg.M5_NUT_SEAT_DEPTH)

    for x, y in guide_rail_positions():
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).rect(
            cfg.METAL_RAIL_WIDTH + cfg.METAL_RAIL_FRAME_CLEARANCE,
            cfg.METAL_RAIL_THICKNESS + cfg.METAL_RAIL_FRAME_CLEARANCE,
        ).cutBlind(-z_height)

    return ring.edges("|Z").chamfer(cfg.FRAME_EDGE_CHAMFER).tag(name)


def create_frame_top() -> cq.Workplane:
    return create_frame_ring("frame_top")


def create_frame_bottom() -> cq.Workplane:
    return create_frame_ring("frame_bottom")
