"""mk0.9.2 modular architecture prototype assembly.

Includes:
* base, RPi/SSD, Mini PC placeholder, and roof modules
* aluminum U-channel rail placeholders
* POM-C shoe placeholders
* M5 threaded rods and caps
* 120 mm fan placeholders
* device placeholders (RPi 3B, external SSD, Mini PC)
* dust filter and top guard placeholders
* central airflow channel placeholder
"""

import cadquery as cq

from cad import config as cfg
from cad.parts import (
    airflow,
    base_module,
    feet,
    mini_pc_placeholder_module,
    placeholders,
    rails,
    roof_module,
    rpi_ssd_module,
)
from cad.parts.rods import create_m5_threaded_rod, create_m5_threaded_rod_cap, rod_positions


def _add_rods(assembly: cq.Assembly) -> None:
    names = ["front_right", "front_left", "rear_left", "rear_right"]
    for index, (px, py) in enumerate(rod_positions()):
        assembly.add(
            create_m5_threaded_rod(),
            name=f"m5_threaded_rod_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, 0)),
        )
        assembly.add(
            create_m5_threaded_rod_cap(),
            name=f"m5_rod_cap_top_{names[index]}",
            loc=cq.Location(cq.Vector(px, py, cfg.TOWER_HEIGHT + cfg.ROD_CAP_HEIGHT / 2)),
        )


def _add_module_rails_and_shoes(
    assembly: cq.Assembly,
    module_name: str,
    module_z: float,
    module_height: float,
    rail_length: float,
    shoes_per_side: int,
) -> None:
    """Add non-printed rail and POM-C shoe placeholders for a single module."""
    x_rail = rails.u_channel_rail_x_offset()
    y_center = -cfg.REAR_RESERVED_DEPTH / 2
    # approximate Z where the shoe sits inside the carriage boss
    deck_z = -module_height / 2 + cfg.CARRIAGE_WALL_THICKNESS / 2
    z_shoe = module_z + deck_z + cfg.CARRIAGE_RUNNER_BOSS_THICKNESS / 2

    side_length = cfg.MODULE_DEPTH - cfg.CARRIAGE_SHOE_END_INSET
    if shoes_per_side <= 1:
        offsets = [0.0]
    else:
        spacing = side_length / (shoes_per_side - 1)
        offsets = [-side_length / 2 + i * spacing for i in range(shoes_per_side)]

    for sign in (-1, 1):
        # Rail placeholder — rotated so its length axis aligns with Y
        assembly.add(
            placeholders.make_aluminum_u_channel_rail_placeholder(rail_length),
            name=f"aluminum_u_channel_rail_{module_name}_{'left' if sign < 0 else 'right'}",
            loc=cq.Location(
                cq.Vector(sign * x_rail, y_center, z_shoe),
                cq.Vector(1, 0, 0),
                90,
            ),
        )
        # Shoe placeholders
        for idx, y_offset in enumerate(offsets):
            assembly.add(
                placeholders.make_pom_c_shoe_placeholder(),
                name=f"pom_c_shoe_{module_name}_{'left' if sign < 0 else 'right'}_{idx}",
                loc=cq.Location(
                    cq.Vector(
                        sign * x_rail + sign * (cfg.RAIL_OUTER_WIDTH / 2 + cfg.RUNNER_PROTRUSION_FROM_CARRIAGE / 2),
                        y_center + y_offset,
                        z_shoe,
                    ),
                    cq.Vector(1, 0, 0),
                    90,
                ),
            )


def build_assembly() -> cq.Assembly:
    assembly = cq.Assembly(name="homelab_modular_tower_mk0_9_2")

    assembly.add(base_module.make_base_module(), name="base_module", loc=cq.Location(cq.Vector(0, 0, cfg.BASE_MODULE_Z)))
    assembly.add(
        rpi_ssd_module.make_rpi_ssd_module(),
        name="rpi_ssd_module",
        loc=cq.Location(cq.Vector(0, 0, cfg.RPI_SSD_MODULE_Z)),
    )
    assembly.add(
        mini_pc_placeholder_module.make_mini_pc_placeholder_module(),
        name="mini_pc_placeholder_module",
        loc=cq.Location(cq.Vector(0, 0, cfg.MINI_PC_MODULE_Z)),
    )
    assembly.add(roof_module.make_roof_module(), name="roof_module", loc=cq.Location(cq.Vector(0, 0, cfg.ROOF_MODULE_Z)))
    _add_rods(assembly)

    # Rail / shoe placeholders for the two carriages
    _add_module_rails_and_shoes(
        assembly,
        "rpi_ssd",
        cfg.RPI_SSD_MODULE_Z,
        cfg.RPI_SSD_MODULE_HEIGHT,
        cfg.RAIL_LENGTH_RPI_SSD,
        cfg.RUNNER_SHOES_PER_SIDE_RPI_SSD,
    )
    _add_module_rails_and_shoes(
        assembly,
        "mini_pc",
        cfg.MINI_PC_MODULE_Z,
        cfg.MINI_PC_MODULE_HEIGHT,
        cfg.RAIL_LENGTH_MINI_PC_PLACEHOLDER,
        cfg.RUNNER_SHOES_PER_SIDE_MINI_PC,
    )

    # Foot placeholders
    foot_z = cfg.BASE_MODULE_Z - cfg.BASE_MODULE_HEIGHT / 2 - cfg.FOOT_HEIGHT / 2 - cfg.FLOOR_THICKNESS
    boss_radius = (cfg.FOOT_DIAMETER + cfg.FOOT_MOUNT_BOSS_EXTRA_DIAMETER) / 2
    x = cfg.TOWER_WIDTH / 2 - boss_radius
    y = cfg.TOWER_DEPTH / 2 - boss_radius
    for idx, (px, py) in enumerate([(-x, -y), (x, -y), (x, y), (-x, y)]):
        assembly.add(
            feet.make_foot(),
            name=f"tpu_foot_{idx}",
            loc=cq.Location(cq.Vector(px, py, foot_z)),
        )

    fan_y = -cfg.REAR_RESERVED_DEPTH / 2
    assembly.add(
        placeholders.make_fan_120_placeholder(),
        name="bottom_fan_120x120x25_placeholder",
        loc=cq.Location(cq.Vector(0, fan_y, cfg.FAN_120_THICKNESS / 2 + cfg.FLOOR_THICKNESS)),
    )
    assembly.add(
        placeholders.make_fan_120_placeholder(),
        name="top_fan_120x120x25_placeholder",
        loc=cq.Location(
            cq.Vector(
                0,
                fan_y,
                cfg.TOWER_HEIGHT - cfg.ROOF_MODULE_HEIGHT + cfg.FAN_120_THICKNESS / 2 + cfg.FLOOR_THICKNESS,
            )
        ),
    )
    assembly.add(
        placeholders.make_raspberry_pi_3b_placeholder(),
        name="raspberry_pi_3b_placeholder",
        loc=cq.Location(
            cq.Vector(
                cfg.RPI3_PLACEHOLDER_X,
                cfg.RPI3_PLACEHOLDER_Y,
                cfg.BASE_MODULE_HEIGHT + cfg.CARRIAGE_WALL_THICKNESS + cfg.RPI3_STANDOFF_HEIGHT + cfg.RPI3B_BOARD_THICKNESS / 2,
            )
        ),
    )
    assembly.add(
        placeholders.make_external_ssd_placeholder(),
        name="external_ssd_placeholder",
        loc=cq.Location(
            cq.Vector(
                cfg.EXTERNAL_SSD_PLACEHOLDER_X,
                cfg.EXTERNAL_SSD_PLACEHOLDER_Y,
                cfg.BASE_MODULE_HEIGHT + cfg.CARRIAGE_WALL_THICKNESS + cfg.EXTERNAL_SSD_PLACEHOLDER_HEIGHT / 2,
            )
        ),
    )
    assembly.add(
        placeholders.make_mini_pc_placeholder(),
        name="mini_pc_placeholder",
        loc=cq.Location(
            cq.Vector(
                0,
                fan_y,
                cfg.BASE_MODULE_HEIGHT
                + cfg.RPI_SSD_MODULE_HEIGHT
                + cfg.CARRIAGE_WALL_THICKNESS
                + cfg.MINI_PC_PLACEHOLDER_HEIGHT / 2,
            )
        ),
    )
    assembly.add(
        placeholders.make_dust_filter_placeholder(),
        name="bottom_dust_filter_placeholder",
        loc=cq.Location(cq.Vector(0, fan_y, cfg.FILTER_SLOT_HEIGHT / 2)),
    )
    assembly.add(
        placeholders.make_top_guard_filter_mesh_placeholder(),
        name="top_guard_filter_mesh_placeholder",
        loc=cq.Location(cq.Vector(0, fan_y, cfg.TOWER_HEIGHT - cfg.TOP_GUARD_FRAME_HEIGHT)),
    )
    assembly.add(
        airflow.make_central_airflow_channel_placeholder(),
        name="central_airflow_channel_placeholder",
        loc=cq.Location(cq.Vector(0, 0, 0)),
    )

    return assembly
