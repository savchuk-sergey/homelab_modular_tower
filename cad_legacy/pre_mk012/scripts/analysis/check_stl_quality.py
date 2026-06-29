"""Check STL mesh watertight/manifold indicators."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.analysis.common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from scripts.analysis.stl_mesh import mesh_stats
else:
    from .common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from .stl_mesh import mesh_stats


FIELDS = [
    "part_name",
    "category",
    "relative_path",
    "status",
    "triangle_count",
    "is_watertight",
    "is_manifold",
    "boundary_edges",
    "nonmanifold_edges",
    "notes",
]


def check_stl_quality(revision: str) -> Path:
    revision = validate_current_revision(revision)
    rows: list[dict[str, object]] = []
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
            notes = []
            if not stats.is_watertight:
                notes.append("open boundary or nonmanifold edge detected")
            row.update(
                {
                    "triangle_count": stats.triangle_count,
                    "is_watertight": stats.is_watertight,
                    "is_manifold": stats.is_manifold,
                    "boundary_edges": stats.boundary_edges,
                    "nonmanifold_edges": stats.nonmanifold_edges,
                    "notes": "; ".join(notes),
                }
            )
        except Exception as exc:
            row["status"] = "error"
            row["notes"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return write_csv(analysis_dir(revision) / "stl_quality.csv", FIELDS, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    args = parser.parse_args()
    print(check_stl_quality(args.revision))


if __name__ == "__main__":
    main()
