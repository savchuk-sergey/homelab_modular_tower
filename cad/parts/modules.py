"""Device-specific module carriage placeholders."""

import cadquery as cq

from .. import config as cfg
from ..utils.geometry import rounded_box
from .carriages import create_carriage


def create_ups_power_tray() -> cq.Workplane:
    tray = create_carriage("ups_power_tray", cfg.UPS_POWER_TRAY_UNITS, ventilation=True, front_handle=True)
    # Placeholder zones for low-voltage UPS electronics, not exposed mains AC.
    for x, y, lx, ly, _ in cfg.UPS_COMPONENT_ZONES:
        tray = tray.union(cq.Workplane("XY").box(lx, ly, cfg.UPS_ZONE_MARKER_HEIGHT).translate((x, y, cfg.UPS_ZONE_MARKER_Z)))
    for y in cfg.UPS_EXTRA_MOUNT_Y:
        tray = tray.faces(">Z").workplane().pushPoints([(x, y) for x in cfg.UPS_EXTRA_MOUNT_X]).hole(cfg.M3_CLEARANCE)
    for x in cfg.UPS_STRAP_SLOT_X:
        tray = tray.faces(">Z").workplane().pushPoints([(x, 0.0)]).slot2D(
            cfg.UPS_STRAP_SLOT_LENGTH, cfg.UPS_STRAP_SLOT_WIDTH, 0
        ).cutThruAll()
    return tray


def create_external_ssd_bay() -> cq.Workplane:
    tray = create_carriage("external_ssd_bay", cfg.EXTERNAL_SSD_BAY_UNITS, ventilation=True, front_handle=True)
    pocket_outer = cq.Workplane("XY").box(
        cfg.SSD_POCKET_LENGTH + cfg.SSD_POCKET_WALL_ALLOWANCE,
        cfg.SSD_POCKET_WIDTH + cfg.SSD_POCKET_WALL_ALLOWANCE,
        cfg.SSD_POCKET_HEIGHT,
    ).translate((cfg.SSD_POCKET_X, cfg.SSD_POCKET_Y, cfg.TRAY_BASE_THICKNESS / 2 + cfg.SSD_POCKET_HEIGHT / 2))
    pocket_inner = cq.Workplane("XY").box(
        cfg.SSD_POCKET_LENGTH,
        cfg.SSD_POCKET_WIDTH,
        cfg.SSD_POCKET_HEIGHT + cfg.SSD_POCKET_CUTTER_OVERLAP,
    ).translate(
        (
            cfg.SSD_POCKET_X,
            cfg.SSD_POCKET_Y,
            cfg.TRAY_BASE_THICKNESS / 2 + cfg.SSD_POCKET_HEIGHT / 2 + cfg.SSD_POCKET_CUTTER_OVERLAP / 2,
        )
    )
    tray = tray.union(pocket_outer.cut(pocket_inner))
    tray = tray.faces("<Y").workplane(centerOption="CenterOfBoundBox").circle(cfg.SSD_FRONT_ACCESS_RADIUS).cutBlind(
        -cfg.SSD_FRONT_ACCESS_DEPTH
    )
    cable = cq.Workplane("XY").box(cfg.SSD_CABLE_CUTOUT_WIDTH, cfg.SSD_CABLE_CUTOUT_LENGTH, cfg.SSD_CABLE_CUTOUT_HEIGHT).translate(
        (cfg.SSD_CABLE_CUTOUT_X, cfg.SSD_CABLE_CUTOUT_Y, cfg.SSD_CABLE_CUTOUT_Z)
    )
    tray = tray.cut(cable)
    for x in cfg.SSD_STRAP_SLOT_X:
        tray = tray.faces(">Z").workplane().pushPoints([(x, cfg.SSD_POCKET_Y)]).slot2D(
            cfg.SSD_STRAP_SLOT_LENGTH, cfg.SSD_STRAP_SLOT_WIDTH, 0
        ).cutThruAll()
    return tray


def create_ssd_expansion_tray() -> cq.Workplane:
    return create_carriage("ssd_expansion_tray", cfg.SSD_EXPANSION_TRAY_UNITS, ventilation=True, front_handle=True)


def create_raspberry_pi_tray() -> cq.Workplane:
    tray = create_carriage("raspberry_pi_tray", cfg.RASPBERRY_PI_TRAY_UNITS, ventilation=True, front_handle=True)
    board = rounded_box(
        cfg.RASPBERRY_PI_PLACEHOLDER[0],
        cfg.RASPBERRY_PI_PLACEHOLDER[1],
        cfg.MODULE_BOARD_MARKER_HEIGHT,
        cfg.PLACEHOLDER_CHAMFER,
    ).translate(cfg.RASPBERRY_PI_PLACEHOLDER_LOC)
    tray = tray.union(board)
    fan_cut = cq.Workplane("XY").box(cfg.RPI_FAN_ZONE_WIDTH, cfg.RPI_FAN_ZONE_DEPTH, cfg.RPI_FAN_ZONE_HEIGHT).translate(
        cfg.RPI_FAN_ZONE_LOC
    )
    return tray.union(fan_cut)


def create_mikrotik_tray() -> cq.Workplane:
    tray = create_carriage("mikrotik_tray", cfg.MIKROTIK_TRAY_UNITS, ventilation=True, front_handle=True)
    board = rounded_box(
        cfg.MIKROTIK_PLACEHOLDER[0],
        cfg.MIKROTIK_PLACEHOLDER[1],
        cfg.MODULE_BOARD_MARKER_HEIGHT,
        cfg.PLACEHOLDER_CHAMFER,
    ).translate(cfg.MIKROTIK_PLACEHOLDER_LOC)
    ethernet_window = cq.Workplane("XY").box(
        cfg.MIKROTIK_ETHERNET_WINDOW_WIDTH,
        cfg.MIKROTIK_ETHERNET_WINDOW_DEPTH,
        cfg.MIKROTIK_ETHERNET_WINDOW_HEIGHT,
    ).translate((0, cfg.TRAY_DEPTH / 2 - cfg.MIKROTIK_ETHERNET_WINDOW_REAR_INSET, cfg.MIKROTIK_ETHERNET_WINDOW_Z))
    return tray.union(board).cut(ethernet_window)


def create_mini_pc_tray() -> cq.Workplane:
    tray = create_carriage("mini_pc_tray", cfg.MINI_PC_TRAY_UNITS, ventilation=True, front_handle=True)
    device = rounded_box(
        cfg.MINI_PC_PLACEHOLDER[0],
        cfg.MINI_PC_PLACEHOLDER[1],
        cfg.MODULE_DEVICE_MARKER_HEIGHT,
        cfg.PLACEHOLDER_CHAMFER,
    ).translate(cfg.MINI_PC_PLACEHOLDER_LOC)
    heat_zone = cq.Workplane("XY").box(cfg.MINI_PC_HEAT_ZONE_WIDTH, cfg.MINI_PC_HEAT_ZONE_DEPTH, cfg.MINI_PC_HEAT_ZONE_HEIGHT).translate(
        cfg.MINI_PC_HEAT_ZONE_LOC
    )
    power_window = cq.Workplane("XY").box(
        cfg.MINI_PC_POWER_WINDOW_WIDTH,
        cfg.MINI_PC_POWER_WINDOW_DEPTH,
        cfg.MINI_PC_POWER_WINDOW_HEIGHT,
    ).translate((cfg.MINI_PC_POWER_WINDOW_X, cfg.TRAY_DEPTH / 2 - cfg.MINI_PC_POWER_WINDOW_REAR_INSET, cfg.MINI_PC_POWER_WINDOW_Z))
    return tray.union(device).union(heat_zone).cut(power_window)


TRAY_FACTORIES = {
    "ups_power_tray": create_ups_power_tray,
    "external_ssd_bay": create_external_ssd_bay,
    "ssd_expansion_tray": create_ssd_expansion_tray,
    "raspberry_pi_tray": create_raspberry_pi_tray,
    "mikrotik_tray": create_mikrotik_tray,
    "mini_pc_tray": create_mini_pc_tray,
}
