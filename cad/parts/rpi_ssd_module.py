"""mk0.9 Raspberry Pi 3B plus external SSD module."""

import cadquery as cq

from .. import config as cfg
from . import module_interface, placeholders


def make_rpi3_placeholder(c=cfg) -> cq.Workplane:
    return placeholders.make_raspberry_pi_3b_placeholder().tag("rpi3_placeholder")


def make_external_ssd_placeholder(c=cfg) -> cq.Workplane:
    return placeholders.make_external_ssd_placeholder().tag("external_ssd_placeholder")


def make_rpi_ssd_tray(c=cfg) -> cq.Workplane:
    tray = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.FLOOR_THICKNESS)
    airflow = cq.Workplane("XY").box(c.AIRFLOW_CHANNEL_WIDTH, c.AIRFLOW_CHANNEL_DEPTH, c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(c.REAR_CABLE_EXIT_WIDTH, c.REAR_RESERVED_DEPTH + c.FILLET_RADIUS, c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    return tray.cut(airflow).cut(rear).tag("rpi_ssd_tray")


def make_rpi_mount_posts(c=cfg) -> cq.Workplane:
    posts = None
    hx = c.RPI3B_BOARD_WIDTH / 2 - c.RPI3B_MOUNT_HOLE_OFFSET_X
    hy = c.RPI3B_BOARD_DEPTH / 2 - c.RPI3B_MOUNT_HOLE_OFFSET_Y
    origin = (c.RPI3_PLACEHOLDER_X, c.RPI3_PLACEHOLDER_Y)
    for x, y in [(origin[0] + px, origin[1] + py) for px in (-hx, hx) for py in (-hy, hy)]:
        post = cq.Workplane("XY").circle(c.RPI3_STANDOFF_DIAMETER / 2).extrude(c.RPI3_STANDOFF_HEIGHT)
        bore = cq.Workplane("XY").circle(c.RPI3_STANDOFF_HOLE / 2).extrude(c.RPI3_STANDOFF_HEIGHT + c.FILLET_RADIUS)
        post = post.cut(bore)
        post = post.translate((x, y, 0))
        posts = post if posts is None else posts.union(post)
    return posts.tag("rpi_mount_posts")


def make_ssd_retainer(c=cfg) -> cq.Workplane:
    retainer = None
    center = (c.EXTERNAL_SSD_PLACEHOLDER_X, c.EXTERNAL_SSD_PLACEHOLDER_Y)
    for x in (-c.EXTERNAL_SSD_PLACEHOLDER_WIDTH / 2 - c.SSD_RETAINER_THICKNESS, c.EXTERNAL_SSD_PLACEHOLDER_WIDTH / 2 + c.SSD_RETAINER_THICKNESS):
        rail = (
            cq.Workplane("XY")
            .box(c.SSD_RETAINER_THICKNESS, c.EXTERNAL_SSD_PLACEHOLDER_DEPTH + c.FRAME_HEIGHT, c.SSD_RETAINER_HEIGHT)
            .translate((center[0] + x, center[1], c.SSD_RETAINER_HEIGHT / 2))
        )
        retainer = rail if retainer is None else retainer.union(rail)
    for x in (-c.ZIP_TIE_SLOT_LENGTH, c.ZIP_TIE_SLOT_LENGTH):
        slot = cq.Workplane("XY").box(c.ZIP_TIE_SLOT_LENGTH, c.ZIP_TIE_SLOT_WIDTH, c.FLOOR_THICKNESS + c.FILLET_RADIUS).translate((center[0] + x, center[1], 0))
        retainer = retainer.cut(slot)
    return retainer.tag("ssd_retainer")


def make_rpi_ssd_module_shell(c=cfg) -> cq.Workplane:
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    inner = cq.Workplane("XY").box(c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL, c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL, c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS).translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    rear = cq.Workplane("XY").box(c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL, c.REAR_RESERVED_DEPTH - c.MODULE_FRAME_RAIL, c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS).translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    ring = ring.cut(inner).cut(rear)
    shell = ring.translate((0, 0, -c.RPI_SSD_MODULE_HEIGHT / 2 + c.MODULE_INTERFACE_HEIGHT / 2)).union(
        ring.translate((0, 0, c.RPI_SSD_MODULE_HEIGHT / 2 - c.MODULE_INTERFACE_HEIGHT / 2))
    )
    post_size = c.CORNER_POST_SIZE
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        shell = shell.union(cq.Workplane("XY").box(post_size, post_size, c.RPI_SSD_MODULE_HEIGHT).translate((px, py, 0)))
    return shell.tag("rpi_ssd_module_shell")


def make_rpi_ssd_module(c=cfg) -> cq.Workplane:
    module = make_rpi_ssd_module_shell(c)
    deck_z = -c.RPI_SSD_MODULE_HEIGHT / 2 + c.FLOOR_THICKNESS / 2
    module = module.union(make_rpi_ssd_tray(c).translate((0, 0, deck_z)))
    module = module.union(make_rpi_mount_posts(c).translate((0, 0, deck_z + c.FLOOR_THICKNESS / 2)))
    module = module.union(make_ssd_retainer(c).translate((0, 0, deck_z + c.FLOOR_THICKNESS / 2)))
    return module_interface.apply_module_interface_features(module, c, top=True, bottom=True).tag("rpi_ssd_module")
