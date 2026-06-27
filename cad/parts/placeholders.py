"""Temporary device volumes used only for mk0.3 assembly layout checks."""

import cadquery as cq

from .. import config as cfg
from ..utils.geometry import rounded_box


def make_placeholder_box(width: float, depth: float, height: float, name: str) -> cq.Workplane:
    return rounded_box(width, depth, height, cfg.PLACEHOLDER_CHAMFER).tag(name)


def make_mini_pc_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.MINI_PC_PLACEHOLDER_WIDTH,
        cfg.MINI_PC_PLACEHOLDER_DEPTH,
        cfg.MINI_PC_PLACEHOLDER_HEIGHT,
        "mini_pc_placeholder",
    )


def make_raspberry_pi_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.RASPBERRY_PI_PLACEHOLDER_WIDTH,
        cfg.RASPBERRY_PI_PLACEHOLDER_DEPTH,
        cfg.RASPBERRY_PI_PLACEHOLDER_HEIGHT,
        "raspberry_pi_placeholder",
    )


def make_mikrotik_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.MIKROTIK_PLACEHOLDER_WIDTH,
        cfg.MIKROTIK_PLACEHOLDER_DEPTH,
        cfg.MIKROTIK_PLACEHOLDER_HEIGHT,
        "mikrotik_placeholder",
    )


def make_ups_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.UPS_PLACEHOLDER_WIDTH,
        cfg.UPS_PLACEHOLDER_DEPTH,
        cfg.UPS_PLACEHOLDER_HEIGHT,
        "ups_placeholder",
    )


def make_external_ssd_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.EXTERNAL_SSD_PLACEHOLDER_WIDTH,
        cfg.EXTERNAL_SSD_PLACEHOLDER_DEPTH,
        cfg.EXTERNAL_SSD_PLACEHOLDER_HEIGHT,
        "external_ssd_placeholder",
    )


def make_ssd_expansion_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.SSD_EXPANSION_PLACEHOLDER_WIDTH,
        cfg.SSD_EXPANSION_PLACEHOLDER_DEPTH,
        cfg.SSD_EXPANSION_PLACEHOLDER_HEIGHT,
        "ssd_expansion_placeholder",
    )


def make_power_bus_zone_placeholder() -> cq.Workplane:
    return make_placeholder_box(
        cfg.POWER_BUS_WIDTH,
        cfg.POWER_BUS_PAD_DEPTH,
        cfg.POWER_BUS_HEIGHT,
        "power_bus_zone_placeholder",
    )
