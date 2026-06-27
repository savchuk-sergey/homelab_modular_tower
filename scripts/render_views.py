"""Render assembly projections to PNG without FreeCAD GUI.

This script uses the CadQuery model directly, tessellates each assembly part,
and renders orthographic engineering views with Matplotlib. It is intended for
quick design review snapshots, not photorealistic rendering.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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


def _shape_triangles(shape, tolerance: float):
    vertices, triangles = shape.tessellate(tolerance)
    points = [(vertex.x, vertex.y, vertex.z) for vertex in vertices]
    return [[points[index] for index in triangle] for triangle in triangles], points


def _collect_meshes(tolerance: float):
    assembly = build_assembly()
    meshes = []
    all_points = []

    for name, child in assembly.objects.items():
        if child.obj is None:
            continue
        shape = child.obj.val().located(child.loc)
        triangles, points = _shape_triangles(shape, tolerance)
        meshes.append((name, triangles))
        all_points.extend(points)

    return meshes, all_points


def _axis_limits(points, margin: float):
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    zs = [point[2] for point in points]
    center = (
        (min(xs) + max(xs)) / 2,
        (min(ys) + max(ys)) / 2,
        (min(zs) + max(zs)) / 2,
    )
    span = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) + margin * 2
    half = span / 2
    return (
        (center[0] - half, center[0] + half),
        (center[1] - half, center[1] + half),
        (center[2] - half, center[2] + half),
    )


def render_view(name: str, view: tuple[int, int], meshes, limits, out_dir: Path, size: int, dpi: int) -> None:
    fig = plt.figure(figsize=(size / dpi, size / dpi), dpi=dpi)
    ax = fig.add_subplot(111, projection="3d", proj_type="ortho")

    for part_name, triangles in meshes:
        collection = Poly3DCollection(
            triangles,
            facecolors=_part_color(part_name),
            edgecolors=(0.08, 0.08, 0.08, 0.35),
            linewidths=0.08,
            alpha=1.0,
        )
        ax.add_collection3d(collection)

    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=view[0], azim=view[1])
    ax.set_axis_off()
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

    out_path = out_dir / f"{name}.png"
    fig.savefig(out_path, dpi=dpi, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Homelab Modular Tower CAD projections.")
    parser.add_argument("--out", default="renders", help="Output directory for PNG files.")
    parser.add_argument("--size", type=int, default=1800, help="Square image size in pixels.")
    parser.add_argument("--dpi", type=int, default=150, help="Output DPI.")
    parser.add_argument("--tolerance", type=float, default=1.2, help="Tessellation tolerance in mm.")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    meshes, points = _collect_meshes(args.tolerance)
    limits = _axis_limits(points, margin=18.0)

    for name, view in VIEWS.items():
        render_view(name, view, meshes, limits, out_dir, args.size, args.dpi)


if __name__ == "__main__":
    main()
