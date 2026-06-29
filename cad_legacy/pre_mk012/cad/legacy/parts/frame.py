"""Top and bottom structural frame rings."""

import cadquery as cq

from cad import config as cfg
from cad.parts.rails import guide_rail_positions
from cad.parts.rods import rod_positions


def _add_rod_stack_seats(ring: cq.Workplane, top_nut: bool) -> cq.Workplane:
    """Cut rod clearance plus the outer nut and inner washer seats."""
    for x, y in rod_positions():
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).hole(cfg.ROD_CLEARANCE)
        ring = ring.faces("<Z").workplane().pushPoints([(x, y)]).hole(cfg.ROD_CLEARANCE)

        if top_nut:
            ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).polygon(
                cfg.M5_NUT_SIDES, cfg.M5_NUT_FLAT_DIAMETER
            ).cutBlind(-cfg.M5_NUT_SEAT_DEPTH)
            ring = ring.faces("<Z").workplane().pushPoints([(x, y)]).circle(
                cfg.M5_WASHER_DIAMETER / 2
            ).cutBlind(-cfg.M5_WASHER_SEAT_DEPTH)
        else:
            ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).circle(
                cfg.M5_WASHER_DIAMETER / 2
            ).cutBlind(-cfg.M5_WASHER_SEAT_DEPTH)
            ring = ring.faces("<Z").workplane().pushPoints([(x, y)]).polygon(
                cfg.M5_NUT_SIDES, cfg.M5_NUT_FLAT_DIAMETER
            ).cutBlind(-cfg.M5_NUT_SEAT_DEPTH)
    return ring


def create_frame_ring(
    name: str,
    z_height: float = cfg.FRAME_THICKNESS,
    top_nut: bool = False,
) -> cq.Workplane:
    """Create the top or bottom structural rectangular ring."""
    outer = cq.Workplane("XY").box(cfg.OUTER_WIDTH, cfg.OUTER_DEPTH, z_height)
    inner = cq.Workplane("XY").box(
        cfg.TOWER_WIDTH - 2 * cfg.FRAME_RAIL,
        cfg.TOWER_DEPTH - 2 * cfg.FRAME_RAIL,
        z_height + cfg.FRAME_RING_CUTTER_OVERLAP,
    )
    ring = outer.cut(inner)

    ring = _add_rod_stack_seats(ring, top_nut=top_nut)

    for x, y in guide_rail_positions():
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).rect(
            cfg.METAL_RAIL_WIDTH + cfg.METAL_RAIL_FRAME_CLEARANCE,
            cfg.METAL_RAIL_THICKNESS + cfg.METAL_RAIL_FRAME_CLEARANCE,
        ).cutBlind(-z_height)
        ring = ring.faces(">Z").workplane().pushPoints(
            [(x, y + cfg.RAIL_END_MOUNT_FRAME_SCREW_OFFSET_Y)]
        ).hole(cfg.M3_CLEARANCE)

    rib_z = z_height / 2 + cfg.FRAME_RIB_HEIGHT / 2
    rib_span_x = cfg.OUTER_WIDTH - 2 * cfg.FRAME_RIB_INSET
    rib_span_y = cfg.OUTER_DEPTH - 2 * cfg.FRAME_RIB_INSET
    for y in (-cfg.OUTER_DEPTH / 2 + cfg.FRAME_RAIL / 2, cfg.OUTER_DEPTH / 2 - cfg.FRAME_RAIL / 2):
        ring = ring.union(cq.Workplane("XY").box(rib_span_x, cfg.FRAME_RIB_WIDTH, cfg.FRAME_RIB_HEIGHT).translate((0, y, rib_z)))
    for x in (-cfg.OUTER_WIDTH / 2 + cfg.FRAME_RAIL / 2, cfg.OUTER_WIDTH / 2 - cfg.FRAME_RAIL / 2):
        ring = ring.union(cq.Workplane("XY").box(cfg.FRAME_RIB_WIDTH, rib_span_y, cfg.FRAME_RIB_HEIGHT).translate((x, 0, rib_z)))

    return ring.edges("|Z").chamfer(cfg.FRAME_EDGE_CHAMFER).tag(name)


def make_top_structural_frame() -> cq.Workplane:
    return create_frame_ring("frame_top", top_nut=True)


def make_bottom_structural_frame() -> cq.Workplane:
    return create_frame_ring("frame_bottom")


def create_frame_top() -> cq.Workplane:
    return make_top_structural_frame()


def create_frame_bottom() -> cq.Workplane:
    return make_bottom_structural_frame()
