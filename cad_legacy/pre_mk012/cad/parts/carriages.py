"""Generic removable carriage geometry shared by all module trays.

mk0.9.3 uses lightweight open-frame carriages with replaceable
perpendicular POM-C shoe runners riding inside aluminum U-channel rails.
Legacy tray functions are kept for backward compatibility.
"""

import cadquery as cq

from .. import config as cfg


# ---------------------------------------------------------------------------
# Legacy mk0.9 tray helpers (kept for backward compatibility)
# ---------------------------------------------------------------------------

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
    """Internal M3 heat-set-insert boss for the standardized front lock screw."""
    boss_y = -cfg.TRAY_DEPTH / 2 + cfg.CARRIAGE_FRONT_PLATE_THICKNESS + cfg.CARRIAGE_LOCK_BOSS_THICKNESS / 2
    boss_z = cfg.TRAY_BASE_THICKNESS + cfg.CARRIAGE_LOCK_OFFSET_Y
    boss = cq.Solid.makeCylinder(
        cfg.CARRIAGE_LOCK_BOSS_DIAMETER / 2,
        cfg.CARRIAGE_LOCK_BOSS_THICKNESS,
        cq.Vector(cfg.CARRIAGE_LOCK_OFFSET_X, boss_y - cfg.CARRIAGE_LOCK_BOSS_THICKNESS / 2, boss_z),
        cq.Vector(0, 1, 0),
    )
    boss_part = cq.Workplane("XY").add(boss)
    insert_cutter = cq.Solid.makeCylinder(
        cfg.MODULE_LOCK_INSERT_OUTER_DIAMETER / 2,
        cfg.MODULE_LOCK_INSERT_DEPTH,
        cq.Vector(cfg.CARRIAGE_LOCK_OFFSET_X, boss_y - cfg.MODULE_LOCK_INSERT_DEPTH / 2, boss_z),
        cq.Vector(0, 1, 0),
    )
    return boss_part.cut(cq.Workplane("XY").add(insert_cutter))


def make_anti_slide_tab() -> cq.Workplane:
    """Small front underside stop that resists accidental forward tray walk-out."""
    return (
        cq.Workplane("XY")
        .box(
            cfg.MODULE_LOCK_ANTI_SLIDE_TAB_WIDTH,
            cfg.MODULE_LOCK_ANTI_SLIDE_TAB_DEPTH,
            cfg.MODULE_LOCK_ANTI_SLIDE_TAB_HEIGHT,
        )
        .translate(
            (
                0,
                -cfg.TRAY_DEPTH / 2 + cfg.CARRIAGE_FRONT_PLATE_THICKNESS + cfg.MODULE_LOCK_ANTI_SLIDE_TAB_DEPTH / 2,
                -cfg.MODULE_LOCK_ANTI_SLIDE_TAB_HEIGHT / 2,
            )
        )
    )


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
    return plate


def make_tray_handle(plate_height: float) -> cq.Workplane:
    return make_carriage_front_plate(plate_height)


def make_tray_front_lock() -> cq.Workplane:
    return make_carriage_lock_boss()


def make_tray_rear_stop() -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .box(cfg.TRAY_WIDTH - cfg.TRAY_BACK_STOP_WIDTH_INSET, cfg.TRAY_STOP_DEPTH, cfg.TRAY_BACK_STOP_HEIGHT)
        .translate(
            (
                0,
                cfg.TRAY_DEPTH / 2 - cfg.TRAY_STOP_DEPTH / 2,
                cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_BACK_STOP_HEIGHT / 2,
            )
        )
    )


def make_tray_cable_exit() -> cq.Workplane:
    cut_height = cfg.TRAY_STRUCTURAL_CLEARANCE_HEIGHT
    cut_z = cut_height / 2 - cfg.UNIT_HEIGHT
    return cq.Workplane("XY").box(
        cfg.REAR_CABLE_EXIT_WIDTH,
        cfg.TRAY_REAR_SERVICE_CUTOUT_DEPTH,
        cut_height,
    ).translate((0, cfg.TRAY_DEPTH / 2 - cfg.TRAY_REAR_SERVICE_CUTOUT_DEPTH / 2, cut_z))


def make_module_rails() -> cq.Workplane:
    rails = cq.Workplane("XY")
    rail_z = cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_BASE_RIB_HEIGHT / 2
    for x in (-cfg.RAIL_OFFSET_X, cfg.RAIL_OFFSET_X):
        rails = rails.union(
            cq.Workplane("XY")
            .box(cfg.TRAY_BASE_RIB_WIDTH, cfg.TRAY_DEPTH - cfg.TRAY_BASE_RIB_LENGTH_INSET, cfg.TRAY_BASE_RIB_HEIGHT)
            .translate((x, 0, rail_z))
        )
    return rails


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

    part = part.cut(make_tray_cable_exit())

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
    front = make_tray_handle(min(tray_height, cfg.CARRIAGE_FRONT_PLATE_HEIGHT))
    back_stops = make_tray_rear_stop()
    tray = base.union(left).union(right).union(front).union(back_stops)
    tray = tray.union(make_anti_slide_tab())

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

    tray = tray.union(make_module_rails())

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
    return tray.tag(name)


def make_standard_tray_base(
    name: str,
    height_units: float,
    ventilation: bool = True,
    front_handle: bool = True,
) -> cq.Workplane:
    return create_carriage(name, height_units, ventilation=ventilation, front_handle=front_handle)


def make_module_tray(name: str, height_units: float, ventilation: bool = True, front_handle: bool = True) -> cq.Workplane:
    """mk0.3 standardized blade module tray factory."""
    return make_standard_tray_base(name, height_units, ventilation=ventilation, front_handle=front_handle)


# ---------------------------------------------------------------------------
# mk0.9.2 open-frame carriage with perpendicular POM-C shoe runners
# ---------------------------------------------------------------------------

def make_pom_c_shoe_socket(c=cfg) -> cq.Workplane:
    """Socket/boss in PETG carriage side wall for replaceable POM-C shoe.

    The socket is a blind hole with a slight interference relief so the
    POM-C shoe can be pressed in by hand but is retained by the clamp screw.
    """
    d = c.RUNNER_SOCKET_DIAMETER
    h = c.RUNNER_SOCKET_DEPTH
    boss_d = c.CARRIAGE_RUNNER_BOSS_DIAMETER
    boss_h = c.CARRIAGE_RUNNER_BOSS_THICKNESS

    boss = cq.Workplane("XY").circle(boss_d / 2).extrude(boss_h)
    socket = cq.Workplane("XY").circle(d / 2).extrude(h + 0.02).translate((0, 0, -0.01))
    return boss.cut(socket).tag("pom_c_shoe_socket")


def make_pom_c_shoe_clamp(c=cfg) -> cq.Workplane:
    """M3 clamp screw / mechanical retention feature.

    A small printed bridge with an M3 clearance hole.  The screw is
    threaded into a heat-set insert in the boss wall; it clamps or stops
    the POM-C shoe but does NOT thread into POM-C.
    """
    bridge = cq.Workplane("XY").box(
        c.CARRIAGE_CLAMP_BRIDGE_WIDTH,
        c.CARRIAGE_CLAMP_BRIDGE_DEPTH,
        c.CARRIAGE_CLAMP_BRIDGE_HEIGHT,
    )
    bridge = bridge.faces(">Z").workplane().hole(c.RUNNER_RETENTION_SCREW_CLEARANCE)
    insert_boss = (
        cq.Workplane("XY")
        .circle(c.CARRIAGE_CLAMP_INSERT_BOSS_DIAMETER / 2)
        .extrude(c.CARRIAGE_CLAMP_INSERT_BOSS_HEIGHT)
        .translate((0, 0, -c.CARRIAGE_CLAMP_INSERT_BOSS_HEIGHT / 2))
    )
    insert_bore = (
        cq.Workplane("XY")
        .circle(c.HEAT_SET_INSERT_M3_DIAMETER / 2)
        .extrude(c.CARRIAGE_CLAMP_INSERT_BOSS_HEIGHT + 0.02)
        .translate((0, 0, -c.CARRIAGE_CLAMP_INSERT_BOSS_HEIGHT / 2 - 0.01))
    )
    insert_boss = insert_boss.cut(insert_bore)
    lip = cq.Workplane("XY").box(
        c.CARRIAGE_CLAMP_LIP_WIDTH,
        c.CARRIAGE_CLAMP_LIP_DEPTH,
        c.CARRIAGE_CLAMP_LIP_HEIGHT,
    ).translate((0, c.CARRIAGE_CLAMP_LIP_OFFSET_Y, c.CARRIAGE_CLAMP_LIP_OFFSET_Z))
    return bridge.union(insert_boss).union(lip).tag("pom_c_shoe_clamp")


def make_carriage_side_shoe_mounts(shoes_per_side: int, c=cfg) -> cq.Workplane:
    """Add reinforced side sockets for perpendicular POM-C shoes.

    Shoes are arranged along the side wall of the carriage, spaced evenly.
    """
    side_length = c.MODULE_DEPTH - c.CARRIAGE_SHOE_END_INSET
    if shoes_per_side <= 1:
        spacing = 0.0
        offsets = [0.0]
    else:
        spacing = side_length / (shoes_per_side - 1)
        offsets = [-side_length / 2 + i * spacing for i in range(shoes_per_side)]

    mounts = cq.Workplane("XY")
    x = c.MODULE_WIDTH / 2 - c.CARRIAGE_WALL_THICKNESS / 2
    for sign in (-1, 1):
        for y in offsets:
            mount = make_pom_c_shoe_socket(c).translate((sign * x, y, c.CARRIAGE_RUNNER_BOSS_THICKNESS / 2))
            rib = cq.Workplane("XY").box(
                c.CARRIAGE_RUNNER_BOSS_DIAMETER + c.CARRIAGE_RUNNER_BOSS_RIB_EXTRA_WIDTH,
                c.CARRIAGE_RUNNER_BOSS_RIB_THICKNESS,
                c.CARRIAGE_RUNNER_BOSS_THICKNESS,
            ).translate((sign * x, y, c.CARRIAGE_RUNNER_BOSS_THICKNESS / 2))
            mount = mount.union(rib)
            clamp = make_pom_c_shoe_clamp(c).translate((sign * x, y, c.CARRIAGE_RUNNER_BOSS_THICKNESS))
            mount = mount.union(clamp)
            mounts = mounts.union(mount)
    return mounts.tag("carriage_side_shoe_mounts")


def make_lightweight_open_frame_carriage(
    name: str = "lightweight_open_frame_carriage",
    shoes_per_side: int = cfg.RUNNER_SHOES_PER_SIDE_RPI_SSD,
    device_mode: str = "generic",
    c=cfg,
    width: float | None = None,
    depth: float | None = None,
) -> cq.Workplane:
    """Lightweight PETG open-frame carriage with large airflow window.

    Instead of a solid floor, the carriage has a peripheral frame,
    local support pads, and side shoe mounts.
    """
    width = c.MODULE_TRAY_WIDTH if width is None else width
    depth = c.MODULE_TRAY_DEPTH if depth is None else depth

    outer = cq.Workplane("XY").box(width, depth, c.CARRIAGE_WALL_THICKNESS)
    inner_clear = cq.Workplane("XY").box(
        width - 2 * c.CARRIAGE_SIDE_WALL_THICKNESS,
        depth - 2 * c.CARRIAGE_SIDE_WALL_THICKNESS,
        c.CARRIAGE_WALL_THICKNESS + 0.02,
    )
    frame = outer.cut(inner_clear)

    wall_h = c.CARRIAGE_FRONT_LIP_HEIGHT
    front = cq.Workplane("XY").box(width, c.CARRIAGE_WALL_THICKNESS, wall_h).translate(
        (0, -depth / 2 + c.CARRIAGE_WALL_THICKNESS / 2, wall_h / 2)
    )
    rear = cq.Workplane("XY").box(width, c.CARRIAGE_WALL_THICKNESS, wall_h).translate(
        (0, depth / 2 - c.CARRIAGE_WALL_THICKNESS / 2, wall_h / 2)
    )
    left = cq.Workplane("XY").box(c.CARRIAGE_WALL_THICKNESS, depth - 2 * c.CARRIAGE_WALL_THICKNESS, wall_h).translate(
        (-width / 2 + c.CARRIAGE_WALL_THICKNESS / 2, 0, wall_h / 2)
    )
    right = cq.Workplane("XY").box(c.CARRIAGE_WALL_THICKNESS, depth - 2 * c.CARRIAGE_WALL_THICKNESS, wall_h).translate(
        (width / 2 - c.CARRIAGE_WALL_THICKNESS / 2, 0, wall_h / 2)
    )
    carriage = frame.union(front).union(rear).union(left).union(right)

    carriage = carriage.union(make_carriage_side_shoe_mounts(shoes_per_side, c))

    # front pull lip / handle bridge
    lip = (
        cq.Workplane("XY")
        .box(c.CARRIAGE_PULL_LIP_WIDTH, c.CARRIAGE_PULL_LIP_DEPTH, c.CARRIAGE_PULL_LIP_HEIGHT)
        .translate((0, -depth / 2 - c.CARRIAGE_PULL_LIP_FRONT_OFFSET, c.CARRIAGE_PULL_LIP_Z))
    )
    carriage = carriage.union(lip)

    lock_z = c.CARRIAGE_FRONT_LIP_HEIGHT / 2
    carriage = carriage.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(0, lock_z)]
    ).hole(c.CARRIAGE_LOCK_SCREW_CLEARANCE)

    cable_exit = cq.Workplane("XY").box(
        c.REAR_CABLE_EXIT_WIDTH,
        c.CARRIAGE_WALL_THICKNESS + 0.02,
        c.REAR_CABLE_EXIT_HEIGHT,
    ).translate((0, depth / 2, c.CARRIAGE_FRONT_LIP_HEIGHT / 2))
    carriage = carriage.cut(cable_exit)

    return carriage.tag(name)


def make_rpi_ssd_carriage(c=cfg) -> cq.Workplane:
    """RPi + SSD carriage with 2 POM-C shoes per side (4 total).

    Includes:
    * open-frame tray
    * 4 replaceable POM-C shoe runners
    * front pull lip
    * M3 front lock screw
    * rear cable exit
    * local support pads for RPi 3B and external SSD
    * large central airflow window
    """
    carriage = make_lightweight_open_frame_carriage(
        name="rpi_ssd_carriage",
        shoes_per_side=c.RUNNER_SHOES_PER_SIDE_RPI_SSD,
        device_mode="rpi_ssd",
        c=c,
    )

    # local support pads for RPi 3B (4 standoffs) and external SSD (2 rails)
    pad_z = c.CARRIAGE_WALL_THICKNESS / 2
    # RPi standoff pads
    hx = c.RPI3B_BOARD_WIDTH / 2 - c.RPI3B_MOUNT_HOLE_OFFSET_X
    hy = c.RPI3B_BOARD_DEPTH / 2 - c.RPI3B_MOUNT_HOLE_OFFSET_Y
    origin = (c.RPI3_PLACEHOLDER_X, c.RPI3_PLACEHOLDER_Y)
    for px, py in [(origin[0] + dx, origin[1] + dy) for dx in (-hx, hx) for dy in (-hy, hy)]:
        pad = cq.Workplane("XY").circle(c.RPI3_STANDOFF_DIAMETER / 2).extrude(c.RPI3_STANDOFF_HEIGHT)
        bore = cq.Workplane("XY").circle(c.RPI3_STANDOFF_HOLE / 2).extrude(c.RPI3_STANDOFF_HEIGHT + 0.02)
        pad = pad.cut(bore).translate((px, py, pad_z))
        carriage = carriage.union(pad)

    # SSD retainer rails
    center = (c.EXTERNAL_SSD_PLACEHOLDER_X, c.EXTERNAL_SSD_PLACEHOLDER_Y)
    for sx in (
        -c.EXTERNAL_SSD_PLACEHOLDER_WIDTH / 2 - c.SSD_RETAINER_THICKNESS,
        c.EXTERNAL_SSD_PLACEHOLDER_WIDTH / 2 + c.SSD_RETAINER_THICKNESS,
    ):
        rail = (
            cq.Workplane("XY")
            .box(c.SSD_RETAINER_THICKNESS, c.EXTERNAL_SSD_PLACEHOLDER_DEPTH + c.FRAME_HEIGHT, c.SSD_RETAINER_HEIGHT)
            .translate((center[0] + sx, center[1], pad_z + c.SSD_RETAINER_HEIGHT / 2))
        )
        carriage = carriage.union(rail)

    # zip-tie slots through the frame near SSD
    for sx in (-c.ZIP_TIE_SLOT_LENGTH, c.ZIP_TIE_SLOT_LENGTH):
        slot = cq.Workplane("XY").box(c.ZIP_TIE_SLOT_LENGTH, c.ZIP_TIE_SLOT_WIDTH, c.CARRIAGE_WALL_THICKNESS + 0.02).translate(
            (center[0] + sx, center[1], pad_z)
        )
        carriage = carriage.cut(slot)

    return carriage.tag("rpi_ssd_carriage")


def make_mini_pc_placeholder_carriage(c=cfg) -> cq.Workplane:
    """Mini PC placeholder carriage with 3 POM-C shoes per side (6 total).

    Includes:
    * open-frame placeholder tray
    * 6 replaceable POM-C shoe runners
    * large airflow window
    * placeholder support pads
    * rear clearance
    * front pull lip
    * M3 front lock screw
    """
    carriage = make_lightweight_open_frame_carriage(
        name="mini_pc_placeholder_carriage",
        shoes_per_side=c.RUNNER_SHOES_PER_SIDE_MINI_PC,
        device_mode="mini_pc_placeholder",
        c=c,
    )

    # local support pads for mini PC placeholder (4 corners)
    pad_z = c.CARRIAGE_WALL_THICKNESS / 2
    cx = c.MINI_PC_PLACEHOLDER_WIDTH / 2 + c.MINI_PC_PLACEHOLDER_CLEARANCE
    cy = c.MINI_PC_PLACEHOLDER_DEPTH / 2 + c.MINI_PC_PLACEHOLDER_CLEARANCE
    center_y = -c.REAR_RESERVED_DEPTH / 2
    for dx, dy in [(-cx, -cy), (cx, -cy), (cx, cy), (-cx, cy)]:
        pad = (
            cq.Workplane("XY")
            .circle(c.MINI_PC_SUPPORT_PAD_RADIUS)
            .extrude(c.MINI_PC_SUPPORT_PAD_HEIGHT)
            .translate((dx, center_y + dy, pad_z))
        )
        carriage = carriage.union(pad)

    # front and rear placeholder retainers (low rails)
    front_y = center_y - cy
    rear_y = center_y + cy
    for py in (front_y, rear_y):
        rail = (
            cq.Workplane("XY")
            .box(c.MINI_PC_PLACEHOLDER_WIDTH * 0.72, c.SSD_RETAINER_THICKNESS, c.MINI_PC_RETAINER_HEIGHT)
            .translate((0, py, pad_z + c.MINI_PC_RETAINER_HEIGHT / 2))
        )
        carriage = carriage.union(rail)

    return carriage.tag("mini_pc_placeholder_carriage")
