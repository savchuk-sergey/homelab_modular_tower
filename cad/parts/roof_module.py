"""mk0.9 Roof Module with upper exhaust fan, guard and top tie frame."""

import cadquery as cq

from .. import config as cfg
from . import module_interface


def make_roof_frame(c=cfg) -> cq.Workplane:
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    inner = cq.Workplane("XY").box(c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL, c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL, c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL, c.REAR_RESERVED_DEPTH - c.MODULE_FRAME_RAIL, c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    ring = ring.cut(inner).cut(rear)
    frame = ring.translate((0, 0, -c.ROOF_MODULE_HEIGHT / 2 + c.MODULE_INTERFACE_HEIGHT / 2)).union(
        ring.translate((0, 0, c.ROOF_MODULE_HEIGHT / 2 - c.MODULE_INTERFACE_HEIGHT / 2))
    )
    post_size = c.CORNER_POST_SIZE
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        frame = frame.union(cq.Workplane("XY").box(post_size, post_size, c.ROOF_MODULE_HEIGHT).translate((px, py, 0)))
    return frame.tag("roof_frame")


def make_top_fan_mount(c=cfg) -> cq.Workplane:
    plate = cq.Workplane("XY").box(c.FAN_120_SIZE + 22.0, c.FAN_120_SIZE + 22.0, c.FLOOR_THICKNESS)
    plate = plate.faces(">Z").workplane().circle(c.FAN_120_SIZE / 2).cutThruAll()
    d = c.FAN_120_HOLE_SPACING / 2
    return plate.faces(">Z").workplane().pushPoints([(x, y) for x in (-d, d) for y in (-d, d)]).hole(c.FAN_SCREW_CLEARANCE).tag("top_fan_mount")


def make_top_grill(c=cfg) -> cq.Workplane:
    grill = cq.Workplane("XY").box(c.FAN_120_SIZE + 18.0, c.FAN_120_SIZE + 18.0, c.TOP_GUARD_FRAME_HEIGHT)
    grill = grill.faces(">Z").workplane().circle(c.FAN_120_SIZE / 2).cutThruAll()
    for offset in c.FAN_GRILLE_BAR_X:
        grill = grill.union(cq.Workplane("XY").box(c.RIB_THICKNESS, c.FAN_120_SIZE - c.FAN_GRILLE_BAR_LENGTH_INSET, c.TOP_GUARD_FRAME_HEIGHT).translate((offset, 0, 0)))
        grill = grill.union(cq.Workplane("XY").box(c.FAN_120_SIZE - c.FAN_GRILLE_BAR_LENGTH_INSET, c.RIB_THICKNESS, c.TOP_GUARD_FRAME_HEIGHT).translate((0, offset, 0)))
    return grill.tag("top_grill")


def make_top_filter_slot(c=cfg) -> cq.Workplane:
    slot = cq.Workplane("XY").box(c.FAN_120_SIZE + 22.0, c.FAN_120_SIZE + 22.0, c.FILTER_SLOT_HEIGHT)
    window = cq.Workplane("XY").box(c.FAN_120_SIZE, c.FAN_120_SIZE, c.FILTER_SLOT_HEIGHT + c.FILLET_RADIUS)
    return slot.cut(window).tag("top_filter_slot")


def make_fan_shroud(c=cfg) -> cq.Workplane:
    shroud = None
    length = c.FAN_120_SIZE + c.MODULE_FRAME_RAIL
    offset = c.FAN_120_SIZE / 2 + c.FAN_SHROUD_WALL / 2
    for y in (-offset, offset):
        rail = cq.Workplane("XY").box(length, c.FAN_SHROUD_WALL, c.FAN_SHROUD_HEIGHT).translate((0, y, c.FAN_SHROUD_HEIGHT / 2))
        shroud = rail if shroud is None else shroud.union(rail)
    for x in (-offset, offset):
        rail = cq.Workplane("XY").box(c.FAN_SHROUD_WALL, length, c.FAN_SHROUD_HEIGHT).translate((x, 0, c.FAN_SHROUD_HEIGHT / 2))
        shroud = shroud.union(rail)
    return shroud.tag("fan_shroud")


def make_roof_module(c=cfg) -> cq.Workplane:
    module = make_roof_frame(c)
    deck_z = -c.ROOF_MODULE_HEIGHT / 2 + c.FLOOR_THICKNESS / 2
    fan_y = -c.REAR_RESERVED_DEPTH / 2
    module = module.union(make_top_fan_mount(c).translate((0, fan_y, deck_z)))
    module = module.union(make_top_filter_slot(c).translate((0, fan_y, deck_z + c.FLOOR_THICKNESS)))
    module = module.union(make_top_grill(c).translate((0, fan_y, c.ROOF_MODULE_HEIGHT / 2 + c.TOP_GUARD_FRAME_HEIGHT / 2)))
    module = module.union(make_fan_shroud(c).translate((0, fan_y, deck_z + c.FLOOR_THICKNESS / 2)))
    return module_interface.apply_module_interface_features(module, c, top=False, bottom=True).tag("roof_module")
