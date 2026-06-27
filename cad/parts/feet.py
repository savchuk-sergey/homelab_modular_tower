"""Removable TPU feet for bottom intake clearance."""

import cadquery as cq

from .. import config as cfg


def make_foot() -> cq.Workplane:
    """Create one removable foot with an M5 through-hole and bottom counterbore."""
    foot = cq.Workplane("XY").circle(cfg.FOOT_DIAMETER / 2).extrude(cfg.FOOT_HEIGHT)
    foot = foot.translate((0, 0, -cfg.FOOT_HEIGHT / 2))

    screw_cutter = cq.Workplane("XY").circle(cfg.FOOT_SCREW_DIAMETER / 2).extrude(
        cfg.FOOT_HEIGHT + cfg.FILLET_RADIUS * 2
    )
    screw_cutter = screw_cutter.translate((0, 0, -cfg.FOOT_HEIGHT / 2 - cfg.FILLET_RADIUS))
    foot = foot.cut(screw_cutter)

    counterbore = cq.Workplane("XY").circle(cfg.FOOT_COUNTERBORE_DIAMETER / 2).extrude(
        cfg.FOOT_COUNTERBORE_DEPTH + cfg.FILLET_RADIUS
    )
    counterbore = counterbore.translate((0, 0, -cfg.FOOT_HEIGHT / 2 - cfg.FILLET_RADIUS / 2))
    foot = foot.cut(counterbore)

    return foot.tag("foot")


def create_foot() -> cq.Workplane:
    return make_foot()
