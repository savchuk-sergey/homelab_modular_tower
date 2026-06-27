"""Complete tower assembly placement."""

import cadquery as cq

from .. import config as cfg
from ..parts import cooling, feet, modules, placeholders, service_spine, side_panels
from ..parts.corner_blocks import create_corner_block
from ..parts.frame import make_bottom_structural_frame, make_top_structural_frame
from ..parts.rails import create_metal_guide_rail, create_rail_end_mount, create_tray_support_ledge, guide_rail_positions
from ..parts.rods import create_m5_threaded_rod, create_m5_threaded_rod_cap, rod_positions


def _add_corner_blocks(assembly: cq.Assembly) -> None:
    x = cfg.OUTER_WIDTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    y = cfg.OUTER_DEPTH / 2 - cfg.CORNER_BLOCK_SIZE / 2
    z_positions = (
        cfg.BOTTOM_CORNER_BLOCK_Z,
        cfg.TOP_CORNER_BLOCK_Z,
    )
    for iz, pz in enumerate(z_positions):
        for ix, px in enumerate([-x, x]):
            for iy, py in enumerate([-y, y]):
                assembly.add(
                    create_corner_block(),
                    name=f"corner_block_{iz}_{ix}_{iy}",
                    loc=cq.Location(cq.Vector(px, py, pz)),
                )


def _add_rods(assembly: cq.Assembly) -> None:
    names = ["front_left", "front_right", "rear_right", "rear_left"]
    for index, (px, py) in enumerate(rod_positions()):
        assembly.add(
            create_m5_threaded_rod(),
            name=f"m5_threaded_rod_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, 0)),
        )
        assembly.add(
            create_m5_threaded_rod_cap(),
            name=f"m5_rod_cap_top_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, cfg.ROD_LENGTH)),
        )


def _add_guide_rails(assembly: cq.Assembly) -> None:
    names = ["front_left", "front_right", "rear_left", "rear_right"]
    rail_bottom_z = (cfg.TOWER_HEIGHT - cfg.METAL_RAIL_HEIGHT) / 2
    rail_top_z = cfg.TOWER_HEIGHT - rail_bottom_z
    for index, (px, py) in enumerate(guide_rail_positions()):
        assembly.add(
            create_metal_guide_rail(),
            name=f"metal_guide_rail_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, cfg.TOWER_HEIGHT / 2)),
        )
        for z_name, pz in (
            ("bottom", rail_bottom_z + cfg.RAIL_END_MOUNT_RAIL_CAPTURE_DEPTH / 2),
            ("top", rail_top_z - cfg.RAIL_END_MOUNT_RAIL_CAPTURE_DEPTH / 2),
        ):
            assembly.add(
                create_rail_end_mount(),
                name=f"rail_end_mount_{z_name}_{names[index]}",
                loc=cq.Location(cq.Vector(px, py, pz)),
            )


def _add_tray_support_ledges(assembly: cq.Assembly) -> None:
    for tray_index, tray_bottom_z in enumerate(_tray_bottom_z_positions()):
        ledge_z = tray_bottom_z - cfg.RAIL_SUPPORT_LEDGE_HEIGHT / 2
        for rail_index, (px, py) in enumerate(guide_rail_positions()):
            assembly.add(
                create_tray_support_ledge(),
                name=f"tray_support_ledge_{tray_index}_{rail_index}",
                loc=cq.Location(cq.Vector(px, py, ledge_z)),
            )


def _add_feet(assembly: cq.Assembly) -> None:
    names = ["front_left", "front_right", "rear_right", "rear_left"]
    socket_z = cfg.BASE_STABILITY_Z - cfg.BASE_STABILITY_THICKNESS / 2 - cfg.FOOT_SOCKET_DEPTH
    for index, (px, py) in enumerate(feet.wide_foot_positions()):
        assembly.add(
            feet.make_foot_socket(),
            name=f"foot_socket_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, socket_z)),
        )
        assembly.add(
            feet.make_foot(),
            name=f"foot_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, cfg.FOOT_Z)),
        )


def _add_sectional_base(assembly: cq.Assembly) -> None:
    z = cfg.BASE_STABILITY_Z
    side_x = cfg.OUTER_WIDTH / 2 + cfg.FOOT_EXTENSION_X / 2 - cfg.BASE_WING_OVERLAP / 2
    wing_y = cfg.OUTER_DEPTH / 2 + cfg.FOOT_EXTENSION_Y / 2 - cfg.BASE_WING_OVERLAP / 2
    assembly.add(feet.make_central_bottom_fan_frame(), name="central_bottom_fan_frame", loc=cq.Location(cq.Vector(0, 0, z)))
    assembly.add(feet.make_left_foot_extension(), name="left_foot_extension", loc=cq.Location(cq.Vector(-side_x, 0, z)))
    assembly.add(feet.make_right_foot_extension(), name="right_foot_extension", loc=cq.Location(cq.Vector(side_x, 0, z)))
    assembly.add(feet.make_front_stability_wing(), name="front_stability_wing", loc=cq.Location(cq.Vector(0, -wing_y, z)))
    assembly.add(feet.make_rear_stability_wing(), name="rear_stability_wing", loc=cq.Location(cq.Vector(0, wing_y, z)))


def _add_module_stack(assembly: cq.Assembly) -> None:
    placeholder_factories = {
        "ups_power_tray": (
            placeholders.make_ups_placeholder,
            (cfg.UPS_PLACEHOLDER_LOC[0], cfg.UPS_PLACEHOLDER_LOC[1], cfg.TRAY_BASE_THICKNESS + cfg.UPS_PLACEHOLDER_HEIGHT / 2),
        ),
        "external_ssd_bay": (
            placeholders.make_external_ssd_placeholder,
            (cfg.SSD_POCKET_X, cfg.SSD_POCKET_Y, cfg.TRAY_BASE_THICKNESS + cfg.EXTERNAL_SSD_PLACEHOLDER_HEIGHT / 2),
        ),
        "ssd_expansion_tray": (
            placeholders.make_ssd_expansion_placeholder,
            (cfg.SSD_EXPANSION_PLACEHOLDER_LOC[0], cfg.SSD_EXPANSION_PLACEHOLDER_LOC[1], cfg.TRAY_BASE_THICKNESS + cfg.SSD_EXPANSION_PLACEHOLDER_HEIGHT / 2),
        ),
        "raspberry_pi_tray": (
            placeholders.make_raspberry_pi_3b_placeholder,
            (cfg.RASPBERRY_PI_PLACEHOLDER_LOC[0], cfg.RASPBERRY_PI_PLACEHOLDER_LOC[1], cfg.TRAY_BASE_THICKNESS + cfg.RPI3B_BOARD_THICKNESS / 2),
        ),
        "mikrotik_tray": (
            placeholders.make_mikrotik_placeholder,
            (cfg.MIKROTIK_PLACEHOLDER_LOC[0], cfg.MIKROTIK_PLACEHOLDER_LOC[1], cfg.TRAY_BASE_THICKNESS + cfg.MIKROTIK_PLACEHOLDER_HEIGHT / 2),
        ),
        "mini_pc_tray": (
            placeholders.make_mini_pc_placeholder,
            (cfg.MINI_PC_PLACEHOLDER_LOC[0], cfg.MINI_PC_PLACEHOLDER_LOC[1], cfg.TRAY_BASE_THICKNESS + cfg.MINI_PC_PLACEHOLDER_HEIGHT / 2),
        ),
    }
    current_z = cfg.STACK_START_Z
    for name, units in cfg.TRAY_STACK:
        tray = modules.TRAY_FACTORIES[name]()
        assembly.add(tray, name=name, loc=cq.Location(cq.Vector(cfg.TRAY_X, cfg.TRAY_Y, current_z)))
        placeholder_factory, local_offset = placeholder_factories[name]
        assembly.add(
            placeholder_factory(),
            name=f"{name}_device_placeholder",
            loc=cq.Location(
                cq.Vector(
                    cfg.TRAY_X + local_offset[0],
                    cfg.TRAY_Y + local_offset[1],
                    current_z + local_offset[2],
                )
            ),
        )
        current_z += units * cfg.UNIT_HEIGHT


def _tray_bottom_z_positions() -> tuple[float, ...]:
    z_values = []
    current_z = cfg.STACK_START_Z
    for _, units in cfg.TRAY_STACK:
        z_values.append(current_z)
        current_z += units * cfg.UNIT_HEIGHT
    return tuple(z_values)


def _mini_pc_tray_z() -> float:
    lower_stack_height = sum(units for _, units in cfg.TRAY_STACK[:-1]) * cfg.UNIT_HEIGHT
    return cfg.STACK_START_Z + lower_stack_height


def _add_side_panels(assembly: cq.Assembly) -> None:
    side_x = cfg.OUTER_WIDTH / 2 + cfg.SIDE_PANEL_THICKNESS / 2
    mount_x = cfg.OUTER_WIDTH / 2 - cfg.SIDE_PANEL_MOUNT_RAIL_WIDTH / 2 - cfg.SIDE_PANEL_MOUNT_RAIL_INSET
    mount_rail_factories = (
        side_panels.make_side_panel_mount_rail_lower,
        side_panels.make_side_panel_mount_rail_middle,
        side_panels.make_side_panel_mount_rail_upper,
    )
    for side_name, x_sign in (("left", -1), ("right", 1)):
        for rail_index, y_position in enumerate(side_panels.side_panel_mount_y_positions()):
            for section_index, factory in enumerate(mount_rail_factories):
                label = cfg.SIDE_PANEL_SECTION_LABELS[section_index]
                assembly.add(
                    factory(),
                    name=f"{side_name}_side_panel_mount_rail_{rail_index}_{label}",
                    loc=cq.Location(
                        cq.Vector(
                            x_sign * mount_x,
                            y_position,
                            side_panels.side_panel_tile_center_z(section_index),
                        )
                    ),
                )

    factories = {
        "left": (
            -side_x,
            (
                side_panels.create_left_side_panel_lower,
                side_panels.create_left_side_panel_middle,
                side_panels.create_left_side_panel_upper,
            ),
        ),
        "right": (
            side_x,
            (
                side_panels.create_right_side_panel_lower,
                side_panels.create_right_side_panel_middle,
                side_panels.create_right_side_panel_upper,
            ),
        ),
    }
    for side, (x_position, panel_factories) in factories.items():
        rotation = (
            cfg.SIDE_PANEL_ASSEMBLY_ROTATION_DEG_LEFT
            if side == "left"
            else cfg.SIDE_PANEL_ASSEMBLY_ROTATION_DEG_RIGHT
        )
        for index, factory in enumerate(panel_factories):
            label = cfg.SIDE_PANEL_SECTION_LABELS[index]
            assembly.add(
                factory(),
                name=f"{side}_side_panel_{label}",
                loc=cq.Location(
                    cq.Vector(x_position, 0, side_panels.side_panel_tile_center_z(index)),
                    cq.Vector(0, 0, 1),
                    rotation,
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
        service_spine.create_rear_service_spine_cover(),
        name="rear_service_spine_cover",
        loc=cq.Location(
            cq.Vector(
                0,
                rear_y + cfg.REAR_SPINE_DEPTH / 2 + cfg.SPINE_COVER_THICKNESS / 2,
                cfg.TOWER_HEIGHT / 2,
            )
        ),
    )
    assembly.add(
        service_spine.create_power_bus_panel(),
        name="power_bus_panel",
        loc=cq.Location(cq.Vector(0, rear_y - cfg.POWER_BUS_PANEL_OFFSET_Y, cfg.TOWER_HEIGHT / 2)),
    )
    assembly.add(
        service_spine.create_power_bus_cover(),
        name="power_bus_cover",
        loc=cq.Location(
            cq.Vector(
                0,
                rear_y - cfg.POWER_BUS_PANEL_OFFSET_Y - cfg.POWER_BUS_THICKNESS,
                cfg.TOWER_HEIGHT / 2,
            )
        ),
    )
    assembly.add(
        placeholders.make_power_bus_zone_placeholder(),
        name="power_bus_zone_placeholder",
        loc=cq.Location(cq.Vector(0, rear_y - cfg.POWER_BUS_PANEL_OFFSET_Y, cfg.TOWER_HEIGHT / 2)),
    )


def _mini_pc_duct_z() -> float:
    lower_stack_height = sum(units for _, units in cfg.TRAY_STACK[:-1]) * cfg.UNIT_HEIGHT
    return cfg.STACK_START_Z + lower_stack_height + cfg.DUCT_HEIGHT / 2


def build_assembly() -> cq.Assembly:
    assembly = cq.Assembly(name="homelab_modular_tower_v1")

    _add_sectional_base(assembly)
    assembly.add(make_bottom_structural_frame(), name="bottom_structural_frame", loc=cq.Location(cq.Vector(0, 0, 0)))
    assembly.add(make_top_structural_frame(), name="top_structural_frame", loc=cq.Location(cq.Vector(0, 0, cfg.TOWER_HEIGHT)))
    _add_corner_blocks(assembly)
    _add_rods(assembly)
    _add_guide_rails(assembly)
    _add_tray_support_ledges(assembly)
    _add_feet(assembly)
    _add_module_stack(assembly)
    assembly.add(
        modules.make_tray_stop(),
        name="mini_pc_tray_stop",
        loc=cq.Location(
            cq.Vector(
                cfg.TRAY_X + cfg.TRAY_STOP_OFFSET_X,
                cfg.TRAY_Y + cfg.TRAY_STOP_OFFSET_Y,
                _mini_pc_tray_z() + cfg.TRAY_STOP_HEIGHT / 2,
            )
        ),
    )
    _add_side_panels(assembly)
    _add_rear_service_area(assembly)

    assembly.add(
        cooling.make_bottom_fan_cartridge(),
        name="bottom_fan_cartridge",
        loc=cq.Location(cq.Vector(0, 0, cfg.BOTTOM_FAN_CARTRIDGE_Z)),
    )
    assembly.add(
        placeholders.make_fan_120_placeholder(),
        name="bottom_fan_120x120x25_placeholder",
        loc=cq.Location(cq.Vector(0, 0, cfg.BOTTOM_FAN_PLACEHOLDER_Z)),
    )
    assembly.add(
        placeholders.make_fan_120_placeholder(),
        name="top_fan_120x120x25_placeholder",
        loc=cq.Location(cq.Vector(0, 0, cfg.TOP_FAN_PLACEHOLDER_Z)),
    )
    assembly.add(cooling.make_bottom_fan_grille(), name="bottom_fan_grille", loc=cq.Location(cq.Vector(0, 0, cfg.BOTTOM_FAN_PANEL_Z)))
    assembly.add(
        cooling.make_top_fan_grille(),
        name="top_fan_grille",
        loc=cq.Location(cq.Vector(0, 0, cfg.TOWER_HEIGHT + cfg.TOP_FAN_PANEL_Z_OFFSET)),
    )
    assembly.add(
        cooling.make_mini_pc_airflow_duct_placeholder(),
        name="mini_pc_airflow_duct_placeholder",
        loc=cq.Location(cq.Vector(cfg.MINI_PC_DUCT_ASSEMBLY_X, cfg.MINI_PC_DUCT_ASSEMBLY_Y, _mini_pc_duct_z())),
    )

    return assembly
