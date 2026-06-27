"""Frame and corner block parts."""

import cadquery as cq

from . import config as cfg


def _rod_positions():
    x = cfg.TOWER_WIDTH / 2 - cfg.ROD_CENTER_OFFSET
    y = cfg.TOWER_DEPTH / 2 - cfg.ROD_CENTER_OFFSET
    return [(-x, -y), (x, -y), (x, y), (-x, y)]


def rod_positions():
    return _rod_positions()


def guide_rail_positions():
    x = cfg.METAL_RAIL_X_OFFSET
    return [
        (-x, cfg.METAL_RAIL_Y_FRONT),
        (x, cfg.METAL_RAIL_Y_FRONT),
        (-x, cfg.METAL_RAIL_Y_REAR),
        (x, cfg.METAL_RAIL_Y_REAR),
    ]


def create_frame_ring(name: str, z_height: float = cfg.FRAME_THICKNESS) -> cq.Workplane:
    """Create the top or bottom structural rectangular ring."""
    outer = cq.Workplane("XY").box(cfg.OUTER_WIDTH, cfg.OUTER_DEPTH, z_height)
    inner = (
        cq.Workplane("XY")
        .box(cfg.TOWER_WIDTH - 2 * cfg.FRAME_RAIL, cfg.TOWER_DEPTH - 2 * cfg.FRAME_RAIL, z_height + 2)
    )
    ring = outer.cut(inner)

    for x, y in _rod_positions():
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).hole(cfg.ROD_CLEARANCE)
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).circle(cfg.M5_WASHER_DIAMETER / 2).cutBlind(
            -cfg.M5_WASHER_SEAT_DEPTH
        )
        ring = ring.faces("<Z").workplane().pushPoints([(x, y)]).polygon(6, cfg.M5_NUT_FLAT_DIAMETER).cutBlind(
            -cfg.M5_NUT_SEAT_DEPTH
        )

    for x, y in guide_rail_positions():
        ring = ring.faces(">Z").workplane().pushPoints([(x, y)]).rect(
            cfg.METAL_RAIL_WIDTH + 1.0, cfg.METAL_RAIL_THICKNESS + 1.0
        ).cutBlind(-z_height)

    # Light chamfers reduce sharp PETG edges without weakening the rod seats.
    return ring.edges("|Z").chamfer(1.0).tag(name)


def create_frame_top() -> cq.Workplane:
    return create_frame_ring("frame_top")


def create_frame_bottom() -> cq.Workplane:
    return create_frame_ring("frame_bottom")


def create_corner_block() -> cq.Workplane:
    """Corner compression block for one M5 rod and panel screws."""
    block = (
        cq.Workplane("XY")
        .box(cfg.CORNER_BLOCK_SIZE, cfg.CORNER_BLOCK_SIZE, cfg.CORNER_BLOCK_HEIGHT)
        .edges("|Z")
        .chamfer(1.0)
    )
    block = block.faces(">Z").workplane().hole(cfg.ROD_CLEARANCE)
    block = block.faces(">Z").workplane().circle(cfg.M5_WASHER_DIAMETER / 2).cutBlind(-cfg.M5_WASHER_SEAT_DEPTH)
    block = block.faces("<Z").workplane().polygon(6, cfg.M5_NUT_FLAT_DIAMETER).cutBlind(-cfg.M5_NUT_SEAT_DEPTH)

    # Side panel holes are intentionally through-holes for M3/M4 service screws.
    block = block.faces(">X").workplane().pushPoints([(0, -6), (0, 6)]).hole(cfg.M3_CLEARANCE)
    block = block.faces(">Y").workplane().pushPoints([(0, -6), (0, 6)]).hole(cfg.M3_CLEARANCE)
    return block


def create_m5_threaded_rod(height: float = cfg.ROD_LENGTH) -> cq.Workplane:
    """Placeholder for a vertical metal M5 threaded rod."""
    return cq.Workplane("XY").circle(cfg.ROD_DIAMETER / 2).extrude(height)


def create_metal_guide_rail(height: float = cfg.METAL_RAIL_HEIGHT) -> cq.Workplane:
    """Placeholder 10 x 3 mm steel/aluminium tray rail with M3 fixing holes."""
    rail = cq.Workplane("XY").box(cfg.METAL_RAIL_WIDTH, cfg.METAL_RAIL_THICKNESS, height)
    z_values = []
    z = -height / 2 + cfg.METAL_RAIL_M3_SPACING / 2
    while z < height / 2:
        z_values.append(z)
        z += cfg.METAL_RAIL_M3_SPACING
    for z in z_values:
        rail = rail.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).hole(cfg.M3_CLEARANCE)
    return rail


def create_corner_blocks_in_place() -> cq.Assembly:
    assembly = cq.Assembly(name="corner_blocks")
    x = cfg.OUTER_WIDTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    y = cfg.OUTER_DEPTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    z = cfg.TOWER_HEIGHT / 2
    for ix, px in enumerate([-x, x]):
        for iy, py in enumerate([-y, y]):
            assembly.add(create_corner_block(), name=f"corner_block_{ix}_{iy}", loc=cq.Location(cq.Vector(px, py, z)))
    return assembly
