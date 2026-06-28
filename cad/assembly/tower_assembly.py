"""mk0.9 modular architecture prototype assembly."""

import cadquery as cq

from .. import config as cfg
from ..parts import airflow, base_module, mini_pc_placeholder_module, placeholders, roof_module, rpi_ssd_module
from ..parts.rods import create_m5_threaded_rod, create_m5_threaded_rod_cap, rod_positions


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


def build_assembly() -> cq.Assembly:
    assembly = cq.Assembly(name="homelab_modular_tower_mk0_9")

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
                cfg.BASE_MODULE_HEIGHT + cfg.FLOOR_THICKNESS + cfg.RPI3_STANDOFF_HEIGHT + cfg.RPI3B_BOARD_THICKNESS / 2,
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
                cfg.BASE_MODULE_HEIGHT + cfg.FLOOR_THICKNESS + cfg.EXTERNAL_SSD_PLACEHOLDER_HEIGHT / 2,
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
                + cfg.FLOOR_THICKNESS
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
