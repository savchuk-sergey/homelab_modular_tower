"""Small geometry helpers used by multiple CAD part modules."""

import cadquery as cq


def rounded_box(length: float, width: float, height: float, vertical_chamfer: float) -> cq.Workplane:
    return cq.Workplane("XY").box(length, width, height).edges("|Z").chamfer(vertical_chamfer)
