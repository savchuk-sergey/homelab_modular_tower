"""Cooling panels and Mini PC priority duct."""

import cadquery as cq

from .. import config as cfg


def create_fan_panel(name: str, intake_filter: bool = False) -> cq.Workplane:
    panel = cq.Workplane("XY").box(cfg.OUTER_WIDTH, cfg.OUTER_DEPTH, cfg.FAN_PANEL_THICKNESS)
    panel = panel.faces(">Z").workplane().circle(cfg.FAN_SIZE / 2).cutThruAll()

    d = cfg.FAN_HOLE_SPACING / 2
    fan_screws = [(x, y) for x in (-d, d) for y in (-d, d)]
    panel = panel.faces(">Z").workplane().pushPoints(fan_screws).hole(cfg.FAN_SCREW_DIAMETER)

    for x in cfg.FAN_GRILLE_BAR_X:
        panel = panel.union(
            cq.Workplane("XY")
            .box(cfg.FAN_GRILLE_BAR_WIDTH, cfg.FAN_SIZE - cfg.FAN_GRILLE_BAR_LENGTH_INSET, cfg.FAN_PANEL_THICKNESS)
            .translate((x, 0, 0))
        )
    for y in cfg.FAN_GRILLE_BAR_Y:
        panel = panel.union(
            cq.Workplane("XY")
            .box(cfg.FAN_SIZE - cfg.FAN_GRILLE_BAR_LENGTH_INSET, cfg.FAN_GRILLE_BAR_WIDTH, cfg.FAN_PANEL_THICKNESS)
            .translate((0, y, 0))
        )

    if intake_filter:
        rail_y = cfg.FAN_SIZE / 2 + cfg.FILTER_RAIL_OFFSET
        for y in (-rail_y, rail_y):
            panel = panel.union(
                cq.Workplane("XY")
                .box(cfg.FAN_SIZE + cfg.FILTER_RAIL_LENGTH_ALLOWANCE, cfg.FILTER_RAIL_WIDTH, cfg.FILTER_RAIL_HEIGHT)
                .translate((0, y, cfg.FAN_PANEL_THICKNESS / 2 + cfg.FILTER_RAIL_HEIGHT / 2))
            )
    return panel.edges("|Z").chamfer(cfg.FAN_PANEL_EDGE_CHAMFER).tag(name)


def create_bottom_fan_panel() -> cq.Workplane:
    return create_fan_panel("bottom_fan_panel", intake_filter=True)


def create_top_fan_panel() -> cq.Workplane:
    return create_fan_panel("top_fan_panel", intake_filter=False)


def create_mini_pc_airflow_duct() -> cq.Workplane:
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
