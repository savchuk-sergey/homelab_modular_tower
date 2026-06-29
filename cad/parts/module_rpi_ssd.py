"""mk0.12 Raspberry Pi + external SSD printable stack module."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg
from cad.parts import stack_interface as si


def _make_rpi_support() -> cq.Workplane:
    return si.union_all(
        [
            si.make_rect_outline(
                cfg.RPI3B_CENTER_X,
                cfg.RPI3B_CENTER_Y,
                cfg.RPI3B_CLEARANCE_WIDTH,
                cfg.RPI3B_CLEARANCE_DEPTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ),
            si.make_rpi_bosses(),
        ]
    )


def _make_ssd_support() -> cq.Workplane:
    cx = cfg.EXTERNAL_SSD_PREFERRED_CENTER_X
    cy = cfg.EXTERNAL_SSD_PREFERRED_CENTER_Y
    rail_y = cfg.EXTERNAL_SSD_DEPTH / 2 - cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH / 2
    anchor_x = cfg.MIN_STRAP_PULL_TAB_ACCESS_WIDTH / 2 + cfg.SKELETON_SSD_STRAP_ANCHOR_WIDTH / 2
    return si.union_all(
        [
            si.box_at_z(
                cfg.EXTERNAL_SSD_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ).translate((cx, cy - rail_y, 0.0)),
            si.box_at_z(
                cfg.EXTERNAL_SSD_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH,
                cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT,
                0.0,
            ).translate((cx, cy + rail_y, 0.0)),
            si.box_at_z(
                cfg.SKELETON_SSD_STRAP_ANCHOR_WIDTH,
                cfg.SKELETON_SSD_STRAP_ANCHOR_DEPTH,
                cfg.SKELETON_DEVICE_RETAINER_RIB_HEIGHT,
                0.0,
            ).translate((cx - anchor_x, cy, 0.0)),
            si.box_at_z(
                cfg.SKELETON_SSD_STRAP_ANCHOR_WIDTH,
                cfg.SKELETON_SSD_STRAP_ANCHOR_DEPTH,
                cfg.SKELETON_DEVICE_RETAINER_RIB_HEIGHT,
                0.0,
            ).translate((cx + anchor_x, cy, 0.0)),
        ]
    )


def _make_rear_window_lips() -> cq.Workplane:
    lip_y = cfg.REAR_SERVICE_ZONE_Y_MIN + cfg.STRUCTURAL_WALL_THICKNESS / 2
    return si.union_all(
        [
            si.box_at_z(
                cfg.SKELETON_REAR_SERVICE_WINDOW_WIDTH,
                cfg.STRUCTURAL_WALL_THICKNESS,
                cfg.RIB_HEIGHT_MAX,
                0.0,
            ).translate((0.0, lip_y, 0.0)),
            si.box_at_z(
                cfg.SKELETON_RPI_CABLE_WINDOW_WIDTH,
                cfg.STRUCTURAL_WALL_THICKNESS,
                cfg.SKELETON_RPI_CABLE_WINDOW_HEIGHT,
                0.0,
            ).translate(
                (
                    (cfg.RPI_SSD_CABLE_CORRIDOR_X_MIN + cfg.RPI_SSD_CABLE_CORRIDOR_X_MAX) / 2,
                    cfg.RPI_SSD_CABLE_CORRIDOR_Y_MAX,
                    0.0,
                )
            ),
        ]
    )


def _make_device_support_connectors() -> cq.Workplane:
    return si.union_all(
        [
            si.box_at_z(
                cfg.TOWER_OUTER_WIDTH - 2 * cfg.STRUCTURAL_WALL_THICKNESS,
                cfg.RIB_THICKNESS,
                cfg.RIB_HEIGHT_MIN,
                0.0,
            ).translate((0.0, cfg.RPI3B_CENTER_Y, 0.0)),
            si.box_at_z(
                cfg.RPI3B_BOARD_WIDTH,
                cfg.RIB_THICKNESS,
                cfg.SKELETON_RPI_BOSS_HEIGHT,
                0.0,
            ).translate((cfg.RPI3B_CENTER_X, cfg.RPI3B_CENTER_Y - cfg.RPI3B_BOARD_DEPTH / 2 + 6.0, 0.0)),
            si.box_at_z(
                cfg.RPI3B_BOARD_WIDTH,
                cfg.RIB_THICKNESS,
                cfg.SKELETON_RPI_BOSS_HEIGHT,
                0.0,
            ).translate((cfg.RPI3B_CENTER_X, cfg.RPI3B_CENTER_Y + cfg.RPI3B_BOARD_DEPTH / 2 - 6.0, 0.0)),
            si.box_at_z(
                cfg.RIB_THICKNESS,
                cfg.TOWER_OUTER_DEPTH - 2 * cfg.STRUCTURAL_WALL_THICKNESS,
                cfg.RIB_HEIGHT_MIN,
                0.0,
            ).translate((cfg.RPI3B_CENTER_X, 0.0, 0.0)),
            si.box_at_z(
                cfg.TOWER_OUTER_WIDTH - 2 * cfg.STRUCTURAL_WALL_THICKNESS,
                cfg.RIB_THICKNESS,
                cfg.RIB_HEIGHT_MIN,
                0.0,
            ).translate((0.0, cfg.EXTERNAL_SSD_PREFERRED_CENTER_Y, 0.0)),
            si.box_at_z(
                cfg.RIB_THICKNESS,
                cfg.TOWER_OUTER_DEPTH - 2 * cfg.STRUCTURAL_WALL_THICKNESS,
                cfg.RIB_HEIGHT_MIN,
                0.0,
            ).translate((cfg.RPI_SSD_CABLE_CORRIDOR_X_MIN, 0.0, 0.0)),
        ]
    )


def build_rpi_ssd_stack_module() -> cq.Workplane:
    """Build one connected printable open-tray RPi/SSD module."""
    module = si.union_all(
        [
            si.make_perimeter_frame(cfg.RPI_SSD_MODULE_HEIGHT),
            si.make_corner_compression_islands(cfg.RPI_SSD_MODULE_HEIGHT),
            si.make_corner_to_frame_ribs(),
            si.make_transverse_ribs((-55.0, 20.0), length=150.0),
            si.make_longitudinal_ribs((-58.0, 58.0), length=130.0),
            _make_rpi_support(),
            _make_ssd_support(),
            _make_device_support_connectors(),
            _make_rear_window_lips(),
        ]
    )
    module = si.cut_rear_service_window(module, cfg.RPI_SSD_MODULE_HEIGHT, cfg.SKELETON_REAR_SERVICE_WINDOW_HEIGHT)
    module = si.cut_rear_cable_window(
        module,
        cfg.SKELETON_RPI_CABLE_WINDOW_WIDTH,
        cfg.SKELETON_RPI_CABLE_WINDOW_HEIGHT,
        cfg.TRAY_FLOOR_THICKNESS,
    )
    module = si.make_washer_seats(module, cfg.RPI_SSD_MODULE_HEIGHT, top=True, bottom=True)
    return si.make_m5_clearance_holes(module, cfg.RPI_SSD_MODULE_HEIGHT).tag("rpi_ssd_stack_module_mk012")
