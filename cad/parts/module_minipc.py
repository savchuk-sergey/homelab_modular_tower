"""mk0.12 Mini PC printable stack module."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg
from cad.parts import stack_interface as si


def _make_minipc_support() -> cq.Workplane:
    cx = cfg.MINIPC_CENTER_X
    cy = cfg.MINIPC_CENTER_Y
    rail_x = cfg.MINIPC_WIDTH / 2 - cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH / 2
    front_y = cy - cfg.MINIPC_DEPTH / 2 + cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH / 2
    rear_y = cy + cfg.MINIPC_DEPTH / 2 - cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH / 2
    retainer_y = cy - cfg.MINIPC_DEPTH / 2 - cfg.MIN_RETAINER_CLEARANCE_AROUND_SCREW_OR_CLIP
    return si.union_all(
        [
            si.box_at_z(
                cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH,
                cfg.MINIPC_DEPTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ).translate((cx - rail_x, cy, 0.0)),
            si.box_at_z(
                cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH,
                cfg.MINIPC_DEPTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ).translate((cx + rail_x, cy, 0.0)),
            si.box_at_z(
                cfg.MINIPC_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ).translate((cx, front_y, 0.0)),
            si.box_at_z(
                cfg.MINIPC_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ).translate((cx, rear_y, 0.0)),
            si.box_at_z(
                cfg.SKELETON_MINIPC_RETAINER_WIDTH,
                cfg.SKELETON_MINIPC_RETAINER_DEPTH,
                cfg.SKELETON_DEVICE_RETAINER_RIB_HEIGHT,
                0.0,
            ).translate((-cfg.MIN_FINGER_ACCESS_SLOT_WIDTH / 2, retainer_y, 0.0)),
            si.box_at_z(
                cfg.SKELETON_MINIPC_RETAINER_WIDTH,
                cfg.SKELETON_MINIPC_RETAINER_DEPTH,
                cfg.SKELETON_DEVICE_RETAINER_RIB_HEIGHT,
                0.0,
            ).translate((cfg.MIN_FINGER_ACCESS_SLOT_WIDTH / 2, retainer_y, 0.0)),
        ]
    )


def _make_side_bypass_edges() -> cq.Workplane:
    slot_center_x = cfg.MINIPC_CLEARANCE_WIDTH / 2 + cfg.SKELETON_MINIPC_BYPASS_SLOT_WIDTH / 2
    return si.union_all(
        [
            si.box_at_z(
                cfg.SKELETON_MINIPC_BYPASS_SLOT_WIDTH,
                cfg.SKELETON_MINIPC_BYPASS_SLOT_LENGTH,
                cfg.RIB_HEIGHT_MAX,
                0.0,
            ).translate((-slot_center_x, cfg.MINIPC_CENTER_Y, 0.0)),
            si.box_at_z(
                cfg.SKELETON_MINIPC_BYPASS_SLOT_WIDTH,
                cfg.SKELETON_MINIPC_BYPASS_SLOT_LENGTH,
                cfg.RIB_HEIGHT_MAX,
                0.0,
            ).translate((slot_center_x, cfg.MINIPC_CENTER_Y, 0.0)),
        ]
    )


def build_minipc_stack_module() -> cq.Workplane:
    """Build one connected printable open-tray Mini PC module."""
    module = si.union_all(
        [
            si.make_perimeter_frame(cfg.MINIPC_MODULE_HEIGHT),
            si.make_corner_compression_islands(cfg.MINIPC_MODULE_HEIGHT),
            si.make_corner_to_frame_ribs(),
            si.make_transverse_ribs((-70.0, 42.0), length=150.0),
            si.make_longitudinal_ribs((-58.0, 58.0), length=130.0),
            _make_side_bypass_edges(),
            _make_minipc_support(),
        ]
    )
    module = si.cut_rear_service_window(module, cfg.MINIPC_MODULE_HEIGHT, cfg.SKELETON_REAR_SERVICE_WINDOW_HEIGHT)
    module = si.cut_rear_cable_window(
        module,
        cfg.SKELETON_MINIPC_REAR_EXIT_WIDTH,
        cfg.SKELETON_MINIPC_REAR_EXIT_HEIGHT,
        cfg.TRAY_FLOOR_THICKNESS,
    )
    module = si.make_washer_seats(module, cfg.MINIPC_MODULE_HEIGHT, top=True, bottom=True)
    return si.make_m5_clearance_holes(module, cfg.MINIPC_MODULE_HEIGHT).tag("minipc_stack_module_mk012")
