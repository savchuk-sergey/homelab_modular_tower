"""Parametric engineering review geometry for mk0.6."""

import cadquery as cq

from .. import config as cfg
from . import feet


def _arrow(name: str, height: float) -> cq.Workplane:
    shaft = cq.Workplane("XY").circle(cfg.AIRFLOW_ARROW_DIAMETER / 2).extrude(height)
    head = cq.Solid.makeCone(
        cfg.AIRFLOW_ARROW_DIAMETER,
        0.0,
        cfg.AIRFLOW_ARROW_DIAMETER * 1.6,
        cq.Vector(0, 0, height),
        cq.Vector(0, 0, 1),
    )
    return shaft.union(cq.Workplane("XY").add(head)).tag(name)


def make_airflow_path_review() -> cq.Workplane:
    review = cq.Workplane("XY")
    for z in cfg.AIRFLOW_ARROW_Z:
        review = review.union(_arrow("airflow_arrow", cfg.AIRFLOW_ARROW_HEIGHT).translate((0, 0, z)))
    for x, y, z in cfg.TEMPERATURE_SENSOR_POINTS:
        sensor = cq.Workplane("XY").circle(cfg.TEMPERATURE_SENSOR_BOSS_DIAMETER / 2).extrude(
            cfg.TEMPERATURE_SENSOR_BOSS_HEIGHT
        )
        review = review.union(sensor.translate((x, y, z)))
    return review.tag("airflow_path_review")


def make_mini_pc_airflow_path_review() -> cq.Workplane:
    return _arrow("mini_pc_airflow_path_review", cfg.AIRFLOW_ARROW_HEIGHT).rotate(
        (0, 0, 0), (1, 0, 0), 90
    ).translate((cfg.MINI_PC_AIRFLOW_ARROW_X, cfg.MINI_PC_AIRFLOW_ARROW_Y, cfg.STABILITY_COM_Z))


def make_blocked_air_zones_review() -> cq.Workplane:
    zone = cq.Workplane("XY")
    for x in (-cfg.REAR_SPINE_WIDTH / 2, cfg.REAR_SPINE_WIDTH / 2):
        zone = zone.union(
            cq.Workplane("XY")
            .box(cfg.BLOCKED_AIR_ZONE_WIDTH, cfg.BLOCKED_AIR_ZONE_DEPTH, cfg.BLOCKED_AIR_ZONE_HEIGHT)
            .translate((x, cfg.OUTER_DEPTH / 2 - cfg.BLOCKED_AIR_ZONE_DEPTH / 2, cfg.TOWER_HEIGHT / 2))
        )
    return zone.tag("blocked_air_zones_review")


def make_stability_review() -> cq.Workplane:
    support = cq.Workplane("XY").box(cfg.BASE_WIDTH, cfg.BASE_DEPTH, cfg.MIN_PRINTABLE_FEATURE)
    margin = cq.Workplane("XY").box(
        cfg.BASE_WIDTH - 2 * cfg.STABILITY_MARGIN,
        cfg.BASE_DEPTH - 2 * cfg.STABILITY_MARGIN,
        cfg.MIN_PRINTABLE_FEATURE,
    ).translate((0, 0, cfg.MIN_PRINTABLE_FEATURE))
    com = cq.Workplane("XY").sphere(cfg.STABILITY_COM_MARKER_DIAMETER / 2).translate(
        (cfg.STABILITY_COM_X, cfg.STABILITY_COM_Y, cfg.STABILITY_COM_Z)
    )
    extended_tray = cq.Workplane("XY").box(cfg.MODULE_WIDTH, cfg.MODULE_DEPTH, cfg.TRAY_BASE_THICKNESS).translate(
        (0, cfg.STABILITY_SERVICE_TRAY_Y, cfg.TOWER_HEIGHT - cfg.UNIT_HEIGHT)
    )
    return support.union(margin).union(com).union(extended_tray).tag("stability_review")


def make_printability_layout_review() -> cq.Workplane:
    gap = cfg.BASE_PRINT_LAYOUT_GAP
    layout = feet.make_central_bottom_fan_frame()
    layout = layout.union(
        feet.make_left_foot_extension().translate(
            (-(cfg.BASE_CENTER_FRAME_WIDTH + cfg.FOOT_EXTENSION_X + cfg.BASE_WING_OVERLAP) / 2 - gap, 0, 0)
        )
    )
    layout = layout.union(
        feet.make_right_foot_extension().translate(
            ((cfg.BASE_CENTER_FRAME_WIDTH + cfg.FOOT_EXTENSION_X + cfg.BASE_WING_OVERLAP) / 2 + gap, 0, 0)
        )
    )
    layout = layout.union(
        feet.make_front_stability_wing().translate((0, -(cfg.BASE_CENTER_FRAME_DEPTH + cfg.FOOT_EXTENSION_Y) / 2 - gap, 0))
    )
    layout = layout.union(
        feet.make_rear_stability_wing().translate((0, (cfg.BASE_CENTER_FRAME_DEPTH + cfg.FOOT_EXTENSION_Y) / 2 + gap, 0))
    )
    return layout.tag("printability_layout_review")
