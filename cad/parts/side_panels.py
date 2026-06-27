"""Removable side service panels."""

import math

import cadquery as cq

from .. import config as cfg


def side_panel_length() -> float:
    return cfg.OUTER_DEPTH - 2 * cfg.SIDE_PANEL_CLEARANCE


def make_side_panel_frame() -> cq.Workplane:
    length = side_panel_length()
    height = cfg.SIDE_PANEL_HEIGHT
    rail = cfg.SIDE_PANEL_FRAME_WIDTH
    y = cfg.SIDE_PANEL_THICKNESS / 2 + cfg.SIDE_PANEL_RIB_HEIGHT / 2
    top_bottom = cq.Workplane("XY")
    for z in (-(height - rail) / 2, (height - rail) / 2):
        top_bottom = top_bottom.union(cq.Workplane("XY").box(length, cfg.SIDE_PANEL_RIB_HEIGHT, rail).translate((0, y, z)))

    sides = cq.Workplane("XY")
    for x in (-(length - rail) / 2, (length - rail) / 2):
        sides = sides.union(cq.Workplane("XY").box(rail, cfg.SIDE_PANEL_RIB_HEIGHT, height).translate((x, y, 0)))
    return top_bottom.union(sides)


def make_side_panel_ribs() -> cq.Workplane:
    length = side_panel_length() - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    height = cfg.SIDE_PANEL_HEIGHT - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    diagonal = (length**2 + height**2) ** 0.5
    angle = math.degrees(math.atan2(height, length))
    y = cfg.SIDE_PANEL_THICKNESS / 2 + cfg.SIDE_PANEL_RIB_HEIGHT / 2
    envelope = cq.Workplane("XY").box(length, cfg.SIDE_PANEL_RIB_HEIGHT, height).translate((0, y, 0))
    ribs = cq.Workplane("XY")
    for rib_angle in (-angle, angle):
        rib = (
            cq.Workplane("XY")
            .box(diagonal, cfg.SIDE_PANEL_RIB_HEIGHT, cfg.SIDE_PANEL_RIB_WIDTH)
            .rotate((0, 0, 0), (0, 1, 0), rib_angle)
            .translate((0, y, 0))
        )
        ribs = ribs.union(rib)
    return ribs.intersect(envelope)


def make_side_panel_mounts() -> cq.Workplane:
    length = side_panel_length()
    height = cfg.SIDE_PANEL_HEIGHT
    x = length / 2 - cfg.SIDE_PANEL_FRAME_WIDTH
    z = height / 2 - cfg.CORNER_BLOCK_HEIGHT
    y = cfg.SIDE_PANEL_THICKNESS / 2 + cfg.SIDE_PANEL_RIB_HEIGHT / 2
    mounts = cq.Workplane("XY")
    for px in (-x, x):
        for pz in (-z, z):
            boss = cq.Solid.makeCylinder(
                cfg.SIDE_PANEL_MOUNT_BOSS_DIAMETER / 2,
                cfg.SIDE_PANEL_RIB_HEIGHT,
                cq.Vector(px, cfg.SIDE_PANEL_THICKNESS / 2, pz),
                cq.Vector(0, 1, 0),
            )
            mounts = mounts.union(cq.Workplane("XY").add(boss))
    return mounts.translate((0, y - cfg.SIDE_PANEL_THICKNESS / 2 - cfg.SIDE_PANEL_RIB_HEIGHT / 2, 0))


def make_side_panel_vents(panel: cq.Workplane) -> cq.Workplane:
    length = side_panel_length()
    usable_length = length - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    usable_height = cfg.SIDE_PANEL_HEIGHT - 2 * cfg.SIDE_PANEL_FRAME_WIDTH
    x_values = []
    x = -usable_length / 2 + cfg.SIDE_PANEL_VENT_SLOT_LENGTH / 2
    while x <= usable_length / 2 - cfg.SIDE_PANEL_VENT_SLOT_LENGTH / 2:
        x_values.append(x)
        x += cfg.SIDE_PANEL_VENT_SLOT_LENGTH + cfg.SIDE_PANEL_VENT_SLOT_SPACING

    mini_pc_zone_center = cfg.MINIPC_DUCT_ZONE_OFFSET_Z - cfg.TOWER_HEIGHT / 2
    mini_pc_zone_half = cfg.MINIPC_DUCT_ZONE_HEIGHT / 2 + cfg.SIDE_PANEL_MINIPC_DUCT_CLEARANCE
    points = []
    z = -usable_height / 2 + cfg.SIDE_PANEL_VENT_SLOT_SPACING
    while z <= usable_height / 2 - cfg.SIDE_PANEL_VENT_SLOT_SPACING:
        if abs(z - mini_pc_zone_center) > mini_pc_zone_half:
            points.extend((x_point, z) for x_point in x_values)
        z += cfg.SIDE_PANEL_VENT_SLOT_SPACING

    return (
        panel.faces(">Y")
        .workplane(centerOption="CenterOfBoundBox")
        .pushPoints(points)
        .slot2D(cfg.SIDE_PANEL_VENT_SLOT_LENGTH, cfg.SIDE_PANEL_VENT_SLOT_WIDTH, 0)
        .cutThruAll()
    )


def create_side_panel(name: str = "left_side_panel") -> cq.Workplane:
    panel = (
        cq.Workplane("XY")
        .box(side_panel_length(), cfg.SIDE_PANEL_THICKNESS, cfg.SIDE_PANEL_HEIGHT)
        .edges("|Z")
        .chamfer(cfg.SIDE_PANEL_CORNER_RADIUS)
    )
    panel = make_side_panel_vents(panel)
    panel = panel.union(make_side_panel_frame()).union(make_side_panel_ribs()).union(make_side_panel_mounts())

    length = side_panel_length()
    x = length / 2 - cfg.SIDE_PANEL_FRAME_WIDTH
    z = cfg.SIDE_PANEL_HEIGHT / 2 - cfg.CORNER_BLOCK_HEIGHT
    mount_points = [(-x, -z), (x, -z), (-x, z), (x, z)]
    panel = panel.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(mount_points).hole(
        cfg.SIDE_PANEL_MOUNT_HOLE_DIAMETER
    )
    return panel.tag(name)


def create_left_side_panel() -> cq.Workplane:
    return create_side_panel("left_side_panel")


def create_right_side_panel() -> cq.Workplane:
    return create_side_panel("right_side_panel")
