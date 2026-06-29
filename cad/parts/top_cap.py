"""mk0.12 top cap skeleton."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg
from cad.parts import stack_interface as si


def build_top_cap() -> cq.Workplane:
    """Build the upper mk0.12 stack-through-rod cap skeleton."""
    cap = si.union_all(
        [
            si.make_perimeter_frame(cfg.TOP_CAP_HEIGHT, cfg.SKELETON_BASE_TOP_FRAME_HEIGHT),
            si.make_corner_compression_islands(cfg.TOP_CAP_HEIGHT),
            si.make_corner_to_frame_ribs(),
            si.make_transverse_ribs((-36.0, 36.0), length=150.0),
            si.make_longitudinal_ribs((-36.0, 36.0), length=130.0),
            si.make_fan_ring(),
            si.make_fan_ring_spokes(),
        ]
    )
    cap = si.add_fan_screw_bosses(cap)
    cap = si.cut_rear_service_window(cap, cfg.TOP_CAP_HEIGHT)
    cap = si.make_washer_seats(cap, cfg.TOP_CAP_HEIGHT, top=True, bottom=True)
    return si.make_m5_clearance_holes(cap, cfg.TOP_CAP_HEIGHT).tag("top_cap_mk012")
