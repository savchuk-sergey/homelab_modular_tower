"""Geometry-only airflow review placeholders for mk0.9."""

import cadquery as cq

from cad import config as cfg


def make_central_airflow_channel_placeholder(c=cfg) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .box(c.AIRFLOW_CHANNEL_WIDTH, c.AIRFLOW_CHANNEL_DEPTH, c.TOWER_HEIGHT)
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, c.TOWER_HEIGHT / 2))
        .tag("central_airflow_channel_placeholder")
    )


def make_airflow_clearance_zone(c=cfg) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .box(c.AIRFLOW_CHANNEL_WIDTH + 12.0, c.AIRFLOW_CHANNEL_DEPTH + 12.0, c.TOWER_HEIGHT)
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, c.TOWER_HEIGHT / 2))
        .tag("airflow_clearance_zone")
    )


def make_simplified_airflow_guide(c=cfg) -> cq.Workplane:
    guide = None
    for z in (
        c.BASE_MODULE_HEIGHT,
        c.BASE_MODULE_HEIGHT + c.RPI_SSD_MODULE_HEIGHT,
        c.BASE_MODULE_HEIGHT + c.RPI_SSD_MODULE_HEIGHT + c.MINI_PC_MODULE_HEIGHT,
    ):
        marker = cq.Workplane("XY").circle(5.0).extrude(24.0).translate((0, -c.REAR_RESERVED_DEPTH / 2, z - 12.0))
        guide = marker if guide is None else guide.union(marker)
    return guide.tag("simplified_airflow_guide")
