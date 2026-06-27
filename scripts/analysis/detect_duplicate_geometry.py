"""Detect identical or near-identical STL meshes."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from cad import config as cfg
    from scripts.analysis.common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from scripts.analysis.stl_mesh import mesh_stats
else:
    from cad import config as cfg
    from .common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from .stl_mesh import mesh_stats


FIELDS = [
    "part_name",
    "category",
    "relative_path",
    "status",
    "geometry_hash",
    "near_duplicate_key",
    "duplicate_group",
    "near_duplicate_group",
    "size_x_mm",
    "size_y_mm",
    "size_z_mm",
    "volume_mm3",
    "notes",
]


def detect_duplicate_geometry(revision: str) -> Path:
    revision = validate_current_revision(revision)
    measured: list[dict[str, object]] = []
    exact_groups: dict[str, list[int]] = defaultdict(list)
    near_groups: dict[tuple[float, float, float, float], list[int]] = defaultdict(list)

    for path in iter_export_files(revision, ".stl"):
        row: dict[str, object] = {
            "part_name": path.stem,
            "category": export_category(path, revision),
            "relative_path": relative_to_repo(path),
            "status": "ok",
            "notes": "",
        }
        try:
            stats = mesh_stats(path)
            sorted_sizes = sorted((stats.size_x, stats.size_y, stats.size_z))
            near_key = tuple(round(value / cfg.DUPLICATE_BBOX_TOLERANCE_MM) * cfg.DUPLICATE_BBOX_TOLERANCE_MM for value in sorted_sizes)
            volume_key = round(stats.volume_mm3 / cfg.DUPLICATE_VOLUME_TOLERANCE_MM) * cfg.DUPLICATE_VOLUME_TOLERANCE_MM
            full_near_key = (*near_key, volume_key)
            row.update(
                {
                    "geometry_hash": stats.geometry_hash,
                    "near_duplicate_key": repr(full_near_key),
                    "size_x_mm": f"{stats.size_x:.3f}",
                    "size_y_mm": f"{stats.size_y:.3f}",
                    "size_z_mm": f"{stats.size_z:.3f}",
                    "volume_mm3": f"{stats.volume_mm3:.3f}",
                }
            )
            index = len(measured)
            exact_groups[stats.geometry_hash].append(index)
            near_groups[full_near_key].append(index)
        except Exception as exc:
            row["status"] = "error"
            row["notes"] = f"{type(exc).__name__}: {exc}"
        measured.append(row)

    _assign_groups(measured, exact_groups, "duplicate_group", "exact")
    _assign_groups(measured, near_groups, "near_duplicate_group", "near")
    return write_csv(analysis_dir(revision) / "duplicate_geometry_check.csv", FIELDS, measured)


def _assign_groups(rows: list[dict[str, object]], groups: dict[object, list[int]], field: str, prefix: str) -> None:
    counter = 1
    for indexes in groups.values():
        if len(indexes) < 2:
            continue
        group_name = f"{prefix}_{counter:03d}"
        counter += 1
        for index in indexes:
            rows[index][field] = group_name
            rows[index]["notes"] = "; ".join(filter(None, [str(rows[index].get("notes", "")), f"{field}={group_name}"]))
    for row in rows:
        row.setdefault(field, "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    args = parser.parse_args()
    print(detect_duplicate_geometry(args.revision))


if __name__ == "__main__":
    main()
