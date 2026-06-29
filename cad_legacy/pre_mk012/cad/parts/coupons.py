"""Small mk0.7.4 fit-test coupons for high-risk interfaces."""

import cadquery as cq

from .. import config as cfg
from .cooling import make_bottom_filter_frame, make_bottom_filter_retainer
from .feet import make_foot, make_foot_socket
from .rails import create_rail_end_mount, create_tray_support_ledge
from .side_panels import make_side_panel_mount_rail


def make_split_joint_coupon() -> cq.Workplane:
    """Create paired tab/socket split-joint blocks with the production screw path."""
    body_w = cfg.COUPON_SPLIT_BODY_WIDTH
    body_d = cfg.COUPON_SPLIT_BODY_DEPTH
    body_h = cfg.COUPON_SPLIT_BODY_HEIGHT
    tab_width = max(body_w - 2 * cfg.SPLIT_JOINT_TAB_SIDE_MARGIN, cfg.SPLIT_JOINT_TAB_MIN_WIDTH)
    offset = body_w / 2 + cfg.COUPON_GAP / 2

    lower = cq.Workplane("XY").box(body_w, body_d, body_h)
    tab = cq.Workplane("XY").box(
        tab_width,
        cfg.SPLIT_JOINT_TAB_DEPTH,
        cfg.SPLIT_JOINT_TAB_HEIGHT,
    ).translate((0, body_d / 2 + cfg.SPLIT_JOINT_TAB_DEPTH / 2, 0))
    lower = lower.union(tab).translate((-offset, 0, 0))

    socket_depth = cfg.SPLIT_JOINT_TAB_DEPTH + cfg.SPLIT_JOINT_SOCKET_CLEARANCE + 2 * cfg.SPLIT_JOINT_SOCKET_WALL
    socket_height = cfg.SPLIT_JOINT_TAB_HEIGHT + 2 * cfg.SPLIT_JOINT_SOCKET_WALL
    upper = cq.Workplane("XY").box(body_w, body_d, body_h)
    socket = cq.Workplane("XY").box(
        tab_width + 2 * cfg.SPLIT_JOINT_SOCKET_WALL,
        socket_depth,
        socket_height,
    ).translate((0, body_d / 2 + socket_depth / 2, 0))
    clearance = cq.Workplane("XY").box(
        tab_width + 2 * cfg.SPLIT_JOINT_SOCKET_CLEARANCE,
        cfg.SPLIT_JOINT_TAB_DEPTH + cfg.SPLIT_JOINT_SOCKET_CLEARANCE,
        cfg.SPLIT_JOINT_TAB_HEIGHT + 2 * cfg.SPLIT_JOINT_SOCKET_CLEARANCE,
    ).translate((0, body_d / 2 + (cfg.SPLIT_JOINT_TAB_DEPTH + cfg.SPLIT_JOINT_SOCKET_CLEARANCE) / 2, 0))
    upper = upper.union(socket.cut(clearance)).translate((offset, 0, 0))

    coupon = lower.union(upper)
    for x_center in (-offset, offset):
        coupon = coupon.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
            [
                (x_center - cfg.SPLIT_JOINT_SCREW_OFFSET_X, 0.0),
                (x_center + cfg.SPLIT_JOINT_SCREW_OFFSET_X, 0.0),
            ]
        ).hole(cfg.M3_CLEARANCE)
    return coupon.tag("coupon_split_joint_tab_socket")


def make_rail_end_mount_coupon() -> cq.Workplane:
    """Create a short frame target plus rail-end mount for screw/access validation."""
    pad = cq.Workplane("XY").box(
        cfg.COUPON_RAIL_FRAME_PAD_WIDTH,
        cfg.COUPON_RAIL_FRAME_PAD_DEPTH,
        cfg.COUPON_RAIL_FRAME_PAD_HEIGHT,
    )
    pad = pad.faces(">Z").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(0.0, cfg.RAIL_END_MOUNT_FRAME_SCREW_OFFSET_Y)]
    ).hole(cfg.M3_CLEARANCE)

    mount = create_rail_end_mount().translate(
        (
            0.0,
            0.0,
            cfg.COUPON_RAIL_FRAME_PAD_HEIGHT / 2 + cfg.RAIL_END_MOUNT_HEIGHT / 2,
        )
    )
    rail_sample_x = cfg.COUPON_RAIL_FRAME_PAD_WIDTH / 2 + cfg.COUPON_GAP + cfg.METAL_RAIL_WIDTH / 2
    rail_sample = cq.Workplane("XY").box(
        cfg.METAL_RAIL_WIDTH,
        cfg.METAL_RAIL_THICKNESS,
        cfg.COUPON_RAIL_SAMPLE_HEIGHT,
    ).translate((rail_sample_x, 0.0, cfg.COUPON_RAIL_FRAME_PAD_HEIGHT / 2 + cfg.COUPON_RAIL_SAMPLE_HEIGHT / 2))
    return pad.union(mount).union(rail_sample).tag("coupon_rail_end_mount_fit")


def make_tray_ledge_coupon() -> cq.Workplane:
    """Create a ledge, rail keepout, and representative tray edge."""
    base = cq.Workplane("XY").box(
        cfg.COUPON_TRAY_EDGE_LENGTH,
        cfg.COUPON_TRAY_EDGE_DEPTH,
        cfg.TRAY_BASE_THICKNESS,
    )
    side_wall = cq.Workplane("XY").box(
        cfg.TRAY_SIDE_WALL,
        cfg.COUPON_TRAY_EDGE_DEPTH,
        cfg.TRAY_SIDE_HEIGHT,
    ).translate(
        (
            -cfg.COUPON_TRAY_EDGE_LENGTH / 2 + cfg.TRAY_SIDE_WALL / 2,
            0.0,
            cfg.TRAY_BASE_THICKNESS / 2 + cfg.TRAY_SIDE_HEIGHT / 2,
        )
    )
    ledge = create_tray_support_ledge().translate(
        (
            cfg.COUPON_TRAY_EDGE_LENGTH / 2 - cfg.RAIL_SUPPORT_LEDGE_WIDTH / 2,
            0.0,
            -cfg.TRAY_BASE_THICKNESS / 2 - cfg.RAIL_SUPPORT_LEDGE_HEIGHT / 2,
        )
    )
    rail_keepout = cq.Workplane("XY").box(
        cfg.METAL_RAIL_WIDTH,
        cfg.METAL_RAIL_THICKNESS,
        cfg.TRAY_SIDE_HEIGHT + cfg.TRAY_BASE_THICKNESS,
    ).translate((cfg.COUPON_TRAY_EDGE_LENGTH / 2 - cfg.METAL_RAIL_WIDTH / 2, 0.0, cfg.TRAY_SIDE_HEIGHT / 2))
    return base.union(side_wall).union(ledge).union(rail_keepout).tag("coupon_tray_ledge_stack")


def make_side_panel_mount_coupon() -> cq.Workplane:
    """Create a panel corner and matching side-panel rail section."""
    length = cfg.COUPON_SIDE_PANEL_SECTION_LENGTH
    height = cfg.COUPON_SIDE_PANEL_SECTION_HEIGHT
    panel = cq.Workplane("XY").box(length, cfg.SIDE_SHEAR_PANEL_THICKNESS, height)
    boss = cq.Solid.makeCylinder(
        cfg.SIDE_PANEL_MOUNT_BOSS_DIAMETER / 2,
        cfg.SIDE_SHEAR_PANEL_RIB_HEIGHT,
        cq.Vector(length / 2 - cfg.SIDE_PANEL_FRAME_WIDTH, cfg.SIDE_SHEAR_PANEL_THICKNESS / 2, height / 2 - cfg.SIDE_PANEL_FRAME_WIDTH),
        cq.Vector(0, 1, 0),
    )
    panel = panel.union(cq.Workplane("XY").add(boss))
    panel = panel.faces(">Y").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(length / 2 - cfg.SIDE_PANEL_FRAME_WIDTH, height / 2 - cfg.SIDE_PANEL_FRAME_WIDTH)]
    ).hole(cfg.SIDE_SHEAR_PANEL_MOUNT_HOLE_DIAMETER)
    panel = panel.translate((-cfg.SIDE_PANEL_MOUNT_RAIL_WIDTH - cfg.COUPON_GAP / 2, 0.0, 0.0))

    rail = make_side_panel_mount_rail(0).intersect(
        cq.Workplane("XY").box(
            cfg.SIDE_PANEL_MOUNT_RAIL_WIDTH + cfg.FILLET_RADIUS,
            cfg.SIDE_PANEL_MOUNT_RAIL_DEPTH + cfg.FILLET_RADIUS,
            height,
        )
    )
    rail = rail.translate((length / 2 + cfg.COUPON_GAP / 2, 0.0, 0.0))
    return panel.union(rail).tag("coupon_side_panel_mount")


def make_bottom_filter_retainer_coupon() -> cq.Workplane:
    """Create a corner slice of the filter frame and retainer stack."""
    cutter_offset = cfg.BOTTOM_FILTER_RETAINER_WIDTH / 2 - cfg.COUPON_FILTER_CORNER_SIZE / 2
    cutter = cq.Workplane("XY").box(
        cfg.COUPON_FILTER_CORNER_SIZE,
        cfg.COUPON_FILTER_CORNER_SIZE,
        cfg.BOTTOM_FILTER_RETAINER_HEIGHT + cfg.BOTTOM_FILTER_FRAME_HEIGHT + cfg.FILLET_RADIUS * 4,
    ).translate((cutter_offset, cutter_offset, 0.0))
    frame = make_bottom_filter_frame().intersect(cutter)
    retainer = make_bottom_filter_retainer().intersect(cutter).translate(
        (0.0, 0.0, cfg.BOTTOM_FILTER_FRAME_HEIGHT / 2 + cfg.BOTTOM_FILTER_RETAINER_HEIGHT / 2 + cfg.COUPON_GAP / 4)
    )
    return frame.union(retainer).tag("coupon_bottom_filter_retainer")


def make_petg_foot_socket_coupon() -> cq.Workplane:
    """Create the PETG half of the TPU-foot socket test."""
    pad_size = cfg.FOOT_SOCKET_BOSS_DIAMETER + 2 * cfg.COUPON_FOOT_SOCKET_CLEARANCE_PAD
    pad = cq.Workplane("XY").box(pad_size, pad_size, cfg.COUPON_BASE_THICKNESS)
    socket = make_foot_socket().translate((0.0, 0.0, cfg.COUPON_BASE_THICKNESS / 2))
    return pad.union(socket).tag("coupon_petg_foot_socket")


def make_tpu_foot_coupon() -> cq.Workplane:
    return make_foot().tag("coupon_tpu_foot")


def make_flat_tile_coupon() -> cq.Workplane:
    return cq.Workplane("XY").box(
        cfg.COUPON_FLAT_TILE_SIZE,
        cfg.COUPON_FLAT_TILE_SIZE,
        cfg.COUPON_FLAT_TILE_THICKNESS,
    ).tag("coupon_flat_petg_tile")


def make_fan_grille_section_coupon() -> cq.Workplane:
    size = cfg.COUPON_GRILLE_SECTION_SIZE
    grille = cq.Workplane("XY").box(size, size, cfg.FAN_GRILLE_THICKNESS)
    bar_spacing = size / (cfg.COUPON_GRILLE_BAR_COUNT + 1)
    for index in range(cfg.COUPON_GRILLE_BAR_COUNT):
        offset = -size / 2 + bar_spacing * (index + 1)
        grille = grille.union(
            cq.Workplane("XY").box(cfg.FAN_GRILLE_BAR_WIDTH, size, cfg.FAN_GRILLE_THICKNESS).translate((offset, 0.0, 0.0))
        )
        grille = grille.union(
            cq.Workplane("XY").box(size, cfg.FAN_GRILLE_BAR_WIDTH, cfg.FAN_GRILLE_THICKNESS).translate((0.0, offset, 0.0))
        )
    screw = size / 2 - cfg.SIDE_PANEL_FRAME_WIDTH
    grille = grille.faces(">Z").workplane(centerOption="CenterOfBoundBox").pushPoints(
        [(-screw, -screw), (screw, screw)]
    ).hole(cfg.FAN_SCREW_DIAMETER)
    return grille.edges("|Z").chamfer(cfg.FAN_PANEL_EDGE_CHAMFER).tag("coupon_fan_grille_section")
