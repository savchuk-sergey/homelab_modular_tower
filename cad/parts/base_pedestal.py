"""mk0.12 base pedestal skeleton."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg
from cad.parts import stack_interface as si


def _add_tpu_foot_pad_placeholders(workplane: cq.Workplane) -> cq.Workplane:
    result = workplane
    offset = cfg.TPU_FOOT_CENTER_OFFSET_PREFERRED
    for center_x, center_y in ((-offset, -offset), (offset, -offset), (-offset, offset), (offset, offset)):
        foot = si.box_at_z(
            cfg.TPU_FOOT_SIZE_X,
            cfg.TPU_FOOT_SIZE_Y,
            cfg.SKELETON_FOOT_PAD_HEIGHT,
            cfg.BASE_PEDESTAL_Z_MIN,
        ).translate((center_x, center_y, cfg.BASE_PEDESTAL_Z_MIN))
        result = result.union(foot)
    return result


def build_base_pedestal() -> cq.Workplane:
    """Build the lower mk0.12 stack-through-rod base pedestal skeleton."""
    pedestal = si.union_all(
        [
            si.make_perimeter_frame(cfg.BASE_PEDESTAL_HEIGHT, cfg.SKELETON_BASE_TOP_FRAME_HEIGHT),
            si.make_corner_compression_islands(cfg.BASE_PEDESTAL_HEIGHT),
            si.make_corner_to_frame_ribs(),
            si.make_transverse_ribs((-36.0, 36.0), length=150.0),
            si.make_longitudinal_ribs((-36.0, 36.0), length=130.0),
            si.make_fan_ring(),
            si.make_fan_ring_spokes(),
        ]
    )
    pedestal = si.add_fan_screw_bosses(pedestal)
    pedestal = si.cut_rear_service_window(pedestal, cfg.BASE_PEDESTAL_HEIGHT)
    pedestal = _add_tpu_foot_pad_placeholders(pedestal)
    pedestal = si.make_washer_seats(pedestal, cfg.BASE_PEDESTAL_HEIGHT, top=True, bottom=True)
    return si.make_m5_clearance_holes(pedestal, cfg.BASE_PEDESTAL_HEIGHT).tag("base_pedestal_mk012")
