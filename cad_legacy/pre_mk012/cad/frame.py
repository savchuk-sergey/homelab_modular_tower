"""Compatibility exports for frame-related part factories."""

from .parts.corner_blocks import create_corner_block, create_corner_blocks_in_place
from .parts.frame import create_frame_bottom, create_frame_ring, create_frame_top
from .parts.rails import create_metal_guide_rail, guide_rail_positions
from .parts.rods import create_m5_threaded_rod, rod_positions

__all__ = [
    "create_corner_block",
    "create_corner_blocks_in_place",
    "create_frame_bottom",
    "create_frame_ring",
    "create_frame_top",
    "create_m5_threaded_rod",
    "create_metal_guide_rail",
    "guide_rail_positions",
    "rod_positions",
]
