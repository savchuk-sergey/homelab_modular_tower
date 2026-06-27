"""Rear service spine and low-voltage power bus placeholders."""

import cadquery as cq

from .. import config as cfg


def _split_section(part: cq.Workplane, width: float, depth: float, height: float, section: str, name: str) -> cq.Workplane:
    half = height / 2
    if section == "lower":
        cutter_z = -height / 4
    elif section == "upper":
        cutter_z = height / 4
    else:
        raise ValueError(f"Unknown split section: {section}")

    cutter = cq.Workplane("XY").box(
        width + cfg.FILLET_RADIUS * 4,
        depth + cfg.FILLET_RADIUS * 4,
        half + cfg.FILLET_RADIUS * 2,
    ).translate((0, 0, cutter_z))
    segment = part.intersect(cutter)

    tab_z = 0
    tab_y = depth / 2 + cfg.SPLIT_JOINT_TAB_DEPTH / 2
    tab = cq.Workplane("XY").box(
        max(width - 12.0, cfg.SPLIT_JOINT_SCREW_OFFSET_X * 2 + 8.0),
        cfg.SPLIT_JOINT_TAB_DEPTH,
        cfg.SPLIT_JOINT_TAB_HEIGHT,
    ).translate((0, tab_y, tab_z))
    segment = segment.union(tab)
    segment = segment.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(-cfg.SPLIT_JOINT_SCREW_OFFSET_X, tab_z), (cfg.SPLIT_JOINT_SCREW_OFFSET_X, tab_z)]
    ).hole(cfg.M3_CLEARANCE)
    return segment.tag(name)


def create_power_bus_panel() -> cq.Workplane:
    panel = cq.Workplane("XY").box(cfg.POWER_BUS_WIDTH, cfg.POWER_BUS_THICKNESS, cfg.POWER_BUS_HEIGHT)
    for _, z in cfg.POWER_BUS_RAIL_LABELS:
        panel = panel.union(
            cq.Workplane("XY")
            .box(cfg.POWER_BUS_PAD_WIDTH, cfg.POWER_BUS_PAD_DEPTH, cfg.POWER_BUS_PAD_HEIGHT)
            .translate((0, cfg.POWER_BUS_PAD_Y, z))
        )
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
            [(-cfg.POWER_BUS_PAD_SCREW_OFFSET_X, z), (cfg.POWER_BUS_PAD_SCREW_OFFSET_X, z)]
        ).hole(cfg.M3_CLEARANCE)
    for x, z, width, height, _ in cfg.POWER_BUS_CONNECTOR_ZONES:
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").center(x, z).rect(width, height).cutBlind(
            -cfg.POWER_BUS_CONNECTOR_CUT_DEPTH
        )
    divider = cq.Workplane("XY").box(
        cfg.POWER_BUS_GUARD_RAIL_WIDTH,
        cfg.POWER_BUS_GUARD_RAIL_DEPTH,
        cfg.POWER_BUS_HEIGHT,
    ).translate((cfg.POWER_BUS_SIGNAL_DIVIDER_X, -cfg.POWER_BUS_THICKNESS / 2, 0))
    panel = panel.union(divider)
    for z in cfg.POWER_BUS_STRAIN_RELIEF_Z:
        clamp = cq.Workplane("XY").box(
            cfg.POWER_BUS_STRAIN_RELIEF_WIDTH,
            cfg.POWER_BUS_STRAIN_RELIEF_DEPTH,
            cfg.POWER_BUS_STRAIN_RELIEF_HEIGHT,
        ).translate((0, -cfg.POWER_BUS_THICKNESS, z))
        panel = panel.union(clamp)
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).slot2D(
            cfg.SPINE_CABLE_TIE_SLOT_HEIGHT,
            cfg.SPINE_CABLE_TIE_SLOT_WIDTH,
            0,
        ).cutThruAll()
    return panel


def create_power_bus_panel_lower() -> cq.Workplane:
    return _split_section(
        create_power_bus_panel(),
        cfg.POWER_BUS_WIDTH,
        cfg.POWER_BUS_THICKNESS + cfg.POWER_BUS_PAD_DEPTH + cfg.POWER_BUS_STRAIN_RELIEF_DEPTH,
        cfg.POWER_BUS_HEIGHT,
        "lower",
        "power_bus_panel_lower",
    )


def create_power_bus_panel_upper() -> cq.Workplane:
    return _split_section(
        create_power_bus_panel(),
        cfg.POWER_BUS_WIDTH,
        cfg.POWER_BUS_THICKNESS + cfg.POWER_BUS_PAD_DEPTH + cfg.POWER_BUS_STRAIN_RELIEF_DEPTH,
        cfg.POWER_BUS_HEIGHT,
        "upper",
        "power_bus_panel_upper",
    )


def create_power_bus_cover() -> cq.Workplane:
    cover = cq.Workplane("XY").box(
        cfg.POWER_BUS_COVER_WIDTH,
        cfg.POWER_BUS_COVER_THICKNESS,
        cfg.POWER_BUS_COVER_HEIGHT,
    )
    rail_x = cfg.POWER_BUS_COVER_WIDTH / 2 - cfg.POWER_BUS_GUARD_RAIL_WIDTH / 2
    for x in (-rail_x, rail_x):
        cover = cover.union(
            cq.Workplane("XY")
            .box(cfg.POWER_BUS_GUARD_RAIL_WIDTH, cfg.POWER_BUS_GUARD_RAIL_DEPTH, cfg.POWER_BUS_COVER_HEIGHT)
            .translate((x, -cfg.POWER_BUS_COVER_THICKNESS / 2, 0))
        )
    for _, z in cfg.POWER_BUS_RAIL_LABELS:
        cover = cover.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
            [(-cfg.POWER_BUS_PAD_SCREW_OFFSET_X, z), (cfg.POWER_BUS_PAD_SCREW_OFFSET_X, z)]
        ).hole(cfg.M3_CLEARANCE)
    return cover.tag("power_bus_cover")


def create_power_bus_cover_lower() -> cq.Workplane:
    return _split_section(
        create_power_bus_cover(),
        cfg.POWER_BUS_COVER_WIDTH,
        cfg.POWER_BUS_COVER_THICKNESS + cfg.POWER_BUS_GUARD_RAIL_DEPTH,
        cfg.POWER_BUS_COVER_HEIGHT,
        "lower",
        "power_bus_cover_lower",
    )


def create_power_bus_cover_upper() -> cq.Workplane:
    return _split_section(
        create_power_bus_cover(),
        cfg.POWER_BUS_COVER_WIDTH,
        cfg.POWER_BUS_COVER_THICKNESS + cfg.POWER_BUS_GUARD_RAIL_DEPTH,
        cfg.POWER_BUS_COVER_HEIGHT,
        "upper",
        "power_bus_cover_upper",
    )


def create_rear_service_spine() -> cq.Workplane:
    spine = cq.Workplane("XY").box(cfg.REAR_SPINE_WIDTH, cfg.REAR_SPINE_DEPTH, cfg.REAR_SPINE_HEIGHT)
    channel = cq.Workplane("XY").box(
        cfg.REAR_SPINE_WIDTH - 2 * cfg.REAR_SPINE_STRUCTURAL_WALL,
        cfg.REAR_SPINE_DEPTH + cfg.REAR_SPINE_CHANNEL_DEPTH_OVERLAP,
        cfg.REAR_SPINE_HEIGHT - cfg.REAR_SPINE_CHANNEL_HEIGHT_MARGIN,
    )
    spine = spine.cut(channel.translate((0, cfg.REAR_SPINE_CHANNEL_Y_OFFSET, 0)))

    for z in cfg.REAR_SPINE_WINDOW_Z:
        window = cq.Workplane("XY").box(
            cfg.REAR_SPINE_WINDOW_WIDTH,
            cfg.REAR_SPINE_WINDOW_DEPTH,
            cfg.REAR_SPINE_WINDOW_HEIGHT,
        ).translate((0, 0, z))
        spine = spine.cut(window)

    separator = cq.Workplane("XY").box(
        cfg.REAR_SPINE_STRUCTURAL_WALL,
        cfg.REAR_SPINE_DEPTH - 2 * cfg.REAR_SPINE_STRUCTURAL_WALL,
        cfg.REAR_SPINE_HEIGHT - cfg.REAR_SPINE_CHANNEL_HEIGHT_MARGIN,
    )
    spine = spine.union(separator.translate((cfg.REAR_SPINE_POWER_ZONE_WIDTH / 2, 0, 0)))

    rib_y = -cfg.REAR_SPINE_DEPTH / 2 + cfg.REAR_SPINE_STRUCTURAL_WALL / 2
    for x in cfg.REAR_SPINE_BACKBONE_RIB_X:
        spine = spine.union(
            cq.Workplane("XY")
            .box(cfg.REAR_SPINE_RIB_THICKNESS, cfg.REAR_SPINE_RIB_HEIGHT, cfg.REAR_SPINE_HEIGHT)
            .translate((x, rib_y, 0))
        )

    for z in cfg.REAR_SPINE_HORIZONTAL_TIE_Z:
        spine = spine.union(
            cq.Workplane("XY")
            .box(cfg.REAR_SPINE_WIDTH, cfg.REAR_SPINE_HORIZONTAL_TIE_DEPTH, cfg.REAR_SPINE_HORIZONTAL_TIE_HEIGHT)
            .translate((0, rib_y, z))
        )

    rail_x = cfg.REAR_SPINE_WIDTH / 2 - cfg.REAR_SPINE_COVER_RAIL_WIDTH / 2
    rail_y = cfg.REAR_SPINE_DEPTH / 2 - cfg.REAR_SPINE_COVER_RAIL_DEPTH / 2
    for x in (-rail_x, rail_x):
        spine = spine.union(
            cq.Workplane("XY")
            .box(cfg.REAR_SPINE_COVER_RAIL_WIDTH, cfg.REAR_SPINE_COVER_RAIL_DEPTH, cfg.REAR_SPINE_HEIGHT)
            .translate((x, rail_y, 0))
        )

    for x in cfg.REAR_SPINE_TIE_SLOT_X:
        for z in cfg.REAR_SPINE_TIE_SLOT_Z:
            spine = (
                spine.faces(">Y")
                .workplane(centerOption="CenterOfBoundBox")
                .center(x, z)
                .slot2D(cfg.SPINE_CABLE_TIE_SLOT_HEIGHT, cfg.SPINE_CABLE_TIE_SLOT_WIDTH, 90)
                .cutThruAll()
            )

    for z in cfg.REAR_SPINE_STRUCTURAL_MOUNT_Z:
        tab = (
            cq.Workplane("XY")
            .box(cfg.REAR_SPINE_MOUNT_TAB_WIDTH, cfg.REAR_SPINE_MOUNT_TAB_DEPTH, cfg.REAR_SPINE_MOUNT_TAB_THICKNESS)
            .translate((0, cfg.REAR_SPINE_DEPTH / 2 + cfg.REAR_SPINE_MOUNT_TAB_DEPTH / 2, z))
        )
        spine = spine.union(tab)
        spine = spine.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).hole(
            cfg.REAR_SPINE_MOUNT_HOLE_DIAMETER
        )
        for x in (-cfg.REAR_SPINE_SIDE_MOUNT_X, cfg.REAR_SPINE_SIDE_MOUNT_X):
            side_tab = (
                cq.Workplane("XY")
                .box(
                    cfg.REAR_SPINE_SIDE_MOUNT_WIDTH,
                    cfg.REAR_SPINE_SIDE_MOUNT_DEPTH,
                    cfg.REAR_SPINE_SIDE_MOUNT_HEIGHT,
                )
                .translate((x, cfg.REAR_SPINE_DEPTH / 2, z))
            )
            spine = spine.union(side_tab)

    for z in cfg.REAR_SPINE_FRAME_TAB_Z:
        for x in (-cfg.REAR_SPINE_WIDTH / 2, cfg.REAR_SPINE_WIDTH / 2):
            tab = (
                cq.Workplane("XY")
                .box(cfg.REAR_SPINE_MOUNT_TAB_WIDTH, cfg.REAR_SPINE_MOUNT_TAB_THICKNESS, cfg.REAR_SPINE_MOUNT_TAB_WIDTH)
                .translate((x, 0, z))
            )
            spine = spine.union(tab)

    if cfg.TORSION_BRACE_MOUNT_ENABLED:
        for x, z in (
            (-cfg.REAR_SPINE_WIDTH / 2, -cfg.REAR_SPINE_HEIGHT / 2 + cfg.TORSION_BRACE_MOUNT_HEIGHT),
            (cfg.REAR_SPINE_WIDTH / 2, cfg.REAR_SPINE_HEIGHT / 2 - cfg.TORSION_BRACE_MOUNT_HEIGHT),
        ):
            mount = (
                cq.Workplane("XY")
                .box(
                    cfg.TORSION_BRACE_MOUNT_WIDTH,
                    cfg.TORSION_BRACE_MOUNT_THICKNESS,
                    cfg.TORSION_BRACE_MOUNT_HEIGHT,
                )
                .translate((x, -cfg.REAR_SPINE_DEPTH / 2, z))
            )
            spine = spine.union(mount)
            spine = spine.faces("<Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(x, z)]).hole(
                cfg.TORSION_BRACE_HOLE_DIAMETER
            )
    return spine.tag("rear_service_spine")


def create_rear_service_spine_lower() -> cq.Workplane:
    return _split_section(
        create_rear_service_spine(),
        cfg.REAR_SPINE_WIDTH + 2 * cfg.REAR_SPINE_SIDE_MOUNT_WIDTH + 2 * cfg.REAR_SPINE_SIDE_MOUNT_X,
        cfg.REAR_SPINE_DEPTH + cfg.REAR_SPINE_MOUNT_TAB_DEPTH + cfg.REAR_SPINE_COVER_RAIL_DEPTH,
        cfg.REAR_SPINE_HEIGHT,
        "lower",
        "rear_service_spine_lower",
    )


def create_rear_service_spine_upper() -> cq.Workplane:
    return _split_section(
        create_rear_service_spine(),
        cfg.REAR_SPINE_WIDTH + 2 * cfg.REAR_SPINE_SIDE_MOUNT_WIDTH + 2 * cfg.REAR_SPINE_SIDE_MOUNT_X,
        cfg.REAR_SPINE_DEPTH + cfg.REAR_SPINE_MOUNT_TAB_DEPTH + cfg.REAR_SPINE_COVER_RAIL_DEPTH,
        cfg.REAR_SPINE_HEIGHT,
        "upper",
        "rear_service_spine_upper",
    )


def create_rear_service_spine_cover() -> cq.Workplane:
    cover = cq.Workplane("XY").box(
        cfg.REAR_SPINE_COVER_WIDTH,
        cfg.REAR_SPINE_COVER_THICKNESS,
        cfg.REAR_SPINE_COVER_HEIGHT,
    )
    for z in cfg.REAR_SPINE_COVER_MOUNT_Z:
        cover = cover.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).hole(
            cfg.REAR_SPINE_MOUNT_HOLE_DIAMETER
        )
    return cover.edges("|Z").chamfer(cfg.FILLET_RADIUS).tag("rear_service_spine_cover")


def create_rear_service_spine_cover_lower() -> cq.Workplane:
    return _split_section(
        create_rear_service_spine_cover(),
        cfg.REAR_SPINE_COVER_WIDTH,
        cfg.REAR_SPINE_COVER_THICKNESS,
        cfg.REAR_SPINE_COVER_HEIGHT,
        "lower",
        "rear_service_spine_cover_lower",
    )


def create_rear_service_spine_cover_upper() -> cq.Workplane:
    return _split_section(
        create_rear_service_spine_cover(),
        cfg.REAR_SPINE_COVER_WIDTH,
        cfg.REAR_SPINE_COVER_THICKNESS,
        cfg.REAR_SPINE_COVER_HEIGHT,
        "upper",
        "rear_service_spine_cover_upper",
    )
