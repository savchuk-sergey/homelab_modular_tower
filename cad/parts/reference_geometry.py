"""Non-printable mk0.12 reference geometry for assembly review only."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg
from cad.parts import stack_interface as si


def build_rpi3b_placeholder() -> cq.Workplane:
    return (
        si.box_at_z(cfg.RPI3B_BOARD_WIDTH, cfg.RPI3B_BOARD_DEPTH, 2.0, cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT)
        .translate((cfg.RPI3B_CENTER_X, cfg.RPI3B_CENTER_Y, 0.0))
        .tag("reference_rpi3b_placeholder")
    )


def build_external_ssd_placeholder() -> cq.Workplane:
    return (
        si.box_at_z(
            cfg.EXTERNAL_SSD_WIDTH,
            cfg.EXTERNAL_SSD_DEPTH,
            cfg.EXTERNAL_SSD_HEIGHT,
            cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
        )
        .translate((cfg.EXTERNAL_SSD_PREFERRED_CENTER_X, cfg.EXTERNAL_SSD_PREFERRED_CENTER_Y, 0.0))
        .tag("reference_external_ssd_placeholder")
    )


def build_minipc_placeholder() -> cq.Workplane:
    return (
        si.box_at_z(cfg.MINIPC_WIDTH, cfg.MINIPC_DEPTH, cfg.MINIPC_HEIGHT, cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT)
        .translate((cfg.MINIPC_CENTER_X, cfg.MINIPC_CENTER_Y, 0.0))
        .tag("reference_minipc_placeholder")
    )


def build_m5_rods_placeholder() -> cq.Workplane:
    rods = [
        si.cylinder_at_z(
            cfg.M5_ROD_DIAMETER,
            cfg.RECOMMENDED_M5_ROD_LENGTH,
            center_x,
            center_y,
            -cfg.ROD_EXTRA_THREAD_ALLOWANCE_BOTTOM,
        )
        for center_x, center_y in cfg.m5_rod_centers()
    ]
    return si.union_all(rods).tag("reference_m5_rods")


def build_washers_placeholder() -> cq.Workplane:
    washers: list[cq.Workplane] = []
    for z_min in (-cfg.M5_WASHER_SEAT_DEPTH, cfg.TOTAL_STACK_HEIGHT):
        for center_x, center_y in cfg.m5_rod_centers():
            washers.append(si.cylinder_at_z(cfg.M5_WASHER_OUTER_DIAMETER, cfg.M5_WASHER_SEAT_DEPTH, center_x, center_y, z_min))
    return si.union_all(washers).tag("reference_washers")


def build_nuts_placeholder() -> cq.Workplane:
    nut_height = 4.0
    nut_diameter = cfg.M5_NUT_ACCESS_DIAMETER_MIN
    nuts: list[cq.Workplane] = []
    for z_min in (-cfg.ROD_EXTRA_THREAD_ALLOWANCE_BOTTOM, cfg.TOTAL_STACK_HEIGHT + cfg.M5_WASHER_SEAT_DEPTH):
        for center_x, center_y in cfg.m5_rod_centers():
            nuts.append(si.cylinder_at_z(nut_diameter, nut_height, center_x, center_y, z_min))
    return si.union_all(nuts).tag("reference_nuts")
