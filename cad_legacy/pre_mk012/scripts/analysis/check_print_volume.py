"""Check printable STL exports against configured Bambu Lab P2S build volume."""

from __future__ import annotations

import argparse
import sys
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
    "size_x_mm",
    "size_y_mm",
    "size_z_mm",
    "print_volume_x_mm",
    "print_volume_y_mm",
    "print_volume_z_mm",
    "fits_axis_aligned",
    "long_thin_risk",
    "max_aspect_ratio",
    "notes",
]


def check_print_volume(revision: str) -> Path:
    revision = validate_current_revision(revision)
    rows: list[dict[str, object]] = []
    volume = (cfg.BAMBU_P2S_PRINT_VOLUME_X, cfg.BAMBU_P2S_PRINT_VOLUME_Y, cfg.BAMBU_P2S_PRINT_VOLUME_Z)
    for path in iter_export_files(revision, ".stl", "printable"):
        row: dict[str, object] = {
            "part_name": path.stem,
            "category": export_category(path, revision),
            "relative_path": relative_to_repo(path),
            "status": "ok",
            "print_volume_x_mm": f"{volume[0]:.3f}",
            "print_volume_y_mm": f"{volume[1]:.3f}",
            "print_volume_z_mm": f"{volume[2]:.3f}",
            "notes": "",
        }
        try:
            stats = mesh_stats(path)
            sizes = sorted((stats.size_x, stats.size_y, stats.size_z))
            smallest = max(sizes[0], 0.001)
            aspect = sizes[-1] / smallest
            fits = stats.size_x <= volume[0] and stats.size_y <= volume[1] and stats.size_z <= volume[2]
            long_thin = aspect >= cfg.PRINTABILITY_LONG_THIN_ASPECT_RATIO and sizes[0] <= cfg.PRINTABILITY_THIN_AXIS_MM
            notes = []
            if not fits:
                notes.append("exceeds configured axis-aligned P2S volume")
            if long_thin:
                notes.append("long-thin geometry risk; orientation/support review required")
            row.update(
                {
                    "size_x_mm": f"{stats.size_x:.3f}",
                    "size_y_mm": f"{stats.size_y:.3f}",
                    "size_z_mm": f"{stats.size_z:.3f}",
                    "fits_axis_aligned": fits,
                    "long_thin_risk": long_thin,
                    "max_aspect_ratio": f"{aspect:.3f}",
                    "notes": "; ".join(notes),
                }
            )
        except Exception as exc:
            row["status"] = "error"
            row["notes"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return write_csv(analysis_dir(revision) / "printability_check.csv", FIELDS, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    args = parser.parse_args()
    print(check_print_volume(args.revision))


if __name__ == "__main__":
    main()
