"""Cooling panels and Mini PC priority duct."""

import cadquery as cq

from cad import config as cfg


def make_fan_grille(name: str, intake_filter: bool = False) -> cq.Workplane:
    grille = cq.Workplane("XY").box(cfg.OUTER_WIDTH, cfg.OUTER_DEPTH, cfg.FAN_GRILLE_THICKNESS)
    grille = grille.faces(">Z").workplane().circle(cfg.FAN_SIZE / 2).cutThruAll()

    d = cfg.FAN_HOLE_SPACING / 2
    fan_screws = [(x, y) for x in (-d, d) for y in (-d, d)]
    grille = grille.faces(">Z").workplane().pushPoints(fan_screws).hole(cfg.FAN_SCREW_DIAMETER)

    for x in cfg.FAN_GRILLE_BAR_X:
        grille = grille.union(
            cq.Workplane("XY")
            .box(cfg.FAN_GRILLE_BAR_WIDTH, cfg.FAN_SIZE - cfg.FAN_GRILLE_BAR_LENGTH_INSET, cfg.FAN_GRILLE_THICKNESS)
            .translate((x, 0, 0))
        )
    for y in cfg.FAN_GRILLE_BAR_Y:
        grille = grille.union(
            cq.Workplane("XY")
            .box(cfg.FAN_SIZE - cfg.FAN_GRILLE_BAR_LENGTH_INSET, cfg.FAN_GRILLE_BAR_WIDTH, cfg.FAN_GRILLE_THICKNESS)
            .translate((0, y, 0))
        )

    if intake_filter:
        rail_y = cfg.FAN_SIZE / 2 + cfg.FILTER_RAIL_OFFSET
        for y in (-rail_y, rail_y):
            grille = grille.union(
                cq.Workplane("XY")
                .box(cfg.FAN_SIZE + cfg.FILTER_RAIL_LENGTH_ALLOWANCE, cfg.FILTER_RAIL_WIDTH, cfg.FILTER_RAIL_HEIGHT)
                .translate((0, y, cfg.FAN_GRILLE_THICKNESS / 2 + cfg.FILTER_RAIL_HEIGHT / 2))
            )
    return grille.edges("|Z").chamfer(cfg.FAN_PANEL_EDGE_CHAMFER).tag(name)


def make_bottom_fan_grille() -> cq.Workplane:
    return make_fan_grille("bottom_fan_grille", intake_filter=True)


def make_top_fan_grille() -> cq.Workplane:
    return make_fan_grille("top_fan_grille", intake_filter=False)


def make_bottom_fan_cartridge() -> cq.Workplane:
    """Create a removable lower intake cartridge for a standard 120 mm fan."""
    cartridge = cq.Workplane("XY").box(
        cfg.BOTTOM_FAN_CARTRIDGE_WIDTH,
        cfg.BOTTOM_FAN_CARTRIDGE_DEPTH,
        cfg.BOTTOM_FAN_CARTRIDGE_HEIGHT,
    )
    cartridge = cartridge.faces(">Z").workplane().circle(cfg.FAN_120_AIR_OPENING_DIAMETER / 2).cutThruAll()

    d = cfg.FAN_120_HOLE_SPACING / 2
    fan_screws = [(x, y) for x in (-d, d) for y in (-d, d)]
    cartridge = cartridge.faces(">Z").workplane().pushPoints(fan_screws).hole(cfg.FAN_120_HOLE_DIAMETER)

    rail_y = (
        cfg.BOTTOM_FAN_CARTRIDGE_DEPTH / 2
        + cfg.BOTTOM_FAN_CARTRIDGE_RAIL_WIDTH / 2
        - cfg.BOTTOM_FAN_CARTRIDGE_FEATURE_OVERLAP
    )
    rail_z = (
        cfg.BOTTOM_FAN_CARTRIDGE_HEIGHT / 2
        + cfg.BOTTOM_FAN_CARTRIDGE_RAIL_HEIGHT / 2
        - cfg.BOTTOM_FAN_CARTRIDGE_FEATURE_OVERLAP
    )
    for y in (-rail_y, rail_y):
        cartridge = cartridge.union(
            cq.Workplane("XY")
            .box(
                cfg.BOTTOM_FAN_CARTRIDGE_WIDTH,
                cfg.BOTTOM_FAN_CARTRIDGE_RAIL_WIDTH,
                cfg.BOTTOM_FAN_CARTRIDGE_RAIL_HEIGHT,
            )
            .translate((0, y, rail_z))
        )

    handle = cq.Workplane("XY").box(
        cfg.BOTTOM_FAN_CARTRIDGE_SERVICE_PULL,
        cfg.BOTTOM_FAN_CARTRIDGE_RAIL_WIDTH,
        cfg.BOTTOM_FAN_CARTRIDGE_RAIL_HEIGHT,
    )
    cartridge = cartridge.union(
        handle.translate(
            (
                0,
                -rail_y,
                rail_z,
            )
        )
    )

    mount = cfg.BOTTOM_FAN_CARTRIDGE_MOUNT_OFFSET
    mount_points = [(x, y) for x in (-mount, mount) for y in (-mount, mount)]
    cartridge = cartridge.faces(">Z").workplane().pushPoints(mount_points).hole(cfg.M3_CLEARANCE)
    return cartridge.tag("bottom_fan_cartridge")


def make_bottom_filter_frame() -> cq.Workplane:
    frame = cq.Workplane("XY").box(
        cfg.BOTTOM_FILTER_FRAME_WIDTH,
        cfg.BOTTOM_FILTER_FRAME_DEPTH,
        cfg.BOTTOM_FILTER_FRAME_HEIGHT,
    )
    frame = frame.faces(">Z").workplane().circle(cfg.FAN_120_AIR_OPENING_DIAMETER / 2).cutThruAll()
    return frame.tag("bottom_filter_frame")


def make_bottom_filter_retainer() -> cq.Workplane:
    retainer = cq.Workplane("XY").box(
        cfg.BOTTOM_FILTER_RETAINER_WIDTH,
        cfg.BOTTOM_FILTER_RETAINER_WIDTH,
        cfg.BOTTOM_FILTER_RETAINER_HEIGHT,
    )
    filter_window = cq.Workplane("XY").box(
        cfg.BOTTOM_FILTER_RETAINER_WIDTH - 2 * cfg.BOTTOM_FILTER_RETAINER_DEPTH,
        cfg.BOTTOM_FILTER_RETAINER_WIDTH - 2 * cfg.BOTTOM_FILTER_RETAINER_DEPTH,
        cfg.BOTTOM_FILTER_RETAINER_HEIGHT + cfg.FILLET_RADIUS,
    )
    retainer = retainer.cut(filter_window)

    clip_offset = cfg.BOTTOM_FILTER_RETAINER_WIDTH / 2 - cfg.BOTTOM_FILTER_CORNER_CLIP_SIZE / 2
    for x in (-clip_offset, clip_offset):
        for y in (-clip_offset, clip_offset):
            pad = cq.Workplane("XY").box(
                cfg.BOTTOM_FILTER_CORNER_CLIP_SIZE,
                cfg.BOTTOM_FILTER_CORNER_CLIP_SIZE,
                cfg.BOTTOM_FILTER_RETAINER_HEIGHT,
            )
            retainer = retainer.union(pad.translate((x, y, 0)))
    return retainer.tag("bottom_filter_retainer")


def make_mini_pc_airflow_duct_placeholder() -> cq.Workplane:
    outer = cq.Workplane("XY").box(cfg.DUCT_WIDTH, cfg.DUCT_DEPTH, cfg.DUCT_HEIGHT)
    inner = cq.Workplane("XY").box(
        cfg.DUCT_WIDTH - 2 * cfg.DUCT_WALL,
        cfg.DUCT_DEPTH + cfg.DUCT_CUTTER_OVERLAP,
        cfg.DUCT_HEIGHT - 2 * cfg.DUCT_WALL,
    )
    duct = outer.cut(inner)

    # Removable tabs let the duct screw into the tray area without trapping it.
    for x in (-cfg.DUCT_WIDTH / 2 - cfg.DUCT_TAB_OFFSET_X, cfg.DUCT_WIDTH / 2 + cfg.DUCT_TAB_OFFSET_X):
        tab = cq.Workplane("XY").box(cfg.DUCT_TAB_WIDTH, cfg.DUCT_TAB_DEPTH, cfg.DUCT_TAB_HEIGHT).translate(
            (x, -cfg.DUCT_DEPTH / 2 + cfg.DUCT_TAB_OFFSET_Y, -cfg.DUCT_HEIGHT / 2 + cfg.DUCT_TAB_OFFSET_Z)
        )
        duct = duct.union(tab)
        duct = duct.faces("<Z").workplane(centerOption="CenterOfBoundBox").pushPoints(
            [(x, -cfg.DUCT_DEPTH / 2 + cfg.DUCT_TAB_OFFSET_Y)]
        ).hole(cfg.M3_CLEARANCE)
    return duct.edges("|Z").chamfer(cfg.DUCT_EDGE_CHAMFER)


def create_fan_panel(name: str, intake_filter: bool = False) -> cq.Workplane:
    return make_fan_grille(name, intake_filter=intake_filter)


def create_bottom_fan_panel() -> cq.Workplane:
    return make_bottom_fan_grille()


def create_top_fan_panel() -> cq.Workplane:
    return make_top_fan_grille()


def create_bottom_fan_cartridge() -> cq.Workplane:
    return make_bottom_fan_cartridge()


def create_bottom_filter_frame() -> cq.Workplane:
    return make_bottom_filter_frame()


def create_bottom_filter_retainer() -> cq.Workplane:
    return make_bottom_filter_retainer()


def create_mini_pc_airflow_duct() -> cq.Workplane:
    return make_mini_pc_airflow_duct_placeholder()
