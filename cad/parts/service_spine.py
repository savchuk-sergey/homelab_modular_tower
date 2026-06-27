"""Rear service spine and low-voltage power bus placeholders."""

import cadquery as cq

from .. import config as cfg


def create_power_bus_panel() -> cq.Workplane:
    panel = cq.Workplane("XY").box(cfg.POWER_BUS_WIDTH, cfg.POWER_BUS_THICKNESS, cfg.POWER_BUS_HEIGHT)
    for _, z in cfg.POWER_BUS_RAIL_LABELS:
        # TODO: replace generic pads with exact terminal/fuse/DC-DC footprints.
        panel = panel.union(
            cq.Workplane("XY")
            .box(cfg.POWER_BUS_PAD_WIDTH, cfg.POWER_BUS_PAD_DEPTH, cfg.POWER_BUS_PAD_HEIGHT)
            .translate((0, cfg.POWER_BUS_PAD_Y, z))
        )
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
            [(-cfg.POWER_BUS_PAD_SCREW_OFFSET_X, z), (cfg.POWER_BUS_PAD_SCREW_OFFSET_X, z)]
        ).hole(cfg.M3_CLEARANCE)
    for x, z, width, height, _ in cfg.POWER_BUS_CONNECTOR_ZONES:
        # TODO: replace these windows with exact connector retention geometry.
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").center(x, z).rect(width, height).cutBlind(
            -cfg.POWER_BUS_CONNECTOR_CUT_DEPTH
        )
    return panel


def create_rear_service_spine() -> cq.Workplane:
    spine = cq.Workplane("XY").box(cfg.REAR_SPINE_WIDTH, cfg.REAR_SPINE_DEPTH, cfg.REAR_SPINE_HEIGHT)
    channel = cq.Workplane("XY").box(
        cfg.REAR_SPINE_WIDTH - cfg.REAR_SPINE_CHANNEL_SIDE_MARGIN,
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

    for z in cfg.REAR_SPINE_MOUNT_Z:
        spine = spine.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).hole(cfg.M3_CLEARANCE)
    return spine
