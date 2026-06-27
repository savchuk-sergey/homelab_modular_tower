"""Part registry used by export scripts."""

from ..parts import cooling, modules, service_spine, side_panels
from ..parts.corner_blocks import create_corner_block
from ..parts.frame import create_frame_bottom, create_frame_top
from ..parts.rails import create_metal_guide_rail
from ..parts.rods import create_m5_threaded_rod


PARTS = {
    "frame_top": create_frame_top,
    "frame_bottom": create_frame_bottom,
    "corner_block": create_corner_block,
    "m5_threaded_rod": create_m5_threaded_rod,
    "metal_guide_rail": create_metal_guide_rail,
    "ups_power_tray": modules.create_ups_power_tray,
    "external_ssd_bay": modules.create_external_ssd_bay,
    "ssd_expansion_tray": modules.create_ssd_expansion_tray,
    "raspberry_pi_tray": modules.create_raspberry_pi_tray,
    "mikrotik_tray": modules.create_mikrotik_tray,
    "mini_pc_tray": modules.create_mini_pc_tray,
    "power_bus_panel": service_spine.create_power_bus_panel,
    "rear_service_spine": service_spine.create_rear_service_spine,
    "left_side_panel": side_panels.create_left_side_panel,
    "right_side_panel": side_panels.create_right_side_panel,
    "bottom_fan_panel": cooling.create_bottom_fan_panel,
    "top_fan_panel": cooling.create_top_fan_panel,
    "mini_pc_airflow_duct": cooling.create_mini_pc_airflow_duct,
}
