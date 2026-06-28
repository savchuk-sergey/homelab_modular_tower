"""mk0.11 generic removable module shell — DEFERRED carriage/rail era.

Superseded for active work by `generic_stack_module.py` in mk0.11.2
(stack-through-rod architecture).  This file is preserved unchanged for
the deferred sliding carriage / rail upgrade path.

See `cad/deferred/README.md` for deferred vs active architecture status.

First subsystem target for the mk0.11 subsystem-first workflow.

This is a device-agnostic module body that establishes the structural shell,
airflow path, rear service zone clearance, rail pocket integration points,
and front handle zone — without committing to any device layout.

Design intent:
- Dimensionally compatible with the tower module standard.
  Uses TOWER_WIDTH × TOWER_DEPTH outer footprint with MODULE_FRAME_RAIL border.
- Compatible with the mk0.9.3 open-frame carriage and POM-C shoe rail standard.
  Rail pocket carriers produced by make_module_rail_pocket_features().
- Reserves REAR_RESERVED_DEPTH zone for Rear Service Spine cabling.
- Open central volume for vertical airflow (no solid floor between rings).
- M5 rod clearance at all four corner posts via apply_module_interface_features().
- Front handle placeholder at lower front face for ergonomic extraction.
- PETG printable in two orientations (upright, with support on frame rings).

Not included here:
- Device-specific mounting pads, standoffs, retainers.
- UPS, router, or power bus geometry.
- Decorative surfaces.
- Carriage geometry (see cad/parts/module_carriage.py).
"""

import cadquery as cq

from .. import config as cfg
from . import module_interface, rails


def _make_frame_ring(c=cfg) -> cq.Workplane:
    """Single horizontal frame ring (MODULE_INTERFACE_HEIGHT thick).

    The ring spans the full tower footprint and leaves an open interior
    zone for airflow and the module interior. The rear reserved zone is
    also cleared to maintain Rear Service Spine access.
    """
    ring = cq.Workplane("XY").box(c.TOWER_WIDTH, c.TOWER_DEPTH, c.MODULE_INTERFACE_HEIGHT)

    # Central interior cutout — leaves MODULE_FRAME_RAIL-wide perimeter on
    # three sides (front, left, right) and full depth on the rear zone.
    inner = (
        cq.Workplane("XY")
        .box(
            c.TOWER_WIDTH - 2 * c.MODULE_FRAME_RAIL,
            c.MODULE_USABLE_DEPTH - 2 * c.MODULE_FRAME_RAIL,
            c.MODULE_INTERFACE_HEIGHT + c.FILLET_RADIUS,
        )
        .translate((0, -c.REAR_RESERVED_DEPTH / 2, 0))
    )

    # Rear zone clearance — maintains cable routing space through Rear Service Spine.
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


def make_generic_module_shell(c=cfg) -> cq.Workplane:
    """Structural shell for the generic module.

    Consists of:
    - Bottom and top frame rings (MODULE_INTERFACE_HEIGHT each).
    - Four corner posts (CORNER_POST_SIZE × CORNER_POST_SIZE × height)
      at M5 rod positions. Rod clearance holes are added by
      apply_module_interface_features() in make_generic_module().
    - Rail pocket carrier features on both lateral sides, produced by
      rails.make_module_rail_pocket_features().

    The space between the two rings is intentionally open — no floor,
    no infill. The carriage (module_carriage.py) occupies this space
    as a separate printable part.
    """
    height = c.GENERIC_MODULE_HEIGHT

    bottom_ring = _make_frame_ring(c).translate(
        (0, 0, -height / 2 + c.MODULE_INTERFACE_HEIGHT / 2)
    )
    top_ring = _make_frame_ring(c).translate(
        (0, 0, height / 2 - c.MODULE_INTERFACE_HEIGHT / 2)
    )
    shell = bottom_ring.union(top_ring)

    # Corner posts — solid pillars connecting both rings at the M5 rod corners.
    # Dimensions use CORNER_POST_SIZE to match the corner block geometry used
    # elsewhere in the tower. Rod clearance holes are cut later by
    # apply_module_interface_features() to avoid double-cutting.
    post_size = c.CORNER_POST_SIZE
    x = c.TOWER_WIDTH / 2 - c.ROD_CENTER_OFFSET
    y = c.TOWER_DEPTH / 2 - c.ROD_CENTER_OFFSET
    for px, py in [(-x, -y), (x, -y), (x, y), (-x, y)]:
        post = cq.Workplane("XY").box(post_size, post_size, height).translate((px, py, 0))
        shell = shell.union(post)

    # Rail pocket carrier features — printed side flanges that capture the
    # U-channel rail and locate its end stops.  Reuses mk0.9.3 standard
    # geometry without any modification.
    rail_pockets = rails.make_module_rail_pocket_features(height, c.GENERIC_MODULE_RAIL_LENGTH)
    shell = shell.union(rail_pockets)

    return shell.tag("generic_module_shell")


def make_generic_module_front_handle(c=cfg) -> cq.Workplane:
    """Front handle placeholder on the module front face.

    A forward-protruding pull lip centered on X at the lower front of
    the module, flush with the tower front face. Dimensioned to match the
    existing carriage pull lip standard (CARRIAGE_PULL_LIP_*) so that
    the handle zone is consistent across all module types.

    Intentionally minimal — no lock screw boss, no label recess, no
    ergonomic shaping. These features are added in device-specific modules
    after the generic prototype is validated.
    """
    height = c.GENERIC_MODULE_HEIGHT

    # Z position: lower 1/3 of the module front face, matching the approximate
    # height of the carriage pull lip when the carriage sits at deck level.
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
    return lip.tag("generic_module_front_handle")


def make_generic_module(c=cfg) -> cq.Workplane:
    """Complete generic module: shell + front handle + module interface features.

    The module interface features (alignment pins on top, sockets on bottom,
    interface bolt holes, M5 rod clearances through corner posts) are applied
    by apply_module_interface_features(), consistent with all other modules.

    The carriage (make_generic_module_carriage) is a separate part that sits
    inside the module shell at deck level. It is combined with this shell in
    cad/assembly/generic_module_assembly.py.

    Airflow path: the open central volume between the two frame rings carries
    vertical airflow. The carriage floor is also open-frame. No solid floor
    blocks the airflow path.
    """
    module = make_generic_module_shell(c)
    module = module.union(make_generic_module_front_handle(c))
    module = module_interface.apply_module_interface_features(module, c, top=True, bottom=True)
    return module.tag("generic_module")
