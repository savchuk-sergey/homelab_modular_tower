"""M5 threaded rod placeholders and rod layout."""

import cadquery as cq

from .. import config as cfg


def rod_positions() -> list[tuple[float, float]]:
    x = cfg.TOWER_WIDTH / 2 - cfg.ROD_CENTER_OFFSET
    y = cfg.TOWER_DEPTH / 2 - cfg.ROD_CENTER_OFFSET
    return [(-x, -y), (x, -y), (x, y), (-x, y)]


def create_m5_threaded_rod(height: float = cfg.ROD_LENGTH) -> cq.Workplane:
    """Placeholder for a vertical metal M5 threaded rod."""
    return cq.Workplane("XY").circle(cfg.ROD_DIAMETER / 2).extrude(height)


def create_m5_threaded_rod_cap() -> cq.Workplane:
    """Printable protective cap placeholder for exposed M5 rod ends."""
    cap = cq.Workplane("XY").circle(cfg.ROD_CAP_DIAMETER / 2).extrude(cfg.ROD_CAP_HEIGHT)
    bore = cq.Workplane("XY").circle(cfg.ROD_CLEARANCE / 2).extrude(cfg.ROD_CAP_HEIGHT + cfg.FILLET_RADIUS)
    return cap.cut(bore).tag("m5_threaded_rod_cap")
