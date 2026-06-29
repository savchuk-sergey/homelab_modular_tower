"""Shared mk0.12 stack-through-rod geometry helpers."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg


def m5_rod_centers() -> list[tuple[float, float]]:
    return cfg.m5_rod_centers()


def fan_screw_centers() -> list[tuple[float, float]]:
    return cfg.fan_screw_centers()


def box_at_z(width: float, depth: float, height: float, z_min: float) -> cq.Workplane:
    return cq.Workplane("XY").box(width, depth, height).translate((0.0, 0.0, z_min + height / 2))


def cylinder_at_z(diameter: float, height: float, center_x: float, center_y: float, z_min: float) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .center(center_x, center_y)
        .circle(diameter / 2)
        .extrude(height)
        .translate((0.0, 0.0, z_min))
    )


def union_all(parts: list[cq.Workplane]) -> cq.Workplane:
    if not parts:
        raise ValueError("union_all requires at least one part")
    result = parts[0]
    for part in parts[1:]:
        result = result.union(part)
    return result


def make_perimeter_frame(height: float, frame_height: float | None = None) -> cq.Workplane:
    wall = cfg.STRUCTURAL_WALL_THICKNESS
    z_height = frame_height or min(height, cfg.SKELETON_PERIMETER_FRAME_HEIGHT)
    half_w = cfg.TOWER_OUTER_WIDTH / 2
    half_d = cfg.TOWER_OUTER_DEPTH / 2
    inner_depth = cfg.TOWER_OUTER_DEPTH - 2 * wall
    return union_all(
        [
            box_at_z(cfg.TOWER_OUTER_WIDTH, wall, z_height, 0.0).translate((0.0, half_d - wall / 2, 0.0)),
            box_at_z(cfg.TOWER_OUTER_WIDTH, wall, z_height, 0.0).translate((0.0, -half_d + wall / 2, 0.0)),
            box_at_z(wall, inner_depth, z_height, 0.0).translate((half_w - wall / 2, 0.0, 0.0)),
            box_at_z(wall, inner_depth, z_height, 0.0).translate((-half_w + wall / 2, 0.0, 0.0)),
        ]
    )


def make_corner_compression_islands(height: float) -> cq.Workplane:
    diameter = cfg.CORNER_COMPRESSION_PAD_SIZE_X
    return union_all(
        [
            cylinder_at_z(diameter, height, center_x, center_y, 0.0)
            for center_x, center_y in m5_rod_centers()
        ]
    )


def make_m5_clearance_holes(workplane: cq.Workplane, height: float) -> cq.Workplane:
    result = workplane
    cutter_height = height + cfg.SKELETON_CUTTER_OVERLAP
    z_min = -cfg.SKELETON_CUTTER_OVERLAP / 2
    for center_x, center_y in m5_rod_centers():
        result = result.cut(cylinder_at_z(cfg.M5_ROD_CLEARANCE_DIAMETER, cutter_height, center_x, center_y, z_min))
    return result


def make_washer_seats(workplane: cq.Workplane, height: float, *, top: bool = True, bottom: bool = True) -> cq.Workplane:
    result = workplane
    cutter_height = cfg.M5_WASHER_SEAT_DEPTH + cfg.SKELETON_CUTTER_OVERLAP
    if bottom:
        for center_x, center_y in m5_rod_centers():
            result = result.cut(
                cylinder_at_z(
                    cfg.M5_WASHER_SEAT_DIAMETER,
                    cutter_height,
                    center_x,
                    center_y,
                    -cfg.SKELETON_CUTTER_OVERLAP / 2,
                )
            )
    if top:
        for center_x, center_y in m5_rod_centers():
            result = result.cut(
                cylinder_at_z(
                    cfg.M5_WASHER_SEAT_DIAMETER,
                    cutter_height,
                    center_x,
                    center_y,
                    height - cfg.M5_WASHER_SEAT_DEPTH,
                )
            )
    return result


def make_corner_to_frame_ribs() -> cq.Workplane:
    rib_h = cfg.RIB_HEIGHT_MAX
    rib_t = cfg.RIB_THICKNESS
    parts: list[cq.Workplane] = []
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            cx = sx * cfg.M5_ROD_CENTER_OFFSET_X
            cy = sy * cfg.M5_ROD_CENTER_OFFSET_Y
            parts.append(box_at_z(rib_t, cfg.TOWER_OUTER_DEPTH - 2 * abs(cy), rib_h, 0.0).translate((cx, sy * 87.5, 0.0)))
            parts.append(box_at_z(cfg.TOWER_OUTER_WIDTH - 2 * abs(cx), rib_t, rib_h, 0.0).translate((sx * 87.5, cy, 0.0)))
    return union_all(parts)


def make_transverse_ribs(y_positions: tuple[float, ...], length: float = 150.0) -> cq.Workplane:
    return union_all(
        [box_at_z(length, cfg.RIB_THICKNESS, cfg.RIB_HEIGHT_MAX, 0.0).translate((0.0, y, 0.0)) for y in y_positions]
    )


def make_longitudinal_ribs(x_positions: tuple[float, ...], length: float = 130.0) -> cq.Workplane:
    return union_all(
        [box_at_z(cfg.RIB_THICKNESS, length, cfg.RIB_HEIGHT_MAX, 0.0).translate((x, -10.0, 0.0)) for x in x_positions]
    )


def make_fan_ring() -> cq.Workplane:
    ring = box_at_z(
        cfg.SKELETON_FAN_RING_OUTER_SIZE,
        cfg.SKELETON_FAN_RING_OUTER_SIZE,
        cfg.SKELETON_FAN_RING_HEIGHT,
        0.0,
    )
    return ring.cut(
        cylinder_at_z(
            cfg.FAN_AIRFLOW_CUTOUT_DIAMETER_MAX,
            cfg.SKELETON_FAN_RING_HEIGHT + cfg.SKELETON_CUTTER_OVERLAP,
            0.0,
            0.0,
            -cfg.SKELETON_CUTTER_OVERLAP / 2,
        )
    )


def make_fan_ring_spokes() -> cq.Workplane:
    span = cfg.TOWER_OUTER_WIDTH - 2 * cfg.STRUCTURAL_WALL_THICKNESS
    return union_all(
        [
            box_at_z(span, cfg.RIB_THICKNESS, cfg.SKELETON_FAN_RING_HEIGHT, 0.0),
            box_at_z(cfg.RIB_THICKNESS, span, cfg.SKELETON_FAN_RING_HEIGHT, 0.0),
        ]
    )


def add_fan_screw_bosses(workplane: cq.Workplane) -> cq.Workplane:
    result = workplane
    for center_x, center_y in fan_screw_centers():
        result = result.union(
            cylinder_at_z(
                cfg.FAN_SCREW_BOSS_DIAMETER_MAX,
                cfg.SKELETON_FAN_BOSS_HEIGHT,
                center_x,
                center_y,
                0.0,
            )
        )
        result = result.cut(
            cylinder_at_z(
                cfg.SKELETON_FAN_SCREW_PLACEHOLDER_DIAMETER,
                cfg.SKELETON_FAN_BOSS_HEIGHT + cfg.SKELETON_CUTTER_OVERLAP,
                center_x,
                center_y,
                -cfg.SKELETON_CUTTER_OVERLAP / 2,
            )
        )
    return result


def cut_rear_service_window(workplane: cq.Workplane, height: float, window_height: float | None = None) -> cq.Workplane:
    wh = window_height or cfg.SKELETON_REAR_SERVICE_WINDOW_HEIGHT
    cutter = box_at_z(
        cfg.SKELETON_REAR_SERVICE_WINDOW_WIDTH,
        cfg.STRUCTURAL_WALL_THICKNESS + cfg.SKELETON_CUTTER_OVERLAP,
        wh,
        cfg.TRAY_FLOOR_THICKNESS,
    ).translate((0.0, cfg.OUTER_HALF_DEPTH - cfg.STRUCTURAL_WALL_THICKNESS / 2, 0.0))
    return workplane.cut(cutter)


def cut_rear_cable_window(workplane: cq.Workplane, width: float, height: float, z_min: float) -> cq.Workplane:
    cutter = box_at_z(
        width,
        cfg.STRUCTURAL_WALL_THICKNESS + cfg.SKELETON_CUTTER_OVERLAP,
        height,
        z_min,
    ).translate((0.0, cfg.OUTER_HALF_DEPTH - cfg.STRUCTURAL_WALL_THICKNESS / 2, 0.0))
    return workplane.cut(cutter)


def make_rpi_bosses() -> cq.Workplane:
    board_w = cfg.RPI3B_BOARD_WIDTH
    board_d = cfg.RPI3B_BOARD_DEPTH
    offsets = (
        (-board_w / 2 + 6.0, -board_d / 2 + 6.0),
        (board_w / 2 - 6.0, -board_d / 2 + 6.0),
        (-board_w / 2 + 6.0, board_d / 2 - 6.0),
        (board_w / 2 - 6.0, board_d / 2 - 6.0),
    )
    return union_all(
        [
            cylinder_at_z(
                cfg.SKELETON_RPI_BOSS_DIAMETER,
                cfg.SKELETON_RPI_BOSS_HEIGHT,
                cfg.RPI3B_CENTER_X + dx,
                cfg.RPI3B_CENTER_Y + dy,
                0.0,
            )
            for dx, dy in offsets
        ]
    )


def make_rect_outline(center_x: float, center_y: float, width: float, depth: float, height: float, z_min: float) -> cq.Workplane:
    rib = cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH
    return union_all(
        [
            box_at_z(width, rib, height, z_min).translate((center_x, center_y + depth / 2 - rib / 2, 0.0)),
            box_at_z(width, rib, height, z_min).translate((center_x, center_y - depth / 2 + rib / 2, 0.0)),
            box_at_z(rib, depth, height, z_min).translate((center_x + width / 2 - rib / 2, center_y, 0.0)),
            box_at_z(rib, depth, height, z_min).translate((center_x - width / 2 + rib / 2, center_y, 0.0)),
        ]
    )
