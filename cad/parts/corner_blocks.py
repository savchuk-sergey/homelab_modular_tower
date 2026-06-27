"""Corner compression blocks for the M5 rod load path."""

import cadquery as cq

from .. import config as cfg
from .rods import rod_positions


def create_corner_block() -> cq.Workplane:
    """Corner compression block for one M5 rod and panel screws."""
    block = (
        cq.Workplane("XY")
        .box(cfg.CORNER_BLOCK_SIZE, cfg.CORNER_BLOCK_SIZE, cfg.CORNER_BLOCK_HEIGHT)
        .edges("|Z")
        .chamfer(cfg.CORNER_BLOCK_EDGE_CHAMFER)
    )
    block = block.faces(">Z").workplane().hole(cfg.ROD_CLEARANCE)
    block = block.faces(">Z").workplane().circle(cfg.M5_WASHER_DIAMETER / 2).cutBlind(-cfg.M5_WASHER_SEAT_DEPTH)
    block = block.faces("<Z").workplane().polygon(cfg.M5_NUT_SIDES, cfg.M5_NUT_FLAT_DIAMETER).cutBlind(
        -cfg.M5_NUT_SEAT_DEPTH
    )

    # These service holes are through-holes so side panels can be removed without disturbing the rod stack.
    block = block.faces(">X").workplane().pushPoints(cfg.CORNER_BLOCK_PANEL_HOLE_POINTS).hole(cfg.M3_CLEARANCE)
    block = block.faces(">Y").workplane().pushPoints(cfg.CORNER_BLOCK_PANEL_HOLE_POINTS).hole(cfg.M3_CLEARANCE)
    return block


def create_corner_blocks_in_place() -> cq.Assembly:
    assembly = cq.Assembly(name="corner_blocks")
    x = cfg.OUTER_WIDTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    y = cfg.OUTER_DEPTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    z = cfg.TOWER_HEIGHT / 2
    for ix, px in enumerate([-x, x]):
        for iy, py in enumerate([-y, y]):
            assembly.add(create_corner_block(), name=f"corner_block_{ix}_{iy}", loc=cq.Location(cq.Vector(px, py, z)))
    return assembly
