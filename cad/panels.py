"""Side and fan panels."""

import cadquery as cq

from . import config as cfg


def _perforate_panel(panel: cq.Workplane, length: float, height: float, rows: int, cols: int) -> cq.Workplane:
    xs = [(-length / 2) + i * length / max(cols - 1, 1) for i in range(cols)]
    zs = [(-height / 2) + i * height / max(rows - 1, 1) for i in range(rows)]
    points = [(x, z) for x in xs for z in zs]
    return panel.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(points).slot2D(14.0, 3.5, 0).cutThruAll()


def create_side_panel(name: str = "left_side_panel") -> cq.Workplane:
    panel = cq.Workplane("XY").box(cfg.OUTER_DEPTH, cfg.PANEL_THICKNESS, cfg.SIDE_PANEL_HEIGHT)
    panel = _perforate_panel(panel, cfg.OUTER_DEPTH - 42.0, cfg.SIDE_PANEL_HEIGHT - 70.0, rows=9, cols=8)
    mount_points = [(-78.0, -122.0), (78.0, -122.0), (-78.0, 122.0), (78.0, 122.0)]
    panel = panel.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(mount_points).hole(cfg.M3_CLEARANCE)
    return panel.edges("|Z").chamfer(0.5).tag(name)


def create_left_side_panel() -> cq.Workplane:
    return create_side_panel("left_side_panel")


def create_right_side_panel() -> cq.Workplane:
    return create_side_panel("right_side_panel")


def create_fan_panel(name: str, intake_filter: bool = False) -> cq.Workplane:
    panel = cq.Workplane("XY").box(cfg.OUTER_WIDTH, cfg.OUTER_DEPTH, cfg.FAN_PANEL_THICKNESS)
    panel = panel.faces(">Z").workplane().circle(cfg.FAN_SIZE / 2).cutThruAll()
    fan_screws = []
    d = cfg.FAN_HOLE_SPACING / 2
    for x in (-d, d):
        for y in (-d, d):
            fan_screws.append((x, y))
    panel = panel.faces(">Z").workplane().pushPoints(fan_screws).hole(cfg.FAN_SCREW_DIAMETER)

    # Simple printable grille bars across the 120 mm opening.
    for x in (-45.0, -22.5, 0.0, 22.5, 45.0):
        panel = panel.union(cq.Workplane("XY").box(4.0, cfg.FAN_SIZE - 16.0, cfg.FAN_PANEL_THICKNESS).translate((x, 0, 0)))
    for y in (-45.0, 0.0, 45.0):
        panel = panel.union(cq.Workplane("XY").box(cfg.FAN_SIZE - 16.0, 4.0, cfg.FAN_PANEL_THICKNESS).translate((0, y, 0)))

    if intake_filter:
        rail_y = cfg.FAN_SIZE / 2 + 8.0
        for y in (-rail_y, rail_y):
            panel = panel.union(
                cq.Workplane("XY")
                .box(cfg.FAN_SIZE + 18.0, 3.0, cfg.FILTER_RAIL_HEIGHT)
                .translate((0, y, cfg.FAN_PANEL_THICKNESS / 2 + cfg.FILTER_RAIL_HEIGHT / 2))
            )
    return panel.edges("|Z").chamfer(0.6).tag(name)


def create_bottom_fan_panel() -> cq.Workplane:
    return create_fan_panel("bottom_fan_panel", intake_filter=True)


def create_top_fan_panel() -> cq.Workplane:
    return create_fan_panel("top_fan_panel", intake_filter=False)
