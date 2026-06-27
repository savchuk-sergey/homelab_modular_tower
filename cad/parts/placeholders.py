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


def make_fan_120_placeholder() -> cq.Workplane:
    """Create a non-printable 120 x 120 x 25 mm fan reference volume."""
    fan = make_placeholder_box(
        cfg.FAN_120_SIZE,
        cfg.FAN_120_SIZE,
        cfg.FAN_120_THICKNESS,
        "fan_120x120x25_placeholder",
    )
    fan = fan.faces(">Z").workplane().circle(cfg.FAN_120_AIR_OPENING_DIAMETER / 2).cutThruAll()
    d = cfg.FAN_120_HOLE_SPACING / 2
    fan = fan.faces(">Z").workplane().pushPoints([(x, y) for x in (-d, d) for y in (-d, d)]).hole(
        cfg.FAN_120_HOLE_DIAMETER
    )
    hub = cq.Workplane("XY").circle(cfg.FAN_120_HUB_DIAMETER / 2).extrude(cfg.FAN_120_KEEP_OUT_HEIGHT)
    return fan.union(hub.translate((0, 0, -cfg.FAN_120_THICKNESS / 2))).tag("fan_120x120x25_placeholder")


def make_raspberry_pi_3b_placeholder() -> cq.Workplane:
    """Create a non-printable Raspberry Pi 3B engineering reference model."""
    board = make_placeholder_box(
        cfg.RPI3B_BOARD_WIDTH,
        cfg.RPI3B_BOARD_DEPTH,
        cfg.RPI3B_BOARD_THICKNESS,
        "raspberry_pi_3b_board",
    )
    hx = cfg.RPI3B_BOARD_WIDTH / 2 - cfg.RPI3B_MOUNT_HOLE_OFFSET_X
    hy = cfg.RPI3B_BOARD_DEPTH / 2 - cfg.RPI3B_MOUNT_HOLE_OFFSET_Y
    board = board.faces(">Z").workplane().pushPoints([(x, y) for x in (-hx, hx) for y in (-hy, hy)]).hole(
        cfg.RPI3B_MOUNT_HOLE_DIAMETER
    )

    component_keepout = cq.Workplane("XY").box(
        cfg.RPI3B_BOARD_WIDTH,
        cfg.RPI3B_BOARD_DEPTH,
        cfg.RPI3B_COMPONENT_KEEP_OUT_HEIGHT,
    ).translate((0, 0, cfg.RPI3B_BOARD_THICKNESS / 2 + cfg.RPI3B_COMPONENT_KEEP_OUT_HEIGHT / 2))
    usb_eth = cq.Workplane("XY").box(
        cfg.RPI3B_USB_ETH_KEEP_OUT_WIDTH,
        cfg.RPI3B_USB_ETH_KEEP_OUT_DEPTH,
        cfg.RPI3B_USB_ETH_KEEP_OUT_HEIGHT,
    ).translate(
        (
            cfg.RPI3B_USB_ETH_KEEP_OUT_X,
            cfg.RPI3B_USB_ETH_KEEP_OUT_Y,
            cfg.RPI3B_BOARD_THICKNESS / 2 + cfg.RPI3B_USB_ETH_KEEP_OUT_HEIGHT / 2,
        )
    )
    hdmi_power = cq.Workplane("XY").box(
        cfg.RPI3B_HDMI_POWER_KEEP_OUT_WIDTH,
        cfg.RPI3B_HDMI_POWER_KEEP_OUT_DEPTH,
        cfg.RPI3B_HDMI_POWER_KEEP_OUT_HEIGHT,
    ).translate(
        (
            cfg.RPI3B_HDMI_POWER_KEEP_OUT_X,
            cfg.RPI3B_HDMI_POWER_KEEP_OUT_Y,
            cfg.RPI3B_BOARD_THICKNESS / 2 + cfg.RPI3B_HDMI_POWER_KEEP_OUT_HEIGHT / 2,
        )
    )
    gpio = cq.Workplane("XY").box(
        cfg.RPI3B_GPIO_KEEP_OUT_WIDTH,
        cfg.RPI3B_GPIO_KEEP_OUT_DEPTH,
        cfg.RPI3B_GPIO_KEEP_OUT_HEIGHT,
    ).translate(
        (
            cfg.RPI3B_GPIO_KEEP_OUT_X,
            cfg.RPI3B_GPIO_KEEP_OUT_Y,
            cfg.RPI3B_BOARD_THICKNESS / 2 + cfg.RPI3B_GPIO_KEEP_OUT_HEIGHT / 2,
        )
    )
    return board.union(component_keepout).union(usb_eth).union(hdmi_power).union(gpio).tag(
        "raspberry_pi_3b_placeholder"
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
