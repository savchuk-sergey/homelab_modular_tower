"""Small STL mesh utilities with no external mesh dependency."""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class MeshStats:
    triangle_count: int
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    size_x: float
    size_y: float
    size_z: float
    volume_mm3: float
    surface_area_mm2: float
    boundary_edges: int
    nonmanifold_edges: int
    is_watertight: bool
    is_manifold: bool
    geometry_hash: str


def load_stl_triangles(path: Path) -> np.ndarray:
    data = path.read_bytes()
    if _looks_binary_stl(data):
        return _read_binary_stl(data)
    return _read_ascii_stl(data.decode("utf-8", errors="ignore"))


def mesh_stats(path: Path) -> MeshStats:
    triangles = load_stl_triangles(path)
    if triangles.size == 0:
        raise ValueError("STL contains no triangles")

    points = triangles.reshape((-1, 3))
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    sizes = maxs - mins

    v0 = triangles[:, 0, :]
    v1 = triangles[:, 1, :]
    v2 = triangles[:, 2, :]
    signed = np.einsum("ij,ij->i", v0, np.cross(v1, v2)) / 6.0
    volume = abs(float(signed.sum()))
    surface = float(np.linalg.norm(np.cross(v1 - v0, v2 - v0), axis=1).sum() / 2.0)
    boundary, nonmanifold = _edge_counts(triangles)
    digest = _geometry_hash(triangles, mins, volume, surface)

    return MeshStats(
        triangle_count=int(triangles.shape[0]),
        min_x=float(mins[0]),
        min_y=float(mins[1]),
        min_z=float(mins[2]),
        max_x=float(maxs[0]),
        max_y=float(maxs[1]),
        max_z=float(maxs[2]),
        size_x=float(sizes[0]),
        size_y=float(sizes[1]),
        size_z=float(sizes[2]),
        volume_mm3=volume,
        surface_area_mm2=surface,
        boundary_edges=boundary,
        nonmanifold_edges=nonmanifold,
        is_watertight=boundary == 0 and nonmanifold == 0,
        is_manifold=nonmanifold == 0,
        geometry_hash=digest,
    )


def _looks_binary_stl(data: bytes) -> bool:
    if len(data) < 84:
        return False
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    return 84 + triangle_count * 50 == len(data)


def _read_binary_stl(data: bytes) -> np.ndarray:
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    triangles = np.zeros((triangle_count, 3, 3), dtype=np.float64)
    offset = 84
    for index in range(triangle_count):
        values = struct.unpack_from("<12fH", data, offset)
        triangles[index] = np.array(values[3:12], dtype=np.float64).reshape((3, 3))
        offset += 50
    return triangles


def _read_ascii_stl(text: str) -> np.ndarray:
    vertices: list[list[float]] = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) == 4 and parts[0].lower() == "vertex":
            vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
    if len(vertices) % 3 != 0:
        raise ValueError("ASCII STL vertex count is not divisible by 3")
    return np.array(vertices, dtype=np.float64).reshape((-1, 3, 3))


def _vertex_key(vertex: np.ndarray) -> tuple[float, float, float]:
    rounded = np.round(vertex, decimals=5)
    return (float(rounded[0]), float(rounded[1]), float(rounded[2]))


def _edge_counts(triangles: np.ndarray) -> tuple[int, int]:
    edges: dict[tuple[tuple[float, float, float], tuple[float, float, float]], int] = {}
    for triangle in triangles:
        keys = [_vertex_key(vertex) for vertex in triangle]
        for start, end in ((keys[0], keys[1]), (keys[1], keys[2]), (keys[2], keys[0])):
            edge = tuple(sorted((start, end)))
            edges[edge] = edges.get(edge, 0) + 1
    boundary = sum(1 for count in edges.values() if count == 1)
    nonmanifold = sum(1 for count in edges.values() if count > 2)
    return boundary, nonmanifold


def _geometry_hash(triangles: np.ndarray, mins: np.ndarray, volume: float, surface: float) -> str:
    normalized = np.round(triangles - mins, decimals=4)
    per_triangle = []
    for triangle in normalized:
        vertices = sorted(tuple(float(value) for value in vertex) for vertex in triangle)
        per_triangle.append(tuple(value for vertex in vertices for value in vertex))
    per_triangle.sort()
    payload = repr((round(volume, 3), round(surface, 3), per_triangle)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
