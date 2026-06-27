"""Compatibility exports for panel factories."""

from .parts.cooling import create_bottom_fan_panel, create_fan_panel, create_top_fan_panel
from .parts.side_panels import (
    create_left_side_panel,
    create_right_side_panel,
    create_side_panel,
    make_side_panel_frame,
    make_side_panel_mounts,
    make_side_panel_ribs,
    make_side_panel_vents,
    side_panel_length,
)

__all__ = [
    "create_bottom_fan_panel",
    "create_fan_panel",
    "create_left_side_panel",
    "create_right_side_panel",
    "create_side_panel",
    "create_top_fan_panel",
    "make_side_panel_frame",
    "make_side_panel_mounts",
    "make_side_panel_ribs",
    "make_side_panel_vents",
    "side_panel_length",
]
