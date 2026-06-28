"""mk0.11.2 generic stack module — stack-through-rod layer.

Active architecture for mk0.11.2: a stackable module layer compressed between
base_pedestal and top_cap by four M5 through-rods.

Each module reserves future carriage/side-adapter mounting zones without
implementing rails, POM-C shoe sockets, or sliding carriage geometry.

Design intent:
- Stackable module layer with top/bottom interface rings.
- 4x M5 pass-through holes aligned by config offsets.
- Local reinforced compression pad zones around M5 corner posts.
- Central vertical airflow opening (no solid floor).
- Rear service reserved cutout/zone.
- Internal device mounting placeholder grid.
- Front handle/label zone placeholder.
- Future carriage/side adapter mounting zones (pads + M3 bosses only).
- PETG printable as a standalone part.
"""

import cadquery as cq

from .. import config as cfg
from . import module_interface, rails


def _corner_rod_points(c=cfg) -> list[tuple[float, float]]:
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    return [(-x, -y), (x, -y), (x, y), (-x, y)]


def _make_frame_ring(c=cfg) -> cq.Workplane:
    """Single horizontal frame ring with airflow and rear service clearance."""
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)
    inner = (
        cq.Workplane("XY")
        .box(
            c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
            c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL,
            c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    )
    rear = (
        cq.Workplane("XY")
        .box(
            c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
            c.REAR_RESERVED_DEPTH - c.MODULE_FRAME_RAIL,
            c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
        )
        .translate((0, c.TOWER_DEPTH / 2 - c.REAR_RESERVED_DEPTH / 2, 0))
    )
    return ring.cut(inner).cut(rear)


def _make_vertical_airflow_opening(height: float, c=cfg) -> cq.Workplane:
    """Central vertical airflow channel through the module interior."""
    return (
        cq.Workplane("XY")
        .box(
            c.AIRFLOW_CHANNEL_WIDTH,
            c.AIRFLOW_CHANNEL_DEPTH,
            height + c.FILLET_RADIUS,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    )


def _apply_compression_pads(part: cq.Workplane, c=cfg) -> cq.Workplane:
    """Washer seat pockets on top and bottom faces at each M5 corner post."""
    pad_radius = c.STACK_MODULE_COMPRESSION_PAD_DIAMETER / 2
    pad_depth = c.STACK_MODULE_COMPRESSION_PAD_DEPTH
    for x, y in _corner_rod_points(c):
        part = part.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(x, y).circle(pad_radius).cutBlind(
            -pad_depth
        )
        part = part.faces("<Z").workplane(centerOption="CenterOfBoundBox").center(x, y).circle(pad_radius).cutBlind(
            -pad_depth
        )
    return part


def _make_future_carriage_mount_zones(height: float, c=cfg) -> cq.Workplane:
    """Left/right reinforced flat pads reserved for future side adapters.

    Pads span the full module height so they are physically anchored to both
    the top and bottom frame rings.  They are centered on the U-channel rail
    lateral position and do not include rail pockets, shoe sockets, or any
    sliding features.
    """
    pads = None
    x_rail = rails.u_channel_rail_x_offset()
    y_center = -c.REAR_RESERVED_DEPTH / 2

    for sign in (-1, 1):
        pad = (
            cq.Workplane("XY")
            .box(
                c.FUTURE_CARRIAGE_PAD_WALL,
                c.FUTURE_CARRIAGE_PAD_WIDTH,
                height,
            )
            .translate((sign * x_rail, y_center, 0.0))
        )
        pads = pad if pads is None else pads.union(pad)

    return pads.tag("future_carriage_mount_zones")


def _make_future_side_adapter_mount_points(height: float, c=cfg) -> cq.Workplane:
    """M3 insert bosses on future side pads — DEFERRED, not called in mk0.11.2 shell.

    This function is kept for reference but is NOT included in the printable
    part because the boss geometry is disconnected from the side pad body
    and produces floating islands.  Reactivate only after the side pad
    geometry is redesigned for full connectivity.
    """
    bosses = None
    x_rail = rails.u_channel_rail_x_offset()
    y_center = -c.REAR_RESERVED_DEPTH / 2
    z_center = c.FUTURE_CARRIAGE_PAD_VERTICAL_CENTER_Z
    half_spacing = c.FUTURE_SIDE_ADAPTER_MOUNT_SPACING_Y / 2
    y_offsets = (
        [0.0]
        if c.FUTURE_SIDE_ADAPTER_MOUNT_COUNT <= 1
        else [-half_spacing, half_spacing][: c.FUTURE_SIDE_ADAPTER_MOUNT_COUNT]
    )

    for sign in (-1, 1):
        x_face = sign * (x_rail + sign * c.FUTURE_CARRIAGE_PAD_WALL / 2)
        for y_off in y_offsets:
            boss = (
                cq.Workplane("YZ")
                .circle(c.INSERT_BOSS_DIAMETER / 2)
                .extrude(c.INSERT_BOSS_HEIGHT)
                .translate((x_face, y_center + y_off, z_center))
            )
            bore = (
                cq.Workplane("YZ")
                .circle(c.M3_CLEARANCE / 2)
                .extrude(c.INSERT_BOSS_HEIGHT + c.FILLET_RADIUS)
                .translate((x_face, y_center + y_off, z_center))
            )
            boss = boss.cut(bore)
            bosses = boss if bosses is None else bosses.union(boss)

    return bosses.tag("future_side_adapter_mount_points")


def _make_future_bottom_adapter_pads(c=cfg) -> cq.Workplane:
    """Optional bottom adapter pad placeholders on the lower interface ring."""
    pads = None
    x_rail = rails.u_channel_rail_x_offset()
    z = -c.GENERIC_STACK_MODULE_HEIGHT / 2 + c.MODULE_INTERFACE_HEIGHT / 2
    y_center = -c.REAR_RESERVED_DEPTH / 2

    for sign in (-1, 1):
        pad = (
            cq.Workplane("XY")
            .box(
                c.FUTURE_BOTTOM_ADAPTER_PAD_WIDTH,
                c.FUTURE_BOTTOM_ADAPTER_PAD_DEPTH,
                c.FUTURE_BOTTOM_ADAPTER_PAD_HEIGHT,
            )
            .translate((sign * x_rail, y_center, z))
        )
        pads = pad if pads is None else pads.union(pad)

    return pads.tag("future_bottom_adapter_pads")


def _make_internal_mount_grid_placeholder(c=cfg) -> cq.Workplane:
    """Placeholder standoff pads for future internal device mounting — DEFERRED.

    NOT included in the mk0.11.2 printable shell.  The pads are positioned
    inside the central airflow opening where no floor material exists, which
    produces floating islands in the exported solid.  Reactivate only after
    a floor or bridging rib is introduced, or when device-specific modules
    replace the generic shell.
    """
    pads = None
    cols = c.STACK_MODULE_MOUNT_GRID_COLS
    rows = c.STACK_MODULE_MOUNT_GRID_ROWS
    pitch = c.STACK_MODULE_MOUNT_GRID_PITCH
    x_span = (cols - 1) * pitch
    y_span = (rows - 1) * pitch
    z = -c.GENERIC_STACK_MODULE_HEIGHT / 2 + c.CARRIAGE_WALL_THICKNESS / 2

    for col in range(cols):
        for row in range(rows):
            x = -x_span / 2 + col * pitch
            y = -c.REAR_RESERVED_DEPTH / 2 - y_span / 2 + row * pitch
            pad = (
                cq.Workplane("XY")
                .circle(c.STACK_MODULE_MOUNT_PAD_DIAMETER / 2)
                .extrude(c.STACK_MODULE_MOUNT_PAD_HEIGHT)
                .translate((x, y, z))
            )
            pads = pad if pads is None else pads.union(pad)

    return pads.tag("internal_mount_grid_placeholder")


def make_generic_stack_module_shell(c=cfg) -> cq.Workplane:
    """Structural shell for the stack module without handle or interface pins."""
    height = c.GENERIC_STACK_MODULE_HEIGHT

    bottom_ring = _make_frame_ring(c).translate(
        (0, 0, -height / 2 + c.MODULE_INTERFACE_HEIGHT / 2)
    )
    top_ring = _make_frame_ring(c).translate(
        (0, 0, height / 2 - c.MODULE_INTERFACE_HEIGHT / 2)
    )
    shell = bottom_ring.union(top_ring)

    post_size = c.CORNER_POST_SIZE
    for px, py in _corner_rod_points(c):
        post = cq.Workplane("XY").box(post_size, post_size, height).translate((px, py, 0))
        shell = shell.union(post)

    shell = shell.cut(_make_vertical_airflow_opening(height, c))
    shell = shell.union(_make_future_carriage_mount_zones(height, c))
    shell = shell.union(_make_future_bottom_adapter_pads(c))
    shell = _apply_compression_pads(shell, c)

    return shell.tag("generic_stack_module_shell")


def make_generic_stack_module_front_handle(c=cfg) -> cq.Workplane:
    """Front handle / label zone placeholder on the module front face."""
    height = c.GENERIC_STACK_MODULE_HEIGHT
    handle_z = -height / 2 + c.GENERIC_MODULE_HANDLE_HEIGHT / 2

    lip = (
        cq.Workplane("XY")
        .box(
            c.CARRIAGE_PULL_LIP_WIDTH,
            c.CARRIAGE_PULL_LIP_DEPTH,
            c.GENERIC_MODULE_HANDLE_HEIGHT,
        )
        .translate(
            (
                0,
                -(c.TOWER_DEPTH / 2) - c.CARRIAGE_PULL_LIP_FRONT_OFFSET,
                handle_z,
            )
        )
    )
    return lip.tag("generic_stack_module_front_handle")


def make_generic_stack_module(c=cfg) -> cq.Workplane:
    """Complete generic stack module for mk0.11.2 layer-cake prototype.

    Alignment pins (top=False) are intentionally disabled for mk0.11.2: the
    front pin positions (±57, −61) fall inside the central airflow channel
    where the frame ring has no solid material, producing floating islands.
    Module-to-module alignment is provided by the four M5 corner post rods.
    Alignment pins can be reactivated in a future revision once the ring
    geometry is redesigned to provide a bearing surface at those positions.
    """
    module = make_generic_stack_module_shell(c)
    module = module.union(make_generic_stack_module_front_handle(c))
    module = module_interface.apply_module_interface_features(module, c, top=False, bottom=True)
    return module.tag("generic_stack_module")
