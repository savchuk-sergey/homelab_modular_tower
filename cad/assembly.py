"""Assembly for Homelab Modular Tower v1."""

import cadquery as cq

from . import airflow, config as cfg, frame, panels, power_bus, trays


def build_assembly() -> cq.Assembly:
    assembly = cq.Assembly(name="homelab_modular_tower_v1")

    assembly.add(frame.create_frame_bottom(), name="frame_bottom", loc=cq.Location(cq.Vector(0, 0, 0)))
    assembly.add(frame.create_frame_top(), name="frame_top", loc=cq.Location(cq.Vector(0, 0, cfg.TOWER_HEIGHT)))

    x = cfg.OUTER_WIDTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    y = cfg.OUTER_DEPTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    z = cfg.TOWER_HEIGHT / 2
    for ix, px in enumerate([-x, x]):
        for iy, py in enumerate([-y, y]):
            assembly.add(frame.create_corner_block(), name=f"corner_block_{ix}_{iy}", loc=cq.Location(cq.Vector(px, py, z)))

    rod_z = -cfg.ROD_LENGTH / 2 + cfg.TOWER_HEIGHT / 2
    for index, (px, py) in enumerate(frame.rod_positions()):
        names = ["front_left", "front_right", "rear_right", "rear_left"]
        assembly.add(
            frame.create_m5_threaded_rod(),
            name=f"m5_threaded_rod_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, rod_z)),
        )

    for index, (px, py) in enumerate(frame.guide_rail_positions()):
        names = ["front_left", "front_right", "rear_left", "rear_right"]
        assembly.add(
            frame.create_metal_guide_rail(),
            name=f"metal_guide_rail_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, cfg.TOWER_HEIGHT / 2)),
        )

    current_z = cfg.STACK_START_Z
    for name, units in cfg.TRAY_STACK:
        tray = trays.TRAY_FACTORIES[name]()
        assembly.add(tray, name=name, loc=cq.Location(cq.Vector(cfg.TRAY_X, cfg.TRAY_Y, current_z)))
        current_z += units * cfg.UNIT_HEIGHT

    side_x = cfg.OUTER_WIDTH / 2 + cfg.PANEL_THICKNESS / 2
    assembly.add(
        panels.create_left_side_panel(),
        name="left_side_panel",
        loc=cq.Location(cq.Vector(-side_x, 0, cfg.TOWER_HEIGHT / 2), cq.Vector(0, 0, 1), 90),
    )
    assembly.add(
        panels.create_right_side_panel(),
        name="right_side_panel",
        loc=cq.Location(cq.Vector(side_x, 0, cfg.TOWER_HEIGHT / 2), cq.Vector(0, 0, 1), 90),
    )

    rear_y = cfg.OUTER_DEPTH / 2 - cfg.REAR_SPINE_DEPTH / 2
    assembly.add(power_bus.create_rear_service_spine(), name="rear_service_spine", loc=cq.Location(cq.Vector(0, rear_y, cfg.TOWER_HEIGHT / 2)))
    assembly.add(
        power_bus.create_power_bus_panel(),
        name="power_bus_panel",
        loc=cq.Location(cq.Vector(0, rear_y - 10.0, cfg.TOWER_HEIGHT / 2)),
    )

    assembly.add(panels.create_bottom_fan_panel(), name="bottom_fan_panel", loc=cq.Location(cq.Vector(0, 0, -8.0)))
    assembly.add(panels.create_top_fan_panel(), name="top_fan_panel", loc=cq.Location(cq.Vector(0, 0, cfg.TOWER_HEIGHT + 8.0)))

    duct_z = cfg.STACK_START_Z + sum(units for _, units in cfg.TRAY_STACK[:-1]) * cfg.UNIT_HEIGHT + cfg.DUCT_HEIGHT / 2
    assembly.add(
        airflow.create_mini_pc_airflow_duct(),
        name="mini_pc_airflow_duct",
        loc=cq.Location(cq.Vector(48.0, 6.0, duct_z)),
    )

    return assembly
