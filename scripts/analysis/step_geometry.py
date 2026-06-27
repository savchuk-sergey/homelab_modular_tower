"""STEP measurement helpers through CadQuery/OCP."""

from __future__ import annotations

from pathlib import Path

import cadquery as cq


def step_bbox(path: Path) -> dict[str, float]:
    workplane = cq.importers.importStep(str(path))
    bbox = workplane.val().BoundingBox()
    return {
        "min_x": float(bbox.xmin),
        "min_y": float(bbox.ymin),
        "min_z": float(bbox.zmin),
        "max_x": float(bbox.xmax),
        "max_y": float(bbox.ymax),
        "max_z": float(bbox.zmax),
        "size_x": float(bbox.xlen),
        "size_y": float(bbox.ylen),
        "size_z": float(bbox.zlen),
    }
