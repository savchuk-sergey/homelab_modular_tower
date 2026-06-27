"""Removable sectional side service panels."""

import math

import cadquery as cq

from .. import config as cfg


def side_panel_length() -> float:
    return cfg.OUTER_DEPTH - 2 * cfg.SIDE_PANEL_CLEARANCE - 2 * cfg.SIDE_PANEL_TILE_MARGIN


def side_panel_tile_height(height_units: float = 1.0) -> float:
    return cfg.SIDE_PANEL_SECTION_HEIGHT * height_units + cfg.SIDE_PANEL_GAP * (height_units - 1)


def side_panel_tile_center_z(index: int, height_units: float = 1.0) -> float:
    return (
        cfg.SIDE_PANEL_BOTTOM_Z
        + side_panel_tile_height(height_units) / 2
        + index * (cfg.SIDE_PANEL_SECTION_HEIGHT + cfg.SIDE_PANEL_GAP)
    )


def _is_structural_section(index: int) -> bool:
    return index in cfg.SIDE_SHEAR_PANEL_STRUCTURAL_SECTIONS


def _panel_thickness(index: int) -> float:
    if _is_structural_section(index):
        return cfg.SIDE_SHEAR_PANEL_THICKNESS
    return cfg.SIDE_PANEL_THICKNESS


def _rib_height(index: int) -> float:
    if _is_structural_section(index):
        return cfg.SIDE_SHEAR_PANEL_RIB_HEIGHT
    return cfg.SIDE_PANEL_RIB_HEIGHT


def _rib_width(index: int) -> float:
    if _is_structural_section(index):
        return cfg.SIDE_SHEAR_PANEL_RIB_THICKNESS
    return cfg.SIDE_PANEL_RIB_WIDTH


def _make_side_panel_frame(length: float, height: float, index: int) -> cq.Workplane:
    rail = cfg.SIDE_PANEL_FRAME_WIDTH
    thickness = _panel_thickness(index)
    rib_height = _rib_height(index)
    y = thickness / 2 + rib_height / 2
    top_bottom = cq.Workplane("XY")
    for z in (-(height - rail) / 2, (height - rail) / 2):
        top_bottom = top_bottom.union(cq.Workplane("XY").box(length, rib_height, rail).translate((0, y, z)))

    sides = cq.Workplane("XY")
    for x in (-(length - rail) / 2, (length - rail) / 2):
        sides = sides.union(cq.Workplane("XY").box(rail, rib_height, height).translate((x, y, 0)))
    frame = top_bottom.union(sides)
    if _is_structural_section(index):
        overlap_y = thickness / 2 + rib_height + cfg.SIDE_PANEL_OVERLAP / 2
        for z in (-(height - rail) / 2, (height - rail) / 2):
            frame = frame.union(
                cq.Workplane("XY")
                .box(length, cfg.SIDE_PANEL_OVERLAP, cfg.SIDE_SHEAR_PANEL_OVERLAP_RIB_WIDTH)
                .translate((0, overlap_y, z))
            )
    return frame


def _make_side_panel_ribs(length: float, height: float, index: int) -> cq.Workplane:
    rib_length = length - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    rib_height = height - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    diagonal = (rib_length**2 + rib_height**2) ** 0.5
    angle = math.degrees(math.atan2(rib_height, rib_length))
    panel_thickness = _panel_thickness(index)
    rib_y_height = _rib_height(index)
    rib_width = _rib_width(index)
    y = panel_thickness / 2 + rib_y_height / 2
    envelope = cq.Workplane("XY").box(rib_length, rib_y_height, rib_height).translate((0, y, 0))
    ribs = cq.Workplane("XY")
    for rib_angle in (-angle, angle):
        rib = (
            cq.Workplane("XY")
            .box(diagonal, rib_y_height, rib_width)
            .rotate((0, 0, 0), (0, 1, 0), rib_angle)
            .translate((0, y, 0))
        )
        ribs = ribs.union(rib)
    return ribs.intersect(envelope)


def _mount_points(length: float, height: float) -> list[tuple[float, float]]:
    x = length / 2 - cfg.SIDE_PANEL_FRAME_WIDTH
    z = height / 2 - cfg.SIDE_PANEL_FRAME_WIDTH
    return [(-x, -z), (x, -z), (-x, z), (x, z)]


def _make_side_panel_mounts(length: float, height: float, index: int) -> cq.Workplane:
    thickness = _panel_thickness(index)
    rib_height = _rib_height(index)
    y = thickness / 2 + rib_height / 2
    mounts = cq.Workplane("XY")
    for px, pz in _mount_points(length, height):
        boss = cq.Solid.makeCylinder(
            cfg.SIDE_PANEL_MOUNT_BOSS_DIAMETER / 2,
            rib_height,
            cq.Vector(px, thickness / 2, pz),
            cq.Vector(0, 1, 0),
        )
        mounts = mounts.union(cq.Workplane("XY").add(boss))
    return mounts.translate((0, y - thickness / 2 - rib_height / 2, 0))


def _cut_side_panel_vents(panel: cq.Workplane, length: float, height: float, tile_center_z: float) -> cq.Workplane:
    usable_length = length - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    usable_height = height - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    x_values = []
    x = -usable_length / 2 + cfg.SIDE_PANEL_VENT_SLOT_LENGTH / 2
    while x <= usable_length / 2 - cfg.SIDE_PANEL_VENT_SLOT_LENGTH / 2:
        x_values.append(x)
        x += cfg.SIDE_PANEL_VENT_SLOT_LENGTH + cfg.SIDE_PANEL_VENT_SLOT_SPACING

    mini_pc_zone_center = cfg.MINIPC_DUCT_ZONE_OFFSET_Z - tile_center_z
    mini_pc_zone_half = cfg.MINIPC_DUCT_ZONE_HEIGHT / 2 + cfg.SIDE_PANEL_MINIPC_DUCT_CLEARANCE
    points = []
    z = -usable_height / 2 + cfg.SIDE_PANEL_VENT_SLOT_SPACING
    while z <= usable_height / 2 - cfg.SIDE_PANEL_VENT_SLOT_SPACING:
        if abs(z - mini_pc_zone_center) > mini_pc_zone_half:
            points.extend((x_point, z) for x_point in x_values)
        z += cfg.SIDE_PANEL_VENT_SLOT_SPACING

    if not points:
        return panel
    return (
        panel.faces(">Y")
        .workplane(centerOption="CenterOfBoundBox")
        .pushPoints(points)
        .slot2D(cfg.SIDE_PANEL_VENT_SLOT_LENGTH, cfg.SIDE_PANEL_VENT_SLOT_WIDTH, 0)
        .cutThruAll()
    )


def make_side_panel_tile(side: str, index: int, height_units: float = 1.0) -> cq.Workplane:
    length = side_panel_length()
    height = side_panel_tile_height(height_units)
    thickness = _panel_thickness(index)
    panel = (
        cq.Workplane("XY")
        .box(length, thickness, height)
        .edges("|Z")
        .chamfer(cfg.SIDE_PANEL_CORNER_RADIUS)
    )
    panel = _cut_side_panel_vents(panel, length, height, side_panel_tile_center_z(index, height_units))
    panel = panel.union(_make_side_panel_frame(length, height, index))
    panel = panel.union(_make_side_panel_ribs(length, height, index))
    panel = panel.union(_make_side_panel_mounts(length, height, index))
    panel = panel.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(_mount_points(length, height)).hole(
        cfg.SIDE_SHEAR_PANEL_MOUNT_HOLE_DIAMETER if _is_structural_section(index) else cfg.SIDE_PANEL_MOUNT_HOLE_DIAMETER
    )
    if _is_structural_section(index):
        panel = panel.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
            _mount_points(length, height)
        ).circle(cfg.SIDE_PANEL_INSERT_DIAMETER / 2).cutBlind(-cfg.SIDE_PANEL_INSERT_DEPTH)
    label = cfg.SIDE_PANEL_SECTION_LABELS[index]
    return panel.tag(f"{side}_side_panel_{label}")


def create_left_side_panel_lower() -> cq.Workplane:
    return make_side_panel_tile("left", 0)


def create_left_side_panel_middle() -> cq.Workplane:
    return make_side_panel_tile("left", 1)


def create_left_side_panel_upper() -> cq.Workplane:
    return make_side_panel_tile("left", 2)


def create_right_side_panel_lower() -> cq.Workplane:
    return make_side_panel_tile("right", 0)


def create_right_side_panel_middle() -> cq.Workplane:
    return make_side_panel_tile("right", 1)


def create_right_side_panel_upper() -> cq.Workplane:
    return make_side_panel_tile("right", 2)


def create_side_panel(name: str = "left_side_panel") -> cq.Workplane:
    side = "right" if "right" in name else "left"
    panel = cq.Workplane("XY")
    for index in range(cfg.SIDE_PANEL_SECTION_COUNT):
        tile = make_side_panel_tile(side, index)
        panel = panel.union(tile.translate((0, 0, side_panel_tile_center_z(index) - cfg.TOWER_HEIGHT / 2)))
    return panel.tag(name)


def create_left_side_panel() -> cq.Workplane:
    return create_side_panel("left_side_panel")


def create_right_side_panel() -> cq.Workplane:
    return create_side_panel("right_side_panel")
