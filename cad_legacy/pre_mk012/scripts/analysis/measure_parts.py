"""Measure bounding boxes for STL and STEP exports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.analysis.common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from scripts.analysis.step_geometry import step_bbox
    from scripts.analysis.stl_mesh import mesh_stats
else:
    from .common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from .step_geometry import step_bbox
    from .stl_mesh import mesh_stats


FIELDS = [
    "part_name",
    "file_type",
    "category",
    "relative_path",
    "status",
    "min_x_mm",
    "min_y_mm",
    "min_z_mm",
    "max_x_mm",
    "max_y_mm",
    "max_z_mm",
    "size_x_mm",
    "size_y_mm",
    "size_z_mm",
    "triangle_count",
    "error",
]


def measure_parts(revision: str) -> Path:
    revision = validate_current_revision(revision)
    rows: list[dict[str, object]] = []
    for path in [*iter_export_files(revision, ".stl"), *iter_export_files(revision, ".step")]:
        row: dict[str, object] = {
            "part_name": path.stem,
            "file_type": path.suffix.lower().lstrip("."),
            "category": export_category(path, revision),
            "relative_path": relative_to_repo(path),
            "status": "ok",
            "error": "",
            "triangle_count": "",
        }
        try:
            if path.suffix.lower() == ".stl":
                stats = mesh_stats(path)
                row.update(
                    {
                        "min_x_mm": f"{stats.min_x:.3f}",
                        "min_y_mm": f"{stats.min_y:.3f}",
                        "min_z_mm": f"{stats.min_z:.3f}",
                        "max_x_mm": f"{stats.max_x:.3f}",
                        "max_y_mm": f"{stats.max_y:.3f}",
                        "max_z_mm": f"{stats.max_z:.3f}",
                        "size_x_mm": f"{stats.size_x:.3f}",
                        "size_y_mm": f"{stats.size_y:.3f}",
                        "size_z_mm": f"{stats.size_z:.3f}",
                        "triangle_count": stats.triangle_count,
                    }
                )
            else:
                bbox = step_bbox(path)
                row.update({f"{key}_mm": f"{value:.3f}" for key, value in bbox.items()})
        except Exception as exc:
            row["status"] = "error"
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return write_csv(analysis_dir(revision) / "part_dimensions.csv", FIELDS, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    args = parser.parse_args()
    print(measure_parts(args.revision))


if __name__ == "__main__":
    main()
