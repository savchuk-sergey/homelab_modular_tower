"""Modular tray parts."""

import cadquery as cq

from . import config as cfg


def _rounded_box(length: float, width: float, height: float) -> cq.Workplane:
    return cq.Workplane("XY").box(length, width, height).edges("|Z").chamfer(0.8)


def _vent_slots(part: cq.Workplane, rows: int, cols: int, area_length: float, area_width: float) -> cq.Workplane:
    xs = [(-area_length / 2) + i * area_length / max(cols - 1, 1) for i in range(cols)]
    ys = [(-area_width / 2) + i * area_width / max(rows - 1, 1) for i in range(rows)]
    points = [(x, y) for x in xs for y in ys]
    return part.faces(">Z").workplane().pushPoints(points).slot2D(18.0, 4.0, 0).cutThruAll()


def _add_mounting_holes(part: cq.Workplane) -> cq.Workplane:
    x = cfg.TRAY_WIDTH / 2 - 18.0
    y = cfg.TRAY_DEPTH / 2 - 24.0
    points = [(-x, -y), (x, -y), (-x, y), (x, y)]
    return part.faces(">Z").workplane().pushPoints(points).hole(cfg.M3_CLEARANCE)


def _cut_structural_clearances(part: cq.Workplane) -> cq.Workplane:
    """Keep trays clear of rods, guide rails, and the rear service spine."""
    cut_height = cfg.UNIT_HEIGHT * 2.2
    corner = cfg.TRAY_ROD_CORNER_CLEARANCE
    x_edge = cfg.TRAY_WIDTH / 2 - corner / 2
    y_edge = cfg.TRAY_DEPTH / 2 - corner / 2
    cut_z = cut_height / 2 - cfg.UNIT_HEIGHT
    for x in (-x_edge, x_edge):
        for y in (-y_edge, y_edge):
            part = part.cut(cq.Workplane("XY").box(corner, corner, cut_height).translate((x, y, cut_z)))

    service_cut = cq.Workplane("XY").box(
        cfg.TRAY_REAR_SERVICE_CUTOUT_WIDTH,
        cfg.TRAY_REAR_SERVICE_CUTOUT_DEPTH,
        cut_height,
    ).translate((0, cfg.TRAY_DEPTH / 2 - cfg.TRAY_REAR_SERVICE_CUTOUT_DEPTH / 2, cut_z))
    part = part.cut(service_cut)

    rail_cut_y = cfg.TRAY_RAIL_CLEARANCE_DEPTH
    rail_cut_x = cfg.TRAY_RAIL_CLEARANCE_WIDTH
    for x in (-cfg.METAL_RAIL_X_OFFSET, cfg.METAL_RAIL_X_OFFSET):
        for y in (cfg.METAL_RAIL_Y_FRONT, cfg.METAL_RAIL_Y_REAR):
            part = part.cut(cq.Workplane("XY").box(rail_cut_x, rail_cut_y, cut_height).translate((x, y, cut_z)))
    return part


def create_tray(name: str, height_units: float, ventilation: bool = True, front_handle: bool = True) -> cq.Workplane:
    """Create a generic removable tray.

    TODO: Replace generic device mount holes with measured device-specific
    standoff and connector dimensions after physical teardown.
    """
    tray_height = height_units * cfg.UNIT_HEIGHT - cfg.TRAY_CLEARANCE_Z
    base = cq.Workplane("XY").box(cfg.TRAY_WIDTH, cfg.TRAY_DEPTH, cfg.TRAY_BASE_THICKNESS)

    side_z = cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_SIDE_HEIGHT / 2
    left = cq.Workplane("XY").box(cfg.TRAY_SIDE_WALL, cfg.TRAY_DEPTH, cfg.TRAY_SIDE_HEIGHT).translate(
        (-cfg.TRAY_WIDTH / 2 + cfg.TRAY_SIDE_WALL / 2, 0, side_z)
    )
    right = cq.Workplane("XY").box(cfg.TRAY_SIDE_WALL, cfg.TRAY_DEPTH, cfg.TRAY_SIDE_HEIGHT).translate(
        (cfg.TRAY_WIDTH / 2 - cfg.TRAY_SIDE_WALL / 2, 0, side_z)
    )
    front = cq.Workplane("XY").box(cfg.TRAY_WIDTH, cfg.TRAY_SIDE_WALL, min(tray_height, 18.0)).translate(
        (0, -cfg.TRAY_DEPTH / 2 + cfg.TRAY_SIDE_WALL / 2, cfg.TRAY_BASE_THICKNESS / 2 + min(tray_height, 18.0) / 2)
    )
    back_stops = (
        cq.Workplane("XY")
        .box(cfg.TRAY_WIDTH - 24.0, cfg.TRAY_SIDE_WALL, 10.0)
        .translate((0, cfg.TRAY_DEPTH / 2 - cfg.TRAY_SIDE_WALL / 2, cfg.TRAY_BASE_THICKNESS / 2 + 5.0))
    )
    tray = base.union(left).union(right).union(front).union(back_stops)

    if front_handle:
        handle = (
            cq.Workplane("XY")
            .box(64.0, cfg.TRAY_FRONT_LIP, 12.0)
            .translate((0, -cfg.TRAY_DEPTH / 2 - cfg.TRAY_FRONT_LIP / 2, 9.0))
            .edges("|Z")
            .chamfer(1.0)
        )
        tray = tray.union(handle)
        tray = tray.faces("<Y").workplane(centerOption="CenterOfBoundBox").slot2D(38.0, 8.0, 0).cutBlind(-4.0)

    for x in (-32.0, 32.0):
        connector_zone = (
            cq.Workplane("XY")
            .box(26.0, 3.0, 15.0)
            .translate((x, cfg.TRAY_DEPTH / 2 + 0.5, cfg.TRAY_BASE_THICKNESS / 2 + 7.5))
        )
        tray = tray.union(connector_zone)

    # Longitudinal ribs keep tray bases flat in PETG.
    for x in (-45.0, 45.0):
        tray = tray.union(cq.Workplane("XY").box(4.0, cfg.TRAY_DEPTH - 20.0, 5.0).translate((x, 0, 4.0)))

    if ventilation:
        tray = _vent_slots(tray, rows=3, cols=5, area_length=105.0, area_width=85.0)

    tray = _add_mounting_holes(tray)
    tray = _cut_structural_clearances(tray)
    return tray


def create_ups_power_tray() -> cq.Workplane:
    tray = create_tray("ups_power_tray", 2.0, ventilation=True, front_handle=True)
    # Placeholder zones for low-voltage UPS electronics, not exposed mains AC.
    zones = [
        (-38.0, -25.0, cfg.BATTERY_PACK_PLACEHOLDER[0], cfg.BATTERY_PACK_PLACEHOLDER[1], "battery"),
        (48.0, 24.0, 54.0, 38.0, "ups_board"),
        (48.0, -26.0, 42.0, 26.0, "bms"),
        (-50.0, 54.0, 48.0, 24.0, "fuse_block"),
        (-6.0, 58.0, 38.0, 24.0, "dc_dc"),
        (44.0, 62.0, 58.0, 18.0, "terminal_blocks"),
    ]
    for x, y, lx, ly, _ in zones:
        tray = tray.union(cq.Workplane("XY").box(lx, ly, 3.0).translate((x, y, 6.0)))
    for y in (-58.0, 58.0):
        tray = tray.faces(">Z").workplane().pushPoints([(-72.0, y), (72.0, y)]).hole(cfg.M3_CLEARANCE)
    for x in (-64.0, -12.0, 36.0, 70.0):
        tray = tray.faces(">Z").workplane().pushPoints([(x, 0.0)]).slot2D(12.0, 3.0, 0).cutThruAll()
    return tray


def create_external_ssd_bay() -> cq.Workplane:
    tray = create_tray("external_ssd_bay", 1.0, ventilation=True, front_handle=True)
    pocket_outer = cq.Workplane("XY").box(cfg.SSD_POCKET_LENGTH + 6.0, cfg.SSD_POCKET_WIDTH + 6.0, cfg.SSD_POCKET_HEIGHT).translate(
        (-32.0, -22.0, cfg.TRAY_BASE_THICKNESS / 2 + cfg.SSD_POCKET_HEIGHT / 2)
    )
    pocket_inner = cq.Workplane("XY").box(cfg.SSD_POCKET_LENGTH, cfg.SSD_POCKET_WIDTH, cfg.SSD_POCKET_HEIGHT + 2.0).translate(
        (-32.0, -22.0, cfg.TRAY_BASE_THICKNESS / 2 + cfg.SSD_POCKET_HEIGHT / 2 + 1.0)
    )
    tray = tray.union(pocket_outer.cut(pocket_inner))
    tray = tray.faces("<Y").workplane(centerOption="CenterOfBoundBox").circle(10.0).cutBlind(-8.0)
    cable = cq.Workplane("XY").box(12.0, 68.0, 8.0).translate((18.0, 34.0, 8.0))
    tray = tray.cut(cable)
    for x in (-68.0, 6.0):
        tray = tray.faces(">Z").workplane().pushPoints([(x, -22.0)]).slot2D(34.0, 4.0, 0).cutThruAll()
    return tray


def create_ssd_expansion_tray() -> cq.Workplane:
    return create_tray("ssd_expansion_tray", 1.0, ventilation=True, front_handle=True)


def create_raspberry_pi_tray() -> cq.Workplane:
    tray = create_tray("raspberry_pi_tray", 1.0, ventilation=True, front_handle=True)
    board = _rounded_box(cfg.RASPBERRY_PI_PLACEHOLDER[0], cfg.RASPBERRY_PI_PLACEHOLDER[1], 2.0).translate((-24.0, -14.0, 6.0))
    tray = tray.union(board)
    fan_cut = cq.Workplane("XY").box(44.0, 44.0, 2.0).translate((48.0, 30.0, 7.0))
    return tray.union(fan_cut)


def create_mikrotik_tray() -> cq.Workplane:
    tray = create_tray("mikrotik_tray", 1.5, ventilation=True, front_handle=True)
    board = _rounded_box(cfg.MIKROTIK_PLACEHOLDER[0], cfg.MIKROTIK_PLACEHOLDER[1], 2.0).translate((0, -8.0, 6.0))
    ethernet_window = cq.Workplane("XY").box(80.0, 8.0, 14.0).translate((0, cfg.TRAY_DEPTH / 2 - 2.0, 12.0))
    return tray.union(board).cut(ethernet_window)


def create_mini_pc_tray() -> cq.Workplane:
    tray = create_tray("mini_pc_tray", 2.0, ventilation=True, front_handle=True)
    device = _rounded_box(cfg.MINI_PC_PLACEHOLDER[0], cfg.MINI_PC_PLACEHOLDER[1], 3.0).translate((0, -8.0, 7.0))
    heat_zone = cq.Workplane("XY").box(76.0, 54.0, 4.0).translate((25.0, 10.0, 11.0))
    power_window = cq.Workplane("XY").box(18.0, 8.0, 14.0).translate((-54.0, cfg.TRAY_DEPTH / 2 - 2.0, 13.0))
    return tray.union(device).union(heat_zone).cut(power_window)


TRAY_FACTORIES = {
    "ups_power_tray": create_ups_power_tray,
    "external_ssd_bay": create_external_ssd_bay,
    "ssd_expansion_tray": create_ssd_expansion_tray,
    "raspberry_pi_tray": create_raspberry_pi_tray,
    "mikrotik_tray": create_mikrotik_tray,
    "mini_pc_tray": create_mini_pc_tray,
}
