"""Airflow duct for Mini PC priority cooling."""

import cadquery as cq

from . import config as cfg


def create_mini_pc_airflow_duct() -> cq.Workplane:
    outer = cq.Workplane("XY").box(cfg.DUCT_WIDTH, cfg.DUCT_DEPTH, cfg.DUCT_HEIGHT)
    inner = cq.Workplane("XY").box(
        cfg.DUCT_WIDTH - 2 * cfg.DUCT_WALL,
        cfg.DUCT_DEPTH + 2.0,
        cfg.DUCT_HEIGHT - 2 * cfg.DUCT_WALL,
    )
    duct = outer.cut(inner)

    # Removable tabs let the duct screw into the tray area without trapping it.
    for x in (-cfg.DUCT_WIDTH / 2 - 8.0, cfg.DUCT_WIDTH / 2 + 8.0):
        tab = cq.Workplane("XY").box(14.0, 20.0, 4.0).translate((x, -cfg.DUCT_DEPTH / 2 + 16.0, -cfg.DUCT_HEIGHT / 2 + 8.0))
        duct = duct.union(tab)
        duct = duct.faces("<Z").workplane(centerOption="CenterOfBoundBox").pushPoints([(x, -cfg.DUCT_DEPTH / 2 + 16.0)]).hole(cfg.M3_CLEARANCE)
    return duct.edges("|Z").chamfer(0.8)
