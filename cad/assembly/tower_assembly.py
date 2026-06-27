"""Complete tower assembly placement."""

import cadquery as cq

from .. import config as cfg
from ..parts import cooling, modules, service_spine, side_panels
from ..parts.corner_blocks import create_corner_block
from ..parts.frame import create_frame_bottom, create_frame_top
from ..parts.rails import create_metal_guide_rail, guide_rail_positions
from ..parts.rods import create_m5_threaded_rod, rod_positions


def _add_corner_blocks(assembly: cq.Assembly) -> None:
    x = cfg.OUTER_WIDTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    y = cfg.OUTER_DEPTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    z = cfg.TOWER_HEIGHT / 2
    for ix, px in enumerate([-x, x]):
        for iy, py in enumerate([-y, y]):
            assembly.add(create_corner_block(), name=f"corner_block_{ix}_{iy}", loc=cq.Location(cq.Vector(px, py, z)))


def _add_rods(assembly: cq.Assembly) -> None:
    rod_z = -cfg.ROD_LENGTH / 2 + cfg.TOWER_HEIGHT / 2
    names = ["front_left", "front_right", "rear_right", "rear_left"]
    for index, (px, py) in enumerate(rod_positions()):
        assembly.add(
            create_m5_threaded_rod(),
            name=f"m5_threaded_rod_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, rod_z)),
        )


def _add_guide_rails(assembly: cq.Assembly) -> None:
    names = ["front_left", "front_right", "rear_left", "rear_right"]
    for index, (px, py) in enumerate(guide_rail_positions()):
        assembly.add(
            create_metal_guide_rail(),
            name=f"metal_guide_rail_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, cfg.TOWER_HEIGHT / 2)),
        )


def _add_module_stack(assembly: cq.Assembly) -> None:
    current_z = cfg.STACK_START_Z
    for name, units in cfg.TRAY_STACK:
        tray = modules.TRAY_FACTORIES[name]()
        assembly.add(tray, name=name, loc=cq.Location(cq.Vector(cfg.TRAY_X, cfg.TRAY_Y, current_z)))
        current_z += units * cfg.UNIT_HEIGHT


def _add_side_panels(assembly: cq.Assembly) -> None:
    side_x = cfg.OUTER_WIDTH / 2 + cfg.SIDE_PANEL_THICKNESS / 2
    assembly.add(
        side_panels.create_left_side_panel(),
        name="left_side_panel",
        loc=cq.Location(
            cq.Vector(-side_x, 0, cfg.TOWER_HEIGHT / 2),
            cq.Vector(0, 0, 1),
            cfg.SIDE_PANEL_ASSEMBLY_ROTATION_DEG,
        ),
    )
    assembly.add(
        side_panels.create_right_side_panel(),
        name="right_side_panel",
        loc=cq.Location(
            cq.Vector(side_x, 0, cfg.TOWER_HEIGHT / 2),
            cq.Vector(0, 0, 1),
            cfg.SIDE_PANEL_ASSEMBLY_ROTATION_DEG,
        ),
    )


def _add_rear_service_area(assembly: cq.Assembly) -> None:
    rear_y = cfg.OUTER_DEPTH / 2 - cfg.REAR_SPINE_DEPTH / 2
    assembly.add(
        service_spine.create_rear_service_spine(),
        name="rear_service_spine",
        loc=cq.Location(cq.Vector(0, rear_y, cfg.TOWER_HEIGHT / 2)),
    )
    assembly.add(
        service_spine.create_power_bus_panel(),
        name="power_bus_panel",
        loc=cq.Location(cq.Vector(0, rear_y - cfg.POWER_BUS_PANEL_OFFSET_Y, cfg.TOWER_HEIGHT / 2)),
    )


def _mini_pc_duct_z() -> float:
    lower_stack_height = sum(units for _, units in cfg.TRAY_STACK[:-1]) * cfg.UNIT_HEIGHT
    return cfg.STACK_START_Z + lower_stack_height + cfg.DUCT_HEIGHT / 2


def build_assembly() -> cq.Assembly:
    assembly = cq.Assembly(name="homelab_modular_tower_v1")

    assembly.add(create_frame_bottom(), name="frame_bottom", loc=cq.Location(cq.Vector(0, 0, 0)))
    assembly.add(create_frame_top(), name="frame_top", loc=cq.Location(cq.Vector(0, 0, cfg.TOWER_HEIGHT)))
    _add_corner_blocks(assembly)
    _add_rods(assembly)
    _add_guide_rails(assembly)
    _add_module_stack(assembly)
    _add_side_panels(assembly)
    _add_rear_service_area(assembly)

    assembly.add(cooling.create_bottom_fan_panel(), name="bottom_fan_panel", loc=cq.Location(cq.Vector(0, 0, cfg.BOTTOM_FAN_PANEL_Z)))
    assembly.add(
        cooling.create_top_fan_panel(),
        name="top_fan_panel",
        loc=cq.Location(cq.Vector(0, 0, cfg.TOWER_HEIGHT + cfg.TOP_FAN_PANEL_Z_OFFSET)),
    )
    assembly.add(
        cooling.create_mini_pc_airflow_duct(),
        name="mini_pc_airflow_duct",
        loc=cq.Location(cq.Vector(cfg.MINI_PC_DUCT_ASSEMBLY_X, cfg.MINI_PC_DUCT_ASSEMBLY_Y, _mini_pc_duct_z())),
    )

    return assembly
