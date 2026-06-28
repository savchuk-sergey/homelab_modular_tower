"""Part registry used by export scripts."""

from ..parts import (
    airflow,
    base_module,
    carriages,
    feet,
    mini_pc_placeholder_module,
    module_interface,
    placeholders,
    rails,
    roof_module,
    rpi_ssd_module,
)
from ..parts.rods import create_m5_threaded_rod, create_m5_threaded_rod_cap


PARTS = {
    "module_interface_top": module_interface.make_module_interface_top,
    "module_interface_bottom": module_interface.make_module_interface_bottom,
    "alignment_pins": module_interface.make_alignment_pins,
    "alignment_sockets": module_interface.make_alignment_sockets,
    "interface_bolt_holes": module_interface.make_interface_bolt_holes,
    "rod_clearance_holes": module_interface.make_rod_clearance_holes,
    "base_frame": base_module.make_base_frame,
    "base_fan_mount": base_module.make_base_fan_mount,
    "bottom_grill": base_module.make_bottom_grill,
    "dust_filter_slot": base_module.make_dust_filter_slot,
    "foot_mounts": base_module.make_foot_mounts,
    "base_module": base_module.make_base_module,
    # rpi_ssd legacy helpers (kept for backward compatibility)
    "rpi3_placeholder": rpi_ssd_module.make_rpi3_placeholder,
    "external_ssd_placeholder_mk09": rpi_ssd_module.make_external_ssd_placeholder,
    "rpi_ssd_tray": rpi_ssd_module.make_rpi_ssd_tray,
    "rpi_mount_posts": rpi_ssd_module.make_rpi_mount_posts,
    "ssd_retainer": rpi_ssd_module.make_ssd_retainer,
    "rpi_ssd_module_shell": rpi_ssd_module.make_rpi_ssd_module_shell,
    # mk0.9.1 open-frame carriage
    "rpi_ssd_carriage": carriages.make_rpi_ssd_carriage,
    "rpi_ssd_module": rpi_ssd_module.make_rpi_ssd_module,
    # mini_pc legacy helpers
    "mini_pc_placeholder": mini_pc_placeholder_module.make_mini_pc_placeholder,
    "mini_pc_placeholder_tray": mini_pc_placeholder_module.make_mini_pc_placeholder_tray,
    "mini_pc_placeholder_airflow_guide": mini_pc_placeholder_module.make_mini_pc_placeholder_airflow_guide,
    "mini_pc_placeholder_retainer": mini_pc_placeholder_module.make_mini_pc_placeholder_retainer,
    "mini_pc_placeholder_module_shell": mini_pc_placeholder_module.make_mini_pc_placeholder_module_shell,
    # mk0.9.1 open-frame carriage
    "mini_pc_placeholder_carriage": carriages.make_mini_pc_placeholder_carriage,
    "mini_pc_placeholder_module": mini_pc_placeholder_module.make_mini_pc_placeholder_module,
    # roof
    "roof_frame": roof_module.make_roof_frame,
    "top_fan_mount": roof_module.make_top_fan_mount,
    "top_grill": roof_module.make_top_grill,
    "top_filter_slot": roof_module.make_top_filter_slot,
    "fan_shroud": roof_module.make_fan_shroud,
    "roof_module": roof_module.make_roof_module,
    # feet
    "foot": feet.make_foot,
    "tpu_foot_placeholder": feet.make_tpu_foot_placeholder,
    # rods
    "m5_threaded_rod": create_m5_threaded_rod,
    "m5_threaded_rod_cap": create_m5_threaded_rod_cap,
    # placeholders
    "fan_120x120x25_placeholder": placeholders.make_fan_120_placeholder,
    "raspberry_pi_3b_placeholder": placeholders.make_raspberry_pi_3b_placeholder,
    "external_ssd_placeholder": placeholders.make_external_ssd_placeholder,
    "dust_filter_placeholder": placeholders.make_dust_filter_placeholder,
    "top_guard_filter_mesh_placeholder": placeholders.make_top_guard_filter_mesh_placeholder,
    "pom_c_shoe_placeholder": placeholders.make_pom_c_shoe_placeholder,
    "aluminum_u_channel_rail_placeholder": placeholders.make_aluminum_u_channel_rail_placeholder,
    # airflow review
    "central_airflow_channel_placeholder": airflow.make_central_airflow_channel_placeholder,
    "airflow_clearance_zone": airflow.make_airflow_clearance_zone,
    "simplified_airflow_guide": airflow.make_simplified_airflow_guide,
    # legacy rail helpers (kept for backward compatibility)
    "rail_end_mount": rails.create_rail_end_mount,
    "tray_support_ledge": rails.create_tray_support_ledge,
    # mk0.9.1 rail
    "rail_end_clip": rails.make_rail_end_clip,
}


EXPORT_CATEGORIES = {
    "printable/plastic": {
        "base_module": base_module.make_base_module,
        "bottom_grill": base_module.make_bottom_grill,
        "foot_mounts": base_module.make_foot_mounts,
        "rpi_ssd_module": rpi_ssd_module.make_rpi_ssd_module,
        "rpi_ssd_carriage": carriages.make_rpi_ssd_carriage,
        "mini_pc_placeholder_module": mini_pc_placeholder_module.make_mini_pc_placeholder_module,
        "mini_pc_placeholder_carriage": carriages.make_mini_pc_placeholder_carriage,
        "roof_module": roof_module.make_roof_module,
        "dust_filter_slot": base_module.make_dust_filter_slot,
        "top_filter_slot": roof_module.make_top_filter_slot,
        "m5_threaded_rod_cap": create_m5_threaded_rod_cap,
        "rail_end_clip": rails.make_rail_end_clip,
    },
    "printable/tpu": {
        "foot": feet.make_foot,
        "tpu_foot_placeholder": feet.make_tpu_foot_placeholder,
    },
    "non_printable/metal_reference": {
        "m5_threaded_rod": create_m5_threaded_rod,
        "aluminum_u_channel_rail_placeholder": placeholders.make_aluminum_u_channel_rail_placeholder,
    },
    "placeholders/devices": {
        "raspberry_pi_3b_placeholder": placeholders.make_raspberry_pi_3b_placeholder,
        "external_ssd_placeholder": placeholders.make_external_ssd_placeholder,
        "mini_pc_placeholder": placeholders.make_mini_pc_placeholder,
        "pom_c_shoe_placeholder": placeholders.make_pom_c_shoe_placeholder,
    },
    "placeholders/fans": {
        "fan_120x120x25_placeholder": placeholders.make_fan_120_placeholder,
    },
    "placeholders/filters": {
        "dust_filter_placeholder": placeholders.make_dust_filter_placeholder,
        "top_guard_filter_mesh_placeholder": placeholders.make_top_guard_filter_mesh_placeholder,
    },
    "review": {
        "module_interface_top": module_interface.make_module_interface_top,
        "module_interface_bottom": module_interface.make_module_interface_bottom,
        "central_airflow_channel_placeholder": airflow.make_central_airflow_channel_placeholder,
        "airflow_clearance_zone": airflow.make_airflow_clearance_zone,
        "simplified_airflow_guide": airflow.make_simplified_airflow_guide,
    },
    "legacy": {
        "rail_end_mount": rails.create_rail_end_mount,
        "tray_support_ledge": rails.create_tray_support_ledge,
        "rpi_ssd_tray": rpi_ssd_module.make_rpi_ssd_tray,
        "rpi_mount_posts": rpi_ssd_module.make_rpi_mount_posts,
        "ssd_retainer": rpi_ssd_module.make_ssd_retainer,
        "mini_pc_placeholder_tray": mini_pc_placeholder_module.make_mini_pc_placeholder_tray,
        "mini_pc_placeholder_airflow_guide": mini_pc_placeholder_module.make_mini_pc_placeholder_airflow_guide,
        "mini_pc_placeholder_retainer": mini_pc_placeholder_module.make_mini_pc_placeholder_retainer,
    },
}
