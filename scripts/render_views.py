"""Render engineering PNG drawings from the CadQuery assembly.

This script uses the CadQuery model directly, tessellates assembly children,
and renders quick orthographic review sheets with Matplotlib. It is for
engineering model review, not photorealistic rendering or formal CAD drafting.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cad import config as cfg
from cad.assembly import build_assembly


VIEWS = {
    "front": (0, -90),
    "rear": (0, 90),
    "left": (0, 180),
    "right": (0, 0),
    "top": (90, -90),
    "bottom": (-90, -90),
    "isometric": (28, -45),
}

DRAWING_VIEWS = ["front", "right", "top", "isometric"]
VIEWPORTS = {
    "front": (0.07, 0.55, 0.32, 0.32),
    "right": (0.42, 0.55, 0.32, 0.32),
    "top": (0.07, 0.18, 0.32, 0.32),
    "isometric": (0.42, 0.18, 0.32, 0.32),
}

Point3D = tuple[float, float, float]
Triangle = list[Point3D]


@dataclass(frozen=True)
class BoundingBox:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float
    max_z: float
    width_x: float
    depth_y: float
    height_z: float
    center: Point3D


@dataclass(frozen=True)
class RenderItem:
    name: str
    triangles: list[Triangle]
    points: list[Point3D]
    bbox: BoundingBox


class RenderError(RuntimeError):
    """User-facing rendering error."""


def sanitize_name(name: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9_.-]+", "_", name.strip())
    clean = re.sub(r"_+", "_", clean).strip("._-")
    return clean or "unnamed_part"


def ensure_output_dir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RenderError(f"Cannot create output directory '{path}': {exc}") from exc


def compute_bounding_box(points: Iterable[Point3D]) -> BoundingBox:
    point_list = list(points)
    if not point_list:
        raise RenderError("Cannot compute bounding box: tessellation returned no points.")

    xs = [point[0] for point in point_list]
    ys = [point[1] for point in point_list]
    zs = [point[2] for point in point_list]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    return BoundingBox(
        min_x=min_x,
        max_x=max_x,
        min_y=min_y,
        max_y=max_y,
        min_z=min_z,
        max_z=max_z,
        width_x=max_x - min_x,
        depth_y=max_y - min_y,
        height_z=max_z - min_z,
        center=((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2),
    )


def combine_bounding_boxes(boxes: Iterable[BoundingBox]) -> BoundingBox:
    box_list = list(boxes)
    if not box_list:
        raise RenderError("Cannot compute assembly bounding box: no part bounding boxes were collected.")

    points = [(box.min_x, box.min_y, box.min_z) for box in box_list]
    points.extend((box.max_x, box.max_y, box.max_z) for box in box_list)
    return compute_bounding_box(points)


def axis_limits_from_bbox(bbox: BoundingBox, margin: float) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    span = max(bbox.width_x, bbox.depth_y, bbox.height_z) + margin * 2
    if span <= 0:
        span = margin * 2
    half = span / 2
    return (
        (bbox.center[0] - half, bbox.center[0] + half),
        (bbox.center[1] - half, bbox.center[1] + half),
        (bbox.center[2] - half, bbox.center[2] + half),
    )


def _part_color(name: str) -> tuple[float, float, float, float]:
    if "rod" in name:
        return (0.12, 0.12, 0.12, 1.0)
    if "metal_guide_rail" in name:
        return (0.12, 0.24, 0.42, 1.0)
    if "power_bus" in name:
        return (0.72, 0.58, 0.22, 1.0)
    if "tray" in name or "bay" in name:
        return (0.68, 0.76, 0.82, 1.0)
    if "panel" in name or "spine" in name:
        return (0.82, 0.82, 0.78, 1.0)
    return (0.72, 0.72, 0.70, 1.0)


def _shape_triangles(shape, tolerance: float, name: str) -> tuple[list[Triangle], list[Point3D]]:
    try:
        vertices, triangles = shape.tessellate(tolerance)
    except Exception as exc:  # noqa: BLE001 - CadQuery/OCC raises several exception types.
        raise RenderError(f"Failed to tessellate part '{name}': {exc}") from exc

    points = [(vertex.x, vertex.y, vertex.z) for vertex in vertices]
    if not points or not triangles:
        raise RenderError(f"Part '{name}' produced empty tessellation points or triangles.")
    return [[points[index] for index in triangle] for triangle in triangles], points


def _shape_from_child(name: str, child):
    if not hasattr(child, "obj") or child.obj is None:
        raise RenderError(f"Assembly child '{name}' has no obj and cannot be rendered.")
    try:
        return child.obj.val().located(child.loc)
    except Exception as exc:  # noqa: BLE001 - keep message readable for CAD object failures.
        raise RenderError(f"Failed to get located shape for part '{name}': {exc}") from exc


def collect_render_items(tolerance: float) -> list[RenderItem]:
    assembly = build_assembly()
    if not assembly.objects:
        raise RenderError("Assembly does not contain any renderable children.")

    items: list[RenderItem] = []
    for name, child in assembly.objects.items():
        if name == assembly.name and (not hasattr(child, "obj") or child.obj is None):
            continue
        shape = _shape_from_child(name, child)
        triangles, points = _shape_triangles(shape, tolerance, name)
        items.append(RenderItem(name=name, triangles=triangles, points=points, bbox=compute_bounding_box(points)))

    if not items:
        raise RenderError("Assembly did not produce any renderable items.")
    return items


def _select_parts(items: list[RenderItem], selected_part: str | None) -> list[RenderItem]:
    if selected_part is None:
        return items

    matches = [item for item in items if item.name == selected_part or sanitize_name(item.name) == selected_part]
    if matches:
        return matches

    available = "\n  ".join(item.name for item in items)
    raise RenderError(f"Part '{selected_part}' was not found. Available parts:\n  {available}")


def _add_meshes_to_axis(ax, items: list[RenderItem]) -> None:
    for item in items:
        collection = Poly3DCollection(
            item.triangles,
            facecolors=_part_color(item.name),
            edgecolors=(0.08, 0.08, 0.08, 0.35),
            linewidths=0.08,
            alpha=1.0,
        )
        ax.add_collection3d(collection)


def draw_viewport(
    fig,
    rect: tuple[float, float, float, float],
    view_name: str,
    view_angles: tuple[int, int],
    items: list[RenderItem],
    bbox: BoundingBox,
    margin: float,
) -> None:
    ax = fig.add_axes(rect, projection="3d", proj_type="ortho")
    _add_meshes_to_axis(ax, items)

    view_margin = margin * 1.2 if view_name == "isometric" else margin
    limits = axis_limits_from_bbox(bbox, margin=view_margin)
    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=view_angles[0], azim=view_angles[1])
    ax.set_axis_off()
    ax.set_facecolor("white")

    left, bottom, width, height = rect
    fig.patches.append(
        Rectangle(
            (left, bottom),
            width,
            height,
            transform=fig.transFigure,
            fill=False,
            edgecolor="#777777",
            linewidth=0.8,
        )
    )
    fig.text(left + 0.01, bottom + height - 0.018, view_name.title(), ha="left", va="top", fontsize=9, color="#222222")


def _draw_sheet_frame(fig) -> None:
    for xy, width, height, linewidth in [
        ((0.015, 0.02), 0.97, 0.955, 1.2),
        ((0.03, 0.04), 0.94, 0.915, 0.7),
    ]:
        fig.patches.append(
            Rectangle(
                xy,
                width,
                height,
                transform=fig.transFigure,
                fill=False,
                edgecolor="#111111",
                linewidth=linewidth,
            )
        )


def _title_block_lines_for_part(item: RenderItem, revision: str) -> list[str]:
    return [
        "Project: Homelab Modular Tower",
        f"Part: {item.name}",
        f"Revision: {revision}",
        f"Width X: {item.bbox.width_x:.1f} mm",
        f"Depth Y: {item.bbox.depth_y:.1f} mm",
        f"Height Z: {item.bbox.height_z:.1f} mm",
        "Scale: auto",
        "Units: mm",
        f"Generated: {date.today().isoformat()}",
    ]


def _title_block_lines_for_assembly(bbox: BoundingBox, part_count: int, revision: str) -> list[str]:
    return [
        "Project: Homelab Modular Tower",
        "Drawing: Assembly",
        f"Revision: {revision}",
        f"Width X: {bbox.width_x:.1f} mm",
        f"Depth Y: {bbox.depth_y:.1f} mm",
        f"Height Z: {bbox.height_z:.1f} mm",
        f"Parts: {part_count}",
        "Scale: auto",
        "Units: mm",
        f"Generated: {date.today().isoformat()}",
    ]


def _draw_title_block(fig, lines: list[str]) -> None:
    left, bottom, width, height = 0.73, 0.075, 0.225, 0.255
    fig.patches.append(
        Rectangle(
            (left, bottom),
            width,
            height,
            transform=fig.transFigure,
            fill=False,
            edgecolor="#111111",
            linewidth=0.9,
        )
    )
    row_height = height / len(lines)
    for index in range(1, len(lines)):
        y = bottom + index * row_height
        fig.lines.append(
            plt.Line2D([left, left + width], [y, y], transform=fig.transFigure, color="#cccccc", linewidth=0.4)
        )

    y = bottom + height - row_height * 0.62
    for line in lines:
        fig.text(left + 0.008, y, line, ha="left", va="center", fontsize=7.5, family="monospace", color="#111111")
        y -= row_height


def _draw_dimension_summary(fig, bbox: BoundingBox) -> None:
    text = (
        f"Overall dimensions: Width X {bbox.width_x:.1f} mm  |  "
        f"Depth Y {bbox.depth_y:.1f} mm  |  Height Z {bbox.height_z:.1f} mm"
    )
    fig.text(0.07, 0.095, text, ha="left", va="center", fontsize=9, family="monospace", color="#111111")


def _render_sheet(
    title: str,
    items: list[RenderItem],
    bbox: BoundingBox,
    out_path: Path,
    sheet_size: tuple[int, int],
    dpi: int,
    title_block_lines: list[str],
) -> None:
    ensure_output_dir(out_path.parent)
    sheet_width, sheet_height = sheet_size
    fig = plt.figure(figsize=(sheet_width / dpi, sheet_height / dpi), dpi=dpi)
    fig.patch.set_facecolor("white")

    _draw_sheet_frame(fig)
    fig.text(0.04, 0.935, title, ha="left", va="top", fontsize=15, weight="bold", color="#111111")

    margin = max(bbox.width_x, bbox.depth_y, bbox.height_z) * 0.08 + 8.0
    for view_name in DRAWING_VIEWS:
        draw_viewport(fig, VIEWPORTS[view_name], view_name, VIEWS[view_name], items, bbox, margin)

    _draw_dimension_summary(fig, bbox)
    _draw_title_block(fig, title_block_lines)
    fig.savefig(out_path, dpi=dpi, facecolor="white")
    plt.close(fig)
    print(out_path)


def render_drawing_sheet(
    item: RenderItem,
    out_path: Path,
    sheet_size: tuple[int, int],
    dpi: int,
    tolerance: float,
    revision: str,
) -> None:
    _ = tolerance  # The item is already tessellated; kept for the requested function signature.
    _render_sheet(
        title=f"Part drawing: {item.name}",
        items=[item],
        bbox=item.bbox,
        out_path=out_path,
        sheet_size=sheet_size,
        dpi=dpi,
        title_block_lines=_title_block_lines_for_part(item, revision),
    )


def render_assembly_drawing_sheet(
    items: list[RenderItem],
    out_path: Path,
    sheet_size: tuple[int, int],
    dpi: int,
    revision: str,
) -> None:
    bbox = combine_bounding_boxes(item.bbox for item in items)
    _render_sheet(
        title="Assembly drawing: Homelab Modular Tower",
        items=items,
        bbox=bbox,
        out_path=out_path,
        sheet_size=sheet_size,
        dpi=dpi,
        title_block_lines=_title_block_lines_for_assembly(bbox, len(items), revision),
    )


def render_drawing_sheets(
    items: list[RenderItem],
    out_dir: Path,
    target: str,
    selected_part: str | None,
    sheet_size: tuple[int, int],
    dpi: int,
    tolerance: float,
    revision: str,
) -> None:
    if selected_part and target == "assembly":
        raise RenderError("--part can only be used with --target parts or --target all.")

    drawings_dir = out_dir / "drawings"
    if target in ("all", "assembly") and selected_part is None:
        render_assembly_drawing_sheet(items, drawings_dir / "assembly.png", sheet_size, dpi, revision)

    if target in ("all", "parts") or selected_part is not None:
        parts_dir = drawings_dir / "parts"
        for item in _select_parts(items, selected_part):
            render_drawing_sheet(
                item,
                parts_dir / f"{sanitize_name(item.name)}.png",
                sheet_size,
                dpi,
                tolerance,
                revision,
            )


def _metadata_for_part_view(item: RenderItem, view_name: str) -> str:
    return (
        f"Part: {item.name}\n"
        f"View: {view_name}\n"
        f"Width X: {item.bbox.width_x:.1f} mm | "
        f"Depth Y: {item.bbox.depth_y:.1f} mm | "
        f"Height Z: {item.bbox.height_z:.1f} mm"
    )


def _metadata_for_assembly_view(bbox: BoundingBox, view_name: str, part_count: int) -> str:
    return (
        "Assembly: Homelab Modular Tower\n"
        f"View: {view_name}\n"
        f"Width X: {bbox.width_x:.1f} mm | "
        f"Depth Y: {bbox.depth_y:.1f} mm | "
        f"Height Z: {bbox.height_z:.1f} mm | "
        f"Parts: {part_count}"
    )


def render_projection_view(
    title: str,
    view_name: str,
    view: tuple[int, int],
    items: list[RenderItem],
    bbox: BoundingBox,
    out_path: Path,
    size: int,
    dpi: int,
    metadata_text: str,
) -> None:
    ensure_output_dir(out_path.parent)

    fig = plt.figure(figsize=(size / dpi, size / dpi), dpi=dpi)
    ax = fig.add_subplot(111, projection="3d", proj_type="ortho")
    _add_meshes_to_axis(ax, items)

    limits = axis_limits_from_bbox(bbox, margin=max(bbox.width_x, bbox.depth_y, bbox.height_z) * 0.08 + 8.0)
    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=view[0], azim=view[1])
    ax.set_title(title, fontsize=10, pad=6)
    ax.set_axis_off()
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    fig.text(0.03, 0.975, metadata_text, ha="left", va="top", fontsize=9, family="monospace", color="#111111")
    plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=0.84)

    fig.savefig(out_path, dpi=dpi, facecolor="white", pad_inches=0.02)
    plt.close(fig)
    print(out_path)


def render_assembly_views(items: list[RenderItem], out_dir: Path, size: int, dpi: int) -> None:
    bbox = combine_bounding_boxes(item.bbox for item in items)
    assembly_dir = out_dir / "assembly"
    for view_name, view in VIEWS.items():
        render_projection_view(
            title="Homelab Modular Tower",
            view_name=view_name,
            view=view,
            items=items,
            bbox=bbox,
            out_path=assembly_dir / f"{view_name}.png",
            size=size,
            dpi=dpi,
            metadata_text=_metadata_for_assembly_view(bbox, view_name, len(items)),
        )


def render_part_views(items: list[RenderItem], out_dir: Path, size: int, dpi: int, selected_part: str | None) -> None:
    for item in _select_parts(items, selected_part):
        part_dir = out_dir / "parts" / sanitize_name(item.name)
        for view_name, view in VIEWS.items():
            render_projection_view(
                title=item.name,
                view_name=view_name,
                view=view,
                items=[item],
                bbox=item.bbox,
                out_path=part_dir / f"{view_name}.png",
                size=size,
                dpi=dpi,
                metadata_text=_metadata_for_part_view(item, view_name),
            )


def render_views(
    items: list[RenderItem],
    out_dir: Path,
    target: str,
    selected_part: str | None,
    size: int,
    dpi: int,
) -> None:
    if selected_part and target == "assembly":
        raise RenderError("--part can only be used with --target parts or --target all.")

    if target in ("all", "assembly") and selected_part is None:
        render_assembly_views(items, out_dir, size, dpi)
    if target in ("all", "parts") or selected_part is not None:
        render_part_views(items, out_dir, size, dpi, selected_part)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Homelab Modular Tower CAD engineering PNG drawings.")
    parser.add_argument("--out", default="renders", help="Output directory for PNG files.")
    parser.add_argument("--size", type=int, default=1800, help="Square image size in pixels for --mode views.")
    parser.add_argument("--dpi", type=int, default=150, help="Output DPI.")
    parser.add_argument("--tolerance", type=float, default=1.2, help="Tessellation tolerance in mm.")
    parser.add_argument(
        "--mode",
        choices=("views", "drawings", "all"),
        default="drawings",
        help="Render old separate projection PNGs, drawing sheets, or both.",
    )
    parser.add_argument(
        "--target",
        choices=("assembly", "parts", "all"),
        default="all",
        help="Render assembly, parts, or both.",
    )
    parser.add_argument("--part", default=None, help="Render one part by assembly name or sanitized file name.")
    parser.add_argument("--revision", default=cfg.CURRENT_REVISION, help="Revision label for drawing sheets.")
    parser.add_argument("--sheet-width", type=int, default=2400, help="Drawing sheet width in pixels.")
    parser.add_argument("--sheet-height", type=int, default=1700, help="Drawing sheet height in pixels.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out)

    try:
        items = collect_render_items(args.tolerance)
        sheet_size = (args.sheet_width, args.sheet_height)
        if args.mode in ("drawings", "all"):
            render_drawing_sheets(
                items=items,
                out_dir=out_dir,
                target=args.target,
                selected_part=args.part,
                sheet_size=sheet_size,
                dpi=args.dpi,
                tolerance=args.tolerance,
                revision=args.revision,
            )
        if args.mode in ("views", "all"):
            render_views(
                items=items,
                out_dir=out_dir,
                target=args.target,
                selected_part=args.part,
                size=args.size,
                dpi=args.dpi,
            )
    except RenderError as exc:
        print(f"render_views.py: error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
