"""Low-voltage power bus and rear service spine placeholders."""

import cadquery as cq

from . import config as cfg


def create_power_bus_panel() -> cq.Workplane:
    panel = cq.Workplane("XY").box(cfg.POWER_BUS_WIDTH, cfg.POWER_BUS_THICKNESS, cfg.POWER_BUS_HEIGHT)
    labels = [
        ("19V", 70.0),
        ("12V", 25.0),
        ("5V", -20.0),
        ("GND", -65.0),
    ]
    for _, z in labels:
        # TODO: replace generic pads with exact terminal/fuse/DC-DC footprints.
        panel = panel.union(cq.Workplane("XY").box(22.0, 4.0, 22.0).translate((0, -3.5, z)))
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(-7.0, z), (7.0, z)]).hole(cfg.M3_CLEARANCE)
    connector_zones = [
        (0.0, 112.0, 24.0, 14.0, "xt30_19v"),
        (0.0, 48.0, 20.0, 10.0, "microfit_12v"),
        (0.0, -48.0, 18.0, 8.0, "usb_c_5v"),
        (0.0, -112.0, 24.0, 10.0, "cable_tie"),
    ]
    for x, z, width, height, _ in connector_zones:
        # TODO: replace these windows with exact connector retention geometry.
        panel = panel.faces("<Y").workplane(centerOption="CenterOfBoundBox").center(x, z).rect(width, height).cutBlind(-5.0)
    return panel


def create_rear_service_spine() -> cq.Workplane:
    spine = cq.Workplane("XY").box(cfg.REAR_SPINE_WIDTH, cfg.REAR_SPINE_DEPTH, cfg.REAR_SPINE_HEIGHT)
    channel = cq.Workplane("XY").box(cfg.REAR_SPINE_WIDTH - 8.0, cfg.REAR_SPINE_DEPTH + 2.0, cfg.REAR_SPINE_HEIGHT - 22.0)
    spine = spine.cut(channel.translate((0, -2.0, 0)))

    for z in (-95.0, -35.0, 25.0, 85.0):
        window = cq.Workplane("XY").box(24.0, 20.0, 20.0).translate((0, 0, z))
        spine = spine.cut(window)

    for z in (-120.0, 0.0, 120.0):
        spine = spine.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints([(0, z)]).hole(cfg.M3_CLEARANCE)
    return spine
