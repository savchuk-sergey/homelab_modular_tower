"""mk0.9 temporary Mini PC placeholder module for pre-measurement layout."""

import cadquery as cq

from .. import config as cfg
from . import module_interface, placeholders


def make_mini_pc_placeholder(c=cfg) -> cq.Workplane:
    return placeholders.make_mini_pc_placeholder().tag("mini_pc_placeholder")


def make_mini_pc_placeholder_tray(c=cfg) -> cq.Workplane:
    tray = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.FLOOR_THICKNESS)
    airflow = cq.Workplane("XY").box(c.AIRFLOW_CHANNEL_WIDTH, c.AIRFLOW_CHANNEL_DEPTH, c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(c.REAR_CABLE_EXIT_WIDTH, c.REAR_RESERVED_DEPTH + c.FILLET_RADIUS, c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    pad = cq.Workplane("XY").box(
        c.MINI_PC_PLACEHOLDER_WIDTH + 2 * c.MINI_PC_PLACEHOLDER_CLEARANCE,
        c.MINI_PC_PLACEHOLDER_DEPTH + 2 * c.MINI_PC_PLACEHOLDER_CLEARANCE,
        c.FLOOR_THICKNESS,
    )
    pad = pad.faces(">Z").workplane().rect(c.AIRFLOW_CHANNEL_WIDTH * 0.55, c.AIRFLOW_CHANNEL_DEPTH * 0.65).cutThruAll()
    return tray.cut(airflow).cut(rear).union(pad).tag("mini_pc_placeholder_tray")


def make_mini_pc_placeholder_airflow_guide(c=cfg) -> cq.Workplane:
    guide = None
    x = c.MINI_PC_PLACEHOLDER_WIDTH / 2 + c.MINI_PC_PLACEHOLDER_CLEARANCE + c.RIB_THICKNESS
    for px in (-x, x):
        rail = (
            cq.Workplane("XY")
            .box(c.RIB_THICKNESS, c.MINI_PC_PLACEHOLDER_DEPTH, c.MINI_PC_AIR_GUIDE_HEIGHT)
            .translate((px, -c.REAR_RESERVED_DEPTH / 2, c.MINI_PC_AIR_GUIDE_HEIGHT / 2))
        )
        guide = rail if guide is None else guide.union(rail)
    return guide.tag("mini_pc_placeholder_airflow_guide")


def make_mini_pc_placeholder_retainer(c=cfg) -> cq.Workplane:
    retainer = None
    center_y = -c.REAR_RESERVED_DEPTH / 2
    front = center_y - c.MINI_PC_PLACEHOLDER_DEPTH / 2 - c.MINI_PC_PLACEHOLDER_CLEARANCE
    rear = center_y + c.MINI_PC_PLACEHOLDER_DEPTH / 2 + c.MINI_PC_PLACEHOLDER_CLEARANCE
    for py in (front, rear):
        rail = (
            cq.Workplane("XY")
            .box(c.MINI_PC_PLACEHOLDER_WIDTH * 0.72, c.SSD_RETAINER_THICKNESS, c.MINI_PC_RETAINER_HEIGHT)
            .translate((0, py, c.MINI_PC_RETAINER_HEIGHT / 2))
        )
        retainer = rail if retainer is None else retainer.union(rail)
    return retainer.tag("mini_pc_placeholder_retainer")


def make_mini_pc_placeholder_module_shell(c=cfg) -> cq.Workplane:
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    inner = cq.Workplane("XY").box(c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL, c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL, c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL, c.REAR_RESERVED_DEPTH - c.MODULE_FRAME_RAIL, c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    ring = ring.cut(inner).cut(rear)
    shell = ring.translate((0, 0, -c.MINI_PC_MODULE_HEIGHT / 2 + c.MODULE_INTERFACE_HEIGHT / 2)).union(
        ring.translate((0, 0, c.MINI_PC_MODULE_HEIGHT / 2 - c.MODULE_INTERFACE_HEIGHT / 2))
    )
    post_size = c.CORNER_POST_SIZE
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        shell = shell.union(cq.Workplane("XY").box(post_size, post_size, c.MINI_PC_MODULE_HEIGHT).translate((px, py, 0)))
    return shell.tag("mini_pc_placeholder_module_shell")


def make_mini_pc_placeholder_module(c=cfg) -> cq.Workplane:
    module = make_mini_pc_placeholder_module_shell(c)
    deck_z = -c.MINI_PC_MODULE_HEIGHT / 2 + c.FLOOR_THICKNESS / 2
    module = module.union(make_mini_pc_placeholder_tray(c).translate((0, 0, deck_z)))
    module = module.union(make_mini_pc_placeholder_airflow_guide(c).translate((0, 0, deck_z + c.FLOOR_THICKNESS / 2)))
    module = module.union(make_mini_pc_placeholder_retainer(c).translate((0, 0, deck_z + c.FLOOR_THICKNESS / 2)))
    return module_interface.apply_module_interface_features(module, c, top=True, bottom=True).tag("mini_pc_placeholder_module")
