"""Compatibility exports for module carriage factories."""

from .parts.carriages import (
    add_mounting_holes,
    create_carriage,
    cut_structural_clearances,
    cut_vent_slots,
    make_carriage_front_plate,
    make_carriage_handle_cutout,
    make_carriage_lock_boss,
    make_module_rails,
    make_standard_tray_base,
    make_tray_cable_exit,
    make_tray_front_lock,
    make_tray_handle,
    make_tray_rear_stop,
)
from .parts.modules import (
    TRAY_FACTORIES,
    create_external_ssd_bay,
    create_mikrotik_tray,
    create_mini_pc_tray,
    create_raspberry_pi_tray,
    create_ssd_expansion_tray,
    create_ups_power_tray,
)

create_tray = create_carriage

__all__ = [
    "TRAY_FACTORIES",
    "add_mounting_holes",
    "create_carriage",
    "create_external_ssd_bay",
    "create_mikrotik_tray",
    "create_mini_pc_tray",
    "create_raspberry_pi_tray",
    "create_ssd_expansion_tray",
    "create_tray",
    "create_ups_power_tray",
    "cut_structural_clearances",
    "cut_vent_slots",
    "make_carriage_front_plate",
    "make_carriage_handle_cutout",
    "make_carriage_lock_boss",
    "make_module_rails",
    "make_standard_tray_base",
    "make_tray_cable_exit",
    "make_tray_front_lock",
    "make_tray_handle",
    "make_tray_rear_stop",
]
