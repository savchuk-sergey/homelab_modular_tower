"""Generic removable carriage geometry shared by all module trays."""

import cadquery as cq

from .. import config as cfg


def cut_vent_slots(part: cq.Workplane, rows: int, cols: int, area_length: float, area_width: float) -> cq.Workplane:
    xs = [(-area_length / 2) + i * area_length / max(cols - 1, 1) for i in range(cols)]
    ys = [(-area_width / 2) + i * area_width / max(rows - 1, 1) for i in range(rows)]
    points = [(x, y) for x in xs for y in ys]
    return part.faces(">Z").workplane().pushPoints(points).slot2D(
        cfg.TRAY_VENT_SLOT_LENGTH, cfg.TRAY_VENT_SLOT_WIDTH, 0
    ).cutThruAll()


def add_mounting_holes(part: cq.Workplane) -> cq.Workplane:
    x = cfg.TRAY_WIDTH / 2 - cfg.TRAY_MOUNT_HOLE_OFFSET_X
    y = cfg.TRAY_DEPTH / 2 - cfg.TRAY_MOUNT_HOLE_OFFSET_Y
    points = [(-x, -y), (x, -y), (-x, y), (x, y)]
    return part.faces(">Z").workplane().pushPoints(points).hole(cfg.M3_CLEARANCE)


def make_carriage_handle_cutout() -> cq.Workplane:
    """Recessed grip pocket cutter for the standardized tray front plate."""
    front_y = -cfg.TRAY_DEPTH / 2 + cfg.CARRIAGE_HANDLE_DEPTH / 2
    handle_z = cfg.TRAY_BASE_THICKNESS + cfg.CARRIAGE_HANDLE_TOP_BRIDGE + cfg.CARRIAGE_HANDLE_HEIGHT / 2
    return (
        cq.Workplane("XY")
        .box(cfg.CARRIAGE_HANDLE_WIDTH, cfg.CARRIAGE_HANDLE_DEPTH, cfg.CARRIAGE_HANDLE_HEIGHT)
        .translate((0, front_y, handle_z))
        .edges("|Y")
        .fillet(cfg.CARRIAGE_HANDLE_CORNER_RADIUS)
    )


def make_carriage_lock_boss() -> cq.Workplane:
    """Internal M3-ready boss for a future screw, TPU plug, latch, or magnet."""
    boss_y = -cfg.TRAY_DEPTH / 2 + cfg.CARRIAGE_FRONT_PLATE_THICKNESS + cfg.CARRIAGE_LOCK_BOSS_THICKNESS / 2
    boss_z = cfg.TRAY_BASE_THICKNESS + cfg.CARRIAGE_LOCK_OFFSET_Y
    boss = cq.Solid.makeCylinder(
        cfg.CARRIAGE_LOCK_BOSS_DIAMETER / 2,
        cfg.CARRIAGE_LOCK_BOSS_THICKNESS,
        cq.Vector(cfg.CARRIAGE_LOCK_OFFSET_X, boss_y - cfg.CARRIAGE_LOCK_BOSS_THICKNESS / 2, boss_z),
        cq.Vector(0, 1, 0),
    )
    return cq.Workplane("XY").add(boss)


def make_carriage_front_plate(plate_height: float) -> cq.Workplane:
    """Create the removable tray service flange with a recessed pull pocket."""
    front_y = -cfg.TRAY_DEPTH / 2 + cfg.CARRIAGE_FRONT_PLATE_THICKNESS / 2
    plate = (
        cq.Workplane("XY")
        .box(cfg.TRAY_WIDTH, cfg.CARRIAGE_FRONT_PLATE_THICKNESS, plate_height)
        .translate((0, front_y, cfg.TRAY_BASE_THICKNESS / 2 + plate_height / 2))
    )

    plate = plate.cut(make_carriage_handle_cutout())

    rib_z = cfg.TRAY_BASE_THICKNESS + cfg.CARRIAGE_HANDLE_TOP_BRIDGE + cfg.CARRIAGE_HANDLE_HEIGHT / 2
    rib_y = -cfg.TRAY_DEPTH / 2 + cfg.CARRIAGE_FRONT_PLATE_THICKNESS + cfg.CARRIAGE_HANDLE_FILLET / 2
    rib_height = cfg.CARRIAGE_HANDLE_HEIGHT + 2 * cfg.CARRIAGE_HANDLE_TOP_BRIDGE
    rib_x = cfg.CARRIAGE_HANDLE_WIDTH / 2 + cfg.CARRIAGE_HANDLE_SIDE_RIB / 2
    for x in (-rib_x, rib_x):
        plate = plate.union(
            cq.Workplane("XY")
            .box(cfg.CARRIAGE_HANDLE_SIDE_RIB, cfg.CARRIAGE_HANDLE_FILLET, rib_height)
            .translate((x, rib_y, rib_z))
        )

    bridge_z = cfg.TRAY_BASE_THICKNESS + cfg.CARRIAGE_HANDLE_TOP_BRIDGE + cfg.CARRIAGE_HANDLE_HEIGHT
    plate = plate.union(
        cq.Workplane("XY")
        .box(
            cfg.CARRIAGE_HANDLE_WIDTH + 2 * cfg.CARRIAGE_HANDLE_SIDE_RIB,
            cfg.CARRIAGE_HANDLE_FILLET,
            cfg.CARRIAGE_HANDLE_TOP_BRIDGE,
        )
        .translate((0, rib_y, bridge_z + cfg.CARRIAGE_HANDLE_TOP_BRIDGE / 2))
    )

    plate = plate.union(make_carriage_lock_boss())
    lock_hole_z = (
        cfg.TRAY_BASE_THICKNESS
        + cfg.CARRIAGE_LOCK_OFFSET_Y
        - (cfg.TRAY_BASE_THICKNESS / 2 + plate_height / 2)
    )
    plate = plate.faces("<Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(cfg.CARRIAGE_LOCK_OFFSET_X, lock_hole_z)]
    ).hole(cfg.CARRIAGE_LOCK_HOLE_DIAMETER)
    return plate.edges("|Y").fillet(cfg.CARRIAGE_HANDLE_FILLET)


def cut_structural_clearances(part: cq.Workplane) -> cq.Workplane:
    """Keep carriages clear of rods, guide rails, and the rear service spine."""
    cut_height = cfg.TRAY_STRUCTURAL_CLEARANCE_HEIGHT
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

    for x in (-cfg.METAL_RAIL_X_OFFSET, cfg.METAL_RAIL_X_OFFSET):
        for y in (cfg.METAL_RAIL_Y_FRONT, cfg.METAL_RAIL_Y_REAR):
            rail_cut = cq.Workplane("XY").box(
                cfg.TRAY_RAIL_CLEARANCE_WIDTH,
                cfg.TRAY_RAIL_CLEARANCE_DEPTH,
                cut_height,
            )
            part = part.cut(rail_cut.translate((x, y, cut_z)))
    return part


def create_carriage(name: str, height_units: float, ventilation: bool = True, front_handle: bool = True) -> cq.Workplane:
    """Create the common removable carriage body used by every module."""
    tray_height = height_units * cfg.UNIT_HEIGHT - cfg.TRAY_CLEARANCE_Z
    base = cq.Workplane("XY").box(cfg.TRAY_WIDTH, cfg.TRAY_DEPTH, cfg.TRAY_BASE_THICKNESS)

    side_z = cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_SIDE_HEIGHT / 2
    left = cq.Workplane("XY").box(cfg.TRAY_SIDE_WALL, cfg.TRAY_DEPTH, cfg.TRAY_SIDE_HEIGHT).translate(
        (-cfg.TRAY_WIDTH / 2 + cfg.TRAY_SIDE_WALL / 2, 0, side_z)
    )
    right = cq.Workplane("XY").box(cfg.TRAY_SIDE_WALL, cfg.TRAY_DEPTH, cfg.TRAY_SIDE_HEIGHT).translate(
        (cfg.TRAY_WIDTH / 2 - cfg.TRAY_SIDE_WALL / 2, 0, side_z)
    )
    front = make_carriage_front_plate(min(tray_height, cfg.CARRIAGE_FRONT_PLATE_HEIGHT))
    back_stops = (
        cq.Workplane("XY")
        .box(cfg.TRAY_WIDTH - cfg.TRAY_BACK_STOP_WIDTH_INSET, cfg.TRAY_SIDE_WALL, cfg.TRAY_BACK_STOP_HEIGHT)
        .translate(
            (
                0,
                cfg.TRAY_DEPTH / 2 - cfg.TRAY_SIDE_WALL / 2,
                cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_BACK_STOP_HEIGHT / 2,
            )
        )
    )
    tray = base.union(left).union(right).union(front).union(back_stops)

    if not front_handle:
        tray = tray.cut(front)

    for x in cfg.TRAY_REAR_CONNECTOR_ZONE_X:
        connector_zone = (
            cq.Workplane("XY")
            .box(cfg.TRAY_REAR_CONNECTOR_ZONE_WIDTH, cfg.TRAY_REAR_CONNECTOR_ZONE_DEPTH, cfg.TRAY_REAR_CONNECTOR_ZONE_HEIGHT)
            .translate(
                (
                    x,
                    cfg.TRAY_DEPTH / 2 + cfg.TRAY_REAR_CONNECTOR_ZONE_Y_OVERHANG,
                    cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_REAR_CONNECTOR_ZONE_HEIGHT / 2,
                )
            )
        )
        tray = tray.union(connector_zone)

    # Longitudinal ribs keep tray bases flat in PETG.
    for x in cfg.TRAY_BASE_RIB_X:
        tray = tray.union(
            cq.Workplane("XY")
            .box(cfg.TRAY_BASE_RIB_WIDTH, cfg.TRAY_DEPTH - cfg.TRAY_BASE_RIB_LENGTH_INSET, cfg.TRAY_BASE_RIB_HEIGHT)
            .translate((x, 0, cfg.TRAY_BASE_RIB_Z))
        )

    if ventilation:
        tray = cut_vent_slots(
            tray,
            rows=cfg.TRAY_VENT_ROWS,
            cols=cfg.TRAY_VENT_COLS,
            area_length=cfg.TRAY_VENT_AREA_LENGTH,
            area_width=cfg.TRAY_VENT_AREA_WIDTH,
        )

    tray = add_mounting_holes(tray)
    tray = cut_structural_clearances(tray)
    return tray
