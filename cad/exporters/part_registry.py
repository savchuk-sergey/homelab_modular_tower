"""Part registry used by export scripts."""

from ..parts import cooling, feet, modules, service_spine, side_panels
from ..parts.corner_blocks import create_corner_block
from ..parts.frame import make_bottom_structural_frame, make_top_structural_frame
from ..parts.rails import create_metal_guide_rail
from ..parts.rods import create_m5_threaded_rod


PARTS = {
    "frame_top": make_top_structural_frame,
    "frame_bottom": make_bottom_structural_frame,
    "top_structural_frame": make_top_structural_frame,
    "bottom_structural_frame": make_bottom_structural_frame,
    "corner_block": create_corner_block,
    "base_stability_plate": feet.make_base_stability_plate,
    "foot_socket": feet.make_foot_socket,
    "foot": feet.make_foot,
    "wide_tpu_foot_placeholder": feet.make_wide_tpu_foot_placeholder,
    "m5_threaded_rod": create_m5_threaded_rod,
    "metal_guide_rail": create_metal_guide_rail,
    "ups_power_tray": modules.create_ups_power_tray,
    "external_ssd_bay": modules.create_external_ssd_bay,
    "ssd_expansion_tray": modules.create_ssd_expansion_tray,
    "raspberry_pi_tray": modules.create_raspberry_pi_tray,
    "mikrotik_tray": modules.create_mikrotik_tray,
    "mini_pc_tray": modules.create_mini_pc_tray,
    "mini_pc_tray_stop": modules.make_tray_stop,
    "power_bus_panel": service_spine.create_power_bus_panel,
    "rear_service_spine": service_spine.create_rear_service_spine,
    "rear_service_spine_cover": service_spine.create_rear_service_spine_cover,
    "left_side_panel_lower": side_panels.create_left_side_panel_lower,
    "left_side_panel_middle": side_panels.create_left_side_panel_middle,
    "left_side_panel_upper": side_panels.create_left_side_panel_upper,
    "right_side_panel_lower": side_panels.create_right_side_panel_lower,
    "right_side_panel_middle": side_panels.create_right_side_panel_middle,
    "right_side_panel_upper": side_panels.create_right_side_panel_upper,
    "bottom_fan_grille": cooling.make_bottom_fan_grille,
    "top_fan_grille": cooling.make_top_fan_grille,
    "bottom_fan_panel": cooling.make_bottom_fan_grille,
    "top_fan_panel": cooling.make_top_fan_grille,
    "mini_pc_airflow_duct": cooling.make_mini_pc_airflow_duct_placeholder,
    "mini_pc_airflow_duct_placeholder": cooling.make_mini_pc_airflow_duct_placeholder,
}
